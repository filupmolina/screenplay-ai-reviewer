# Lessons Learned

**DO NOT DELETE THIS FILE. READ IT EVERY SESSION.**

<!--
═══════════════════════════════════════════════════════════════════
HOW TO UPDATE THIS FILE
═══════════════════════════════════════════════════════════════════

WHEN TO ADD A LESSON:
- When Filup says "Never do this again" or gives ANY directive
- When YOU solve a problem ("Solved!", "Got it!", "There's the problem!")
- When YOU discover a pattern worth documenting
- When YOU catch a mistake you made
- When YOU learn how a tool/library works

HOW TO ADD A LESSON:
1. Choose category: Progress Tracking / Code Quality / UX / Technical / Workflow
2. Add to "Active Lessons" section at top (most important)
3. Use required 5-part format (see below)
4. Add horizontal rule (---) after each lesson
5. Git commit the update immediately
6. Tell Filup: "✓ Added to LESSONS_LEARNED.md"

REQUIRED FORMAT (ALL 5 PARTS):
### [Brief Title]

**Date**: Oct 23, 2025
**What happened**: [The mistake or discovery in 1-2 sentences]
**Why it happened**: [Root cause]
**The rule**: [Clear directive - "Always X" or "Never Y"]
**How to check**: [Verification steps before claiming done]

WHEN TO SUGGEST ADDING:
After solving something, say:
"Solved! [explanation]

Should I add this to LESSONS_LEARNED.md? This would help prevent [problem] / ensure [benefit] in future sessions."

WHEN TO MOVE TO RETIRED:
- When underlying issue is permanently fixed in code
- When lesson no longer applies
- Move to "Retired Lessons" section with note explaining why

FORMATTING RULES:
- Keep Active Lessons at top (most visible)
- Use horizontal rules (---) between lessons
- Date format: Oct 23, 2025
- Be specific in "How to check" section
- Make "The rule" actionable and clear

═══════════════════════════════════════════════════════════════════
-->

This file tracks mistakes, learnings, and "never do this again" rules specific to this app.

---

## Active Lessons (CHECK THESE EVERY SESSION)

### NEVER read Horror Brain PDFs directly - use vectorization or extraction

**Date**: Oct 25, 2025
**What happened**: Opened large Horror Brain PDF (186KB-600KB) directly with Read tool, instantly killed context window, lost all session work
**Why**: Didn't check file size first, treated PDFs like small text files
**The rule**: NEVER use Read tool on Horror Brain PDFs (or any PDF >100KB). Always check size with `ls -lh` first. Use extraction or vectorization for large files.
**How to check**:
  1. Before reading ANY PDF: `ls -lh [file]` to check size
  2. If >100KB → STOP, use extraction method instead
  3. For Horror Brains: Extract specific sections or use vectorDB
  4. Never load full PDF into context
  5. Horror Brain PDFs are 186KB-600KB - ALL require extraction

---

### NEVER inflate progress % - code ≠ working features

**Date**: Oct 23, 2025
**What happened**: Claimed 75-85% complete when only ~15% of total features actually work
**Why**: Confused "code files exist" with "features work" and ignored 80% of roadmap features
**The rule**: Total % = (Working usable features / ALL roadmap features) × 100. Be BRUTAL.
**How to check**:
  1. Count total features across ALL phases in ROADMAP.md
  2. Count how many Filup can ACTUALLY USE right now
  3. Calculate: (usable / total) × 100
  4. Never claim a feature is "done" if only backend exists
  5. Data connectors aren't done until real data syncs
  6. Voice/mobile/integrations = 0% unless actually built

---

### NEVER give multiple choice options - be decisive

**Date**: Oct 23, 2025
**What happened**: Asked "Would you like me to: 1) X 2) Y 3) Z?" - overwhelming
**Why**: Trying to be helpful but created decision paralysis
**The rule**: Recommend the ONE obvious next thing. User can redirect if they want something else.
**How to check**:
  - Before responding, ask: "What's the ONE most important thing?"
  - Never format as numbered list of options
  - Say "Let's do X" not "Would you like me to..."
  - If truly unclear, ask ONE specific question, not multiple choice

---

### ALWAYS use Webflow × iPad design language - NO UGLY APPS

**Date**: Oct 23, 2025
**What happened**: Built functional but ugly apps - cramped spacing, tiny text, no visual polish
**Why**: Focused only on functionality, treated design as optional "nice to have"
**The rule**: Design language = Webflow (spacious, clean) × iPad apps (touch-friendly, polished). NO UGLY APPS ALLOWED.
**How to check**:
  1. Generous whitespace (24-32px between sections)
  2. Large text (16px+ body, 32-48px headings)
  3. Touch-friendly (44px minimum hit areas)
  4. Premium feel (subtle shadows, smooth animations)
  5. **Lucide icons installed (`npm install lucide-react`)** - not emoji or text
  6. Styled inputs (never browser defaults)
  7. Run quality tests: Squint Test, Webflow Test, iPad Test, Screenshot Test
  8. If looks cheap/cramped/dated → NOT DONE, fix design first
  9. **Design audit on EVERY session start** - fix issues before continuing work

---

### ALWAYS assume user wants a GUI (unless explicitly stated otherwise)

**Date**: Oct 23, 2025
**What happened**: Built CLI-only tools when user wanted visual, point-and-click interface
**Why**: Didn't ask, defaulted to "easier" command-line approach
**The rule**: Default to GUI-first. More often than not, user wants a visual interface, not scripts.
**How to check**:
  - Planning an app? Start with: "Building web-based GUI with [framework]"
  - Only build CLI if explicitly requested
  - If ambiguous, ask: "GUI or CLI?" (but default assumption is GUI)

---

### ALWAYS separate code from data - build for easy updates

**Date**: Oct 23, 2025
**What happened**: Code changes required wiping user data and starting over
**Why**: Mixed data files with source code, no migration system
**The rule**: User data must survive code updates. Separate `/src`, `/data`, `/config` from day one.
**How to check**:
  1. Data stored in `/data` folder (excluded from git)
  2. Config in `/config` folder (excluded from git)
  3. Can pull new code, run npm install, restart - data intact
  4. Database has migration system for schema changes
  5. Settings persist across updates
  6. Never requires "delete everything and start over"

---

### ALWAYS save progress BEFORE hitting token limits

**Date**: Oct 23, 2025
**What happened**: Hit token warnings and couldn't save progress - lost work context
**Why**: Waited too long to check tokens, kept working past safe threshold
**The rule**: Monitor tokens proactively and save at 170k (85%) - don't wait for warnings.
**How to check**:
  - At 120k tokens: Mention it, continue working
  - At 150k tokens: Create WORK_IN_PROGRESS.md, continue carefully
  - At 170k tokens: STOP IMMEDIATELY, save everything, commit, recommend fresh session
  - Never continue past 170k without saving
  - Once warnings appear, it's already too late

---

## Lessons by Category

### Progress Tracking

*(Lessons about honest % tracking, completion criteria, etc.)*

---

### Code Quality

*(Lessons about architecture, patterns, antipatterns for THIS app)*

---

### User Experience

*(Lessons about what Filup wants/doesn't want in THIS app)*

---

### Technical Decisions

*(Lessons about library choices, API usage, performance, etc.)*

---

### Workflow & Process

*(Lessons about git, commits, testing, deployment, etc.)*

---

## Retired Lessons (Fixed/No longer applicable)

*(Move lessons here once the underlying issue is permanently fixed)*

---

## Instructions for Claude

**Every session opening:**
1. Read this file BEFORE presenting briefing
2. Check "Active Lessons" section
3. Apply rules to current work

**When Filup gives ANY directive (BE ALERT):**

Watch for corrections or rules from Filup:
- "Never do this again" / "Don't ever X" / "Stop doing Z"
- "Always do Y" / "I keep telling you..."
- **ANY correction, suggestion, or directive from Filup**

**IMMEDIATELY when detected:**
1. Add new lesson to "Active Lessons"
2. Include all 5 parts (date, what, why, rule, check)
3. Categorize it properly
4. Git commit the update
5. Say: "✓ Added to LESSONS_LEARNED.md - won't happen again"

**When YOU discover a pattern (BE AGGRESSIVE):**

You should **proactively suggest** adding lessons in YOUR OWN work:

**When You SOLVE Something:**
- "Solved!" / "Got it!" / "There's the problem!"
- "Figured it out!" / "Found the issue!"
- "Ah, that's why..." / "Now I see..."
- You fix a bug or discover a root cause
- You find a workaround or solution

**When You DISCOVER Patterns:**
- Same type of bug/issue appears twice
- You catch yourself about to repeat a mistake
- You notice inconsistent behavior across files
- You realize "we should always do X when Y"
- You discover edge cases that weren't handled

**When You LEARN Something:**
- You discover a helpful technique or pattern
- You learn how a tool/library works
- You figure out a gotcha or pitfall
- You find a better way to do something

**When You CATCH Mistakes:**
- You realize you forgot to check something
- You made an assumption that was wrong
- You overlooked something important
- "I should have checked X before doing Y"

**Suggest to Filup:**
```
[After solving something]

Solved! [Brief explanation]

Should I add this to LESSONS_LEARNED.md? This would help prevent [problem] / ensure [benefit] in future sessions.
```

**Be proud when you solve things and identify patterns!**

If Filup agrees:
1. Add the lesson immediately
2. Make it clear and actionable
3. Include how to check for it
4. Commit it
5. Feel good about making the project better!

**When adding a lesson:**
```markdown
### [Brief Title]

**Date**: [Today's date]
**What happened**: [The mistake in 1-2 sentences]
**Why it happened**: [Root cause]
**The rule**: [Clear directive - "Always X" or "Never Y"]
**How to check**: [Verification step before claiming done]
```

---

## Why This File Exists

Context windows reset. You forget. Filup gets frustrated.

This file ensures we don't make the same mistake twice.

**Treat this like a sacred contract.**
