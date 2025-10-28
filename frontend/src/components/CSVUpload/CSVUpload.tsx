import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { AlertCircle, FileText, Upload, X } from "lucide-react";
import { useCallback, useRef, useState } from "react";

interface CSVUploadProps {
  onFileSelect?: (file: File) => void;
  onFileRemove?: () => void;
  onFileUpload?: (file: File) => void;
  maxSize?: number;
  className?: string;
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
}

export function CSVUpload({
  onFileSelect,
  onFileRemove,
  onFileUpload,
  maxSize = 10,
  className,
  selectedFile,
  setSelectedFile,
}: CSVUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false);

  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = useCallback(
    (file: File): string | null => {
      if (!file.name.toLowerCase().endsWith(".csv")) {
        return "There are only csv files allowed";
      }

      return null;
    },
    [maxSize]
  );

  const handleFileSelect = useCallback(
    (file: File) => {
      const validationError = validateFile(file);

      if (validationError) {
        setError(validationError);
        return;
      }

      setError(null);
      setSelectedFile(file);
    },
    [validateFile, onFileSelect]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);

      const files = Array.from(e.dataTransfer.files);
      if (files.length > 0) {
        handleFileSelect(files[0]);
      }
    },
    [handleFileSelect]
  );

  const handleFileInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        handleFileSelect(files[0]);
      }
    },
    [handleFileSelect]
  );

  const handleRemoveFile = useCallback(() => {
    setSelectedFile(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    onFileRemove?.();
  }, [onFileRemove]);

  const handleUploadFile = useCallback(() => {
    if (selectedFile) {
      onFileUpload?.(selectedFile);
    }
  }, [selectedFile, onFileUpload]);

  const handleClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  return (
    <div className={cn("w-full", className)}>
      <Card className="border-2 border-dashed border-gray-300 hover:border-gray-400 transition-colors p-0 m-1">
        <CardContent className="p-1">
          {!selectedFile ? (
            <div
              className={cn(
                "flex flex-col items-center justify-center space-y-3 py-6 cursor-pointer transition-colors",
                isDragOver ? "bg-blue-50 border-blue-300" : "hover:bg-gray-50"
              )}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={handleClick}
            >
              <div
                className={cn(
                  "p-2 rounded-full transition-colors",
                  isDragOver ? "bg-blue-100" : "bg-gray-100"
                )}
              >
                <Upload
                  className={cn(
                    "h-6 w-6",
                    isDragOver ? "text-blue-600" : "text-gray-600"
                  )}
                />
              </div>

              <div className="text-center space-y-1">
                <h3 className="text-base font-semibold text-gray-900">
                  {isDragOver ? "Suelta el archivo aquí" : "Subir archivo CSV"}
                </h3>
                <p className="text-xs text-gray-500">
                  Drag and drop your csv file here, or click to select
                </p>
              </div>

              <Button
                type="button"
                variant="outline"
                size="sm"
                className="mt-2"
                onClick={(e) => {
                  e.stopPropagation();
                  handleClick();
                }}
              >
                Select file
              </Button>
            </div>
          ) : (
            <div className="flex items-center justify-between p-2 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="p-1.5 bg-green-100 rounded-full">
                  <FileText className="h-4 w-4 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-green-900">
                    {selectedFile.name}
                  </p>
                  <p className="text-xs text-green-600">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Button
                  type="button"
                  size="sm"
                  onClick={handleUploadFile}
                  className="bg-green-600 hover:bg-green-700 text-white"
                >
                  <Upload className="h-4 w-4 mr-1" />
                  Upload
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={handleRemoveFile}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileInputChange}
            className="hidden"
          />
        </CardContent>
      </Card>

      {error && (
        <Alert className="mt-4 border-red-200 bg-red-50">
          <AlertCircle className="h-4 w-4 text-red-600" />
          <AlertDescription className="text-red-800">{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
