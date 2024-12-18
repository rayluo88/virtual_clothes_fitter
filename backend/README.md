# AI Fitting App Backend

The backend server for the AI Fitting virtual try-on system. Built with FastAPI and Python.

## Features

- FastAPI REST API
- Image processing with OpenCV and MediaPipe
- Pose detection and clothing alignment
- Error handling and validation
- Efficient image processing pipeline

## Tech Stack

- Python 3.8+
- FastAPI
- OpenCV
- MediaPipe
- PIL (Python Imaging Library)
- NumPy

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip
- Virtual environment tool

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

3. Create a `.env` file:
```bash
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
MAX_UPLOAD_SIZE=10485760  # 10MB
```

4. Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Project Structure

```
backend/
├── main.py                 # FastAPI application and routes
├── image_processor.py      # Image processing logic
├── requirements.txt        # Python dependencies
└── static/                # Processed images and assets
```

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "ok"}
```

### Process Images
```
POST /process-images
Content-Type: multipart/form-data
Body: 
  - user_image: file
  - clothing_image: file
Response: 
  - processed_image_url: string
  - measurements: object
```

## Image Processing Pipeline

1. Image Validation
   - Format checking
   - Size validation
   - Quality assessment

2. Pose Detection
   - Body landmark detection
   - Key points extraction
   - Pose estimation

3. Clothing Processing
   - Background removal
   - Size adjustment
   - Perspective transformation

4. Image Overlay
   - Alignment with body landmarks
   - Blending and color adjustment
   - Final rendering

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

## Contributing

1. Follow Python best practices
2. Add docstrings for new functions
3. Include tests for new features
4. Update API documentation 