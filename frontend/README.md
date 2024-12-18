# AI Fitting App Frontend

The frontend application for the AI Fitting virtual try-on system. Built with Next.js and TypeScript.

## Features

- Modern React components with TypeScript
- Responsive design with Tailwind CSS
- Image upload with drag & drop support
- Real-time backend status monitoring
- Interactive measurements display
- Size recommendations
- Body type analysis
- Error handling and validation

## Tech Stack

- Next.js 13+
- React 18+
- TypeScript
- Tailwind CSS
- React Hooks
- Type-safe API integration

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn
- Backend server running (see main README)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Project Structure

```
src/
├── app/
│   ├── page.tsx        # Main application page
│   ├── layout.tsx      # Root layout
│   └── globals.css     # Global styles
├── components/
│   ├── ImageUploader/  # Image upload functionality
│   ├── FittingResult/  # Results display
│   └── MeasurementsDisplay/ # Measurements UI
└── lib/
    └── api.ts         # API integration utilities
```

## Components

### ImageUploader
- Drag & drop file upload
- File type validation
- Size validation
- Preview functionality

### FittingResult
- Processed image display
- Download functionality
- Fullscreen view
- Image quality information

### MeasurementsDisplay
- Size recommendations
- Body type analysis
- Detailed measurements
- Fit tips
- Error handling

## Development

### State Management
- React hooks for local state
- TypeScript for type safety
- Proper error handling
- Loading states

### API Integration
The frontend communicates with the backend through these endpoints:

- `GET /health` - Backend health check
- `POST /process-images` - Submit images for processing
- `GET /measurements/{id}` - Get measurements

### Error Handling
- Input validation
- Network error handling
- Backend status monitoring
- Invalid data handling
- User feedback

## Building for Production

```bash
npm run build
npm start
```

## Testing

```bash
npm run test        # Run unit tests
npm run test:e2e    # Run end-to-end tests
```

## Contributing

1. Follow the project's coding standards
2. Write meaningful commit messages
3. Add tests for new features
4. Update documentation as needed

## Type Safety

The application uses TypeScript for full type safety:

```typescript
interface Measurements {
  shoulder_width: number;
  torso_height: number;
  chest_width: number;
  shoulder_to_chest_ratio: number;
  torso_aspect_ratio: number;
}

interface ProcessingResult {
  status: string;
  measurements: Measurements;
  result_url: string;
}
```
