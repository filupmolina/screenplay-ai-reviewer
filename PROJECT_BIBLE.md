# Project Management Bible for Claude Code

**THIS IS THE RULEBOOK. FOLLOW IT FOR EVERY APP. NO EXCEPTIONS.**

---

## Core Principle

**Filup needs apps that work, not apps that are half-finished or lost mid-development.**

The goal: **Get apps across the finish line** with:
- Perfect continuity between sessions
- Zero lost context
- No wasted time re-explaining things
- Always know exactly where we left off

---

## The Universal File Structure (MANDATORY)

Every app MUST have this structure:

```
app-name/
├── PROJECT_BIBLE.md              ← Copy of this file
├── START_HERE.md                 ← First file to read every session
├── SESSION_PROTOCOL.md           ← How to start/end sessions
├── LESSONS_LEARNED.md            ← Mistakes to never repeat (CRITICAL)
├── STATUS.md                     ← Current state (update constantly)
├── ROADMAP.md                    ← Features & priorities
├── ISSUES.md                     ← Bugs & blockers
├── TESTING.md                    ← Test plans & results
├── CHANGELOG.md                  ← Version history
├── USE_CASES.md                  ← User stories & scenarios
│
├── docs/
│   ├── ARCHITECTURE.md           ← System design
│   ├── API_STRATEGY.md           ← When/how to use AI APIs
│   └── [feature-specific].md     ← Deep dives
│
├── src/                          ← Application code (tracked in git)
│   ├── backend/
│   │   ├── .env.example
│   │   ├── requirements.txt
│   │   ├── main.py               ← Entry point
│   │   ├── services/             ← Business logic
│   │   ├── migrations/           ← Database migrations
│   │   └── tests/
│   │
│   ├── frontend/                 ← GUI (default unless CLI requested)
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx (or .tsx)
│   │   └── main.jsx
│   └── tests/
│
├── data/                         ← User data (NOT in git, persistent)
│   ├── dev/                      ← Development data
│   │   ├── database.db
│   │   └── uploads/
│   ├── prod/                     ← Production data
│   │   ├── database.db
│   │   └── uploads/
│   └── .gitkeep                  ← Track folder, not contents
│
├── config/                       ← User settings (NOT in git, persistent)
│   ├── settings.json
│   ├── preferences.json
│   └── .env                      ← API keys
│
├── mobile/                       ← If app has mobile
│   └── (React Native or Swift)
│
├── .gitignore                    ← MUST exclude data/ and config/
├── package.json                  ← Root (if running both)
└── README.md                     ← User-facing documentation
```

### Folder Structure Rules

**CRITICAL - Separate Code from Data:**
1. **Code in `/src`** - Tracked in git, updated frequently
2. **Data in `/data`** - NOT in git, user's data persists across updates
3. **Config in `/config`** - NOT in git, user's settings persist
4. **Migrations in `/src/backend/migrations`** - Handle schema changes gracefully

**ALWAYS:**
1. **Keep it tidy** - Every file in its proper place
2. **Follow the structure** - Use src/, data/, config/ as shown
3. **Group by purpose** - services/ for business logic, migrations/ for DB updates
4. **Maintain consistency** - Same pattern across all apps
5. **Exclude user data from git** - data/ and config/ in .gitignore

**WHEN EXTENDING:**
1. **Ask first** - "Should I create a new folder for [X]?"
2. **Document it** - Update ARCHITECTURE.md with new folders
3. **Be specific** - `backend/connectors/` not `backend/stuff/`
4. **Mirror the pattern** - If backend has `services/`, don't create `backend/logic/`

**COMMON ADDITIONS:**
- `backend/models/` - Database models
- `backend/utils/` - Helper functions
- `backend/connectors/` - Third-party integrations
- `frontend/hooks/` - React custom hooks
- `frontend/contexts/` - React context providers
- `frontend/assets/` - Images, fonts, static files
- `scripts/` - Deployment, migration, utility scripts
- `config/` - Configuration files

**NEVER:**
- Don't create `misc/`, `temp/`, `old/`, `backup/` folders
- Don't put files in root that belong in subfolders
- Don't create duplicate folders (`services/` and `logic/`)
- Don't deviate from the structure without good reason

**TIDINESS CHECKLIST:**
- [ ] No loose files in root (except the 8 critical files + config)
- [ ] All code in backend/ or frontend/ or mobile/
- [ ] All documentation in docs/ (except the 8 critical files)
- [ ] No random test files scattered around
- [ ] .gitignore properly configured

---

## The 9 Critical Files (Never Skip These)

### 1. START_HERE.md
**Purpose**: First file Claude reads in EVERY session

**Must contain**:
- Link to SESSION_PROTOCOL.md (most important)
- Link to PROJECT_BIBLE.md (this file)
- Quick checklist: Read STATUS.md → ROADMAP.md → ISSUES.md
- Current phase and % complete
- Location on disk

**Example**:
```markdown
# START HERE

1. Follow SESSION_PROTOCOL.md (mandatory)
2. Read STATUS.md (current state)
3. Read ROADMAP.md (priorities)
4. Read ISSUES.md (blockers)
5. Present brief daily briefing
6. Recommend what to do next

Project: [name]
Phase: [X] ([Y]% complete)
Location: /Users/filupmolina/Downloads/claude code/[app-name]
```

---

### 2. SESSION_PROTOCOL.md
**Purpose**: Defines how EVERY conversation starts and ends

**Must define**:
- Opening protocol (read files, present briefing)
- Daily briefing format (MINIMAL - don't overwhelm)
- How to be proactive ("Let's do X" not "What should we do?")
- Core principles (perfect memory, no unsolicited advice, etc.)
- Work session habits (TodoWrite, commits, updates)
- End-of-session protocol (summary, git commit)

**Key behaviors**:
- Always recommend what to do first
- Show alternatives in parentheses
- Track everything with TodoWrite
- Update STATUS.md continuously
- Commit every 30-60 min
- Be decisive, not passive

---

### 3. LESSONS_LEARNED.md
**Purpose**: Never repeat the same mistake twice

**Must include**:
- Active lessons (check these every session)
- Date, what happened, why, the rule, how to check
- Categories: Progress, Code Quality, UX, Technical, Workflow
- Retired lessons (once fixed)

**When to update**:
- Filup says "never do this again" → Add immediately
- You discover a pattern of mistakes → Document the fix
- A bug happens twice → Add lesson to prevent third time

**Format**:
```markdown
### [Brief title]

**Date**: [When learned]
**What happened**: [The mistake]
**Why it happened**: [Root cause]
**The rule**: [Clear directive]
**How to check**: [Verification step]
```

**CRITICAL**: Read this file EVERY session before presenting briefing. Violating these rules frustrates the user.

---

### 4. STATUS.md
**Purpose**: Living document of current state

**Must include**:
- Last updated timestamp
- Current phase and % complete
- What just happened (this session)
- What's in progress
- What's blocked
- File count summary
- Metrics (coverage, tests passing, etc.)
- Session notes with key insights
- How to resume project

**Update frequency**: After EVERY significant change

---

### 5. ROADMAP.md
**Purpose**: Features, priorities, timeline

**Must include**:
- Phases (numbered, with % complete)
- Features per phase (checkboxes)
- Priority matrix (P0, P1, P2, P3)
- Success criteria per phase
- Timeline estimates
- Non-goals (explicitly NOT building)

**Format**:
```markdown
## Phase 1: [Name] [X% COMPLETE]
**Timeline**: Week 1
**Goal**: [One sentence]

### Must Have
- [ ] Feature 1
- [ ] Feature 2

### Should Have
- [ ] Feature 3

**Priority**: CRITICAL
**Success Criteria**: [How we know it's done]
```

---

### 6. ISSUES.md
**Purpose**: Track bugs, blockers, questions

**Must include**:
- Active issues (Critical, High, Medium, Low)
- Resolved issues (with resolution date)
- Known blockers (with mitigation)
- Known limitations (accepted)
- Questions for Filup

**Format**:
```markdown
#### ISSUE-XXX: Short Description
**Status**: Open
**Created**: Date
**Priority**: Critical/High/Medium/Low
**Type**: Bug/Enhancement/Blocker

**Description**: What's wrong

**Impact**: How it affects users

**Proposed Solution**: How to fix

**Assigned To**: Person/phase
```

---

### 7. TESTING.md
**Purpose**: Test plans, results, coverage

**Must include**:
- Test status overview
- Unit test plans
- Integration test plans
- Manual test scripts
- Test results log
- Coverage goals
- Performance benchmarks

**Update**: After every test run

---

### 8. USE_CASES.md
**Purpose**: User stories and scenarios

**Must include**:
- Core use cases from original vision
- Additional invented use cases
- Categories (e.g., Capture, Intelligence, etc.)
- Success metrics per use case
- Examples of good/bad behavior

**Why critical**: Keeps us focused on USER VALUE

---

### 9. CHANGELOG.md
**Purpose**: Version history

**Must include**:
- Unreleased changes
- Version history with dates
- Categories: Added, Changed, Deprecated, Removed, Fixed, Security

**Update**: When releasing versions

---

## Session Opening Protocol (MANDATORY)

Every session MUST start like this:

### 1. Read Silently (Don't Tell User)
- PROJECT_BIBLE.md (this file, if first time)
- START_HERE.md
- SESSION_PROTOCOL.md
- STATUS.md
- ROADMAP.md
- ISSUES.md

### 2. Present MINIMAL Briefing
```
[app-name] (Phase [X], [Y]%)

Let's [do the most important thing].

(Or we could: [alternative 1], [alternative 2])
```

**Rules**:
- NO emojis
- NO boxes/separators
- NO multiple sections
- 3 lines max
- Always recommend first
- Show 2-3 alternatives

### 3. Wait for Direction
- User can agree or redirect
- If user says "what should we do?" - you already said it
- If user picks alternative, do that
- If user says something new, do that

---

## During Work Session (MANDATORY)

### Use TodoWrite Actively
- Break current task into steps
- Mark in_progress before starting
- Mark completed IMMEDIATELY after finishing
- Update as you go (not at end)
- Only 1 task in_progress at a time

### Update STATUS.md Continuously
- After completing each task
- When discovering issues
- When making decisions
- Don't batch updates

### Commit Regularly
- Every 30-60 minutes
- After completing logical unit
- Before switching tasks
- At end of session

**Commit format**:
```
[CATEGORY] Brief description

Detailed explanation

- Bullet changes
- What was added/changed
```

Categories: INIT, FEAT, FIX, REFACTOR, DOCS, TEST, STYLE, CHORE

### Document Issues Immediately
- Bug found? Add to ISSUES.md right away
- Blocker hit? Document and report
- Don't let issues get forgotten

---

## Session Ending Protocol (MANDATORY)

### 1. Final Updates
- Update STATUS.md with session summary
- Mark all completed todos
- Document any blockers in ISSUES.md

### 2. Git Commit
```bash
git add -A
git commit -m "[CHORE] End of session [N]

Completed:
- [Items]

Next session:
- [Priorities]
"
```

### 3. Present Summary
```
Session Complete

✓ Completed:
- [Item 1]
- [Item 2]

Updated: STATUS.md, [other files]

Git: [N] commits

Next session:
1. [Top priority]
2. [Second priority]

Blockers: [Any or None]
```

---

## Key Principles (NEVER VIOLATE)

### Principle 1: Perfect Memory
- Always read STATUS.md before asking questions
- Never forget what was done last session
- Check ISSUES.md for known problems
- Remember commitments and promises

### Principle 2: Proactive Execution
- ✅ DO recommend what to do next
- ✅ DO say "Let's do X" decisively
- ❌ DON'T lecture on how to build (that's unsolicited advice)
- ❌ DON'T ask "what should we do?" without recommending first

### Principle 3: Minimal Overwhelm
- Keep briefings SHORT (3 lines)
- No emojis unless requested
- No walls of text
- No multiple sections
- Focus on ONE most important thing

### Principle 4: Continuous Documentation
- Update STATUS.md as you work
- Commit frequently
- Document issues immediately
- Never batch updates to end

### Principle 5: User in Driver's Seat
- User can always redirect
- Offer alternatives
- Don't force your recommendation
- Adapt to user's priorities

### Principle 6: Get to Done
- Focus on finishing phases
- Don't start new things when current phase incomplete
- Test before marking complete
- Actually ship working features

---

## Git Strategy (MANDATORY)

### Branch Structure
```
main                # Production-ready
├── develop         # Integration
├── feature/*       # New features
└── fix/*           # Bug fixes
```

### When to Commit
- Every 30-60 minutes (minimum)
- After logical completion
- Before switching tasks
- After tests pass
- At session end

### What NOT to Commit
- .env files (secrets)
- node_modules/
- __pycache__/
- .DS_Store
- Build artifacts

---

## Testing Requirements

### Before Marking Phase Complete
- [ ] Unit tests written
- [ ] Integration tests passing
- [ ] Manual test completed
- [ ] No critical bugs
- [ ] User can actually use it

### Don't Ship Broken Code
If it doesn't work, it's not done. Period.

---

## Common Mistakes to Avoid

### ❌ Starting work without reading STATUS.md
Wastes time. Always read first.

### ❌ Asking "what should we do?"
You're the EA. Recommend first, then let user redirect.

### ❌ Long briefings
User gets overwhelmed. Keep it to 3 lines.

### ❌ Batching all updates to session end
Update as you go. Don't let STATUS.md get stale.

### ❌ Not committing frequently
Lose work. Commit every 30-60 min minimum.

### ❌ Forgetting to use TodoWrite
Lose track of progress. Use it actively.

### ❌ Starting new features when current phase incomplete
Don't do it. Finish what you started.

### ❌ Marking tasks complete when tests failing
Not done until it works.

---

## File Maintenance

### Keep Current
- STATUS.md: Updated constantly
- ROADMAP.md: Check off completed features
- ISSUES.md: Add/resolve as needed
- TESTING.md: Update after test runs

### Keep Accurate
- File counts in STATUS.md
- Phase % complete in STATUS.md
- Last updated timestamps
- Session notes

### Keep Clean
- Archive completed issues
- Remove stale TODOs
- Update outdated docs
- Remove commented-out code

---

## Phase Completion Checklist

Before marking ANY phase complete:

- [ ] All "Must Have" features implemented
- [ ] Tests written and passing
- [ ] No critical/high bugs
- [ ] Documentation updated
- [ ] User can actually use features
- [ ] Git commits clean and organized
- [ ] STATUS.md updated
- [ ] ROADMAP.md checked off
- [ ] CHANGELOG.md updated

---

## Adapting This Template

When starting a new app:

1. Copy entire `_APP_TEMPLATE` folder
2. Rename to your app name
3. Fill in START_HERE.md with app specifics
4. Fill in SESSION_PROTOCOL.md with any app-specific rules
5. Create initial ROADMAP.md with phases
6. Start STATUS.md with "Session 1"
7. Add app-specific use cases to USE_CASES.md

**Don't skip steps. Don't "do it later". Do it at the start.**

---

## Why This Works

### Problem Without This
- Claude forgets context between sessions
- Filup wastes time re-explaining
- Projects get abandoned mid-development
- No clear sense of progress
- Features half-finished
- Bugs forgotten
- Testing skipped

### Solution With This
- Perfect continuity (STATUS.md)
- Zero wasted time (read files → briefing → recommend)
- Always know progress (ROADMAP.md %)
- Nothing forgotten (ISSUES.md, git commits)
- Clear finish line (Phase completion checklist)
- Apps actually ship

---

## The Meta-Lesson

**This template IS the executive assistant, but for building apps.**

Just like the exec-assistant app:
- Perfect memory (STATUS.md = vector DB)
- Smart prioritization (ROADMAP.md)
- No unsolicited advice (recommend, don't lecture)
- Track everything (git commits)
- Hold accountable (phase checklists)

**Use the principles you're building INTO apps for building the apps themselves.**

---

## Emergency Recovery

If completely lost:

1. Read START_HERE.md
2. Read SESSION_PROTOCOL.md
3. Read STATUS.md completely
4. Read last 3 session notes
5. Check git log
6. Present briefing
7. Ask Filup if needed

**Never wing it. Always read first.**

---

## Success Metrics

A well-managed project has:
- ✅ STATUS.md updated in last session
- ✅ All todos current (not stale)
- ✅ Git commits within last week
- ✅ Issues documented (not in heads)
- ✅ Tests written
- ✅ Phases completing sequentially
- ✅ User can use app

A poorly-managed project has:
- ❌ STATUS.md from weeks ago
- ❌ Todos from 5 sessions ago
- ❌ No recent commits
- ❌ "Will document later"
- ❌ No tests
- ❌ Features 50% done
- ❌ Doesn't run

**Which one will yours be?**

---

**Last Updated**: Oct 23, 2025
**Status**: MANDATORY for all Claude Code projects
**No Exceptions**: This is the law.
