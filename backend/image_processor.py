import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def _get_torso_points(self, landmarks, width, height):
        """Extract and validate torso keypoints"""
        keypoints = {}
        for point in ['LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_HIP', 'RIGHT_HIP']:
            landmark = landmarks[getattr(self.mp_pose.PoseLandmark, point)]
            keypoints[point] = (
                int(landmark.x * width),
                int(landmark.y * height)
            )
        return keypoints

    def _calculate_perspective_transform(self, keypoints, clothing_img):
        """Calculate perspective transform for clothing"""
        # Source points from clothing image
        src_pts = np.array([
            [0, 0],
            [clothing_img.shape[1], 0],
            [clothing_img.shape[1], clothing_img.shape[0]],
            [0, clothing_img.shape[0]]
        ], dtype=np.float32)

        # Destination points from torso keypoints
        dst_pts = np.array([
            keypoints['LEFT_SHOULDER'],
            keypoints['RIGHT_SHOULDER'],
            keypoints['RIGHT_HIP'],
            keypoints['LEFT_HIP']
        ], dtype=np.float32)

        # Calculate transformation matrix
        return cv2.getPerspectiveTransform(src_pts, dst_pts)

    def _create_blending_mask(self, user_img, keypoints):
        """Create smooth blending mask for the torso region"""
        mask = np.zeros(user_img.shape[:2], dtype=np.uint8)
        points = np.array([
            keypoints['LEFT_SHOULDER'],
            keypoints['RIGHT_SHOULDER'],
            keypoints['RIGHT_HIP'],
            keypoints['LEFT_HIP']
        ])
        
        # Create base mask
        cv2.fillConvexPoly(mask, points, 255)
        
        # Apply gradient for smooth edges
        mask = cv2.GaussianBlur(mask, (31, 31), 15)
        return mask / 255.0

    def process_images(self, user_image_path: str, clothing_image_path: str) -> np.ndarray:
        try:
            # Load images
            user_img = cv2.imread(user_image_path)
            clothing_img = cv2.imread(clothing_image_path)
            
            if user_img is None or clothing_img is None:
                raise ValueError("Failed to load input images")

            # Get image dimensions
            height, width = user_img.shape[:2]
            
            # Process pose
            user_rgb = cv2.cvtColor(user_img, cv2.COLOR_BGR2RGB)
            results = self.pose.process(user_rgb)
            
            if not results.pose_landmarks:
                raise ValueError("No pose detected. Please use a clear, front-facing photo.")

            # Get torso keypoints
            keypoints = self._get_torso_points(results.pose_landmarks.landmark, width, height)
            
            # Calculate transformation
            transform_matrix = self._calculate_perspective_transform(keypoints, clothing_img)
            
            # Apply perspective transform to clothing
            warped_clothing = cv2.warpPerspective(
                clothing_img,
                transform_matrix,
                (width, height)
            )

            # Create blending mask
            blend_mask = self._create_blending_mask(user_img, keypoints)
            
            # Blend images
            result = user_img.copy()
            for c in range(3):  # Process each color channel
                result[:,:,c] = (
                    user_img[:,:,c] * (1 - blend_mask) +
                    warped_clothing[:,:,c] * blend_mask
                )

            logger.debug("Image processing completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error in process_images: {str(e)}")
            logger.exception("Full traceback:")
            raise ValueError(f"Image processing failed: {str(e)}")

    def __del__(self):
        self.pose.close() 