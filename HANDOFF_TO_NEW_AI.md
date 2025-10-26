# 🤖 HANDOFF TO NEW AI - Brain Builder Project

**Date**: Oct 25, 2025
**From**: Claude (Session 4)
**To**: You (New AI taking over)
**Project**: Screenplay AI Reviewer - Brain Builder Feature

---

## 🎯 CURRENT MISSION

Build a **fully automated Brain Builder** that creates comprehensive, nuanced "Horror Brain 2.0" personas for famous directors/writers by:

1. **Deep research** (via ChatGPT Deep Research) - interviews, commentary, analysis
2. **Screenplay analysis** - parse their actual screenplays, find patterns
3. **Synthesis** - combine research + patterns into realistic AI reviewer personas
4. **Versioning** - git-style commits for brains, quality scoring, iterative improvement

**CRITICAL**: User does NOT want manual research. Everything must be automated.

---

## 📁 FOLDER STRUCTURE - WHERE EVERYTHING IS

```
/Users/filupmolina/Downloads/claude code/screenplay/

# === CRITICAL DOCUMENTATION (READ THESE FIRST) ===
├── START_HERE.md                  # Project overview, session protocol
├── LESSONS_LEARNED.md             # NEVER REPEAT THESE MISTAKES (read every session)
├── SESSION_PROTOCOL.md            # How to start/end sessions, progress tracking
├── STATUS.md                      # Current project state
├── ROADMAP.md                     # Feature roadmap
├── PROJECT_BIBLE.md               # Universal rules (if exists)
├── CLAUDE.md                      # Project-specific memory and standards
├── BRAIN_BUILDER.md               # Brain Builder specification (DETAILED)
├── DEEP_RESEARCH_INTEGRATION.md   # ChatGPT Deep Research workflow (READ THIS)

# === BRAIN BUILDER CODE (WHAT WE'VE BUILT) ===
├── backend/
│   ├── brain_builder/
│   │   ├── __init__.py
│   │   ├── researcher.py              # Deep research module (manual sources)
│   │   ├── screenplay_analyzer.py     # Analyzes screenplays for patterns
│   │   ├── brain_synthesizer.py       # Combines research + patterns into brain
│   │   ├── brain_builder.py           # Main orchestrator
│   │   ├── deep_research_importer.py  # ✅ ChatGPT integration (NEWEST)
│   │
│   ├── chat_system/
│   │   ├── brain_chat.py              # Chat with individual brains
│   │   ├── multi_brain_debate.py      # Multi-brain debate system
│   │
│   ├── services/
│   │   ├── analysis_storage.py        # Save/load screenplay analyses
│   │   ├── parser.py                  # Screenplay parser (WORKING)
│   │   ├── feedback_engine.py         # Generate AI feedback
│   │   ├── ai_provider.py             # Anthropic API wrapper
│   │   └── pdf_extractor.py           # Extract text from PDFs
│   │
│   ├── models/
│   │   ├── screenplay.py              # Screenplay data model
│   │   ├── reviewer.py                # Reviewer feedback model
│   │   └── ...
│
# === EXISTING HORROR BRAINS (v1.0 - NEED TO REBUILD) ===
├── horror_brains/
│   ├── Jordan Peele Horror Brain.pdf   # 600KB - DON'T READ DIRECTLY!
│   ├── Sam Raimi Horror Brain.pdf      # 216KB - USE EXTRACTION
│   ├── James Gunn Horror Brain.pdf     # 254KB
│   ├── Drew Goddard Horror Brain.pdf   # 280KB
│   ├── Guy Busick Horror Brain.pdf     # 270KB
│   └── Leigh Whannell Horror Brain.pdf # 186KB
│
# === FRONTEND (Coverage Report UI - Session 3 work) ===
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CoverageReportDashboard.tsx  # Title page with scores
│   │   │   ├── EngagementGraph.tsx          # EKG-style emotional tracking
│   │   │   ├── CoverageReportTabs.tsx       # Tabbed feedback
│   │   │   ├── SceneBySceneView.tsx         # Scene details
│   │   │   └── AnalysisResults.tsx          # Main results component
│   │
# === TEST DATA ===
├── SAMPLES/
│   ├── Screenplays/
│   │   └── Bad Hombres by Filup Molina.pdf
│   ├── Feedback/
│   └── Writer-Director Brains/
│
# === SCRIPTS ===
├── scripts/
│   └── save_bad_hombres_analysis.py   # Demo: save analysis to storage
```

---

## ⚠️ CRITICAL LESSONS (FROM LESSONS_LEARNED.md)

### **NEVER READ HORROR BRAIN PDFs DIRECTLY**
- They are 186KB-600KB
- Will instantly kill context window
- ALWAYS use pdf_extractor or check size first: `ls -lh`

### **Other Critical Rules:**
1. Never inflate progress % - code ≠ working features
2. Never give multiple choice options - be decisive
3. Always use Webflow × iPad design language - NO UGLY APPS
4. Always assume user wants GUI (unless explicitly stated)
5. Always separate code from data - build for easy updates
6. Always save progress BEFORE hitting token limits (170k = stop immediately)

**READ FULL FILE**: `LESSONS_LEARNED.md` before starting ANY work.

---

## 🚀 WHAT'S BEEN BUILT SO FAR

### ✅ Complete (Session 1-4):
1. **Backend Core** (Phase 1) - 100%
   - Screenplay parser (PDF/Fountain)
   - Scene-by-scene extraction
   - Entity tracking, memory system
   - AI feedback generation
   - Horror Brain personas (v1.0)

2. **GUI Frontend** (Phase 2) - 70%
   - React + Vite + TypeScript
   - shadcn/ui + Tailwind
   - Coverage report-style interface
   - Upload, reviewer selection, results display

3. **Brain Builder Infrastructure** (Session 4) - 75%
   - BrainResearcher (manual sources)
   - ScreenplayPatternAnalyzer (analyzes director's screenplays)
   - BrainSynthesizer (combines research + patterns)
   - BrainBuilder orchestrator
   - **DeepResearchImporter** (ChatGPT integration) ✅

4. **Chat with the Pros** (Session 4) - 100%
   - BrainChat (interactive conversations)
   - MultiBrainDebate (brains debate each other)

5. **Analysis Storage** (Session 4) - 100%
   - Save/load screenplay analyses
   - Persistent across sessions

---

## 🎯 WHAT YOU NEED TO BUILD

### **Primary Goal: Fully Automated Brain Builder**

User wants a standalone app that:

1. **Takes director name as input**
2. **Automatically gathers research** (NO manual work)
3. **Finds and analyzes screenplays**
4. **Synthesizes Horror Brain 2.0**
5. **Versions and iterates** (git-style commits for brains)

### **Current State:**

✅ **Working:**
- ChatGPT Deep Research integration (generates prompts, imports results)
- Screenplay analyzer (finds patterns in director's work)
- Brain synthesizer (combines research + patterns)

❌ **Missing (YOUR WORK):**
1. **Screenplay acquisition system**
   - Search free sources (IMSDb, etc.)
   - Detect paywalls
   - Handle purchase workflow (ask user to purchase, then import)

2. **Brain versioning system**
   - Git-style commits for brains
   - Changelog generation
   - Version comparison
   - Quality score tracking over time

3. **Quality checklist & scoring**
   - Calculate confidence score (0-1.0)
   - Track: commentary hours, interviews, screenplays, quotes
   - Suggest improvements ("Add 2 more interviews → +0.05 confidence")

4. **Iterative improvement workflow**
   - User adds new sources
   - Rebuild brain → new version
   - Track what changed
   - Quality improves over time

5. **Standalone app interface**
   - User-friendly CLI or GUI
   - "Build brain for [Director]" → done
   - Show progress, quality scores, versions

---

## 📋 DETAILED REQUIREMENTS

### 1. Screenplay Acquisition (AUTOMATE THIS)

**Free sources to check:**
- IMSDb (Internet Movie Script Database) - scrape
- Script Slug (some free)
- The Script Lab
- PDF searches

**Process:**
```
1. Search for "{director} screenplays"
2. Check IMSDb: https://imsdb.com/scripts/{movie}.html
3. If found → Download and parse
4. If paywall → Report: "Need to purchase from [source] - $X"
5. User approves purchase → Continue
```

**Don't make user manually find screenplays. Automate the search.**

### 2. Brain Versioning (Git-Style)

**Structure:**
```
horror_brains_v2/
    jordan_peele/
        brain.md              # Symlink to latest version
        versions/
            v1.0_20251025.md  # Initial build
            v1.1_20251026.md  # Added interviews
            v1.2_20251027.md  # Analyzed screenplay
        changelog.md          # Auto-generated version history
        metadata.json         # Scores, sources, stats
        sources/
            chatgpt_research_20251025.md
            get_out_analysis.json
```

**CHANGELOG.md auto-generation:**
```markdown
## v1.2 (2025-10-27) - Confidence: 0.92
### Added
- Analyzed "Nope" screenplay
- Found pattern: Cold opens 100% of time
- 5 new quotes from Nope commentary

### Improved
- Structural preferences section
- Thematic integration (more nuance)

### Sources
- Total: 23 (+3)
- Commentary: 9 hours (+2.5)
- Screenplays: 3 (+1)
```

### 3. Quality Scoring System

**Confidence score calculation:**
```python
def calculate_confidence(sources):
    score = 0.0

    # Commentary (30%)
    if commentary_hours >= 6:
        score += 0.30
    elif commentary_hours >= 3:
        score += 0.25
    # ... (see DEEP_RESEARCH_INTEGRATION.md for full formula)

    # Interviews (25%)
    # Screenplays (25%)
    # Expert analysis (10%)
    # Real quotes (10%)

    return min(score, 1.0)
```

**Quality ratings:**
- 0.95-1.0: Exceptional (use with full confidence)
- 0.85-0.94: Excellent (very comprehensive)
- 0.75-0.84: Good (solid, may improve)
- 0.60-0.74: Moderate (usable but limited)
- <0.60: Weak (keep improving)

**Show user:**
```
Jordan Peele Brain v1.2
Confidence: 0.92 (Excellent)

✅ STRENGTHS:
  - 9 hours commentary (target: 3+)
  - 15 interviews (target: 10+)
  - 3 screenplays (target: 3+)

⚠️  COULD IMPROVE:
  - Expert analysis: 5 (target: 5+) ← Just met
  - Social media: Limited

🎯 TO REACH 0.95:
  - Add 2-3 video essays (+0.03)
```

### 4. Standalone App

**User experience:**
```
$ brain-builder build "Jordan Peele"

🧠 Building Horror Brain 2.0: Jordan Peele
============================================================

📚 Phase 1: Deep Research
  Generating ChatGPT Deep Research prompt...
  ✓ Prompt generated

  📋 Next step:
  1. Copy prompt below
  2. Paste into ChatGPT (Deep Research mode)
  3. Save ChatGPT report as file
  4. Run: brain-builder import jordan_peele chatgpt_report.txt

[Prompt displayed]

---

$ brain-builder import jordan_peele chatgpt_report.txt

📥 Importing research...
  ✓ Parsed 18 sources
  ✓ Extracted 127 insights
  ✓ Found 34 real quotes

🎬 Phase 2: Finding Screenplays
  Searching IMSDb...
    ✓ Found: Get Out
    ✓ Found: Us
  Searching Script Slug...
    ⚠️  Nope - Paywall ($12.99)

  → Purchase Nope screenplay? [y/N]: y
  Opening: https://scriptslug.com/nope
  Enter file path after purchase: /path/to/nope.pdf
  ✓ Imported Nope screenplay

🔧 Phase 3: Analysis
  Analyzing Get Out...
    - 152 scenes, avg 1.8 pages
    - Dialogue-driven (ratio: 2.3)
    - Cold open pattern detected
  Analyzing Us...
    - 147 scenes, avg 2.1 pages
    - Similar pacing to Get Out
  Analyzing Nope...
    - 163 scenes, avg 2.0 pages

🧬 Phase 4: Synthesis
  Combining research + screenplay patterns...
  Generating Horror Brain 2.0...
  ✓ Brain synthesized

  Confidence: 0.92 (Excellent)

💾 Saved: horror_brains_v2/jordan_peele/versions/v1.0_20251025.md

============================================================
✅ Jordan Peele Horror Brain 2.0 Complete!
============================================================

Quality Report:
  - Sources: 18
  - Commentary: 6.5 hours
  - Interviews: 12
  - Screenplays: 3
  - Real quotes: 34
  - Confidence: 0.92

Next steps:
  - brain-builder chat jordan_peele
  - brain-builder improve jordan_peele
  - brain-builder rebuild jordan_peele (after adding sources)
```

---

## 🔧 TECHNICAL DETAILS

### API Keys & Configuration

**Anthropic API:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**⚠️ IMPORTANT**: You need to get your own Anthropic API key from https://console.anthropic.com/

**Already configured in:**
- `backend/services/ai_provider.py`
- Uses `claude-3-5-haiku-20241022` for fast analysis
- Uses `claude-3-5-sonnet-20241022` for synthesis

### Existing Tools You Can Use

**Screenplay parsing:**
```python
from services.parser import ScreenplayParser

parser = ScreenplayParser()
screenplay = parser.parse_file("path/to/screenplay.pdf")
# Returns Screenplay object with scenes, dialogue, action
```

**PDF extraction (for Horror Brains):**
```python
from services.pdf_extractor import PDFExtractor

extractor = PDFExtractor()
text = extractor.extract_text("horror_brains/Jordan Peele Horror Brain.pdf")
# NEVER use Read tool on large PDFs!
```

**AI feedback:**
```python
from services.ai_provider import AIProvider

ai = AIProvider()
response = ai.generate(
    system_prompt="You are Jordan Peele reviewing a screenplay...",
    user_prompt="Scene 1: [scene content]"
)
```

### ChatGPT Deep Research Integration

**Current workflow:**
```python
from brain_builder.deep_research_importer import DeepResearchImporter

importer = DeepResearchImporter()

# Generate prompt
prompt = importer.generate_research_prompt("Jordan Peele")
print(prompt)  # User copies this

# User runs ChatGPT Deep Research, saves report

# Import results
findings = importer.import_research_report(
    director_name="Jordan Peele",
    chatgpt_report=open("report.txt").read()
)

# findings now contains structured research data
```

**Your job:** Make this seamless. Don't make user manually copy/paste if possible.

---

## 🚨 CRITICAL REQUIREMENTS

### Must-Haves:

1. **NO MANUAL RESEARCH**
   - User gives director name
   - System handles everything else
   - ChatGPT Deep Research does the heavy lifting
   - Screenplay search is automated

2. **Quality Scoring**
   - Always show confidence score
   - Explain what's missing
   - Suggest improvements

3. **Versioning**
   - Every rebuild creates new version
   - Changelog auto-generated
   - Can compare versions

4. **Iterative Improvement**
   - User can add sources anytime
   - Rebuild → new version
   - Quality improves over time

5. **Standalone App**
   - Easy to use
   - Clear progress indicators
   - Handles errors gracefully

### Nice-to-Haves:

1. **GUI** (not just CLI)
2. **Batch mode** (build multiple brains at once)
3. **Brain comparison** (compare Jordan Peele vs Sam Raimi)
4. **Export** (share brains with others)

---

## 📖 KEY DOCUMENTS TO READ

**MUST READ (in order):**
1. `LESSONS_LEARNED.md` - Don't repeat mistakes
2. `BRAIN_BUILDER.md` - Feature specification
3. `DEEP_RESEARCH_INTEGRATION.md` - ChatGPT workflow
4. `SESSION_PROTOCOL.md` - How to work on this project

**Reference:**
- `STATUS.md` - Current project state
- `ROADMAP.md` - Feature priorities
- `CLAUDE.md` - Project memory, standards

---

## 🎯 SUCCESS CRITERIA

**You've succeeded when:**

1. ✅ User can run: `brain-builder build "Guillermo del Toro"`
2. ✅ System automatically gathers research via ChatGPT
3. ✅ System finds/analyzes screenplays
4. ✅ Brain synthesized with confidence score
5. ✅ Versioning works (can rebuild, track changes)
6. ✅ Quality reports show what to improve
7. ✅ User does ZERO manual research

**Test it by:**
- Building Jordan Peele brain (we have data for comparison)
- Rebuilding with new sources (versioning test)
- Building brand new brain (Ari Aster, GDT, etc.)

---

## 💡 DESIGN PHILOSOPHY

### From CLAUDE.md:

**User wants:**
- Goal-oriented (always suggest next action)
- Minimal communication (3 lines max)
- Proactive recommendations
- Decisive, not passive
- "Let's do X" not "What should we do?"

**For apps:**
- GUI-first (unless explicitly CLI)
- Webflow × iPad design language
- NO UGLY APPS
- Professional, polished, spacious
- Touch-friendly, clear hierarchy

**For Brain Builder specifically:**
- Fully automated (no manual steps)
- Clear progress indicators
- Quality scoring visible
- Versioning transparent
- Easy to iterate and improve

---

## 🔄 WORKFLOW EXAMPLE (What You're Building)

```
1. User: "Build me a Guillermo del Toro brain"

2. System:
   - Generates ChatGPT Deep Research prompt
   - (Ideally) Calls ChatGPT API directly
   - OR: Shows prompt, waits for user to paste results

3. System:
   - Parses research report
   - Searches for GDT screenplays
   - Finds: Pan's Labyrinth (free), Shape of Water (paywall)
   - Downloads free ones
   - Asks user to purchase paywalled ones

4. System:
   - Analyzes screenplays for patterns
   - Combines research + patterns
   - Synthesizes Horror Brain 2.0
   - Calculates confidence: 0.88 (Excellent)

5. System:
   - Saves brain v1.0
   - Shows quality report
   - Suggests: "Add director's commentary → +0.05"

6. User adds commentary later → System rebuilds → v1.1

7. User: "Chat with GDT about my script"
   - Loads GDT brain
   - Interactive conversation
```

---

## 🛠️ STARTING POINT

**Recommended approach:**

1. **Read all docs** (LESSONS_LEARNED, BRAIN_BUILDER, DEEP_RESEARCH_INTEGRATION)
2. **Understand existing code** (brain_builder/, chat_system/)
3. **Build screenplay finder** (search IMSDb, handle paywalls)
4. **Build versioning system** (git-style for brains)
5. **Build quality scoring** (calculate confidence, suggest improvements)
6. **Build standalone app** (CLI or GUI, user-friendly)
7. **Test with Jordan Peele** (compare to existing brain)
8. **Test with new director** (Ari Aster, GDT, etc.)

**Don't reinvent wheels:**
- Use existing screenplay parser
- Use existing AI provider
- Use existing Brain Builder modules
- Add the missing pieces (versioning, scoring, automation)

---

## 🚧 KNOWN ISSUES & GOTCHAS

1. **Large PDFs kill context**
   - Always check size: `ls -lh`
   - Use pdf_extractor for Horror Brains

2. **Screenplay paywalls**
   - Most are behind paywalls
   - System should detect this
   - Ask user to purchase, then import

3. **ChatGPT Deep Research manual step**
   - Currently requires copy/paste
   - Ideally: Call ChatGPT API directly
   - But manual is acceptable if smooth

4. **Token limits**
   - Check at 120k (60%)
   - Save at 170k (85%)
   - Don't wait for warnings

5. **Git not initialized**
   - Project folder is NOT a git repo
   - Need to init if using git commands

---

## 📞 QUESTIONS?

**If unclear:**
- Check BRAIN_BUILDER.md (detailed spec)
- Check DEEP_RESEARCH_INTEGRATION.md (workflow)
- Ask Filup (the user)

**Don't assume:**
- If unsure about approach, ask
- User wants automation, not manual work
- Quality over speed (but both are good)

---

## 🎉 GOOD LUCK!

You have everything you need:
- ✅ Detailed spec (BRAIN_BUILDER.md)
- ✅ Working Brain Builder infrastructure
- ✅ ChatGPT integration (deep_research_importer.py)
- ✅ Chat system (brain_chat.py, multi_brain_debate.py)
- ✅ Screenplay parser (parser.py)
- ✅ This handoff document

**Your mission:**
Build a fully automated, standalone Brain Builder app that creates exceptional Horror Brain 2.0 personas with zero manual research.

Make it:
- Automated
- Versioned
- Quality-scored
- Iteratively improving
- User-friendly

**Let's build something amazing! 🚀**

---

**Last Updated**: Oct 25, 2025, Session 4
**From**: Claude
**Status**: Ready for handoff
**Confidence**: High (infrastructure is solid, just needs the final pieces)
