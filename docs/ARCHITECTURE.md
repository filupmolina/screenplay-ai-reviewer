# Technical Architecture

**Last Updated**: Oct 23, 2025

---

## System Overview

The screenplay feedback app processes long-form screenplays (120+ pages) using multiple AI reviewers without exceeding context windows. It uses a human-like memory system with detailed recent memory and compressed historical memory, plus persistent entity tracking.

---

## Core Components

### 1. Memory Management System

**Problem**: 120-page screenplays destroy AI context windows

**Solution**: Human-like memory architecture

#### Recent Memory (Detailed)
- **Size**: Last 3-5 scenes
- **Content**: Full scene text, all dialogue, character actions
- **Purpose**: Immediate context for current scene
- **Storage**: In-memory queue/deque structure

#### Historical Memory (Compressed)
- **Size**: All scenes before recent window
- **Content**: Digested summaries (~20% original size for plot, BUT 100% emotional data preserved)
- **Format**:
  ```json
  {
    "scene_id": 12,
    "summary": "John confronts his father about the inheritance. Tension rises. Father reveals he changed the will.",
    "characters_present": ["JOHN", "FATHER"],
    "key_objects": ["will", "letter"],
    "plot_beats": ["revelation", "conflict"],
    "importance_score": 0.85,

    "emotional_states_by_reviewer": {
      "THE_MAINSTREAM": {
        "primary_emotion": "tense",
        "intensity": 0.9,
        "cumulative_feelings": "Finally! The confrontation we've been waiting for. Stakes are real now.",
        "character_investment": {
          "JOHN": {"feeling": "rooting_for", "intensity": 0.8}
        },
        "revised": false
      },
      "THE_ARTISTE": {
        "primary_emotion": "disappointed",
        "intensity": 0.6,
        "cumulative_feelings": "Too on-the-nose. Would prefer more subtext in this confrontation.",
        "revised": false
      }
    },

    "questions_raised": ["Q_012", "Q_015"],
    "questions_answered": ["Q_003"]
  }
  ```
- **Purpose**: Background context, pattern recognition, FULL emotional continuity
- **Storage**: Vector database or structured JSON
- **Key**: Plot gets compressed, emotions NEVER do

#### Memory Sliding Window
```
Scene 1-10: [Digest] [Digest] [Digest] [Digest] [Digest] [Digest] [Digest] [Digest] [Digest] [Digest]
Scene 11-13: [FULL] [FULL] [FULL] <- Recent detailed memory
Scene 14: <- Current scene being processed
```

As processing moves forward:
1. Current scene added to recent memory
2. Oldest scene in recent memory gets compressed
3. Compressed digest moves to historical memory

---

### 2. Entity Tracking System

**Problem**: The "forgotten maid" - plot-critical elements lost when compressed

**Solution**: Persistent entity tracker across entire screenplay

#### Entity Types
- **Characters**: All named characters, speaking and non-speaking
- **Objects**: Props, MacGuffins, plot devices
- **Locations**: Settings that recur or matter
- **Relationships**: Character connections, conflicts

#### Entity Record Structure
```json
{
  "entity_id": "MAID_001",
  "type": "character",
  "name": "The Maid",
  "aliases": ["Maria", "the help", "she"],
  "first_appearance": 3,
  "last_appearance": 87,
  "total_appearances": 12,
  "importance_score": 0.92,  // Auto-calculated
  "speaking_lines": 8,
  "key_moments": [
    {
      "scene": 3,
      "moment": "Overhears argument about will",
      "significance": "high"
    },
    {
      "scene": 87,
      "moment": "Revealed as murderer",
      "significance": "critical"
    }
  ],
  "relationships": [
    {"entity": "VICTIM", "type": "employer", "tension": "hidden_resentment"}
  ],
  "mentioned_when_absent": [45, 62, 71],  // Scenes where discussed but not present
  "narrative_function": "antagonist_hidden"
}
```

#### Importance Scoring Algorithm
```python
importance_score = (
    (speaking_lines * 0.2) +
    (total_appearances * 0.15) +
    (scene_span * 0.15) +  # last_appearance - first_appearance
    (mentioned_when_absent * 0.2) +
    (relationship_count * 0.1) +
    (key_moments_count * 0.2)
) / theoretical_maximum
```

#### Entity Persistence Rules
1. **High Importance (>0.7)**: Always included in context, even if not in recent scenes
2. **Medium Importance (0.4-0.7)**: Included when mentioned or relevant
3. **Low Importance (<0.4)**: Only in scene digests
4. **Foreshadowing Detection**: Entities mentioned cryptically early get boosted importance

---

### 3. Emotional Memory System

**Problem**: AI reviewers need to build emotional momentum like real viewers - feelings compound over time

**Solution**: 100% persistent emotional tracking per reviewer with retroactive revision capability

#### Core Principle
Each reviewer maintains their own emotional journey through the screenplay. Feelings are NEVER compressed - they're as important as the plot itself. A reviewer who was bored in scene 10 and excited in scene 50 carries both emotions forward, creating genuine emotional continuity.

#### Emotional State Record Structure
```json
{
  "reviewer_id": "THE_MAINSTREAM",
  "scene_id": 14,
  "emotional_state": {
    "primary_emotion": "intrigued",
    "intensity": 0.75,
    "secondary_emotions": ["curious", "slightly_confused"],
    "mood_trajectory": "rising",  // rising, falling, stable
    "engagement_level": 0.8,
    "emotional_investment": {
      "characters": {
        "JOHN": {"feeling": "rooting_for", "intensity": 0.7},
        "MAID": {"feeling": "suspicious", "intensity": 0.3}
      }
    },
    "cumulative_feelings": "Building tension effectively. The mystery is engaging.",
    "momentum": "Each scene raises the stakes - I'm hooked."
  },
  "timestamp": "2025-10-23T10:30:00Z",
  "revised": false
}
```

#### Retroactive Emotional Revision
When plot twists recontextualize earlier scenes, reviewers can revise their emotional take:

```json
{
  "scene_id": 3,
  "original_emotional_state": {
    "primary_emotion": "bored",
    "cumulative_feelings": "The maid scenes are dragging. Why so much focus on her?"
  },
  "revised_emotional_state": {
    "primary_emotion": "impressed",
    "cumulative_feelings": "RETROACTIVE: I was bored by these maid scenes, but scene 87 revealed she's the killer - this was brilliant foreshadowing! Completely changes how I feel about this scene.",
    "revision_triggered_by_scene": 87,
    "revision_reason": "Major plot reveal recontextualizes earlier setup"
  },
  "revision_timestamp": "2025-10-23T12:45:00Z"
}
```

#### Emotional Continuity in Prompts
When processing each new scene, the reviewer's prompt includes:

1. **Recent Emotional Arc** (last 5 scenes):
   - Full emotional states
   - Trajectory analysis
   - Character investment levels

2. **Overall Emotional Journey** (compressed summary):
   - Starting emotion (scene 1)
   - Major emotional shifts and when they occurred
   - Current cumulative feeling
   - Momentum direction

3. **Emotional Investment**:
   - Which characters/storylines the reviewer cares about
   - What they're hoping will happen
   - What they're dreading/fearing

#### Reviewer-Specific Emotional Profiles

Different reviewers have different emotional responses to the same scenes:

**THE MAINSTREAM** watching scene with ambiguous dialogue:
```json
{
  "primary_emotion": "confused",
  "cumulative_feelings": "I don't understand what they're talking about. Make it clearer."
}
```

**THE ARTISTE** watching same scene:
```json
{
  "primary_emotion": "delighted",
  "cumulative_feelings": "Love the ambiguity here. Subtext doing heavy lifting. Trust the audience."
}
```

#### Emotional Persistence Rules
1. **ALL emotional data preserved** - Never compressed or lost
2. **Revisions tracked** - Original feelings + revised feelings both stored
3. **Emotional weight** - Stronger emotions (intensity >0.8) weighted higher in summaries
4. **Momentum tracking** - System detects if reviewer is getting more/less engaged over time

---

### 4. Open Questions Tracker

**Problem**: Real viewers hold mysteries/questions in mind until resolved - AI should too

**Solution**: Importance-scored question tracking system with automatic resolution detection

#### Question Record Structure
```json
{
  "question_id": "Q_047",
  "question": "Why did the maid overhear that conversation - was she eavesdropping or coincidence?",
  "raised_in_scene": 3,
  "raised_by_reviewer": "THE_MAINSTREAM",
  "importance_score": 0.85,
  "status": "open",  // open, answered, irrelevant
  "references": [3, 12, 45],  // Scenes where this question was mentioned/relevant
  "related_entities": ["MAID_001", "CONVERSATION_003"],
  "narrative_weight": "high",  // How central this seems to the plot
  "urgency": 0.6,  // How pressing this feels (increases over time if unanswered)
  "reviewer_speculation": "Could be foreshadowing something sinister",
  "answered_in_scene": null,
  "answer": null
}
```

#### Question Importance Scoring Algorithm
```python
def calculate_question_importance(question, current_scene):
    """
    Calculate how important this question is to keep in memory
    """
    # Base factors
    reference_count = len(question.references) * 0.25
    duration_weight = (current_scene - question.raised_in_scene) / current_scene * 0.15

    # Narrative weight (manually tagged or detected)
    narrative_weight_score = {
        "critical": 0.3,
        "high": 0.2,
        "medium": 0.1,
        "low": 0.05
    }[question.narrative_weight]

    # Entity importance (if related to important entities)
    max_entity_importance = max([
        entity_tracker.get_importance(entity_id)
        for entity_id in question.related_entities
    ]) * 0.15

    # Urgency (increases if repeatedly referenced but not answered)
    urgency_score = question.urgency * 0.15

    # Recency boost (recently mentioned)
    last_reference = question.references[-1] if question.references else question.raised_in_scene
    recency_boost = 0.1 if (current_scene - last_reference) < 5 else 0

    total = (reference_count + duration_weight + narrative_weight_score +
             max_entity_importance + urgency_score + recency_boost)

    return min(total, 1.0)
```

#### Question Lifecycle

**1. Question Raised** (Scene 3):
```
"Why is the maid always around for private conversations?"
importance_score: 0.3 (seems minor)
```

**2. Question Referenced** (Scene 12, 45):
```
Maid appears again in suspicious circumstances
importance_score: 0.6 → 0.85 (importance rising)
urgency: 0.3 → 0.6
```

**3. Question Answered** (Scene 87):
```
"She's the killer! She was gathering information."
status: open → answered
answer: "The maid was deliberately eavesdropping as part of her murder plot"
```

**4. Question Becomes Irrelevant** (Scene 30):
```
Early question: "Will they find the missing letter?"
Scene 30: Letter revealed to be a red herring, doesn't matter
status: open → irrelevant
reason: "Plot moved past this - letter wasn't important after all"
```

#### Question Persistence Rules
1. **High Importance (>0.7)**: Always included in reviewer's context
2. **Medium Importance (0.4-0.7)**: Included when related entities appear
3. **Low Importance (<0.4)**: Tracked but not in active context
4. **Auto-Pruning**: Questions marked "answered" or "irrelevant" move to archive
5. **Urgency Escalation**: Unanswered questions gain urgency over time

#### Question Types
- **Mystery Questions**: "Who killed him?" (high importance, builds over time)
- **Character Motivation**: "Why did she do that?" (medium, may be answered or left ambiguous)
- **Plot Mechanics**: "How did he escape?" (varies, some get answered, some don't matter)
- **Thematic Questions**: "What is this saying about family?" (low urgency, cumulative)

#### Integration with Emotional Memory
Questions affect emotional state:
- Unanswered mysteries (high importance) → increase engagement
- Too many unanswered questions → potential confusion/frustration
- Satisfying answers → emotional payoff, increased investment
- Unresolved questions at end → reviewer notes this as strength or weakness

---

### 5. Screenplay Parser

**Input Formats**:
- PDF (converted to text)
- Fountain format (.fountain)
- Final Draft XML
- Plain text (screenwriting format)

**Parser Responsibilities**:
1. **Scene Segmentation**: Split on scene headings (INT./EXT.)
2. **Element Classification**:
   - Scene Headings
   - Action/Description
   - Character Names
   - Dialogue
   - Parentheticals
   - Transitions
3. **Character Extraction**: Identify all character names (usually ALL CAPS)
4. **Metadata Extraction**:
   - Scene numbers
   - Location
   - Time of day (DAY/NIGHT)
   - Page numbers

**Output Structure**:
```json
{
  "screenplay": {
    "title": "The Forgotten Maid",
    "total_scenes": 95,
    "total_pages": 122,
    "characters": ["JOHN", "FATHER", "MAID", ...],
    "scenes": [
      {
        "scene_number": 1,
        "heading": "INT. MANSION - LIBRARY - NIGHT",
        "location": "MANSION - LIBRARY",
        "time": "NIGHT",
        "page_start": 1,
        "page_end": 3,
        "full_text": "...",
        "elements": [
          {"type": "action", "text": "JOHN enters..."},
          {"type": "character", "text": "JOHN"},
          {"type": "dialogue", "text": "Father, we need to talk."}
        ],
        "characters_present": ["JOHN", "FATHER"],
        "word_count": 287
      }
    ]
  }
}
```

---

### 6. Multi-Reviewer System

**Reviewer Profiles**:

1. **Blockbuster Fan ("THE MAINSTREAM")**
   - Values: Pacing, clarity, marketability, likability
   - Biases: Dislikes slow burns, ambiguity
   - Reference Frame: MCU, Spielberg, crowd-pleasers

2. **Avant Garde Critic ("THE ARTISTE")**
   - Values: Originality, subversion, visual storytelling, ambiguity
   - Biases: Dislikes formula, exposition
   - Reference Frame: A24, Cannes winners, auteur cinema

3. **Screenwriting Purist ("THE TECHNICIAN")**
   - Values: Structure, formatting, character arcs, economy of language
   - Biases: Strict adherence to "rules"
   - Reference Frame: Syd Field, Save the Cat, McKee

4. **General Audience ("THE CASUAL")**
   - Values: Entertainment, emotional engagement, clarity
   - Biases: None strong, balanced
   - Reference Frame: "Would I watch this on a Friday night?"

5. **Genre Specialist (configurable)**
   - Horror: Scares, atmosphere, subtext
   - Comedy: Timing, escalation, surprise
   - Drama: Character depth, themes, realism
   - Thriller: Suspense, twists, pacing

**Profile Implementation**:
Each profile is a system prompt + evaluation criteria

```python
class ReviewerProfile:
    name: str
    personality: str  # For system prompt
    evaluation_criteria: List[str]
    bias_weights: Dict[str, float]
    reference_frame: List[str]

    def generate_prompt(self, scene, recent_memory, entities):
        """Create prompt for this scene from this reviewer's POV"""
        pass
```

---

### 7. Multi-API Integration

**Supported APIs**:
- Anthropic Claude (Sonnet, Opus)
- OpenAI GPT-4 (Turbo, O1)
- Google Gemini
- (Future: Cohere, local models)

**API Selection Strategy**:
1. **Cost-Based**: Cheaper APIs for early scenes, premium for critical scenes
2. **Profile-Matched**: Certain reviewers paired with certain APIs
   - Blockbuster Fan → GPT-4 (trained on mainstream content)
   - Avant Garde → Claude Opus (better at nuance)
3. **Fallback**: If API fails, rotate to next available
4. **Rate Limiting**: Respect API limits, queue requests

**Cost Management**:
```python
class APIManager:
    def estimate_cost(screenplay):
        """Calculate cost before processing"""
        scenes = len(screenplay.scenes)
        reviewers = len(active_reviewers)
        avg_tokens_per_scene = 1500
        return scenes * reviewers * cost_per_token

    def track_spending(self):
        """Monitor actual costs"""
        pass
```

---

### 8. Feedback Generation Engine

**Processing Flow**:
```
For each scene:
  For each reviewer:
    1. Load recent memory (last 3-5 scenes, full text)
    2. Load historical memory (digests with FULL emotional data)
    3. Load relevant entities (high importance + mentioned in scene)
    4. Load reviewer's emotional journey (all previous emotional states)
    5. Load open questions (importance-scored, active questions)
    6. Generate reviewer-specific prompt with:
       - Plot context (recent + historical)
       - Emotional context (how they've been feeling)
       - Active questions (what they're wondering about)
       - Entity context (who/what matters)
    7. Call appropriate API
    8. Parse feedback (extract: reaction, notes, emotional_state, new_questions)
    9. Update emotional memory (store new emotional state)
    10. Update question tracker (mark answered, raise new, update importance)
    11. Update entity tracker (new appearances, importance changes)
    12. Update memory (compress oldest recent scene if needed, PRESERVE emotions)
    13. Store feedback
    14. Check for emotional revisions (did this scene change feelings about past scenes?)
```

**Feedback Structure**:
```json
{
  "scene_id": 14,
  "reviewer": "THE MAINSTREAM",
  "feedback": {
    "overall_reaction": "This scene drags. The dialogue is too on-the-nose.",
    "specific_notes": [
      {
        "element": "dialogue",
        "line": "Father, we need to talk.",
        "note": "Cliché opening. Find a more interesting way in.",
        "severity": "minor"
      }
    ],
    "rating": 6.5,

    "emotional_state": {
      "primary_emotion": "bored",
      "intensity": 0.5,
      "secondary_emotions": ["impatient"],
      "mood_trajectory": "falling",
      "engagement_level": 0.4,
      "cumulative_feelings": "We're 14 scenes in and the pacing is slowing down. Need more conflict.",
      "momentum": "Losing steam. The last 3 scenes haven't moved the plot forward enough.",
      "character_investment": {
        "JOHN": {"feeling": "frustrated_with", "intensity": 0.3}
      }
    },

    "questions": {
      "raised": [
        {
          "question": "Why doesn't John just call the lawyer?",
          "narrative_weight": "medium",
          "related_entities": ["JOHN", "LAWYER"]
        }
      ],
      "still_wondering": ["Q_003", "Q_007"],  // References to open questions
      "answered": []
    },

    "predictions": ["The father will have a heart attack"],

    "emotional_revisions": []  // Will be populated if this scene triggers retroactive feelings
  }
}
```

---

## Data Flow

```
1. Upload Screenplay
   ↓
2. Parse into Scenes
   ↓
3. Initialize Entity Tracker
   ↓
4. For each Scene:
   │
   ├→ Update Entity Tracker
   │
   ├→ For each Reviewer:
   │   ├→ Build Context (recent + historical + entities)
   │   ├→ Generate Prompt
   │   ├→ Call AI API
   │   └→ Store Feedback
   │
   ├→ Compress Oldest Recent Memory
   │
   └→ Slide Memory Window
   ↓
5. Aggregate All Feedback
   ↓
6. Generate Report
```

---

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Memory Management**:
  - Recent: Python deque
  - Historical: PostgreSQL or SQLite
  - Vectors: ChromaDB or Pinecone (for semantic search if needed)
- **AI SDKs**:
  - anthropic
  - openai
  - google-generativeai
- **Parser**:
  - pypdf for PDF
  - Custom parser for Fountain/FDX
- **Entity Tracking**: Custom classes + SQLite

### Frontend
- **Framework**: React + Vite
- **UI Library**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand or React Context
- **File Upload**: react-dropzone
- **PDF Preview**: react-pdf
- **Charts/Viz**: recharts

### Infrastructure
- **Deployment**: Docker containers
- **API Gateway**: FastAPI CORS + nginx
- **Background Jobs**: Celery or Python asyncio
- **Storage**: Local filesystem or S3 for uploaded files

---

## File Structure

```
screenplay/
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── models/
│   │   ├── screenplay.py          # Screenplay data models
│   │   ├── scene.py               # Scene models
│   │   ├── entity.py              # Entity tracker models
│   │   ├── memory.py              # Memory system models
│   │   └── feedback.py            # Feedback models
│   ├── services/
│   │   ├── parser.py              # Screenplay parser
│   │   ├── memory_manager.py     # Memory sliding window
│   │   ├── entity_tracker.py     # Entity tracking system
│   │   ├── reviewer.py            # Reviewer profiles
│   │   ├── api_manager.py         # Multi-API integration
│   │   └── feedback_engine.py     # Scene-by-scene processing
│   ├── api/
│   │   ├── routes.py              # API endpoints
│   │   └── schemas.py             # Pydantic schemas
│   ├── utils/
│   │   ├── compression.py         # Scene compression/digesting
│   │   └── importance_scorer.py   # Entity importance algorithm
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.jsx
│   │   │   ├── SceneNavigator.jsx
│   │   │   ├── FeedbackPanel.jsx
│   │   │   ├── ReviewerToggle.jsx
│   │   │   └── EntityTracker.jsx
│   │   ├── pages/
│   │   │   ├── Upload.jsx
│   │   │   ├── Analysis.jsx
│   │   │   └── Report.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
└── docs/
    └── ARCHITECTURE.md (this file)
```

---

## Key Algorithms

### Scene Compression Algorithm

```python
def compress_scene(scene, entity_tracker):
    """
    Compress full scene to ~20% size digest
    """
    # 1. Extract key information
    characters = scene.characters_present
    dialogue_highlights = extract_key_dialogue(scene)
    actions = extract_key_actions(scene)

    # 2. Identify plot beats
    plot_beats = identify_plot_beats(scene, entity_tracker)

    # 3. Calculate scene importance
    importance = calculate_scene_importance(scene, entity_tracker)

    # 4. Generate summary
    summary = generate_summary(
        characters=characters,
        key_dialogue=dialogue_highlights,
        key_actions=actions,
        plot_beats=plot_beats
    )

    return {
        "scene_id": scene.id,
        "summary": summary,
        "characters_present": characters,
        "key_objects": extract_objects(scene),
        "emotional_tone": detect_tone(scene),
        "plot_beats": plot_beats,
        "importance_score": importance
    }
```

### Entity Importance Recalculation

```python
def recalculate_importance(entity, current_scene_number):
    """
    Recalculate entity importance as screenplay progresses
    """
    # Base factors
    speaking_weight = entity.speaking_lines * 0.2
    appearance_weight = len(entity.appearances) * 0.15

    # Span factor (appears early and late = important)
    span = (entity.last_appearance - entity.first_appearance) / current_scene_number
    span_weight = span * 0.15

    # Mentioned when absent (people talk about them)
    mention_weight = len(entity.mentioned_when_absent) * 0.2

    # Relationship complexity
    relationship_weight = len(entity.relationships) * 0.1

    # Key moments (assigned manually or detected)
    key_moments_weight = len(entity.key_moments) * 0.2

    # Bonus: Recently appeared
    recency_bonus = 0.1 if (current_scene_number - entity.last_appearance) < 5 else 0

    total = (speaking_weight + appearance_weight + span_weight +
             mention_weight + relationship_weight + key_moments_weight + recency_bonus)

    return min(total, 1.0)  # Cap at 1.0
```

---

## Critical Design Decisions

### Decision 1: Why Scene-by-Scene vs Full Script?
**Choice**: Scene-by-scene processing
**Reason**: 120+ pages exceed all AI context windows. Human-like processing is more natural.
**Tradeoff**: More API calls = higher cost, but maintains quality

### Decision 2: Why Multiple APIs vs Single?
**Choice**: Multi-API support
**Reason**: Different AIs have different "tastes" - diversity improves feedback
**Tradeoff**: Complexity in integration, but better output

### Decision 3: Why Entity Tracking vs Pure Memory?
**Choice**: Separate entity tracking system
**Reason**: Pure memory compression loses important details (the "forgotten maid")
**Tradeoff**: Additional complexity, but solves critical problem

### Decision 4: Vector DB vs Structured Storage?
**Choice**: Start with structured (JSON/SQLite), add vectors if needed
**Reason**: Simpler to implement, may not need semantic search yet
**Tradeoff**: May need to refactor later, but faster to start

---

## Performance Targets

- **Parse Time**: <30 seconds for 120-page screenplay
- **Processing Time**: <2 minutes per scene per reviewer
- **Total Analysis Time**: ~6 hours for 120-page script with 3 reviewers (100 scenes × 3 reviewers × 2 min)
- **Memory Usage**: <2GB RAM during processing
- **Cost**: <$5 per full screenplay analysis (optimized API usage)

---

## Future Enhancements

1. **Parallel Processing**: Process multiple scenes simultaneously (if APIs allow)
2. **Incremental Analysis**: Analyze as user writes, not just complete scripts
3. **Learning System**: Reviewers learn from user feedback on their notes
4. **Comparative Analysis**: Compare multiple drafts, track improvements
5. **Genre Detection**: Auto-detect genre and recommend relevant reviewers
6. **Character Arc Visualization**: Graph character development over time
7. **Thematic Analysis**: Extract themes across entire screenplay
8. **Pacing Visualization**: Show pacing issues visually

---

**Next Steps**:
1. Implement screenplay parser
2. Build memory management system
3. Create entity tracker
4. Develop one reviewer profile for testing
