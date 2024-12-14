# AI Fitting App - Technical Design

## Project Structure 
project-root/
├── frontend/
│ ├── src/
│ │ ├── app/
│ │ │ ├── page.tsx # Main application page
│ │ │ ├── layout.tsx # Root layout with fonts
│ │ │ └── globals.css # Global styles
│ │ └── components/
│ │ └── ImageUploader.tsx # Reusable image upload component
│ ├── public/ # Static assets
│ └── [config files] # Next.js, TypeScript, Tailwind configs
└── backend/
├── main.py # FastAPI application
├── requirements.txt # Python dependencies
└── venv/ # Python virtual environment

## Technical Stack

### Frontend
- Next.js 15.1.0 with TypeScript
- React 19 with modern hooks
- Tailwind CSS for styling
- Axios for API communication
- react-dropzone for file uploads
- @heroicons/react for icons

### Backend
- FastAPI for REST API
- Python 3.x
- Image processing: Pillow, NumPy
- CORS middleware enabled

## Key Components

### ImageUploader
- Drag & drop interface
- Image preview functionality
- File type validation
- Size limits (10MB)
- Progress feedback

### Main Application Page
- Dual upload zones (user photo & clothing)
- Backend health monitoring
- Processing status handling
- Result display

## API Endpoints

Current:
- GET `/` - Welcome message
- GET `/health` - Backend health check

Planned:
- POST `/process-images` - Image processing endpoint

## Development Setup

### Frontend
- Development server: `npm run dev` (with turbopack)
- TypeScript for type safety
- ESLint for code quality
- Tailwind for responsive design

### Backend
- Virtual environment for dependency isolation
- FastAPI with automatic OpenAPI docs
- CORS configured for local development

## Technical Highlights

1. Type Safety
   - TypeScript throughout frontend
   - Type definitions for props and state
   - API response typing

2. Modern React Patterns
   - Client components with 'use client'
   - React hooks for state management
   - Callback optimization

3. Scalable Architecture
   - Clear separation of frontend/backend
   - Component-based UI architecture
   - Modular file structure

4. Development Experience
   - Hot reload enabled
   - Development tools configured
   - Clear project structure