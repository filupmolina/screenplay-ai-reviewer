/**
 * AnalysisResults Component (Redesigned)
 *
 * Coverage report-style results display with:
 * 1. Dashboard with scores (title page)
 * 2. EKG engagement graph
 * 3. Tabbed narrative sections (Opening Thoughts, Characters, Plot, etc.)
 * 4. "Dive Deeper" button to access scene-by-scene mode
 *
 * Design: Webflow × iPad aesthetic - clean, spacious, premium
 */

import { useState } from 'react'
import { ChevronDown, Download, FileText, Copy } from 'lucide-react'
import { Button } from './ui/button'
import { CoverageReportDashboard } from './CoverageReportDashboard'
import { EngagementGraph } from './EngagementGraph'
import { CoverageReportTabs } from './CoverageReportTabs'
import { SceneBySceneView } from './SceneBySceneView'

interface AnalysisResultsProps {
  screenplay: string
  reviewers: string[]
  data: any
}

export default function AnalysisResults({ screenplay, reviewers, data }: AnalysisResultsProps) {
  const [viewMode, setViewMode] = useState<'coverage' | 'scene-by-scene'>('coverage')
  const [selectedScene, setSelectedScene] = useState<number | null>(null)

  // Extract data from API response
  const feedbackData = data.feedback || []
  const overallStats = data.overall_stats || {}
  const screenplayTitle = data.screenplay_title || screenplay.replace('.pdf', '').replace('.fountain', '')
  const totalScenes = data.total_scenes || feedbackData.length

  // Calculate scores for coverage report (convert emotional metrics to percentiles)
  const calculatePercentile = (value: number) => Math.round(value * 100)

  const scores = {
    plot: calculatePercentile(overallStats.avg_engagement || 0.75),
    concept: calculatePercentile(overallStats.avg_enjoyment || 0.70),
    characters: calculatePercentile(overallStats.avg_engagement || 0.72),
    dialogue: calculatePercentile(overallStats.avg_enjoyment || 0.68),
    structure: calculatePercentile((1 - (overallStats.avg_confusion || 0.2)) || 0.80)
  }

  // Determine overall rating based on average scores
  const avgScore = Object.values(scores).reduce((a, b) => a + b, 0) / Object.values(scores).length
  const overallRating: 'RECOMMEND' | 'CONSIDER' | 'PASS' =
    avgScore >= 85 ? 'RECOMMEND' : avgScore >= 70 ? 'CONSIDER' : 'PASS'

  // Prepare engagement graph data
  const engagementData = feedbackData.map((feedback: any) => ({
    sceneNumber: feedback.scene_number || feedback.sceneNumber || 0,
    engagement: feedback.emotional_state?.engagement || feedback.emotionalState?.engagement || 0.5,
    enjoyment: feedback.emotional_state?.enjoyment || feedback.emotionalState?.enjoyment || 0.5,
    suspense: feedback.emotional_state?.suspense || feedback.emotionalState?.suspense || 0.5
  }))

  // Prepare coverage report sections (mock data - will be populated by backend later)
  const reportSections = {
    openingThoughts: `This is a strong draft with dynamic, complex characters, a unique and compelling plot, and high stakes. The dialogue is witty and clever without being distracting, and key story elements are slowly revealed in a way that keeps the audience engaged.

The screenplay demonstrates excellent pacing in the first two acts, with each scene building naturally on the previous one. However, there's room for a much longer third act to fully develop the climax and resolution.`,

    characters: `${reviewers[0] || 'The reviewer'} provides detailed character analysis:

The protagonist is a well-rounded, relatable character who is set up quickly, and we're instantly able to get behind them because they're funny but smart. The character work demonstrates clear motivations and believable reactions throughout.

Supporting characters add depth to the story, though some could benefit from additional development. Consider giving each major character at least one moment that reveals their inner conflict or desire.`,

    plot: `The plot is fully immersive from the very first scene. Details are slowly teased out in a way that keeps the audience engaged. The exposition is well-done, with information revealed naturally through character interactions rather than heavy-handed dialogue.

Key plot points:
- Strong opening that establishes tone and stakes
- Well-structured rising action with clear obstacles
- Climax delivers on the setup established earlier
- Resolution ties up major threads while leaving room for future development`,

    structure: `The overall structure follows a solid three-act format with clear turning points. The pacing is generally strong, though some scenes in the second act could be tightened.

Consider:
- Starting scenes as late as possible and ending them as soon as dramatic tension resolves
- Breaking up longer dialogue scenes with visual moments or action
- Ensuring each scene has a clear purpose that moves the plot or develops character`,

    dialogue: `The dialogue is excellent. Each character's voice feels distinct and consistent. All dialogue is engaging without being overly theatrical or expository.

Particularly strong moments include character interactions that reveal subtext and relationships through what's left unsaid. The dialogue feels natural while still being purposeful and driving the story forward.`,

    concept: `This is a great concept that taps into relevant themes without feeling preachy or heavy-handed. The core idea is strong and provides ample opportunity for both character development and plot complications.

The concept will resonate with audiences because it explores universal themes through a specific, well-defined lens. There's clear commercial potential while maintaining artistic integrity.`,

    finalThoughts: `This is a dynamic, engaging script with strong, dimensional characters, compelling storytelling, and great dialogue. The screenplay demonstrates professional craft and a clear vision.

For future drafts, focus on tightening the structure and expanding the third act. The foundation is solid - with some refinement, this could be a standout piece.

Best of luck with the next draft!`
  }

  // Handle scene click from engagement graph
  const handleSceneClick = (sceneNumber: number) => {
    setSelectedScene(sceneNumber)
    setViewMode('scene-by-scene')
    // Scroll to scene
    setTimeout(() => {
      const sceneElement = document.getElementById(`scene-${sceneNumber}`)
      sceneElement?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 100)
  }

  return (
    <div className="space-y-12">
      {/* View Mode Toggle */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold mb-2">Analysis Complete</h2>
          <p className="text-muted-foreground">
            {totalScenes} scenes analyzed by {reviewers.length} reviewer{reviewers.length > 1 ? 's' : ''}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant={viewMode === 'coverage' ? 'default' : 'outline'}
            onClick={() => setViewMode('coverage')}
          >
            Coverage Report
          </Button>
          <Button
            variant={viewMode === 'scene-by-scene' ? 'default' : 'outline'}
            onClick={() => setViewMode('scene-by-scene')}
          >
            Dive Deeper
          </Button>
        </div>
      </div>

      {/* Coverage Report View */}
      {viewMode === 'coverage' && (
        <div className="space-y-16">
          {/* Coverage Dashboard (Title Page) */}
          <CoverageReportDashboard
            screenplayTitle={screenplayTitle}
            genre="Drama"
            pageCount={data.total_pages}
            reviewerName={reviewers[0] || 'AI Reviewer'}
            overallRating={overallRating}
            overallPercentile={avgScore}
            scores={scores}
          />

          {/* Engagement Graph (EKG style) */}
          <div className="border-t border-border pt-16">
            <EngagementGraph
              data={engagementData}
              reviewerName={reviewers[0] || 'AI Reviewer'}
              onSceneClick={handleSceneClick}
            />
          </div>

          {/* Coverage Report Tabs */}
          <div className="border-t border-border pt-16">
            <CoverageReportTabs
              sections={reportSections}
              reviewerName={reviewers[0] || 'AI Reviewer'}
            />
          </div>

          {/* Dive Deeper CTA */}
          <div className="border-t border-border pt-12">
            <div className="card bg-primary/5 border-2 border-primary/20">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-semibold mb-2">
                    Want More Detail?
                  </h3>
                  <p className="text-muted-foreground">
                    View scene-by-scene feedback with emotional tracking and specific notes
                  </p>
                </div>
                <Button
                  size="lg"
                  onClick={() => setViewMode('scene-by-scene')}
                >
                  Dive Deeper
                  <ChevronDown className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </div>
          </div>

          {/* Export Options */}
          <div className="border-t border-border pt-12">
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Export Analysis</h3>
              <div className="flex flex-wrap gap-3">
                <Button>
                  <Download className="w-4 h-4 mr-2" />
                  Download PDF
                </Button>
                <Button variant="outline">
                  <FileText className="w-4 h-4 mr-2" />
                  Export Markdown
                </Button>
                <Button variant="outline">
                  <Copy className="w-4 h-4 mr-2" />
                  Copy to Clipboard
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Scene-by-Scene View */}
      {viewMode === 'scene-by-scene' && (
        <SceneBySceneView
          feedbackData={feedbackData}
          selectedScene={selectedScene}
        />
      )}
    </div>
  )
}
