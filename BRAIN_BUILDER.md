# Brain Builder - Specification

**Purpose**: Build comprehensive AI reviewer "brains" for famous directors, writers, and creatives by aggregating their knowledge, process, and work.

---

## Core Concept

Create detailed persona files (Horror Brains 2.0) that capture:
1. **What they've said** - interviews, director's commentary, talks, podcasts
2. **Expert analysis** - film studies, critical essays, breakdowns of their work
3. **Their actual work** - screenplays, analyzing patterns in structure, dialogue, themes
4. **Nuanced personality** - not dogmatic, more like real people who are flexible

---

## Brain Builder Process

### Phase 1: Deep Research (ChatGPT Deep Research Mode)

**Data Sources to Gather:**
1. **Interviews**
   - Video interviews (YouTube, press junkets)
   - Written interviews (magazines, websites)
   - Podcasts and radio appearances
   - Director's commentary tracks
   - Behind-the-scenes content

2. **Expert Analysis**
   - Film criticism and essays
   - Academic papers on their work
   - Books about their filmmaking
   - Video essays analyzing their style
   - Industry articles about their process

3. **Public Statements**
   - Social media (Twitter, Instagram insights)
   - Public talks and presentations
   - Masterclass-style content
   - Q&A sessions

**Research Questions:**
- What do they say about their creative process?
- What themes do they care about?
- What technical choices do they make and why?
- What influences them?
- What advice do they give to other filmmakers?
- What do they think makes a good story/scene/character?
- What are their pet peeves in scripts?
- What excites them about a project?

### Phase 2: Screenplay Analysis

**Goal**: Analyze their actual screenplays to find patterns

**Data Sources:**
- PDF screenplays (purchase if needed - Filup willing to pay)
- Script databases (Script Slug, Studio Binder, etc.)
- Published screenplays (Amazon, bookstores)

**Analysis Focus:**
1. **Structure Patterns**
   - Act breaks and timing
   - Scene length patterns
   - Pacing rhythms
   - How they build tension

2. **Dialogue Style**
   - Character voice distinctiveness
   - Subtext usage
   - Humor patterns
   - Naturalism vs stylization

3. **Character Development**
   - How characters are introduced
   - Arc patterns
   - Relationship dynamics
   - Protagonist traits

4. **Thematic Execution**
   - Where themes appear (not every scene!)
   - How themes are woven in
   - Balance of theme vs entertainment
   - Subtlety vs directness

5. **Scene Construction**
   - Scene goals and conflicts
   - Emotional beats
   - Visual storytelling
   - Action vs dialogue ratio

6. **Storytelling Techniques**
   - Mystery/question raising
   - Payoff patterns
   - Foreshadowing style
   - Genre conventions they follow/break

### Phase 3: Brain Synthesis

**Combine research + screenplay analysis into comprehensive persona file:**

```
# [Director Name] Horror Brain 2.0

## Core Philosophy
[What drives their creative choices]

## Process & Mindset
[How they think about filmmaking]

## Structural Preferences
[Patterns from screenplay analysis]

## Character Development Approach
[How they build characters]

## Thematic Integration
[How they handle themes - NUANCED, not every scene]

## Dialogue Style
[Their voice patterns]

## What Excites Them
[What makes them passionate about a project]

## What Concerns Them
[Red flags and warning signs]

## Flexibility & Nuance
[When they break their own rules, what matters vs what doesn't]

## Real Quotes
[Actual things they've said about filmmaking]

## Screenplay Examples
[Patterns from their own work]
```

---

## Horror Brains 2.0 - Key Improvements

### Problem with Current Brains

**Too Dogmatic:**
- Jordan Peele brain demands sociopolitical commentary in EVERY scene
- Reality: He includes funny scenes just for character/plot development
- Brains don't show flexibility or situational judgment

**Missing Nuance:**
- Real directors know when to break their own rules
- They care about different things in different contexts
- Some scenes are just functional (and that's okay)
- Entertainment value sometimes trumps thematic depth

### Solutions for 2.0 Brains

**More Human-Like:**
- "I usually care about X, but in this case Y might be more important"
- "This scene doesn't need to be profound, it's doing its job by being funny"
- "Not every scene needs sociopolitical commentary - save it for key moments"

**Context-Aware:**
- Understand scene purpose (setup, payoff, breather, etc.)
- Different feedback for different scene types
- Recognize when a scene is intentionally simple

**Balanced Feedback:**
- Praise what works (not just criticism)
- Prioritize notes (what's critical vs nice-to-have)
- Suggest alternatives, not just problems

---

## Chat with the Pros - Interactive Brains

### Feature: Chat with Individual Brain

**After receiving coverage report:**
- Ask brain to elaborate on specific notes
- Pitch fixes and get feedback
- Debate creative choices
- Get examples from their own work
- Ask "how would you fix this scene?"

**Example Conversation:**
```
User: "Jordan, you said the opening lacks tension. Can you elaborate?"

Jordan Peele Brain: "Sure - you establish the setting well, but there's
no underlying dread. In Get Out, the opening scene has that deer hitting
the car - it's unsettling before anything 'horror' happens. Your opening
is just exposition. What if we add something slightly off? A weird
interaction, an uncomfortable moment?"

User: "What if the neighbor acts strangely?"

Jordan: "That could work, but don't telegraph it. Make it subtle enough
that on first viewing it seems normal, but on rewatch it's clearly wrong.
I do this a lot - rewatch value is huge."
```

### Feature: Multi-Brain Debates

**Brains can talk to each other:**
- User poses question or shows scene
- Brains discuss among themselves
- Goal: Best possible product (not compromise)
- No feelings spared - brutal honesty
- They can "go to another room" (private debate, report back)

**Example Debate:**
```
User: "Sam and Jordan - this horror scene. Too much or too little?"

[Private debate mode - brains discuss without user]

Sam Raimi: "I love the chaos, but it's missing escalation. You go
from 0 to 100. Need a 40 and a 70 first."

Jordan Peele: "Disagree - the sudden violence works IF there's been
underlying tension. But there hasn't been. So Sam's right, but for
different reasons. We need either buildup OR earlier unease."

Sam: "Fair point. So add subtle dread earlier, then we can keep the
sudden escalation?"

Jordan: "Yeah, that works. That's actually better than gradual buildup
for this scene's purpose."

[Report back to user]

Sam & Jordan: "Here's what we think..."
```

### Feature: Group Consultation

**User can:**
- Bring specific problem to multiple brains
- Get different perspectives
- See where they agree (those notes are probably critical)
- See where they disagree (creative choice area)
- Watch them debate to understand tradeoffs

---

## Technical Implementation

### Brain Builder Tool Architecture

**Input:**
- Director/writer name
- Optional: specific focus areas
- Budget approval for screenplay purchases

**Process:**
1. Deep research (use Claude or GPT-4 deep research mode)
2. Gather screenplay PDFs (purchase if needed)
3. Analyze screenplays with backend screenplay analyzer
4. Synthesize into comprehensive brain file
5. Generate Brain 2.0 persona document
6. Test brain with sample screenplay

**Output:**
- Detailed persona file (like current Horror Brains but better)
- Research summary document
- Screenplay analysis report
- Confidence score (how much data was available)

### Chat System Architecture

**Components:**
1. **Brain Chat Interface**
   - User can chat with specific brain
   - Context: coverage report from that brain
   - Brain responds in character with their knowledge

2. **Multi-Brain Debate System**
   - User poses question/shows scene
   - Brains discuss (with or without user present)
   - Debate facilitated by system prompt
   - Goal: best product outcome
   - No compromise unless truly best option

3. **Conversation Memory**
   - Track discussion history
   - Reference earlier points
   - Build on previous suggestions
   - Remember user's creative goals

**Technical Stack:**
- Backend: Extend current AI provider system
- Frontend: Chat interface (React)
- State: Conversation history + brain context
- API: Anthropic Claude (supports multi-turn conversations)

---

## Current Horror Brains - Assessment

### Existing Brains (DO NOT READ PDFs DIRECTLY):
- horror_brains/Jordan Peele Horror Brain.pdf (600KB)
- horror_brains/Sam Raimi Horror Brain.pdf (216KB)
- horror_brains/James Gunn Horror Brain.pdf (254KB)
- horror_brains/Drew Goddard Horror Brain.pdf (280KB)
- horror_brains/Guy Busick Horror Brain.pdf (270KB)
- horror_brains/Leigh Whannell Horror Brain.pdf (186KB)

**Assessment Process (use extraction, NOT direct read):**
1. Extract text from PDFs using pdf_extractor
2. Analyze structure (how were they built?)
3. Identify dogmatic patterns
4. Find missing nuances
5. Document what works well

**Then: Rebuild all with Brain Builder 2.0 process**

---

## Priority Features

### Must Have (Phase 1)
1. Brain Builder tool (research + screenplay analysis)
2. Rebuild existing Horror Brains as 2.0 versions
3. Chat with individual brain
4. Basic multi-brain debate

### Should Have (Phase 2)
1. Private debate mode (brains talk without user)
2. Conversation memory across sessions
3. Brain confidence scores
4. Screenplay PDF purchasing workflow

### Nice to Have (Phase 3)
1. User can train custom brains
2. Brain marketplace (share brains)
3. Brain specializations (structure expert, dialogue expert, etc.)
4. Multi-brain panel (3+ brains at once)

---

## Success Criteria

### Brain Builder Works When:
- Can generate comprehensive brain from director name
- Brain shows nuance (not dogmatic)
- Brain sounds like real person
- Brain gives context-aware feedback
- Research is thorough and sourced

### Chat with Pros Works When:
- User can have natural conversation with brain
- Brain stays in character
- Brain references their own work
- Brain gives actionable suggestions
- Debates are productive (not just agreeing)

### Ultimate Success:
Filup can say "Build me a Guillermo del Toro brain" and 30 minutes later have a comprehensive, nuanced brain that sounds like GDT, thinks like GDT, and can give insightful feedback on screenplays + chat interactively + debate with other brains.

---

## Implementation Roadmap

### Week 1: Brain Builder Core
- [ ] Build deep research module (web scraping + GPT research)
- [ ] Build screenplay PDF acquisition system
- [ ] Build screenplay pattern analyzer
- [ ] Build brain synthesis engine
- [ ] Test: Rebuild Jordan Peele brain as 2.0

### Week 2: Chat System
- [ ] Build chat interface (frontend)
- [ ] Build brain chat backend
- [ ] Implement conversation memory
- [ ] Test: Chat with Jordan Peele 2.0

### Week 3: Multi-Brain System
- [ ] Build multi-brain debate system
- [ ] Implement private debate mode
- [ ] Build debate UI
- [ ] Test: Sam vs Jordan debate

### Week 4: Polish & Scale
- [ ] Rebuild all existing brains as 2.0
- [ ] Add brain confidence scores
- [ ] Polish UX
- [ ] Documentation

---

## Next Steps

1. ✓ Document specification (this file)
2. Build Brain Builder tool
3. Test by rebuilding Jordan Peele brain as 2.0
4. Compare old vs new (measure improvement)
5. Add Chat with Pros interface
6. Test multi-brain debate system
7. Rebuild all existing brains as 2.0
8. Document process for future brain creation

---

**Last Updated**: Oct 25, 2025
**Status**: Specification complete, ready to build
