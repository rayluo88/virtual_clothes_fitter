from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from PIL import Image
import shutil
from datetime import datetime
from typing import List
import cv2
from image_processor import ImageProcessor

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/processed", exist_ok=True)

# Initialize the image processor
image_processor = ImageProcessor()

@app.get("/")
async def read_root():
    return {"message": "Welcome to AI Fitting App API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Fitting App Backend"}

@app.post("/process-images")
async def process_images(
    user_image: UploadFile = File(...),
    clothing_image: UploadFile = File(...)
):
    try:
        # Validate file types
        allowed_types = {"image/jpeg", "image/png", "image/jpg"}
        if user_image.content_type not in allowed_types or clothing_image.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Only JPEG and PNG images are allowed")

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_filename = f"user_{timestamp}.png"
        clothing_filename = f"clothing_{timestamp}.png"
        result_filename = f"result_{timestamp}.png"

        # Save uploaded files
        user_path = f"static/uploads/{user_filename}"
        clothing_path = f"static/uploads/{clothing_filename}"
        result_path = f"static/processed/{result_filename}"

        # Save files
        with open(user_path, "wb") as buffer:
            shutil.copyfileobj(user_image.file, buffer)
        with open(clothing_path, "wb") as buffer:
            shutil.copyfileobj(clothing_image.file, buffer)

        try:
            result_img = image_processor.process_images(user_path, clothing_path)
            result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            result_pil = Image.fromarray(result_img_rgb)
            result_pil.save(result_path)
            
            return {
                "result_url": f"http://127.0.0.1:8000/static/processed/{result_filename}"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
        finally:
            # Clean up uploaded files
            if os.path.exists(user_path):
                os.remove(user_path)
            if os.path.exists(clothing_path):
                os.remove(clothing_path)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
