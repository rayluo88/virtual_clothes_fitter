# AI Fitting App Backend

The backend server for the AI Fitting virtual try-on system. Built with FastAPI and PyTorch.

## Features

- FastAPI REST API
- PyTorch-based MGN model
- MediaPipe pose detection
- Body measurements extraction
- Size recommendations
- Error handling and validation
- Efficient image processing pipeline

## Tech Stack

- Python 3.8+
- FastAPI
- PyTorch 2.5+
- MediaPipe
- OpenCV
- NumPy

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
- Virtual environment tool
- CUDA-capable GPU (optional, for faster processing)

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Project Structure

```
backend/
├── main.py                 # FastAPI application and routes
├── image_processor.py      # Image processing and ML models
├── requirements.txt        # Python dependencies
└── static/                # Processed images storage
```

## API Endpoints

### Health Check
```
GET /health
Response: {
    "status": "ok",
    "timestamp": "2024-01-01T00:00:00.000Z",
    "service": "AI Fitting App API",
    "version": "1.0.0"
}
```

### Process Images
```
POST /process-images
Content-Type: multipart/form-data
Body: 
  - user_image: file
  - clothing_image: file
Response: 
  - status: string
  - measurements: object
  - result_url: string
```

## Image Processing Pipeline

1. Image Validation
   - Format checking
   - Size validation
   - Quality assessment

2. Pose Detection
   - MediaPipe pose detection
   - Landmark extraction
   - Pose validation

3. Measurements Extraction
   - Body measurements calculation
   - Size recommendations
   - Body type analysis

4. Virtual Try-On
   - MGN model processing
   - Image transformation
   - Result generation

## Development

### Running Tests
```bash
pytest
pytest --cov=app tests/
```

### Code Style
The project follows PEP 8 guidelines. Run linting:
```bash
flake8
black .
```

### Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request (invalid input)
- 422: Unprocessable Entity (invalid image)
- 500: Internal Server Error

## Models

### MGN (Multi-Garment Network)
- Input: User photo and clothing image
- Output: Virtual try-on result
- Resolution: 256x256
- Supported formats: JPEG, PNG

### Pose Detection
- Framework: MediaPipe
- Confidence threshold: 0.7
- Model complexity: 2
- Key points: 33 landmarks

## Contributing

1. Follow Python best practices
2. Add docstrings for new functions
3. Include tests for new features
4. Update API documentation

## Performance

### Hardware Requirements
- Minimum: 4GB RAM, CPU
- Recommended: 8GB RAM, CUDA GPU
- Storage: 1GB for models and cache

### Processing Times
- Pose Detection: ~100ms
- Measurements: ~50ms
- Virtual Try-on: ~200ms
- Total: ~350ms per request