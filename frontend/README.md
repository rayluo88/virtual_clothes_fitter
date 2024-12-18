# AI Fitting App Frontend

The frontend application for the AI Fitting virtual try-on system. Built with Next.js and TypeScript.

## Features

- Modern React components with TypeScript
- Responsive design with Tailwind CSS
- Image upload with drag & drop support
- Real-time image processing preview
- Secure API integration with backend

## Tech Stack

- Next.js 15.1.0
- React 19
- TypeScript
- Tailwind CSS
- Axios
- React-dropzone

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

2. Create a `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start the development server:
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
│   └── Preview/        # Result preview components
└── lib/
    └── api.ts         # API integration utilities
```

## Development

### Key Components

- `ImageUploader`: Handles image upload with drag & drop
- `Preview`: Displays processed images and results
- `Layout`: Main application layout and navigation

### API Integration

The frontend communicates with the backend through these main endpoints:

- `POST /process-images`: Submit images for processing
- `GET /health`: Backend health check

### State Management

- React hooks for local state
- Context API for global state (when needed)
- Form state handled by controlled components

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
