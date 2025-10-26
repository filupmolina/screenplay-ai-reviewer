import { Loader2 } from 'lucide-react'

interface AnalysisProgressProps {
  currentScene: number
  totalScenes: number
  currentReviewer: string
  status: string
}

export default function AnalysisProgress({
  currentScene,
  totalScenes,
  currentReviewer,
  status,
}: AnalysisProgressProps) {
  const progress = totalScenes > 0 ? (currentScene / totalScenes) * 100 : 0

  return (
    <div className="card max-w-2xl mx-auto">
      <div className="flex items-center gap-4 mb-6">
        <Loader2 className="w-8 h-8 text-blue-400 animate-spin" />
        <div>
          <h3 className="text-xl font-semibold">Analyzing Screenplay</h3>
          <p className="text-sm text-neutral-400">{status}</p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-neutral-400">Progress</span>
          <span className="font-medium text-neutral-200">
            {currentScene} / {totalScenes} scenes
          </span>
        </div>
        <div className="w-full bg-neutral-800 rounded-full h-3 overflow-hidden">
          <div
            className="bg-blue-600 h-full rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Current Reviewer */}
      <div className="p-4 bg-blue-950 border border-blue-900 rounded-lg">
        <div className="text-sm text-blue-400 font-medium mb-1">Current Reviewer</div>
        <div className="font-semibold text-blue-200">{currentReviewer}</div>
      </div>

      {/* Estimated Time */}
      <div className="mt-6 text-center">
        <p className="text-sm text-neutral-500">
          This usually takes 2-5 minutes depending on screenplay length
        </p>
      </div>
    </div>
  )
}
