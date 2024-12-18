import React from 'react';
import MeasurementsDisplay from './MeasurementsDisplay';
import { ArrowDownTrayIcon, ArrowsPointingOutIcon } from '@heroicons/react/24/outline';

interface FittingResultProps {
  resultImageUrl: string;
  measurements: {
    shoulder_width: number;
    torso_height: number;
    chest_width: number;
    shoulder_to_chest_ratio: number;
    torso_aspect_ratio: number;
  };
}

export default function FittingResult({ resultImageUrl, measurements }: FittingResultProps) {
  const [isFullscreen, setIsFullscreen] = React.useState(false);

  const handleDownload = async () => {
    try {
      const response = await fetch(resultImageUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'virtual-fitting-result.jpg';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading image:', error);
    }
  };

  const handleFullscreen = () => {
    const img = document.getElementById('result-image') as HTMLImageElement;
    if (!isFullscreen && img) {
      if (img.requestFullscreen) {
        img.requestFullscreen();
      }
      setIsFullscreen(true);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Result Image Section */}
        <div className="space-y-4">
          <div className="relative group">
            <img
              id="result-image"
              src={resultImageUrl}
              alt="Virtual Try-on Result"
              className="w-full rounded-lg shadow-lg object-cover"
            />
            <div className="absolute bottom-4 right-4 space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                onClick={handleFullscreen}
                className="bg-white p-2 rounded-full shadow-md hover:bg-gray-100 transition-colors"
                title="View fullscreen"
              >
                <ArrowsPointingOutIcon className="h-5 w-5 text-gray-600" />
              </button>
              <button
                onClick={handleDownload}
                className="bg-white p-2 rounded-full shadow-md hover:bg-gray-100 transition-colors"
                title="Download image"
              >
                <ArrowDownTrayIcon className="h-5 w-5 text-gray-600" />
              </button>
            </div>
          </div>
          
          {/* Image Quality Notice */}
          <div className="bg-gray-50 p-4 rounded-md">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Image Quality</h4>
            <p className="text-sm text-gray-600">
              This is a virtual try-on preview. Actual garment appearance may vary slightly.
              For best results, use a well-lit, front-facing photo against a plain background.
            </p>
          </div>
        </div>

        {/* Measurements Section */}
        <div>
          <MeasurementsDisplay measurements={measurements} />
          
          {/* Additional Information */}
          <div className="mt-6 bg-gray-50 p-4 rounded-md">
            <h4 className="text-sm font-medium text-gray-900 mb-2">About Measurements</h4>
            <p className="text-sm text-gray-600">
              Measurements are calculated using AI-powered body detection.
              For the most accurate results, wear fitted clothing in your photo
              and stand straight with arms slightly away from your body.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 