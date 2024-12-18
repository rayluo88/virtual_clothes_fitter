from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
import cv2
import numpy as np
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging
from image_processor import ImageProcessor, ProcessingConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Fitting App API",
    description="API for virtual clothing try-on and body measurements",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_dir = "static"
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize image processor with custom config
processor_config = ProcessingConfig(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=2,
    blur_kernel_size=31,
    blur_sigma=15,
    clahe_clip_limit=3.0,
    clahe_grid_size=(8, 8),
    edge_low_threshold=100,
    edge_high_threshold=200
)
image_processor = ImageProcessor(config=processor_config)

def save_upload_file(upload_file: UploadFile) -> str:
    """Save uploaded file and return the file path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{upload_file.filename}"
    file_path = os.path.join(static_dir, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(upload_file.file.read())
        return file_path
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving uploaded file")

def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file"""
    # Check file size (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size too large")
    
    # Check file type
    allowed_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "name": "AI Fitting App API",
        "version": "1.0.0",
        "description": "Virtual clothing try-on and body measurements API",
        "endpoints": {
            "POST /process-images": "Process user and clothing images",
            "GET /health": "Health check endpoint",
            "GET /measurements/{image_id}": "Get measurements for a processed image",
            "GET /docs": "API documentation (Swagger UI)",
            "GET /redoc": "API documentation (ReDoc)"
        },
        "status": "running",
        "documentation_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Fitting App API",
        "version": "1.0.0"
    }

@app.post("/process-images", response_model=Dict)
async def process_images(
    user_image: UploadFile = File(..., description="User's photo for virtual try-on"),
    clothing_image: UploadFile = File(..., description="Clothing item image to try on"),
):
    """
    Process user and clothing images for virtual try-on
    
    - **user_image**: Front-facing photo of the user
    - **clothing_image**: Image of the clothing item to try on
    
    Returns:
    - **status**: Processing status
    - **measurements**: Body measurements and proportions
    - **result_url**: URL of the processed image
    """
    try:
        # Validate uploaded files
        validate_image(user_image)
        validate_image(clothing_image)
        
        # Save uploaded files
        user_image_path = save_upload_file(user_image)
        clothing_image_path = save_upload_file(clothing_image)
        
        # Process images
        result_image, measurements = image_processor.process_images(
            user_image_path,
            clothing_image_path
        )
        
        # Save result image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_filename = f"result_{timestamp}.jpg"
        result_path = os.path.join(static_dir, result_filename)
        cv2.imwrite(result_path, result_image)
        
        # Clean up temporary files
        os.remove(user_image_path)
        os.remove(clothing_image_path)
        
        return {
            "status": "success",
            "measurements": measurements,
            "result_url": f"/static/{result_filename}"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing images: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail="Error processing images")

@app.get("/measurements/{image_id}")
async def get_measurements(image_id: str):
    """
    Get measurements for a processed image
    
    - **image_id**: ID of the processed image
    
    Returns:
    - Body measurements and proportions
    """
    # TODO: Implement measurement storage and retrieval
    raise HTTPException(status_code=501, detail="Not implemented yet")

# Customize OpenAPI documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI Fitting App API",
        version="1.0.0",
        description="API for virtual clothing try-on and body measurements",
        routes=app.routes,
    )
    
    # Add additional metadata
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"  # Add your logo URL here
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
