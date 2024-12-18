# AI Fitting App

A virtual try-on application that helps users visualize how clothes will look on them before purchasing. The app uses AI-powered technology to provide accurate clothing visualization, saving time and reducing returns.

## Current Status - MVP Phase 1

### Implemented Features ✓
- Basic image upload and validation
- Simple clothing overlay on user photos
- Pose detection and basic fitting
- Result preview and download
- Basic error handling and validation
- Development environment setup
- Project documentation

### In Progress 🚧
- Enhanced image processing pipeline
- Improved pose detection accuracy
- Better clothing alignment algorithms
- Unit test coverage
- API response optimization

### Planned Features ⏳
- Real-time preview
- Smart sizing recommendations
- Multiple clothing items support
- Style management system
- User profile and preferences
- Social sharing integration
- Mobile responsiveness
- Performance optimization

## Tech Stack

### Frontend
- Next.js 15.1.0 with TypeScript
- React 19 with modern hooks
- Tailwind CSS for styling
- Axios for API communication
- React-dropzone for file uploads
- Jest and React Testing Library

### Backend
- FastAPI for REST API
- Python 3.8+
- OpenCV and MediaPipe for image processing
- PIL (Python Imaging Library)
- NumPy for numerical operations
- pytest for testing

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

3. Create `.env` file with required configurations

4. Start the server:
```bash
uvicorn main:app --reload
```

### Frontend Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create `.env.local` with required configurations

3. Start the development server:
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
│   │   ├── components/
│   │   │   ├── ImageUploader/  # Image upload component
│   │   │   └── Preview/        # Result preview
│   │   └── lib/
│   │       └── api.ts          # API integration
│   ├── public/                 # Static assets
│   └── [config files]         # Configuration files
└── backend/
    ├── main.py                # FastAPI application
    ├── image_processor.py     # Image processing logic
    ├── requirements.txt       # Python dependencies
    └── static/               # Processed images storage
```

## Development

### API Endpoints
- GET `/health` - Backend health check
- POST `/process-images` - Process user and clothing images

### Key Components
- ImageUploader: Handles image upload with drag & drop
- Image Processor: Manages clothing overlay and pose detection
- Preview: Displays processing results
- API Integration: Handles communication between frontend and backend

### Current Limitations
- Single front-view processing only
- Basic clothing overlay
- Limited pose detection accuracy
- No size recommendations
- No style management
- Limited error handling

## Testing

### Frontend
```bash
cd frontend
npm run test        # Unit tests
npm run test:e2e    # End-to-end tests
```

### Backend
```bash
cd backend
pytest              # Unit tests
pytest --cov=app    # Coverage report
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
