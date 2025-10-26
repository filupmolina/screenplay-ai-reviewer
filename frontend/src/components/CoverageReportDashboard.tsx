/**
 * CoverageReportDashboard Component
 *
 * Displays a professional coverage report-style dashboard inspired by WeScreenplay format.
 * Shows screenplay title, scores by category, and overall rating in a clean layout.
 *
 * Design: Webflow × iPad aesthetic - spacious, premium, polished
 */

import { Award, TrendingUp, Users, MessageCircle, BarChart3, Lightbulb } from 'lucide-react'

interface CoverageScore {
  category: string
  percentile: number  // 0-100
  icon: React.ReactNode
}

interface CoverageReportDashboardProps {
  screenplayTitle: string
  genre?: string
  pageCount?: number
  reviewerName: string
  overallRating: 'RECOMMEND' | 'CONSIDER' | 'PASS'
  overallPercentile: number  // 0-100
  scores: {
    plot?: number
    concept?: number
    characters?: number
    dialogue?: number
    structure?: number
  }
}

export function CoverageReportDashboard({
  screenplayTitle,
  genre = 'Drama',
  pageCount,
  reviewerName,
  overallRating,
  overallPercentile,
  scores
}: CoverageReportDashboardProps) {

  // Map scores to coverage format
  const coverageScores: CoverageScore[] = [
    {
      category: 'PLOT',
      percentile: scores.plot || 0,
      icon: <TrendingUp className="w-6 h-6" />
    },
    {
      category: 'CONCEPT',
      percentile: scores.concept || 0,
      icon: <Lightbulb className="w-6 h-6" />
    },
    {
      category: 'CHARACTERS',
      percentile: scores.characters || 0,
      icon: <Users className="w-6 h-6" />
    },
    {
      category: 'DIALOGUE',
      percentile: scores.dialogue || 0,
      icon: <MessageCircle className="w-6 h-6" />
    },
    {
      category: 'STRUCTURE',
      percentile: scores.structure || 0,
      icon: <BarChart3 className="w-6 h-6" />
    }
  ]

  // Get rating color
  const getRatingColor = () => {
    if (overallRating === 'RECOMMEND') return 'text-green-600 bg-green-50 border-green-200'
    if (overallRating === 'CONSIDER') return 'text-blue-600 bg-blue-50 border-blue-200'
    return 'text-gray-600 bg-gray-50 border-gray-200'
  }

  // Get percentile display with "TOP X%" format
  const getPercentileDisplay = (percentile: number) => {
    const topPercentile = Math.max(1, Math.round((100 - percentile) / 5) * 5)
    return `TOP ${topPercentile}%`
  }

  return (
    <div className="w-full max-w-5xl mx-auto space-y-12 py-12">
      {/* Title Card - Clean, centered, spacious */}
      <div className="text-center space-y-6">
        <div>
          <h1 className="text-5xl font-bold tracking-tight mb-4">
            {screenplayTitle}
          </h1>
          <div className="flex items-center justify-center gap-4 text-lg text-muted-foreground">
            <span>{genre}</span>
            <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/40" />
            <span>Television (One-hour)</span>
            {pageCount && (
              <>
                <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/40" />
                <span>{pageCount} Pages</span>
              </>
            )}
          </div>
        </div>

        <div className="text-sm text-muted-foreground">
          Analyzed by <span className="font-medium text-foreground">{reviewerName}</span>
        </div>
      </div>

      {/* Scores Grid - Spacious, card-based layout */}
      <div className="grid grid-cols-3 gap-8">
        {coverageScores.map((score) => (
          <div
            key={score.category}
            className="text-center space-y-3"
          >
            <div className="flex justify-center text-muted-foreground">
              {score.icon}
            </div>
            <div>
              <div className="text-3xl font-bold mb-1">
                {getPercentileDisplay(score.percentile)}
              </div>
              <div className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
                {score.category}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Overall Rating - Large, prominent */}
      <div className="text-center space-y-4 py-8 border-t border-b border-border">
        <div className="flex items-center justify-center gap-3">
          <Award className="w-8 h-8 text-muted-foreground" />
          <span className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
            Rating
          </span>
        </div>

        <div className={`inline-block px-8 py-3 rounded-lg text-4xl font-bold border-2 ${getRatingColor()}`}>
          {overallRating}
        </div>

        <div className="text-sm text-muted-foreground">
          Placed in the top {100 - overallPercentile}%
        </div>
      </div>

      {/* Analysis Note */}
      <div className="text-center text-sm text-muted-foreground max-w-2xl mx-auto leading-relaxed">
        <p>
          Percentiles are based on historical data of scores given out by this analyst.
          Approximately 3% of projects receive a recommend and ~20% of projects receive a consider.
        </p>
      </div>
    </div>
  )
}
