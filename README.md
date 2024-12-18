# AI Fitting App

A virtual try-on application that helps users visualize how clothes will look on them before purchasing. The app uses AI-powered technology to provide accurate clothing visualization and size recommendations.

## Current Status - MVP Phase 1

### Implemented Features ✓
- Image upload with drag & drop support
- Pose detection and validation
- Body measurements extraction
- Size recommendations
- Body type analysis
- Real-time backend status monitoring
- Error handling and validation
- Responsive UI design

### In Progress 🚧
- MGN (Multi-Garment Network) integration
- Advanced cloth draping simulation
- Improved pose detection accuracy
- Enhanced image processing quality
- Unit test coverage

### Planned Features ⏳
- Multiple clothing items support
- 3D visualization
- User profile and history
- Style recommendations
- Mobile responsiveness
- Performance optimization

## Tech Stack

### Frontend
- Next.js 13+ with TypeScript
- React 18+ with modern hooks
- Tailwind CSS for styling
- Responsive design components
- Real-time status monitoring
- Type-safe measurements interface

### Backend
- FastAPI for REST API
- Python 3.8+
- PyTorch for deep learning
- MediaPipe for pose detection
- OpenCV for image processing
- Advanced error handling

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Virtual environment for Python
- Git

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
- API Documentation: http://localhost:8000/docs

## Project Structure

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx        # Main application page
│   │   │   ├── layout.tsx      # Root layout
│   │   │   └── globals.css     # Global styles
│   │   ├── components/
│   │   │   ├── ImageUploader/  # Image upload component
│   │   │   ├── FittingResult/  # Results display
│   │   │   └── MeasurementsDisplay/ # Measurements UI
│   │   └── lib/
│   │       └── api.ts         # API integration
│   ├── public/                # Static assets
│   └── [config files]        # Configuration files
└── backend/
    ├── main.py               # FastAPI application
    ├── image_processor.py    # Image processing logic
    ├── requirements.txt      # Python dependencies
    └── static/              # Processed images storage
```

## Features

### Image Processing
- Pose detection using MediaPipe
- Body measurements extraction
- Size recommendations
- Body type analysis

### User Interface
- Drag & drop image upload
- Real-time backend status
- Interactive measurements display
- Responsive design
- Error handling

### API Endpoints
- `GET /health` - Backend health check
- `POST /process-images` - Process user and clothing images
- `GET /measurements/{image_id}` - Get stored measurements

## Development

### Current Limitations
- Single front-view processing only
- Basic clothing overlay
- Limited pose variations
- No size history
- No style management

### Error Handling
- Input validation
- Pose detection validation
- Image format validation
- Network error handling
- Measurement validation

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
