import { useState, useRef } from 'react';
import { Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
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

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <>
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept=".pdf,.doc,.docx"
        onChange={handleFileChange}
        disabled={isUploading}
      />
      <Button
        variant="outline"
        size="sm"
        className="border-white/20 text-white hover:bg-white/10 transition-colors"
        onClick={handleButtonClick}
        disabled={isUploading}
      >
        <Upload className="h-4 w-4 mr-2" />
        {isUploading ? 'Uploading...' : 'Upload CV'}
      </Button>
      {isUploading && (
        <div className="mt-2 text-sm text-white/40">
          Analyzing your CV...
        </div>
      )}
    </>
  );
}
