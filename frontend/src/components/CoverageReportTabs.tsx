/**
 * CoverageReportTabs Component
 *
 * Tabbed interface for screenplay coverage report sections.
 * Mimics professional coverage report structure: Opening Thoughts, Characters, Plot, etc.
 *
 * Design: Clean tabs with generous spacing, narrative paragraphs like PDF samples
 */

import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Lightbulb, Users, TrendingUp, BarChart3, MessageCircle, FileText, CheckCircle } from 'lucide-react'

interface ReportSection {
  id: string
  title: string
  icon: React.ReactNode
  content: string
}

interface CoverageReportTabsProps {
  sections: {
    openingThoughts?: string
    characters?: string
    plot?: string
    structure?: string
    dialogue?: string
    concept?: string
    finalThoughts?: string
  }
  reviewerName: string
}

export function CoverageReportTabs({ sections, reviewerName }: CoverageReportTabsProps) {
  const reportSections: ReportSection[] = [
    {
      id: 'opening',
      title: 'Opening Thoughts',
      icon: <Lightbulb className="w-4 h-4" />,
      content: sections.openingThoughts || 'No opening thoughts available.'
    },
    {
      id: 'characters',
      title: 'Characters',
      icon: <Users className="w-4 h-4" />,
      content: sections.characters || 'No character analysis available.'
    },
    {
      id: 'plot',
      title: 'Plot',
      icon: <TrendingUp className="w-4 h-4" />,
      content: sections.plot || 'No plot analysis available.'
    },
    {
      id: 'structure',
      title: 'Structure',
      icon: <BarChart3 className="w-4 h-4" />,
      content: sections.structure || 'No structure analysis available.'
    },
    {
      id: 'dialogue',
      title: 'Dialogue',
      icon: <MessageCircle className="w-4 h-4" />,
      content: sections.dialogue || 'No dialogue analysis available.'
    },
    {
      id: 'concept',
      title: 'Concept',
      icon: <FileText className="w-4 h-4" />,
      content: sections.concept || 'No concept analysis available.'
    },
    {
      id: 'final',
      title: 'Final Thoughts',
      icon: <CheckCircle className="w-4 h-4" />,
      content: sections.finalThoughts || 'No final thoughts available.'
    }
  ]

  return (
    <div className="w-full space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold">Coverage Report</h2>
        <p className="text-muted-foreground">
          Detailed feedback from {reviewerName}
        </p>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="opening" className="w-full">
        <TabsList className="w-full grid grid-cols-7 h-auto p-1">
          {reportSections.map((section) => (
            <TabsTrigger
              key={section.id}
              value={section.id}
              className="flex items-center gap-2 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground py-3 px-4"
            >
              {section.icon}
              <span className="hidden sm:inline">{section.title}</span>
            </TabsTrigger>
          ))}
        </TabsList>

        {reportSections.map((section) => (
          <TabsContent
            key={section.id}
            value={section.id}
            className="mt-8 space-y-6"
          >
            {/* Section Header */}
            <div className="border-b border-border pb-4">
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 rounded-lg bg-primary/10 text-primary">
                  {section.icon}
                </div>
                <h3 className="text-xl font-semibold">{section.title}</h3>
              </div>
            </div>

            {/* Section Content - Formatted as narrative paragraphs */}
            <div className="prose prose-lg dark:prose-invert max-w-none">
              <div className="whitespace-pre-wrap leading-relaxed text-foreground">
                {section.content}
              </div>
            </div>

            {/* Section Footer - Helpful notes */}
            {section.id === 'opening' && (
              <div className="mt-8 p-4 bg-muted/50 rounded-lg border border-border">
                <p className="text-sm text-muted-foreground">
                  💡 <strong>Note:</strong> This section provides a high-level overview of the screenplay's
                  strengths and areas for improvement. Detailed analysis follows in subsequent sections.
                </p>
              </div>
            )}

            {section.id === 'final' && (
              <div className="mt-8 p-4 bg-muted/50 rounded-lg border border-border">
                <p className="text-sm text-muted-foreground">
                  ✅ <strong>Next Steps:</strong> Review the specific recommendations in each section to
                  strengthen your screenplay. Consider the overall rating and percentile scores when planning revisions.
                </p>
              </div>
            )}
          </TabsContent>
        ))}
      </Tabs>
    </div>
  )
}
