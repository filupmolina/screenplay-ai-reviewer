/**
 * EngagementGraph Component
 *
 * EKG-style graph showing reader engagement/enjoyment over the screenplay timeline.
 * Clickable beats allow jumping to specific scenes in "Dive Deeper" mode.
 *
 * Design: Heart rate monitor aesthetic with smooth curves and interactive points
 */

import { Activity } from 'lucide-react'

interface EngagementDataPoint {
  sceneNumber: number
  engagement: number  // 0-1
  enjoyment: number   // 0-1
  suspense: number    // 0-1
}

interface EngagementGraphProps {
  data: EngagementDataPoint[]
  reviewerName: string
  onSceneClick?: (sceneNumber: number) => void
}

export function EngagementGraph({ data, reviewerName, onSceneClick }: EngagementGraphProps) {
  if (!data || data.length === 0) {
    return (
      <div className="w-full p-12 text-center text-muted-foreground">
        <Activity className="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No engagement data available</p>
      </div>
    )
  }

  // Calculate dimensions
  const width = 1000
  const height = 200
  const padding = { top: 20, right: 20, bottom: 40, left: 60 }
  const graphWidth = width - padding.left - padding.right
  const graphHeight = height - padding.top - padding.bottom

  // Calculate scale
  const xScale = graphWidth / (data.length - 1)

  // Generate SVG path for enjoyment curve (primary metric)
  const generatePath = (dataPoints: EngagementDataPoint[], metric: 'engagement' | 'enjoyment' | 'suspense') => {
    if (dataPoints.length === 0) return ''

    const points = dataPoints.map((point, index) => {
      const x = padding.left + (index * xScale)
      const y = padding.top + graphHeight - (point[metric] * graphHeight)
      return { x, y }
    })

    // Create smooth curve using quadratic bezier
    let path = `M ${points[0].x},${points[0].y}`

    for (let i = 0; i < points.length - 1; i++) {
      const current = points[i]
      const next = points[i + 1]
      const midX = (current.x + next.x) / 2
      const midY = (current.y + next.y) / 2

      path += ` Q ${current.x},${current.y} ${midX},${midY}`
      path += ` Q ${next.x},${next.y} ${next.x},${next.y}`
    }

    return path
  }

  const enjoymentPath = generatePath(data, 'enjoyment')
  const engagementPath = generatePath(data, 'engagement')

  // Generate area fill
  const generateAreaPath = (dataPoints: EngagementDataPoint[], metric: 'enjoyment') => {
    const linePath = generatePath(dataPoints, metric)
    const lastPoint = dataPoints[dataPoints.length - 1]
    const lastX = padding.left + ((dataPoints.length - 1) * xScale)
    const bottomY = padding.top + graphHeight

    return `${linePath} L ${lastX},${bottomY} L ${padding.left},${bottomY} Z`
  }

  const areaPath = generateAreaPath(data, 'enjoyment')

  return (
    <div className="w-full space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Activity className="w-5 h-5 text-red-500" />
          <h3 className="text-lg font-semibold">Engagement Timeline</h3>
        </div>
        <div className="text-sm text-muted-foreground">
          {reviewerName}
        </div>
      </div>

      {/* Graph Container */}
      <div className="relative bg-card border border-border rounded-lg p-6 overflow-hidden">
        {/* Grid Background */}
        <div className="absolute inset-0 pointer-events-none">
          <svg width={width} height={height} className="w-full h-auto">
            {/* Horizontal grid lines */}
            {[0, 0.25, 0.5, 0.75, 1].map((level) => {
              const y = padding.top + graphHeight - (level * graphHeight)
              return (
                <g key={level}>
                  <line
                    x1={padding.left}
                    y1={y}
                    x2={padding.left + graphWidth}
                    y2={y}
                    stroke="hsl(var(--border))"
                    strokeWidth="1"
                    strokeDasharray="4 4"
                    opacity="0.3"
                  />
                  <text
                    x={padding.left - 12}
                    y={y + 4}
                    textAnchor="end"
                    className="text-xs fill-muted-foreground"
                  >
                    {(level * 10).toFixed(0)}
                  </text>
                </g>
              )
            })}
          </svg>
        </div>

        {/* Main Graph SVG */}
        <svg width={width} height={height} className="w-full h-auto relative z-10">
          {/* Area fill under enjoyment curve */}
          <path
            d={areaPath}
            fill="url(#enjoymentGradient)"
            opacity="0.2"
          />

          {/* Gradients */}
          <defs>
            <linearGradient id="enjoymentGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="rgb(239, 68, 68)" stopOpacity="0.8" />
              <stop offset="100%" stopColor="rgb(239, 68, 68)" stopOpacity="0" />
            </linearGradient>
          </defs>

          {/* Engagement line (secondary, dashed) */}
          <path
            d={engagementPath}
            fill="none"
            stroke="rgb(59, 130, 246)"
            strokeWidth="2"
            strokeDasharray="5 5"
            opacity="0.6"
          />

          {/* Enjoyment line (primary, solid) */}
          <path
            d={enjoymentPath}
            fill="none"
            stroke="rgb(239, 68, 68)"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Interactive points */}
          {data.map((point, index) => {
            const x = padding.left + (index * xScale)
            const y = padding.top + graphHeight - (point.enjoyment * graphHeight)

            return (
              <g key={index}>
                {/* Clickable area */}
                <circle
                  cx={x}
                  cy={y}
                  r="8"
                  fill="transparent"
                  className="cursor-pointer"
                  onClick={() => onSceneClick?.(point.sceneNumber)}
                />

                {/* Visible dot */}
                <circle
                  cx={x}
                  cy={y}
                  r="4"
                  fill="rgb(239, 68, 68)"
                  stroke="white"
                  strokeWidth="2"
                  className="pointer-events-none transition-all"
                />

                {/* Scene number label (on hover) */}
                <text
                  x={x}
                  y={padding.top + graphHeight + 20}
                  textAnchor="middle"
                  className="text-xs fill-muted-foreground"
                >
                  {index % Math.ceil(data.length / 10) === 0 ? point.sceneNumber : ''}
                </text>
              </g>
            )
          })}

          {/* X-axis label */}
          <text
            x={padding.left + graphWidth / 2}
            y={height - 5}
            textAnchor="middle"
            className="text-xs fill-muted-foreground font-medium"
          >
            Scene Number
          </text>

          {/* Y-axis label */}
          <text
            x={20}
            y={padding.top + graphHeight / 2}
            textAnchor="middle"
            transform={`rotate(-90, 20, ${padding.top + graphHeight / 2})`}
            className="text-xs fill-muted-foreground font-medium"
          >
            Enjoyment / Engagement
          </text>
        </svg>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-8 h-0.5 bg-red-500"></div>
          <span className="text-muted-foreground">Enjoyment</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-8 h-0.5 border-t-2 border-dashed border-blue-500"></div>
          <span className="text-muted-foreground">Engagement</span>
        </div>
      </div>

      {/* Instruction */}
      <p className="text-center text-sm text-muted-foreground">
        Click any point on the graph to jump to that scene's detailed feedback
      </p>
    </div>
  )
}
