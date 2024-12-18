import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import logging
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
import torch
import torch.nn as nn
from torchvision import transforms
import json
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class ProcessingConfig:
    """Configuration for image processing parameters"""
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.7
    model_complexity: int = 2
    blur_kernel_size: int = 31
    blur_sigma: int = 15
    clahe_clip_limit: float = 3.0
    clahe_grid_size: Tuple[int, int] = (8, 8)
    edge_low_threshold: int = 100
    edge_high_threshold: int = 200
    image_size: int = 256
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

class MGNModel(nn.Module):
    """Multi-Garment Network for virtual try-on"""
    def __init__(self, config: ProcessingConfig):
        super().__init__()
        self.config = config
        self.device = torch.device(config.device)
        
        # Load pre-trained MGN model
        self.model = self._load_pretrained_model()
        self.model.to(self.device)
        self.model.eval()

        # Setup image transforms
        self.transform = transforms.Compose([
            transforms.Resize((config.image_size, config.image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])

    def _load_pretrained_model(self):
        """Load pre-trained MGN model weights"""
        # This would load the actual pre-trained model
        # For now, we'll use a placeholder network
        model = nn.Sequential(
            nn.Conv2d(6, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 3, 3, padding=1),
            nn.Tanh()
        )
        return model

    def forward(self, person_image: torch.Tensor, cloth_image: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network"""
        # Concatenate person and clothing images
        x = torch.cat([person_image, cloth_image], dim=1)
        return self.model(x)

class ImageProcessor:
    def __init__(self, config: Optional[ProcessingConfig] = None):
        self.config = config or ProcessingConfig()
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=self.config.model_complexity,
            enable_segmentation=True,
            min_detection_confidence=self.config.min_detection_confidence,
            min_tracking_confidence=self.config.min_tracking_confidence
        )
        
        # Initialize MGN model
        self.mgn_model = MGNModel(self.config)
        
        # Initialize transform for preprocessing
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((self.config.image_size, self.config.image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])

    def _preprocess_image(self, image: np.ndarray) -> torch.Tensor:
        """Preprocess image for the network"""
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Apply transforms
        tensor = self.transform(image_rgb)
        # Add batch dimension
        return tensor.unsqueeze(0).to(self.config.device)

    def _postprocess_image(self, tensor: torch.Tensor) -> np.ndarray:
        """Convert network output to image"""
        # Remove batch dimension and move to CPU
        image = tensor.squeeze(0).cpu()
        # Denormalize
        image = image * torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
        image = image + torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
        # Convert to numpy and correct format
        image = image.permute(1, 2, 0).numpy()
        image = (image * 255).clip(0, 255).astype(np.uint8)
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    def _get_pose_landmarks(self, image: np.ndarray) -> Dict:
        """Extract pose landmarks from image"""
        results = self.pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            raise ValueError("No pose detected. Please use a clear, front-facing photo.")
        
        # Convert landmarks to dictionary
        landmarks_dict = {}
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            landmarks_dict[f"landmark_{idx}"] = {
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility
            }
        return landmarks_dict

    def _get_torso_measurements(self, landmarks: Dict, width: int, height: int) -> Dict[str, float]:
        """Calculate body measurements from landmarks"""
        # Extract key points
        left_shoulder = landmarks["landmark_11"]
        right_shoulder = landmarks["landmark_12"]
        left_hip = landmarks["landmark_23"]
        right_hip = landmarks["landmark_24"]
        left_elbow = landmarks["landmark_13"]
        right_elbow = landmarks["landmark_14"]
        
        # Calculate measurements
        shoulder_width = abs(left_shoulder["x"] - right_shoulder["x"]) * width
        chest_width = abs(left_elbow["x"] - right_elbow["x"]) * width
        torso_height = abs(
            (left_shoulder["y"] + right_shoulder["y"])/2 - 
            (left_hip["y"] + right_hip["y"])/2
        ) * height
        
        # Calculate ratios
        shoulder_to_chest_ratio = float(shoulder_width / chest_width if chest_width > 0 else 1.0)
        torso_aspect_ratio = float(shoulder_width / torso_height if torso_height > 0 else 1.0)
        
        return {
            "shoulder_width": float(shoulder_width),
            "chest_width": float(chest_width),
            "torso_height": float(torso_height),
            "shoulder_to_chest_ratio": shoulder_to_chest_ratio,
            "torso_aspect_ratio": torso_aspect_ratio
        }

    def process_images(self, user_image_path: str, clothing_image_path: str) -> Tuple[np.ndarray, Dict[str, float]]:
        """Process images using MGN model"""
        try:
            # Load images
            user_img = cv2.imread(user_image_path)
            clothing_img = cv2.imread(clothing_image_path)
            
            if user_img is None or clothing_img is None:
                raise ValueError("Failed to load input images")

            # Get pose landmarks and measurements
            landmarks = self._get_pose_landmarks(user_img)
            measurements = self._get_torso_measurements(
                landmarks, 
                user_img.shape[1], 
                user_img.shape[0]
            )
            
            # Preprocess images
            user_tensor = self._preprocess_image(user_img)
            clothing_tensor = self._preprocess_image(clothing_img)
            
            # Process through MGN model
            with torch.no_grad():
                result_tensor = self.mgn_model(user_tensor, clothing_tensor)
            
            # Postprocess result
            result_image = self._postprocess_image(result_tensor)
            
            # Resize result to original size
            result_image = cv2.resize(
                result_image, 
                (user_img.shape[1], user_img.shape[0]), 
                interpolation=cv2.INTER_LANCZOS4
            )
            
            logger.debug("Image processing completed successfully")
            return result_image, measurements

        except Exception as e:
            logger.error(f"Error in process_images: {str(e)}")
            logger.exception("Full traceback:")
            raise ValueError(f"Image processing failed: {str(e)}")

    def __del__(self):
        self.pose.close()