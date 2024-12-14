'use client';
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline';

type ImageType = 'user' | 'clothing';

interface ImageUploaderProps {
  type: ImageType;
  onImageSelect: (file: File) => void;
}

export default function ImageUploader({ type, onImageSelect }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    onImageSelect(file);
    
    // Create preview
    const objectUrl = URL.createObjectURL(file);
    setPreview(objectUrl);

    // Clean up preview URL when component unmounts
    return () => URL.revokeObjectURL(objectUrl);
  }, [onImageSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1
  });

  return (
    <div className="w-full max-w-md mx-auto">
      <div
        {...getRootProps()}
        className={`p-6 border-2 border-dashed rounded-lg text-center cursor-pointer
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
          ${preview ? 'border-green-500' : ''}`}
      >
        <input {...getInputProps()} />
        
        {preview ? (
          <div className="space-y-4">
            <img 
              src={preview} 
              alt="Preview" 
              className="max-h-48 mx-auto object-contain"
            />
            <p className="text-sm text-gray-500">Click or drag to replace</p>
          </div>
        ) : (
          <div className="space-y-4">
            <ArrowUpTrayIcon className="h-8 w-8 mx-auto text-gray-400" />
            <div className="space-y-1">
              <p className="text-sm text-gray-500">
                Click or drag file to upload {type === 'user' ? 'your photo' : 'clothing image'}
              </p>
              <p className="text-xs text-gray-400">
                PNG, JPG up to 10MB
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
