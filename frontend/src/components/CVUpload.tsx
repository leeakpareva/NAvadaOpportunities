import { useState } from 'react';
import { parseCV } from '@/lib/api';
import type { CVParseResponse } from '@/types/files';

interface CVUploadProps {
  onUploadSuccess: (data: CVParseResponse['data']) => void;
  onUploadError: (error: string) => void;
}

export function CVUpload({ onUploadSuccess, onUploadError }: CVUploadProps) {
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setIsUploading(true);
      const response = await parseCV(file);
      onUploadSuccess(response.data);
    } catch (error) {
      onUploadError(error instanceof Error ? error.message : 'Failed to upload CV');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full max-w-md p-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-lg">
      <label
        htmlFor="cv-upload"
        className="block w-full p-4 text-center border-2 border-dashed border-white/20 rounded-lg cursor-pointer hover:border-white/40 transition-colors"
      >
        <span className="text-white/60">
          {isUploading ? 'Uploading...' : 'Upload your CV (PDF, DOC, DOCX)'}
        </span>
        <input
          id="cv-upload"
          type="file"
          className="hidden"
          accept=".pdf,.doc,.docx"
          onChange={handleFileChange}
          disabled={isUploading}
        />
      </label>
      {isUploading && (
        <div className="mt-2 text-sm text-white/40 text-center">
          Analyzing your CV...
        </div>
      )}
    </div>
  );
}
