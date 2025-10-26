import { useCallback, useState } from 'react'
import { Upload, File, X } from 'lucide-react'
import { Card } from './ui/card'
import { Button } from './ui/button'

interface UploadZoneProps {
  onFileSelect: (file: File) => void
  selectedFile: File | null
  onClearFile: () => void
}

export function UploadZone({ onFileSelect, selectedFile, onClearFile }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const validateFile = (file: File): boolean => {
    const validTypes = ['.pdf', '.fountain']
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()

    if (!validTypes.includes(fileExtension)) {
      setError(`Invalid file type. Please upload a PDF or Fountain file.`)
      return false
    }

    // Max 50MB
    const maxSize = 50 * 1024 * 1024
    if (file.size > maxSize) {
      setError(`File too large. Maximum size is 50MB.`)
      return false
    }

    setError(null)
    return true
  }

  const handleFile = useCallback((file: File) => {
    if (validateFile(file)) {
      onFileSelect(file)
    }
  }, [onFileSelect])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }, [handleFile])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }, [handleFile])

  return (
    <div className="space-y-4">
      {!selectedFile ? (
        <Card
          className={`border-2 border-dashed transition-colors ${
            isDragging
              ? 'border-primary bg-primary/5'
              : error
              ? 'border-destructive bg-destructive/5'
              : 'border-border hover:border-primary/50'
          }`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <div className="p-12 text-center">
            <div className="flex justify-center mb-4">
              <div className="p-4 rounded-full bg-primary/10">
                <Upload className="w-8 h-8 text-primary" />
              </div>
            </div>

            <h3 className="text-lg font-semibold mb-2">
              Drop your screenplay here
            </h3>

            <p className="text-sm text-muted-foreground mb-6">
              or click to browse
            </p>

            <label htmlFor="file-upload">
              <Button asChild variant="outline">
                <span>
                  Browse Files
                </span>
              </Button>
              <input
                id="file-upload"
                type="file"
                accept=".pdf,.fountain"
                onChange={handleFileInput}
                className="hidden"
              />
            </label>

            <p className="text-xs text-muted-foreground mt-4">
              Supports PDF and Fountain files (max 50MB)
            </p>
          </div>
        </Card>
      ) : (
        <Card className="border-primary/50 bg-primary/5">
          <div className="p-6">
            <div className="flex items-start gap-4">
              <div className="p-3 rounded-lg bg-primary/10">
                <File className="w-6 h-6 text-primary" />
              </div>

              <div className="flex-1 min-w-0">
                <h4 className="font-semibold truncate">{selectedFile.name}</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>

              <Button
                variant="ghost"
                size="sm"
                onClick={onClearFile}
                className="shrink-0"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </Card>
      )}

      {error && (
        <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20">
          <p className="text-sm text-destructive">{error}</p>
        </div>
      )}
    </div>
  )
}
