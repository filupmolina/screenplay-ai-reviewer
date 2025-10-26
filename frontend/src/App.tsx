import { useState } from 'react'
import { ArrowLeft, Upload, Users, BarChart3 } from 'lucide-react'
import { Toaster, toast } from 'sonner'
import { Button } from './components/ui/button'
import ReviewerSelector from './components/ReviewerSelector'
import AnalysisProgress from './components/AnalysisProgress'
import AnalysisResults from './components/AnalysisResults'
import { UploadZone } from './components/UploadZone'
import { ThemeProvider } from './providers/ThemeProvider'
import { ThemeToggle } from './components/ThemeToggle'
import { DevTools } from './components/DevTools'
import { VersionDisplay } from './components/VersionDisplay'
import { logger } from './lib/logger'

type Step = 'upload' | 'select' | 'analyzing' | 'results'

function App() {
  const [step, setStep] = useState<Step>('upload')
  const [file, setFile] = useState<File | null>(null)
  const [selectedReviewers, setSelectedReviewers] = useState<string[]>([])
  const [analysisData, setAnalysisData] = useState<any>(null)

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile)
    toast.success('File selected', {
      description: `${selectedFile.name} ready for analysis`
    })
  }

  const handleClearFile = () => {
    setFile(null)
  }

  const handleToggleReviewer = (reviewerId: string) => {
    setSelectedReviewers((prev) =>
      prev.includes(reviewerId)
        ? prev.filter((id) => id !== reviewerId)
        : [...prev, reviewerId]
    )
  }

  const handleStartAnalysis = async () => {
    if (!file) return

    logger.action('Start analysis clicked', { fileName: file.name, reviewers: selectedReviewers })

    const loadingToast = toast.loading('Starting analysis...', {
      description: 'Uploading screenplay and preparing reviewers'
    })

    setStep('analyzing')

    // Create form data
    const formData = new FormData()
    formData.append('file', file)
    formData.append('reviewer_ids', selectedReviewers.join(','))

    try {
      logger.debug('Sending analysis request', { fileName: file.name, reviewerCount: selectedReviewers.length })

      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      })

      logger.api('POST', '/analyze', response.status)

      if (!response.ok) {
        const errorText = await response.text()
        logger.error('Analysis request failed', new Error(errorText), {
          status: response.status,
          fileName: file.name
        })
        throw new Error('Analysis failed')
      }

      const data = await response.json()
      logger.info('Analysis complete', data)

      toast.dismiss(loadingToast)
      toast.success('Analysis complete!', {
        description: 'Your screenplay has been analyzed successfully',
        duration: 4000
      })

      setAnalysisData(data)
      setStep('results')
    } catch (error) {
      logger.error('Analysis error caught', error as Error, {
        fileName: file.name,
        reviewers: selectedReviewers
      })

      toast.dismiss(loadingToast)
      toast.error('Analysis failed', {
        description: 'Please check your connection and try again. Backend server may not be running.',
        duration: 6000
      })

      setStep('select')
    }
  }

  const handleReset = () => {
    setStep('upload')
    setFile(null)
    setSelectedReviewers([])
  }

  return (
    <ThemeProvider>
      <Toaster richColors position="top-center" />
      <div className="min-h-screen bg-background text-foreground">
        {/* Header */}
        <header className="bg-card border-b border-border">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold tracking-tight">
                  Screenplay AI Reviewer
                </h1>
                <p className="text-muted-foreground mt-2">
                  Get expert feedback from Horror Brain personas
                </p>
              </div>

              <div className="flex items-center gap-4">
                <ThemeToggle />

                {step !== 'upload' && (
                  <button
                    onClick={handleReset}
                    className="btn bg-muted border-2 border-border hover:bg-muted/80 flex items-center gap-2"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    Start Over
                  </button>
                )}
              </div>
            </div>
          </div>
        </header>

      {/* Progress Steps */}
      <div className="bg-neutral-900 border-b border-neutral-800">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-8">
            {/* Upload Step */}
            <div className="flex items-center gap-2">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step === 'upload'
                    ? 'bg-blue-600 text-white'
                    : 'bg-neutral-800 text-neutral-500'
                }`}
              >
                <Upload className="w-4 h-4" />
              </div>
              <span className="text-sm font-medium text-neutral-300">Upload</span>
            </div>

            <div className="h-px flex-1 bg-neutral-800" />

            {/* Select Step */}
            <div className="flex items-center gap-2">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step === 'select'
                    ? 'bg-blue-600 text-white'
                    : step === 'analyzing' || step === 'results'
                    ? 'bg-green-600 text-white'
                    : 'bg-neutral-800 text-neutral-500'
                }`}
              >
                <Users className="w-4 h-4" />
              </div>
              <span className="text-sm font-medium text-neutral-300">Select Reviewers</span>
            </div>

            <div className="h-px flex-1 bg-neutral-800" />

            {/* Results Step */}
            <div className="flex items-center gap-2">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step === 'results'
                    ? 'bg-blue-600 text-white'
                    : 'bg-neutral-800 text-neutral-500'
                }`}
              >
                <BarChart3 className="w-4 h-4" />
              </div>
              <span className="text-sm font-medium text-neutral-300">View Results</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Upload Step */}
        {step === 'upload' && (
          <div className="space-y-8">
            <div className="max-w-2xl mx-auto space-y-6">
              <div>
                <h2 className="text-2xl font-semibold mb-2">Upload Screenplay</h2>
                <p className="text-muted-foreground">
                  Upload your screenplay to get AI-powered feedback
                </p>
              </div>

              <UploadZone
                onFileSelect={handleFileSelect}
                selectedFile={file}
                onClearFile={handleClearFile}
              />

              {file && (
                <Button
                  onClick={() => setStep('select')}
                  className="w-full"
                  size="lg"
                >
                  Continue to Reviewer Selection
                </Button>
              )}
            </div>

            {/* Features Preview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="card">
                <h3 className="font-semibold mb-2">Horror Brain Personas</h3>
                <p className="text-sm text-neutral-400">
                  Get feedback from Jordan Peele, James Gunn, Sam Raimi, and more
                </p>
              </div>

              <div className="card">
                <h3 className="font-semibold mb-2">Scene-by-Scene</h3>
                <p className="text-sm text-neutral-400">
                  Detailed analysis of every scene with emotional tracking
                </p>
              </div>

              <div className="card">
                <h3 className="font-semibold mb-2">Character Analysis</h3>
                <p className="text-sm text-neutral-400">
                  Track character arcs, relationships, and narrative questions
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Select Reviewers Step */}
        {step === 'select' && (
          <div className="space-y-8">
            <div className="card">
              <h2 className="text-2xl font-semibold mb-2">Select Reviewers</h2>
              <p className="text-neutral-400 mb-8">
                Choose which AI personas will review your screenplay
              </p>

              <ReviewerSelector
                selectedReviewers={selectedReviewers}
                onToggleReviewer={handleToggleReviewer}
              />

              <div className="mt-8">
                <button
                  disabled={selectedReviewers.length === 0}
                  onClick={handleStartAnalysis}
                  className="btn btn-primary w-full"
                >
                  Start Analysis
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Analyzing Step */}
        {step === 'analyzing' && (
          <div className="max-w-2xl mx-auto">
            <div className="card">
              <div className="flex items-center gap-4 mb-6">
                <div className="relative">
                  <div className="w-12 h-12 rounded-full border-4 border-primary/20"></div>
                  <div className="absolute top-0 left-0 w-12 h-12 rounded-full border-4 border-primary border-t-transparent animate-spin"></div>
                </div>
                <div>
                  <h3 className="text-xl font-semibold">Analyzing Screenplay</h3>
                  <p className="text-sm text-muted-foreground">Processing with AI reviewers...</p>
                </div>
              </div>

              <div className="space-y-3">
                <div className="p-4 bg-muted/50 rounded-lg">
                  <p className="text-sm text-muted-foreground">
                    {selectedReviewers.length} reviewer{selectedReviewers.length > 1 ? 's' : ''} analyzing your screenplay
                  </p>
                </div>

                <div className="text-center py-6">
                  <p className="text-sm text-muted-foreground">
                    This usually takes 2-5 minutes depending on screenplay length
                  </p>
                  <p className="text-xs text-muted-foreground mt-2">
                    Please keep this tab open while analysis is running
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results Step */}
        {step === 'results' && file && analysisData && (
          <AnalysisResults
            screenplay={file.name}
            reviewers={selectedReviewers}
            data={analysisData}
          />
        )}
      </main>

      {/* Dev Tools */}
      <DevTools />

      {/* Version Display */}
      <VersionDisplay />
    </div>
    </ThemeProvider>
  )
}

export default App
