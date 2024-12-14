# AI Fitting App

A virtual try-on application that helps users visualize how clothes will look on them before purchasing. The app uses AI-powered technology to provide accurate clothing visualization, saving time and reducing returns.

## Features

### Virtual Try-On
- Upload personal photos
- See clothes fitted to your body
- Real-time preview
- High-quality rendering

### Smart Sizing
- Automatic body measurements
- Size recommendations
- Fit predictions
- Personalized adjustments

### Style Management
- Save favorite looks
- Share results
- Purchase links
- Style history

## Tech Stack

### Frontend
- Next.js 15.1.0 with TypeScript
- React 19 with modern hooks
- Tailwind CSS for styling
- Axios for API communication
- react-dropzone for file uploads

### Backend
- FastAPI for REST API
- Python 3.x
- OpenCV and MediaPipe for image processing
- PIL (Python Imaging Library)
- NumPy for numerical operations

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Virtual environment for Python

### Backend Setup
1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the server:
```bash
uvicorn main:app --reload
```

### Frontend Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Project Structure

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx        # Main application page
│   │   │   ├── layout.tsx      # Root layout
│   │   │   └── globals.css     # Global styles
│   │   └── components/
│   │       └── ImageUploader.tsx # Image upload component
│   ├── public/                  # Static assets
│   └── [config files]          # Configuration files
└── backend/
    ├── main.py                 # FastAPI application
    ├── image_processor.py      # Image processing logic
    ├── requirements.txt        # Python dependencies
    └── venv/                   # Python virtual environment
```

## Development

### API Endpoints
- GET `/health` - Backend health check
- POST `/process-images` - Process user and clothing images

### Key Components
- ImageUploader: Handles image upload with drag & drop
- Image Processor: Manages clothing overlay and pose detection

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
