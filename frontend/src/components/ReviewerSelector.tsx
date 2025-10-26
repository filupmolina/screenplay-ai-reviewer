import { Check } from 'lucide-react'

interface Reviewer {
  id: string
  name: string
  description: string
  type: 'horror_brain' | 'genre' | 'industry'
}

const HORROR_BRAINS: Reviewer[] = [
  {
    id: 'jordan_peele',
    name: 'Jordan Peele',
    description: 'Thoughtful, thematic, social commentary focus',
    type: 'horror_brain',
  },
  {
    id: 'james_gunn',
    name: 'James Gunn',
    description: 'Energetic, balances horror with heart and humor',
    type: 'horror_brain',
  },
  {
    id: 'sam_raimi',
    name: 'Sam Raimi',
    description: 'Kinetic, visceral, focused on energy',
    type: 'horror_brain',
  },
  {
    id: 'drew_goddard',
    name: 'Drew Goddard',
    description: 'Structural, clever plot mechanics',
    type: 'horror_brain',
  },
  {
    id: 'guy_busick',
    name: 'Guy Busick',
    description: 'Suspenseful, sharp, tension and scares',
    type: 'horror_brain',
  },
  {
    id: 'leigh_whannell',
    name: 'Leigh Whannell',
    description: 'Dark, inventive, horror craft and twists',
    type: 'horror_brain',
  },
]

const GENRE_REVIEWERS: Reviewer[] = [
  {
    id: 'horror_fan',
    name: 'Horror Fan',
    description: 'Genre specialist perspective',
    type: 'genre',
  },
  {
    id: 'indie_critic',
    name: 'Indie Critic',
    description: 'Arthouse and character-driven focus',
    type: 'genre',
  },
  {
    id: 'blockbuster_fan',
    name: 'Blockbuster Fan',
    description: 'Mainstream entertainment focus',
    type: 'genre',
  },
]

interface ReviewerSelectorProps {
  selectedReviewers: string[]
  onToggleReviewer: (reviewerId: string) => void
}

export default function ReviewerSelector({
  selectedReviewers,
  onToggleReviewer,
}: ReviewerSelectorProps) {
  const isSelected = (id: string) => selectedReviewers.includes(id)

  return (
    <div className="space-y-8">
      {/* Horror Brains Section */}
      <div>
        <h3 className="text-xl font-semibold mb-4">Horror Brain Personas</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {HORROR_BRAINS.map((reviewer) => (
            <button
              key={reviewer.id}
              onClick={() => onToggleReviewer(reviewer.id)}
              className={`
                p-4 rounded-lg border-2 text-left transition-all
                ${
                  isSelected(reviewer.id)
                    ? 'border-blue-600 bg-blue-950'
                    : 'border-neutral-800 bg-neutral-900 hover:border-blue-800'
                }
              `}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="font-semibold text-neutral-100">
                    {reviewer.name}
                  </div>
                  <div className="text-sm text-neutral-400 mt-1">
                    {reviewer.description}
                  </div>
                </div>
                {isSelected(reviewer.id) && (
                  <Check className="w-5 h-5 text-blue-400 ml-2 flex-shrink-0" />
                )}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Other Reviewers Section */}
      <div>
        <h3 className="text-xl font-semibold mb-4">Other Reviewers</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {GENRE_REVIEWERS.map((reviewer) => (
            <button
              key={reviewer.id}
              onClick={() => onToggleReviewer(reviewer.id)}
              className={`
                p-4 rounded-lg border-2 text-left transition-all
                ${
                  isSelected(reviewer.id)
                    ? 'border-blue-600 bg-blue-950'
                    : 'border-neutral-800 bg-neutral-900 hover:border-blue-800'
                }
              `}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="font-semibold text-neutral-100">
                    {reviewer.name}
                  </div>
                  <div className="text-sm text-neutral-400 mt-1">
                    {reviewer.description}
                  </div>
                </div>
                {isSelected(reviewer.id) && (
                  <Check className="w-5 h-5 text-blue-400 ml-2 flex-shrink-0" />
                )}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Selection Summary */}
      <div className="p-4 bg-neutral-900 border border-neutral-800 rounded-lg">
        <p className="text-sm text-neutral-400">
          <span className="font-medium text-neutral-200">
            {selectedReviewers.length} reviewer{selectedReviewers.length !== 1 ? 's' : ''} selected
          </span>
          {selectedReviewers.length === 0 && ' - Select at least one to continue'}
        </p>
      </div>
    </div>
  )
}
