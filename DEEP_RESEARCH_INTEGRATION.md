# ChatGPT Deep Research Integration

**Purpose**: Use ChatGPT Deep Research to fully automate source gathering for Horror Brain 2.0 personas.

---

## Workflow

### Step 1: Generate Deep Research Prompt

Brain Builder generates a comprehensive research prompt for ChatGPT:

```
I need deep research on [Director Name]'s filmmaking process, philosophy, and creative approach for building an AI reviewer persona.

RESEARCH FOCUS AREAS:

1. Creative Philosophy & Process
   - What drives their creative choices?
   - How do they think about storytelling?
   - What makes them passionate about a project?
   - Their approach to the craft of filmmaking

2. Themes & Interests
   - What themes do they consistently explore?
   - What subjects fascinate them?
   - How do they integrate themes into their work?
   - Balance of entertainment vs deeper meaning

3. Technical Preferences
   - Structural patterns (pacing, act breaks, scene construction)
   - Dialogue style (naturalistic vs stylized)
   - Character development approach
   - Visual storytelling techniques

4. What They Look For in Scripts
   - What excites them about a screenplay?
   - Red flags and warning signs
   - Pet peeves in scripts
   - What makes a scene work for them

5. Advice & Insights
   - Advice they give to other filmmakers
   - Common mistakes they see
   - Lessons they've learned
   - Their influences and inspirations

6. Real Quotes & Examples
   - Direct quotes about their process (verbatim)
   - Examples from their own work
   - Stories about specific creative decisions
   - Behind-the-scenes insights

PRIORITY SOURCES (find and analyze these):

1. Director's Commentary Tracks
   - Find YouTube videos or transcripts of director's commentary
   - Example search: "[Director] director's commentary [Film Name]"
   - These are GOLD - hours of them explaining their choices scene-by-scene

2. In-Depth Interviews
   - Long-form interviews (30+ minutes)
   - Podcasts about filmmaking
   - Written interviews in major publications
   - Q&A sessions, masterclasses

3. Expert Analysis
   - Video essays analyzing their work
   - Film criticism and scholarly analysis
   - Books about their filmmaking
   - Industry articles about their process

4. Social Media & Public Statements
   - Twitter/X threads about filmmaking
   - Instagram posts with insights
   - Reddit AMAs
   - Public talks and presentations

DELIVERABLES:

For each source found:
1. URL or citation
2. Key quotes (verbatim, with timestamp/page number)
3. Insights extracted
4. Categorize: commentary/interview/analysis/social

Focus on QUALITY sources where [Director] speaks in their own words about their craft.

Aim for:
- 3+ hours of director's commentary (if available)
- 10+ substantial interviews
- 5+ expert analyses
- Real quotes from multiple sources

Generate a comprehensive research report organized by the focus areas above.
```

### Step 2: User Runs ChatGPT Deep Research

**Process:**
1. Copy generated prompt
2. Paste into ChatGPT with Deep Research enabled
3. ChatGPT searches the web, compiles sources, analyzes
4. Returns comprehensive research report

**Expected output from ChatGPT:**
- 10-20 page research report
- Organized by focus areas
- Sources cited with URLs
- Direct quotes with attribution
- Insights categorized

### Step 3: Import Research Into Brain Builder

**Brain Builder parses ChatGPT output:**

```python
class DeepResearchImporter:
    """Import ChatGPT Deep Research results into Brain Builder"""

    def import_research_report(
        self,
        director_name: str,
        chatgpt_report: str
    ) -> ResearchFindings:
        """
        Parse ChatGPT Deep Research report

        Args:
            director_name: Director's name
            chatgpt_report: Full text of ChatGPT research report

        Returns:
            ResearchFindings ready for Brain Builder
        """

        # Use Claude to parse the report
        findings = self.parse_with_ai(director_name, chatgpt_report)

        return findings
```

### Step 4: Brain Builder Continues Automatically

Once research is imported:
1. ✅ Research findings loaded
2. → Find screenplays (check free sources)
3. → Analyze screenplay patterns
4. → Synthesize Horror Brain 2.0
5. → Calculate confidence score
6. → Save with version number

---

## Brain Versioning System

### Git-Style Commits for Brains

```
horror_brains_v2/
    jordan_peele/
        brain.md                 # Current version (symlink to latest)
        versions/
            v1.0_20251025.md     # Initial build
            v2.0_20251026.md     # Added more interviews
            v2.1_20251027.md     # Analyzed Nope screenplay
            v2.2_20251028.md     # Improved nuance
        changelog.md             # Version history
        metadata.json            # Confidence scores, sources, stats
        sources/
            chatgpt_research_20251025.md
            get_out_screenplay_analysis.json
            us_screenplay_analysis.json
```

### CHANGELOG.md Format

```markdown
# Jordan Peele Horror Brain - Changelog

## v2.2 (2025-10-28) - Confidence: 0.95
### Added
- Analyzed Nope screenplay (patterns found)
- 5 new quotes from Nope director's commentary
- Structural preference: Opens with isolated protagonist 100% of time

### Improved
- Thematic integration section (more nuance about when themes appear)
- Flexibility section (when he breaks his own rules)

### Sources
- Total: 23 sources (+3)
- Commentary: 9 hours (+2.5 hours)
- Interviews: 15 (+2)
- Screenplays: 3 (+1)

---

## v2.1 (2025-10-27) - Confidence: 0.92
### Added
- 3 podcast interviews (Marc Maron, Fresh Air, The Q&A)
- 15 new verbatim quotes
- Insights about balancing horror and comedy

### Improved
- Creative philosophy section
- Advice section (what he tells other filmmakers)

### Sources
- Total: 20 sources (+3)
- Commentary: 6.5 hours
- Interviews: 13 (+3)
- Screenplays: 2

---

## v2.0 (2025-10-26) - Confidence: 0.85
### Added
- Rebuilt from v1.0 with ChatGPT Deep Research
- Director's commentary: Get Out (2.5 hours), Us (4 hours)
- Screenplay analysis: Get Out, Us
- More human-like, less dogmatic

### Changed
- Thematic approach: Not every scene needs social commentary
- Added context-awareness
- Balanced feedback (praise + criticism)

### Sources
- Total: 17 sources
- Commentary: 6.5 hours
- Interviews: 10
- Screenplays: 2

---

## v1.0 (2024-10-24) - Confidence: 0.70
- Original Horror Brain 1.0
- Manual research
- Too dogmatic about themes
```

### metadata.json Format

```json
{
  "brain_name": "Jordan Peele",
  "current_version": "v2.2",
  "confidence_score": 0.95,
  "versions": [
    {
      "version": "v2.2",
      "date": "2025-10-28",
      "confidence": 0.95,
      "sources_count": 23,
      "screenplay_count": 3,
      "commentary_hours": 9.0,
      "interview_count": 15
    },
    {
      "version": "v2.1",
      "date": "2025-10-27",
      "confidence": 0.92,
      "sources_count": 20,
      "screenplay_count": 2,
      "commentary_hours": 6.5,
      "interview_count": 13
    }
  ],
  "quality_checklist": {
    "commentary_hours": 9.0,
    "target_commentary_hours": 3.0,
    "status": "excellent",

    "interviews": 15,
    "target_interviews": 10,
    "status": "excellent",

    "screenplays": 3,
    "target_screenplays": 3,
    "status": "excellent",

    "expert_analysis": 5,
    "target_expert_analysis": 5,
    "status": "good",

    "real_quotes": 45,
    "target_real_quotes": 20,
    "status": "excellent"
  }
}
```

---

## Brain Quality Checklist

### Confidence Score Calculation

```python
def calculate_confidence_score(sources):
    """
    Calculate confidence score (0-1.0) based on source quality
    """

    score = 0.0

    # Commentary (worth 30%)
    commentary_hours = sources['commentary_hours']
    if commentary_hours >= 6:
        score += 0.30
    elif commentary_hours >= 3:
        score += 0.25
    elif commentary_hours >= 1:
        score += 0.15
    elif commentary_hours > 0:
        score += 0.05

    # Interviews (worth 25%)
    interviews = sources['interview_count']
    if interviews >= 15:
        score += 0.25
    elif interviews >= 10:
        score += 0.20
    elif interviews >= 5:
        score += 0.15
    elif interviews >= 2:
        score += 0.10

    # Screenplays (worth 25%)
    screenplays = sources['screenplay_count']
    if screenplays >= 3:
        score += 0.25
    elif screenplays >= 2:
        score += 0.20
    elif screenplays >= 1:
        score += 0.15

    # Expert Analysis (worth 10%)
    analysis = sources['expert_analysis_count']
    if analysis >= 5:
        score += 0.10
    elif analysis >= 3:
        score += 0.07
    elif analysis >= 1:
        score += 0.05

    # Real Quotes (worth 10%)
    quotes = sources['real_quotes_count']
    if quotes >= 30:
        score += 0.10
    elif quotes >= 20:
        score += 0.07
    elif quotes >= 10:
        score += 0.05

    return min(score, 1.0)
```

### Quality Rating

- **0.95-1.0: Exceptional** - Use with full confidence
- **0.85-0.94: Excellent** - Very comprehensive, ready to use
- **0.75-0.84: Good** - Solid brain, may improve with more sources
- **0.60-0.74: Moderate** - Usable but limited, keep improving
- **0.40-0.59: Weak** - Not enough data, continue research
- **<0.40: Insufficient** - Don't use yet, needs much more research

---

## Iterative Improvement Process

### How Brains Get Smarter Over Time

```
Week 1: Build v1.0
  - Run ChatGPT Deep Research
  - Import findings
  - Find 1-2 screenplays
  - Synthesize brain
  - Confidence: 0.75 (Good)

Week 2: Upgrade to v1.1
  - User finds more director's commentary
  - Add to sources
  - Rebuild brain
  - Confidence: 0.85 (Excellent)

Week 3: Upgrade to v1.2
  - Analyze third screenplay
  - Find 5 more interviews
  - Rebuild brain
  - Confidence: 0.92 (Excellent)

Month 2: Upgrade to v2.0
  - Major synthesis improvements
  - Better nuance handling
  - Confidence: 0.95 (Exceptional)
```

### Automatic Quality Reports

```
Jordan Peele Horror Brain v2.2
Confidence: 0.95 (Exceptional)

✅ STRENGTHS:
  - 9 hours director's commentary (target: 3+)
  - 15 interviews (target: 10+)
  - 3 screenplays analyzed (target: 3+)
  - 45 real quotes (target: 20+)

⚠️  COULD IMPROVE:
  - Expert analysis: 5 (target: 5+) ← Just met target
  - Social media insights: Limited

🎯 NEXT STEPS TO REACH 1.0:
  - Add 2-3 more video essay analyses
  - Find social media threads about his process
  - Estimated confidence gain: +0.03 → 0.98
```

---

## Example: Full Workflow

### User wants Jordan Peele Brain 2.0

**Step 1: Brain Builder generates prompt**
```python
builder = BrainBuilder()
prompt = builder.generate_deep_research_prompt("Jordan Peele")
print(prompt)
# User copies this prompt
```

**Step 2: User runs ChatGPT Deep Research**
- Paste prompt into ChatGPT (Deep Research mode)
- Wait 5-10 minutes
- ChatGPT returns comprehensive report

**Step 3: Import research**
```python
# User saves ChatGPT report as text file
chatgpt_report = open("jordan_peele_research.txt").read()

builder.import_deep_research(
    director_name="Jordan Peele",
    research_report=chatgpt_report
)
```

**Step 4: Brain Builder finds screenplays**
```python
# Checks free sources automatically
screenplays_found = builder.find_screenplays("Jordan Peele")
# → Found: Get Out (IMSDb), Us (Script Slug - paywall)

builder.add_screenplays([
    "screenplays/get_out.pdf",  # User provides
    "screenplays/us.pdf"        # User provides
])
```

**Step 5: Build brain**
```python
brain = builder.build_brain("Jordan Peele")
# → Analyzing sources...
# → Analyzing screenplays...
# → Synthesizing Horror Brain 2.0...
# → Confidence: 0.92 (Excellent)
# → Saved: horror_brains_v2/jordan_peele/versions/v1.0_20251025.md
```

**Step 6: Review and iterate**
```python
builder.show_quality_report("Jordan Peele")
# → Shows what's strong, what could improve
# → Suggests next sources to add

# Week later: Found more sources
builder.add_sources("Jordan Peele", new_sources)
builder.rebuild_brain("Jordan Peele")  # → v1.1
```

---

## Implementation Priority

### Phase 1: Deep Research Integration (This Week)
- [ ] Build DeepResearchImporter
- [ ] Create prompt generator
- [ ] Test with Jordan Peele
- [ ] Verify it works end-to-end

### Phase 2: Versioning System (Next Week)
- [ ] Git-style brain versions
- [ ] Changelog generation
- [ ] Quality scoring
- [ ] Improvement suggestions

### Phase 3: Automation (Following Week)
- [ ] Screenplay finder (free sources)
- [ ] Automatic quality reports
- [ ] Iterative improvement workflow

---

**Next Step: Build DeepResearchImporter?**
