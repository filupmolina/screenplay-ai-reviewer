/**
 * SceneBySceneView Component
 *
 * Detailed scene-by-scene feedback display with emotional tracking.
 * This is the "Dive Deeper" mode that shows granular feedback.
 *
 * Design: Card-based layout with clear visual hierarchy
 */

import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface SceneFeedback {
  scene_number?: number
  sceneNumber?: number
  reviewer_name?: string
  reviewerName?: string
  feedback: string
  emotional_state?: {
    engagement: number
    enjoyment: number
    suspense: number
    confusion: number
  }
  emotionalState?: {
    engagement: number
    enjoyment: number
    suspense: number
    confusion: number
  }
}

interface SceneBySceneViewProps {
  feedbackData: SceneFeedback[]
  selectedScene?: number | null
}

const EmotionIndicator = ({ value, label }: { value: number; label: string }) => {
  const getIcon = () => {
    if (value > 0.7) return <TrendingUp className="w-4 h-4" />
    if (value < 0.3) return <TrendingDown className="w-4 h-4" />
    return <Minus className="w-4 h-4" />
  }

  const getColor = () => {
    if (value > 0.7) return 'bg-green-500/10 text-green-600 dark:text-green-400'
    if (value < 0.3) return 'bg-red-500/10 text-red-600 dark:text-red-400'
    return 'bg-muted text-muted-foreground'
  }

  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium ${getColor()}`}>
      {getIcon()}
      <span>{label}</span>
      <span className="text-xs opacity-75">{(value * 100).toFixed(0)}%</span>
    </div>
  )
}

export function SceneBySceneView({ feedbackData, selectedScene }: SceneBySceneViewProps) {
  if (!feedbackData || feedbackData.length === 0) {
    return (
      <div className="card text-center py-12">
        <p className="text-muted-foreground">No scene-by-scene feedback available.</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h3 className="text-2xl font-semibold mb-2">Scene-by-Scene Feedback</h3>
        <p className="text-muted-foreground">
          Detailed analysis of each scene with emotional tracking
        </p>
      </div>

      {/* Scene Cards */}
      <div className="space-y-6">
        {feedbackData.map((feedback, idx) => {
          const sceneNum = feedback.scene_number || feedback.sceneNumber || idx + 1
          const reviewerName = feedback.reviewer_name || feedback.reviewerName || 'AI Reviewer'
          const emotionalState = feedback.emotional_state || feedback.emotionalState

          return (
            <div
              key={idx}
              id={`scene-${sceneNum}`}
              className={`card transition-all ${
                selectedScene === sceneNum
                  ? 'ring-2 ring-primary shadow-lg'
                  : ''
              }`}
            >
              {/* Scene Header */}
              <div className="flex items-start justify-between mb-6 pb-4 border-b border-border">
                <div>
                  <div className="text-sm font-medium text-primary mb-1">
                    Scene {sceneNum}
                  </div>
                  <div className="font-semibold text-lg">{reviewerName}</div>
                </div>

                {/* Primary Emotional Indicators */}
                {emotionalState && (
                  <div className="flex flex-wrap gap-2 justify-end">
                    <EmotionIndicator
                      value={emotionalState.engagement}
                      label="Engagement"
                    />
                    <EmotionIndicator
                      value={emotionalState.enjoyment}
                      label="Enjoyment"
                    />
                  </div>
                )}
              </div>

              {/* Feedback Text */}
              <div className="prose prose-lg dark:prose-invert max-w-none mb-6">
                <p className="leading-relaxed whitespace-pre-wrap">{feedback.feedback}</p>
              </div>

              {/* Additional Metrics */}
              {emotionalState && (
                <div className="flex gap-3 pt-4 border-t border-border">
                  <EmotionIndicator
                    value={emotionalState.suspense}
                    label="Suspense"
                  />
                  <EmotionIndicator
                    value={emotionalState.confusion}
                    label="Confusion"
                  />
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Summary Stats */}
      <div className="card bg-muted/30">
        <h4 className="font-semibold mb-3">Analysis Summary</h4>
        <div className="text-sm text-muted-foreground space-y-1">
          <p>Total Scenes Analyzed: {feedbackData.length}</p>
          <p>Reviewers: {[...new Set(feedbackData.map(f => f.reviewer_name || f.reviewerName))].length}</p>
        </div>
      </div>
    </div>
  )
}
