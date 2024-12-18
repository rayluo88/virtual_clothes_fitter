import React from 'react';

interface Measurements {
  shoulder_width: number;
  torso_height: number;
  chest_width: number;
  shoulder_to_chest_ratio: number;
  torso_aspect_ratio: number;
}

interface MeasurementsDisplayProps {
  measurements: Measurements;
}

function validateMeasurements(measurements: Partial<Measurements>): measurements is Measurements {
  return (
    typeof measurements?.shoulder_width === 'number' &&
    typeof measurements?.torso_height === 'number' &&
    typeof measurements?.chest_width === 'number' &&
    typeof measurements?.shoulder_to_chest_ratio === 'number' &&
    typeof measurements?.torso_aspect_ratio === 'number'
  );
}

function getSizeRecommendation(measurements: Measurements): string {
  // Basic size recommendation based on shoulder width and chest measurements
  const { shoulder_width, chest_width, shoulder_to_chest_ratio } = measurements;
  
  // These thresholds are approximate and should be adjusted based on your data
  if (shoulder_width < 380) return 'XS';
  if (shoulder_width < 400) return 'S';
  if (shoulder_width < 420) return 'M';
  if (shoulder_width < 440) return 'L';
  return 'XL';
}

function getProportionDescription(ratio: number): string {
  if (ratio < 0.8) return 'Slim';
  if (ratio < 1.0) return 'Regular';
  if (ratio < 1.2) return 'Athletic';
  return 'Broad';
}

export default function MeasurementsDisplay({ measurements }: MeasurementsDisplayProps) {
  // Validate measurements
  if (!validateMeasurements(measurements)) {
    return (
      <div className="bg-red-50 p-4 rounded-lg">
        <p className="text-red-600">Error: Invalid measurement data</p>
      </div>
    );
  }

  const sizeRecommendation = getSizeRecommendation(measurements);
  const buildType = getProportionDescription(measurements.shoulder_to_chest_ratio);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <div className="space-y-6">
        {/* Size Recommendation */}
        <div className="text-center pb-4 border-b border-gray-200">
          <h3 className="text-xl font-semibold text-gray-900">Recommended Size</h3>
          <div className="mt-2 text-3xl font-bold text-blue-600">{sizeRecommendation}</div>
          <p className="mt-1 text-sm text-gray-500">Based on your measurements</p>
        </div>

        {/* Body Type */}
        <div className="text-center pb-4 border-b border-gray-200">
          <h4 className="text-lg font-medium text-gray-900">Body Type</h4>
          <div className="mt-1 text-xl font-semibold text-gray-700">{buildType}</div>
        </div>

        {/* Detailed Measurements */}
        <div>
          <h4 className="text-lg font-medium text-gray-900 mb-3">Detailed Measurements</h4>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Shoulder Width</span>
              <div className="flex items-center space-x-2">
                <span className="font-medium">{measurements.shoulder_width.toFixed(1)}</span>
                <span className="text-sm text-gray-500">px</span>
              </div>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Chest Width</span>
              <div className="flex items-center space-x-2">
                <span className="font-medium">{measurements.chest_width.toFixed(1)}</span>
                <span className="text-sm text-gray-500">px</span>
              </div>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Torso Height</span>
              <div className="flex items-center space-x-2">
                <span className="font-medium">{measurements.torso_height.toFixed(1)}</span>
                <span className="text-sm text-gray-500">px</span>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-600">Shoulder/Chest Ratio</span>
              <span className="font-medium">{measurements.shoulder_to_chest_ratio.toFixed(2)}</span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-gray-600">Torso Ratio</span>
              <span className="font-medium">{measurements.torso_aspect_ratio.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Fit Tips */}
        <div className="mt-4 p-4 bg-blue-50 rounded-md">
          <h4 className="text-sm font-medium text-blue-900 mb-2">Fit Tips</h4>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• {buildType} build: {
              buildType === 'Slim' ? 'Consider fitted or slim-cut styles' :
              buildType === 'Regular' ? 'Most standard cuts will fit well' :
              buildType === 'Athletic' ? 'Look for styles with room in shoulders' :
              'Choose relaxed fits for comfort'
            }</li>
            <li>• Recommended length based on torso height: {
              measurements.torso_height < 400 ? 'Standard length should work well' :
              measurements.torso_height < 450 ? 'Consider regular fit length' :
              'You might prefer longer cuts'
            }</li>
          </ul>
        </div>
      </div>
    </div>
  );
} 