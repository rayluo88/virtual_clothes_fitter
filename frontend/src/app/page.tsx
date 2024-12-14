'use client';
import { useState, useEffect } from 'react';
import axios from 'axios';
import ImageUploader from '@/components/ImageUploader';

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<string>('Loading...');
  const [userImage, setUserImage] = useState<File | null>(null);
  const [clothingImage, setClothingImage] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/health');
        setBackendStatus(response.data.status);
      } catch (error) {
        setBackendStatus('Error connecting to backend');
      }
    };

    checkBackend();
  }, []);

  const handleUserImageSelect = (file: File) => {
    setUserImage(file);
    setResult(null);
  };

  const handleClothingImageSelect = (file: File) => {
    setClothingImage(file);
    setResult(null);
  };

  const handleSubmit = async () => {
    if (!userImage || !clothingImage) {
      alert('Please upload both images');
      return;
    }

    setIsProcessing(true);
    try {
      const formData = new FormData();
      formData.append('user_image', userImage);
      formData.append('clothing_image', clothingImage);

      const response = await axios.post('http://127.0.0.1:8000/process-images', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data.result_url);
    } catch (error) {
      alert('Error processing images. Please try again.');
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">AI Fitting App</h1>
        
        <div className="mb-4 text-center">
          <p>Backend Status: <span className="font-semibold">{backendStatus}</span></p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-8">
          <div>
            <h2 className="text-xl font-semibold mb-4 text-center">Upload Your Photo</h2>
            <ImageUploader type="user" onImageSelect={handleUserImageSelect} />
          </div>
          
          <div>
            <h2 className="text-xl font-semibold mb-4 text-center">Upload Clothing Image</h2>
            <ImageUploader type="clothing" onImageSelect={handleClothingImageSelect} />
          </div>
        </div>

        <div className="text-center">
          <button
            onClick={handleSubmit}
            disabled={!userImage || !clothingImage || isProcessing}
            className={`px-6 py-2 rounded-lg font-semibold
              ${(!userImage || !clothingImage || isProcessing)
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
          >
            {isProcessing ? 'Processing...' : 'Process Images'}
          </button>
        </div>

        {result && (
          <div className="mt-8 text-center">
            <h2 className="text-xl font-semibold mb-4">Result</h2>
            <img src={result} alt="Processed Result" className="max-w-full mx-auto" />
          </div>
        )}
      </div>
    </main>
  );
}