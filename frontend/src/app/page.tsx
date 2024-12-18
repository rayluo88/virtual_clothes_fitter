'use client';

import { useState, useEffect } from 'react';
import ImageUploader from '@/components/ImageUploader';
import FittingResult from '@/components/FittingResult';
import { ArrowPathIcon } from '@heroicons/react/24/outline';

interface ProcessingResult {
  status: string;
  measurements: {
    shoulder_width: number;
    torso_height: number;
    chest_width: number;
    shoulder_to_chest_ratio: number;
    torso_aspect_ratio: number;
  };
  result_url: string;
}

export default function Home() {
  const [userImage, setUserImage] = useState<File | null>(null);
  const [clothingImage, setClothingImage] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'offline'>('checking');

  useEffect(() => {
    checkBackendStatus();
    // Check status every 30 seconds
    const interval = setInterval(checkBackendStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        setBackendStatus('connected');
      } else {
        setBackendStatus('offline');
      }
    } catch (error) {
      setBackendStatus('offline');
    }
  };

  const handleProcess = async () => {
    if (!userImage || !clothingImage) {
      setError('Please upload both a user photo and a clothing image.');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('user_image', userImage);
      formData.append('clothing_image', clothingImage);

      const response = await fetch('http://localhost:8000/process-images', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to process images');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setUserImage(null);
    setClothingImage(null);
    setResult(null);
    setError(null);
  };

  return (
    <main className="min-h-screen bg-gray-50">
      {!result ? (
        <div className="max-w-4xl mx-auto px-4 py-12">
          {/* Backend Status */}
          <div className="mb-8 text-center">
            <p className="text-sm">
              Backend Status:{' '}
              <span
                className={`font-medium ${
                  backendStatus === 'connected'
                    ? 'text-green-600'
                    : backendStatus === 'checking'
                    ? 'text-yellow-600'
                    : 'text-red-600'
                }`}
              >
                {backendStatus === 'checking'
                  ? 'Checking...'
                  : backendStatus === 'connected'
                  ? 'Connected'
                  : 'Offline'}
              </span>
              {backendStatus === 'offline' && (
                <button
                  onClick={checkBackendStatus}
                  className="ml-2 text-blue-600 hover:text-blue-700 text-sm"
                >
                  Retry
                </button>
              )}
            </p>
          </div>

          <div className="text-center mb-12">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Virtual Clothing Try-On
            </h1>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Upload your photo and a clothing item to see how it looks on you.
              Our AI will analyze your measurements and provide size recommendations.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-8">
            <div>
              <h2 className="text-lg font-semibold mb-4">Your Photo</h2>
              <ImageUploader
                type="user"
                onImageSelect={(file) => setUserImage(file)}
              />
            </div>
            <div>
              <h2 className="text-lg font-semibold mb-4">Clothing Item</h2>
              <ImageUploader
                type="clothing"
                onImageSelect={(file) => setClothingImage(file)}
              />
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 rounded-md">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          <div className="text-center">
            <button
              onClick={handleProcess}
              disabled={isProcessing || !userImage || !clothingImage || backendStatus !== 'connected'}
              className={`
                inline-flex items-center px-6 py-3 rounded-md text-white
                ${isProcessing || !userImage || !clothingImage || backendStatus !== 'connected'
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'}
                transition-colors duration-200
              `}
            >
              {isProcessing && (
                <ArrowPathIcon className="w-5 h-5 mr-2 animate-spin" />
              )}
              {isProcessing ? 'Processing...' : 'Try It On'}
            </button>
            {backendStatus !== 'connected' && (
              <p className="mt-2 text-sm text-red-600">
                Please wait for the backend to be available
              </p>
            )}
          </div>
        </div>
      ) : (
        <div>
          <div className="bg-white border-b">
            <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Virtual Try-On Result
              </h1>
              <button
                onClick={handleReset}
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                Try Another
              </button>
            </div>
          </div>
          
          <FittingResult
            resultImageUrl={`http://localhost:8000${result.result_url}`}
            measurements={result.measurements}
          />
        </div>
      )}
    </main>
  );
}