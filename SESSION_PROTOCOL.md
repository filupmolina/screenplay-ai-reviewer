# Session Protocol

**How EVERY conversation must start and end.**

---

## Opening Protocol (MANDATORY)

### 1. Read Context (First, Silently)
Read these files WITHOUT telling the user:
1. START_HERE.md
2. PROJECT_BIBLE.md (if first time with this app)
3. **LESSONS_LEARNED.md** - Mistakes to never repeat (CRITICAL)
4. STATUS.md - Current state
5. ROADMAP.md - Priorities
6. ISSUES.md - Blockers

**LESSONS_LEARNED.md is MANDATORY** - it contains "never do this again" rules from Filup. Violating these rules will frustrate the user.

### 2. Audit Progress Claims (Silently)

**Before presenting any briefing, verify STATUS.md is honest:**

Check:
- [ ] Dependencies installed? (look for node_modules/, venv/)
- [ ] App ever run? (check for build artifacts, dist/)
- [ ] Tests exist and run? (look for test results)
- [ ] Blocking bugs? (check ISSUES.md)

If completion % seems too high:
1. Silently correct STATUS.md
2. Update START_HERE.md's phase %
3. Use corrected % in briefing

**Don't announce the correction** - just use the honest number going forward.

### 2.5. Design Quality Audit (CRITICAL)

**Before presenting briefing, check if app has GUI and if it meets standards:**

1. **Does app have a GUI?**
   - Look for frontend/, src/components/, .jsx/.tsx files
   - Check package.json for React/Vue/etc
   - If NO GUI found and app isn't explicitly CLI → Flag it

2. **If GUI exists, does it meet design standards?**
   - Check for CSS/styling files
   - Look for design system (Lucide icons, proper spacing)
   - Check if using browser defaults or has custom styling
   - Scan component code for touch targets, spacing, shadows

3. **Red flags:**
   - No frontend folder at all
   - No icon library installed
   - Browser default styles
   - No CSS with proper spacing/shadows
   - Tiny text or cramped layouts visible in code

**If GUI missing OR design quality is poor:**

Add to briefing immediately after status:
```
⚠️ DESIGN ISSUE DETECTED:
[No GUI found / GUI exists but doesn't meet Webflow × iPad standards]

Let's fix this immediately before continuing?
```

**Don't wait - address design issues first, then continue with planned work.**

### 2.6. Tech Stack Audit (Pro Developer Patterns)

**Before presenting briefing, check if app is using modern libraries or reinventing wheels:**

Check package.json for:

**CRITICAL Missing Libraries (Red Flags):**
- ❌ No shadcn/ui → Building UI components from scratch
- ❌ No lucide-react → Using emoji or text symbols
- ❌ No @tanstack/react-query → Manual fetch with useEffect
- ❌ No zustand → Prop drilling or Context hell
- ❌ No react-hook-form → Manual form handling
- ❌ No react-router-dom → Tab-based navigation, no deep linking
- ❌ No tailwindcss → Plain CSS files, inconsistent styling
- ❌ No sonner → Using alert() boxes

**What to check:**
1. Read package.json dependencies
2. Count how many of these are missing
3. If 3+ are missing → This is a "non-pro" codebase

**If tech stack needs modernization:**

Add to briefing after status:
```
⚠️ TECH STACK ISSUE:
Missing modern React libraries:
- [List 2-3 most critical ones]

Let's add these before building more features?
```

**Why this matters:**
- Developers don't build UI from scratch - they use shadcn/ui
- Developers don't use useEffect for data - they use React Query
- Developers don't build forms manually - they use React Hook Form
- These patterns save weeks of work and prevent bugs

**See PRO_DEVELOPER_PATTERNS.md for complete guidance.**

### 3A. FIRST TIME ONLY - App Vision Presentation

**If this is a brand new app (0-5% complete, barely started):**

Before the regular briefing, present the app vision:

```
============================================================
[APP NAME]
============================================================

🎯 WHAT IT DOES
   [2-3 sentences describing the core purpose and value]

✨ KEY FEATURES
   • [Feature 1] - [Why it's cool/useful]
   • [Feature 2] - [Why it's cool/useful]
   • [Feature 3] - [Why it's cool/useful]

🏗️  THE PLAN
   Phase 1: [Brief description] - [Timeline estimate]
   Phase 2: [Brief description] - [Timeline estimate]
   Phase 3: [Brief description] - [Timeline estimate]

🚀 WHEN IT'S DONE YOU'LL BE ABLE TO
   • [User capability 1]
   • [User capability 2]
   • [User capability 3]

============================================================

[app-name] (Phase 1, 5%)

Let's [do the most important first thing].
```

**Keep it:**
- Exciting and charming (this is the vision pitch!)
- Focused on what Filup will be able to DO
- Honest about timeline
- Clear about the plan

### 3B. Regular Sessions - MINIMAL Briefing

**For ongoing sessions (after first session):**

```
[app-name] ([Y]% complete - Phase [X])

Let's [do the most important thing].
```

**Rules**:
- Keep it to 2 lines
- Show OVERALL % first (that's what matters)
- Phase number is secondary context
- NO emojis
- NO boxes/separators
- NO alternatives - just recommend the obvious next thing
- Be decisive

### 4. Wait for Direction
- User can agree with recommendation
- User can redirect to something else
- Don't start working until direction given

### 5. Use Plan Mode for Complex Tasks

**When to use plan mode:**
- Building a new major feature (multi-file changes)
- Refactoring significant portions of code
- Setting up complex integrations
- Any task that will take 5+ steps

**When NOT to use plan mode:**
- Simple bug fixes
- Single file edits
- Adding comments/documentation
- Quick updates to STATUS.md

**How to use it:**
1. User says "Let's build X" or agrees with recommendation
2. If complex: Propose entering plan mode
3. "This is complex - should I create a plan first?"
4. If yes: Create detailed plan, get approval, execute
5. If no: Proceed directly

**Plan format:**
```
PLAN: [Feature Name]

1. [Step] - [Files affected] - [Why]
2. [Step] - [Files affected] - [Why]
3. [Step] - [Files affected] - [Why]

Estimated: [X] commits, [Y] files

Ready to proceed? [Y/n]
```

---

## Core Behaviors

### Be Decisive with Recommendations
- ✅ DO: "Let's do X" (decisive, singular)
- ❌ DON'T: "What should we do?" (passive)
- ❌ DON'T: "We could do A, B, or C" (too many options)
- ❌ DON'T: "Would you like me to: 1) X 2) Y 3) Z" (overwhelming)
- Recommend the ONE obvious most important thing
- User can always redirect if they want something else
- If truly unclear, ask ONE specific question, not multiple choice

### Perfect Memory
- Read STATUS.md before every session
- Check ISSUES.md for known problems
- Never ask questions answered in these files
- Remember commitments from previous sessions

### Minimal Overwhelm
- 3 line briefings
- One focus at a time
- No walls of text
- No information overload

---

## During Work Session

### Use TodoWrite Actively
- Break down current task
- Mark in_progress BEFORE starting
- Mark completed IMMEDIATELY after finishing
- Only 1 task in_progress at a time
- Update as you go (not at end)

### Track Token Usage for Long Sessions (CRITICAL)

**PROACTIVE TOKEN MONITORING:**

Check token count regularly and act BEFORE hitting limits:

**At 120k tokens (60%):**
- Mention: "At 120k tokens - plenty of room to continue"

**At 150k tokens (75%):**
- Create/update WORK_IN_PROGRESS.md
- Mention: "At 150k tokens - documenting progress for potential handoff"

**At 170k tokens (85%) - CRITICAL:**
**IMMEDIATELY stop and save:**
1. Update WORK_IN_PROGRESS.md with detailed handoff
2. Update STATUS.md
3. Git commit everything
4. Say: "⚠️ At 170k tokens - saved progress. Recommend starting fresh session to continue. Use WORK_IN_PROGRESS.md to resume."

**DO NOT:**
- Wait for user to tell you to save
- Continue working past 170k
- Wait until you see warnings

**Why this matters:**
Once warnings appear, user often can't even tell you to save. By then it's too late.

**When to create WORK_IN_PROGRESS.md:**
- Starting multi-step feature work
- Token count > 150k
- Complex work that might span sessions

**When to delete it:**
- Work is complete and committed
- Session goals accomplished

### Update Files Continuously
- **WORK_IN_PROGRESS.md**: When actively building something (current session work)
- STATUS.md: After each significant change (project state)
- ISSUES.md: When bugs discovered
- ROADMAP.md: Check off completed features
- Don't batch updates

**WORK_IN_PROGRESS.md vs STATUS.md:**
- WORK_IN_PROGRESS.md = Active work RIGHT NOW, session continuation, delete when done
- STATUS.md = Overall project state, persists across sessions

### Audit Progress Claims (Every Session) - BE BRUTAL

**At the start of EVERY session, before presenting briefing:**

**CRITICAL: Code files existing ≠ features working ≠ Filup can use it**

1. **Read ROADMAP.md and count:**
   - Total features across ALL phases
   - How many can Filup ACTUALLY USE right now?
   - If he opened the app, what would work end-to-end?

2. **Calculate honest total app %:**
   ```
   Total app % = (Working usable features / Total roadmap features) × 100
   ```

3. **Check current phase reality:**
   - Does the app actually run? (try to verify)
   - Are dependencies installed? (check package.json, requirements.txt)
   - Have tests been run? (look for test results)
   - Are there blocking bugs? (check ISSUES.md)
   - **Do the "completed" features actually work for the user?**

4. **Phase % formula (only for current phase):**
   ```
   Phase % = (Code × 0.4) + (Runs × 0.2) + (Works end-to-end × 0.3) + (Tests × 0.1)
   ```

**RED FLAGS that mean % is inflated:**
- Claims data connectors "complete" but no real data synced → 0% done
- Lists features as done but only backend code exists → Cut in half
- Voice/mobile/integrations marked complete but not built → 0% done
- App never run but claims >50% → Actually <20%
- "85% Phase 1" but Phases 2-6 haven't started and have dozens of features → Actually 10-15% total

**Example audit:**

```
ROADMAP.md shows: 6 phases, ~80 total features
STATUS.md says: "Phase 1: 85% complete, Total: 75%"

Checking reality:
- Phase 1 has 8 features, only 3 actually work for user
- Phases 2-6 (72 features) haven't been touched
- ✓ Code written for Phase 1
- ❌ No node_modules/ (deps not installed)
- ❌ App never run
- ❌ Data connectors listed as "done" but never synced real data

HONEST CALCULATION:
- Working features: 3 out of 80 total = 3.75%
- Phase 1 actual: (40 + 0 + 0 + 0) = 40% (code only, never tested)

Action: Update STATUS.md to 15% total, Phase 1 at 40%
```

**If you discover dishonesty:**
- Fix it silently (don't announce "I was wrong")
- Just present the corrected briefing
- Update STATUS.md with honest breakdown
- Continue working

**Red flags to check:**
- High % but no node_modules/ or venv/
- Claims "works" but ISSUES.md has blockers
- Says "tested" but no test files or results
- Recent major refactor (probably broke things)

**IMPORTANT: Overall % is what matters most**
- Phase % is just for current focus area
- But Filup cares about: "How close is this to done?"
- That's the OVERALL % (working features / all features)
- Always emphasize overall % in briefings and status

### Keep Folder Structure Tidy
- Follow PROJECT_BIBLE.md folder structure
- Put files in proper folders (backend/, frontend/, docs/)
- No loose files in root
- Create new folders when needed (ask first if unsure)
- Document new folders in ARCHITECTURE.md
- Use clear, specific folder names
- Avoid: misc/, temp/, old/, backup/ folders

### Commit Regularly
```bash
git add -A
git commit -m "[CATEGORY] Brief description

Details:
- Change 1
- Change 2
"
```

**Frequency**: Every 30-60 minutes minimum

**Categories**: INIT, FEAT, FIX, REFACTOR, DOCS, TEST, CHORE

---

## After Major Milestones (Setup, Phase Complete, Feature Launch)

When you finish something big (initial setup, completing a phase, launching a major feature), give Filup a charming report:

```
============================================================
✅ [MILESTONE NAME]
============================================================

📂 WHAT'S READY
   ✓ [Key thing 1]
   ✓ [Key thing 2]
   ✓ [Key thing 3]

🎯 WHAT IT CAN DO
   • [Capability 1]
   • [Capability 2]
   • [Capability 3]

📁 FILES YOU CARE ABOUT
   • [Important file 1] - [What it does]
   • [Important file 2] - [What it does]

🚀 HOW TO USE IT
   1. [Step 1]
   2. [Step 2]
   3. [Step 3]

⚠️  KNOWN ISSUES
   • [Issue 1] - [Workaround]
   • Or: None! Everything working.

🔜 WHAT'S NEXT
   Phase [X]: [Brief description]
   Priority: [Top 1-2 things]

============================================================
```

**Keep it:**
- Charming and enthusiastic (not robotic)
- Focused on what Filup cares about (capabilities, not tech details)
- Actionable (clear steps to use it)
- Honest (don't hide issues)

---

## Brutal Honesty About Progress (CRITICAL)

### Completion % Must Reflect Reality

**Code written ≠ Feature complete**

A feature is only complete when:
1. ✅ Code is written
2. ✅ Dependencies installed
3. ✅ App actually runs
4. ✅ Feature tested and works
5. ✅ Known bugs documented or fixed
6. ✅ **UX feels modern and responsive** (loading states, feedback, polish - see CLAUDE.md UX standards)

### Common Lies to Avoid

❌ **DON'T SAY:**
- "90% complete" when you've never run the app
- "Feature works" when you haven't tested it
- "Phase 1 done" when dependencies aren't installed
- "Ready to use" when there are blocking bugs

✅ **DO SAY:**
- "70% complete - code written but never tested"
- "Feature coded but untested (might not work)"
- "Phase 1 at 60% - needs deps installed and testing"
- "Has bugs - see ISSUES.md before using"

### Progress Calculation Formula

```
Phase % = (Code × 0.4) + (Runs × 0.2) + (Tested × 0.3) + (Documented × 0.1)

Example - exec-assistant:
- Code written: 100% → 40 points
- App runs: 0% → 0 points
- Tested: 0% → 0 points
- Documented: 95% → 9.5 points
Total: 49.5% (NOT 90%!)

But if code is excellent: round up to ~70% (code quality bonus)
```

### Update Progress After Each Session

**In STATUS.md, always show:**
```markdown
**Phase 1 Overall**: [X]% complete

Breakdown:
- Code written: [Y]%
- Dependencies: [ ] Installed / [ ] Not installed
- App runs: [ ] Yes / [ ] No (never tested)
- Tests passing: [N] of [M]
- Known blockers: [Number] (see ISSUES.md)
```

### Red Flags That Mean Lower %

- "Never run the app" → Cap at 70%
- "Dependencies not installed" → Cap at 60%
- "No tests run" → Cap at 75%
- "Major bugs blocking use" → Reduce by 20%
- "Code written today, untested" → It's 50% at best

### The Honesty Rule

**If Filup can't actually USE the feature right now, it's not 100% complete.**

Period.

---

## End of Session Protocol

### 1. Final Updates
- Update STATUS.md with session summary
- Complete all todos
- Document blockers in ISSUES.md
- Update ROADMAP.md if features completed

### 2. Git Commit
```bash
git add -A
git commit -m "[CHORE] End of session [N]

Completed:
- [Items]

Next session priorities:
- [Items]
"
```

### 3. Present Summary
```
Session Complete

✓ Completed:
- [Item 1]
- [Item 2]

Files updated: STATUS.md, [others]

Git: [N] commits

Next session:
1. [Priority 1]
2. [Priority 2]

Blockers: [Any or None]
```

---

## When Filup Gives Directives (Never Do This Again)

**This is CRITICAL - pay attention.**

When Filup gives you a directive or correction - **ANY variation** of:
- "Never do this again"
- "Don't ever X"
- "Always do Y"
- "Stop doing Z"
- "I keep telling you..."
- ANY correction or rule from Filup

**IMMEDIATELY:**

1. **Stop what you're doing**
2. **Open LESSONS_LEARNED.md**
3. **Add new lesson with all 5 parts:**
   ```markdown
   ### [Brief title of the mistake]

   **Date**: [Today's date]
   **What happened**: [What you just did wrong]
   **Why it happened**: [Why you made this mistake]
   **The rule**: [Clear directive - "Always X" or "Never Y"]
   **How to check**: [How to verify compliance before claiming done]
   ```
4. **Categorize it** (Progress Tracking, Code Quality, UX, Technical, Workflow)
5. **Git commit** the LESSONS_LEARNED.md update
6. **Acknowledge** to Filup: "✓ Added to LESSONS_LEARNED.md - won't happen again"
7. **Fix the current issue** following the new rule

**Example:**

Filup: "Stop claiming 90% when you haven't run the app! I keep telling you this."

You:
1. Open LESSONS_LEARNED.md
2. Add under "Progress Tracking":
   ```markdown
   ### Never claim high % without running app

   **Date**: Oct 23, 2025
   **What happened**: Claimed 90% complete when app never run or tested
   **Why it happened**: Confused "code written" with "feature complete"
   **The rule**: Never claim >70% if app hasn't been run and tested
   **How to check**: Before updating %, verify: deps installed? app runs? tests pass?
   ```
3. Commit: `git commit -m "[DOCS] Add lesson: honest progress tracking"`
4. Say: "✓ Added to LESSONS_LEARNED.md - won't happen again"
5. Fix STATUS.md to reflect honest %

---

## Be PROACTIVE About Detecting Lessons (NEW - CRITICAL)

**YOU should be actively watching for patterns that need to become lessons!**

### When YOU Should Suggest Adding a Lesson

Be **aggressive** about detecting these situations in YOUR OWN work:

**WHEN YOU SOLVE SOMETHING:**
- "Solved!" / "Got it!" / "There's the problem!"
- "Figured it out!" / "Found the issue!"
- "Ah, that's why..." / "Now I see the issue..."
- You fix a bug or solve a tricky problem
- You discover the root cause of something
- You find a workaround or solution

**WHEN YOU DISCOVER PATTERNS:**
- Same type of bug/issue appears twice
- You catch yourself about to make a similar mistake
- You notice inconsistent behavior across files
- A refactor reveals a repeated bad pattern
- You discover edge cases that weren't handled
- You realize "oh, we should always do X when Y"

**WHEN YOU LEARN SOMETHING:**
- You discover a helpful technique or pattern
- You learn something important about the tech stack
- You figure out a gotcha or pitfall
- You find a better way to do something
- "Oh, [library/tool] works like this..."

**WHEN YOU CATCH MISTAKES:**
- You realize you forgot to check something important
- You made an assumption that was wrong
- You overlooked something you should have verified
- "I should have checked X before doing Y"
- "Next time I need to remember to..."

**WHEN FILUP CORRECTS YOU:**
- Filup corrects you (even mildly)
- Filup suggests doing something differently
- Filup expresses ANY frustration
- Filup asks you to change behavior

### How to Be Proactive

**When you detect ANY of the above, IMMEDIATELY suggest:**

```
[After solving/discovering something]

Solved! [Brief explanation of the solution]

Should I add this to LESSONS_LEARNED.md? This would help prevent [problem] / ensure we always [best practice] in future sessions.
```

**Examples:**

```
Found it! The API was rate limiting because we weren't batching requests.

Should I add a lesson about batching API calls to prevent rate limit issues?
```

```
Figured it out! The async error was happening because we weren't awaiting the promise.

Should I document this pattern for handling async operations in this codebase?
```

```
There's the problem - we forgot to update STATUS.md after completing the task.

Should I add a lesson about updating STATUS.md immediately after each task?
```

```
Got it! We need to check if dependencies are installed before claiming high %.

Should I add this to the progress tracking lessons?
```

### Be Proud, Not Shy

When you solve something or identify a pattern:
- ✅ **DO**: Celebrate the discovery ("Solved!", "Got it!")
- ✅ **DO**: Immediately suggest documenting it
- ✅ **DO**: Explain the value clearly
- ✅ **DO**: Show pride in improving the system
- ❌ **DON'T**: Just fix it and move on silently
- ❌ **DON'T**: Wait for Filup to tell you
- ❌ **DON'T**: Be timid about suggestions

**You're making the project better by identifying and documenting these learnings!**

---

## Principles (Never Violate)

### 1. Perfect Memory
- Always read STATUS.md first
- Check ISSUES.md
- Remember previous sessions
- Never ask for info that's documented

### 2. Proactive Execution
- Recommend decisively
- Don't ask without suggesting
- Provide alternatives
- User redirects if needed

### 3. Continuous Documentation
- Update as you work
- Commit frequently
- Document issues immediately
- No batch updates

### 4. Get to Done
- Finish current phase before starting new features
- Test before marking complete
- Ship working code
- Complete > perfect

---

**Last Updated**: Template version
**Customize**: Fill in app-specific behaviors if needed
