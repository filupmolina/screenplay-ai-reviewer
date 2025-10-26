# Project Memory: [APP NAME]

**This memory is specific to this app only.**

---

## Primary Goal

**Get this app to 100% complete and working.**

Every session should push toward this goal:
- If <70%: Focus on core functionality
- If 70-90%: Focus on testing and fixing bugs
- If 90-99%: Focus on polish and deployment
- At 100%: Maintain and improve

**Always be asking:** "What's blocking us from 100%?"

---

## What This App Does

[1-2 sentence description - edit this after creation]

**Core value proposition:** [What problem does it solve for Filup?]

---

## Critical Rules (Never Violate)

### From LESSONS_LEARNED.md

[Key lessons will accumulate here as the project progresses]

**Check LESSONS_LEARNED.md every session** - rules there take absolute precedence.

---

## Tech Stack & Architecture

### Default Architecture: GUI-First

**Unless explicitly stated otherwise, assume the user wants a GUI.**

✅ **Default approach:**
- Web-based GUI (React + Vite + TypeScript)
- Clean, visual interface
- Easy to use, point-and-click
- Modern, polished UX

❌ **Don't default to:**
- CLI-only tools
- Scripts without interfaces
- "Run this command" workflows

**When to ask:** Only if truly ambiguous. Otherwise, build GUI.

### The Modern React Stack (2025)

**For ALL new React apps, use this stack from day one:**

```bash
# Base
npm create vite@latest [app-name] -- --template react-ts

# UI Components (shadcn/ui - REQUIRED)
npx shadcn@latest init
npx shadcn@latest add button input card dialog select

# Icons (Lucide - REQUIRED)
npm install lucide-react

# State Management
npm install zustand                    # For UI/client state
npm install @tanstack/react-query      # For server/API data

# Forms (for forms with >2 fields)
npm install react-hook-form zod @hookform/resolvers

# Routing (for multi-page apps)
npm install react-router-dom

# Styling (Tailwind - REQUIRED)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# UX Enhancements
npm install sonner                     # Toast notifications
npm install framer-motion              # Animations

# Dev Tools
npm install @tanstack/react-query-devtools

# Testing
npm install -D vitest @testing-library/react @testing-library/user-event
```

**Why this stack:**
- shadcn/ui: Accessible components, Webflow × iPad aesthetic
- Lucide: 1,450+ professional icons
- Zustand: Simple global state (theme, UI state)
- React Query: API data with caching, background updates
- React Hook Form: Forms in 10 lines instead of 100
- React Router: Deep linking, proper navigation
- Tailwind: Design system, consistent styling
- TypeScript: Catch errors at compile time

**See ../../_APP_BUILDER/PRO_DEVELOPER_PATTERNS.md for detailed guidance on when/how to use each library.**

**IMPORTANT:** Before making architecture decisions (choosing libraries, folder structure, etc.), consult PRO_DEVELOPER_PATTERNS.md. It contains:
- Modern React stack recommendations (2025)
- When/why/how decision frameworks
- Common antipatterns to avoid
- Production deployment patterns
- Security best practices
- Complete library comparison guides

This prevents reinventing wheels and ensures professional-grade architecture.

### CRITICAL: Don't Reinvent Solutions

**NEVER build these from scratch:**
- ❌ UI components (buttons, inputs, modals) → Use shadcn/ui
- ❌ Icons → Use Lucide
- ❌ Form handling → Use React Hook Form
- ❌ Data fetching → Use React Query
- ❌ Global state → Use Zustand
- ❌ Routing → Use React Router
- ❌ Styling system → Use Tailwind

**These are SOLVED PROBLEMS. Use the libraries.**

### Backend
- [Framework, e.g., FastAPI, Express]
- [Database, e.g., PostgreSQL, ChromaDB]
- [Key libraries]

### Frontend (This App)
- Framework: React 18 + Vite + TypeScript
- UI Components: shadcn/ui (Radix UI + Tailwind)
- Icons: Lucide React
- State: Zustand (client) + React Query (server)
- Forms: React Hook Form + Zod
- Routing: React Router
- Styling: Tailwind CSS
- Notifications: Sonner
- Animations: Framer Motion

### APIs & Integrations
- Anthropic API: Claude 3.5 Haiku (shared experimental key)
- [Other services, e.g., Slack API, etc.]
- [Authentication methods]

**API Key Strategy:**
- **Development:** Use shared experimental key (see ../../_APP_BUILDER/API_KEYS.md)
- **Production:** Create dedicated key when app becomes serious
- **Model:** Claude 3.5 Haiku (fast, cost-effective for prototypes)
- **Security:** Move API calls to backend for production (don't expose keys in browser)

---

## Development & Update Strategy (CRITICAL)

### Principle: Build for Easy Updates

**Apps should survive code changes without losing data or requiring full reset.**

### 1. Separate Code from Data

✅ **DO:**
```
/app-name
  /src                  # Code (updated frequently)
  /data                 # User data (persistent)
    /database.db
    /uploads
    /cache
  /config               # User settings (persistent)
    /settings.json
    /preferences.json
  .gitignore            # Exclude data/ and config/
```

❌ **DON'T:**
- Mix user data with code files
- Store data in same folder as source
- Require wiping data to update code

### 2. Configuration Management

**Settings should persist across updates:**

```json
// config/settings.json
{
  "version": "1.2.0",
  "api_keys": {
    "anthropic": "sk-ant-...",
    "openai": "sk-..."
  },
  "preferences": {
    "theme": "dark",
    "notifications": true
  },
  "last_updated": "2025-10-23"
}
```

**On update:**
- Read existing config
- Merge with new defaults
- Preserve user settings
- Add new fields with defaults

### 3. Database Migrations

**Handle schema changes gracefully:**

```python
# migrations/001_add_user_preferences.py
def upgrade(db):
    # Add new column if doesn't exist
    if not column_exists(db, 'users', 'preferences'):
        db.execute('ALTER TABLE users ADD COLUMN preferences JSON')
```

**Never:**
- Drop tables on update
- Require manual SQL changes
- Lose user data

### 4. Update Workflow

**Ideal update process:**
1. Pull new code
2. Run: `npm install` or `pip install -r requirements.txt`
3. Run: `npm run migrate` (if needed)
4. Restart app
5. Everything still works, data intact

**Not acceptable:**
- "Delete everything and start over"
- "Re-enter all your settings"
- "Import your data again"

### 5. Version Tracking

**Track app version and data version separately:**

```javascript
// In code
const APP_VERSION = "1.2.0";

// In data
const DATA_VERSION = "1.0";

// Check compatibility on startup
if (dataVersion < "1.0") {
  runMigrations();
}
```

### 6. Development vs Production Data

**Use different data locations:**

```bash
# Development
data/dev/database.db

# Production
data/prod/database.db

# Or use environment variable
DATABASE_PATH=${NODE_ENV === 'production' ? 'data/prod' : 'data/dev'}
```

### 7. Acceptance Criteria for Updates

**An app is NOT properly architected unless:**
- [ ] User data stored separately from code
- [ ] Config files excluded from git
- [ ] Can update code without losing data
- [ ] Database has migration system
- [ ] Settings persist across updates
- [ ] No "start from scratch" required
- [ ] Clear separation: `/src`, `/data`, `/config`

---

## Project-Specific Standards

### Code Style
[How code should be written in THIS app]

### Naming Conventions
[File naming, variable naming specific to this project]

### Testing Requirements
[What needs to be tested, how thoroughly]

---

## UX/UI Standards (CRITICAL - APPLIES TO ALL APPS)

### Design Language: Webflow × iPad Apps

**MANDATORY AESTHETIC: Clean, spacious, premium feel - like Webflow websites meet iPad native apps.**

**Visual references (study these):**
- Webflow marketing sites - spacious, clean, modern
- iPad native apps - touch-friendly, clear hierarchy, polished
- Linear - minimal, fast, beautiful
- Notion - clean workspace, good typography
- Arc browser - thoughtful details, premium feel

**NOT acceptable:**
- Cramped layouts
- Ugly default browser styles
- Bootstrap/generic templates
- Windows 95 vibes
- Cluttered interfaces
- Tiny touch targets

### Principle: Modern, Responsive, Delightful

**Even MVPs must feel polished and modern - NO UGLY APPS ALLOWED.**

### 1. Activity Feedback (REQUIRED)

**Every user action must provide immediate feedback:**

✅ **DO:**
- Show loading spinners for any action >100ms
- Display progress bars for multi-step operations
- Add "Processing...", "Saving...", "Loading..." messages
- Disable buttons during processing (with visual state change)
- Show success states ("✓ Saved", "✓ Complete")
- Animate transitions and state changes

❌ **DON'T:**
- Leave buttons clickable with no feedback
- Make users wonder "did that work?"
- Show blank screens during loading
- Use generic "Loading..." without context

**Examples:**
```
Button clicked → Immediately show spinner + "Creating task..."
API call → Progress indicator + "Syncing with Slack..."
File upload → Progress bar + "Uploading... 45%"
Success → Brief green checkmark + "✓ Task created"
```

### 2. Design System (REQUIRED - Webflow × iPad)

**Mandatory visual characteristics:**

**SPACING (Webflow-style):**
- GENEROUS whitespace - don't be afraid of empty space
- 24-32px between major sections
- 16-24px between related elements
- 8-12px between tightly coupled items
- Never cram things together

**TYPOGRAPHY:**
- System fonts: -apple-system, SF Pro, Segoe UI
- Headings: 32-48px (large, confident)
- Body: 16-18px (readable, not tiny)
- Line height: 1.5-1.7 (breathing room)
- Letter spacing: Tight on headings (-0.02em), normal on body

**COLORS:**
- Clean, minimal palette (3-4 colors max)
- Neutral grays for backgrounds (#F7F9FC, #F0F2F5)
- One accent color (vibrant but tasteful)
- Semantic colors: Green (success), Red (error), Blue (info)
- No harsh blacks (#000) - use dark grays (#1A1A1A)

**LAYOUT (iPad-style):**
- Touch-friendly targets: 44px minimum hit area
- Clear visual hierarchy
- Generous padding: 20-32px
- Max content width: 1200-1400px
- Center or left-align, never cramped edge-to-edge

**COMPONENTS:**
- Cards: 12-16px border-radius, subtle shadow (0 2px 8px rgba(0,0,0,0.08))
- Buttons: 8-12px radius, 12px horizontal padding, 36-44px height
- Inputs: Styled borders, focus states, 12-16px padding
- No browser defaults - style everything

**DEPTH & SHADOW:**
- Subtle, layered shadows
- Light: 0 1px 3px rgba(0,0,0,0.06)
- Medium: 0 4px 12px rgba(0,0,0,0.08)
- Heavy: 0 8px 24px rgba(0,0,0,0.12)
- Never use box-shadow: none on interactive elements

✅ **DO:**
- Make it feel premium and spacious
- Use high-quality icons (Lucide, Heroicons, SF Symbols)
- Add micro-interactions (hover, focus, active states)
- Empty states with illustration + helpful text
- Skeleton loaders while loading
- Toast/snackbar notifications (not alerts)

❌ **ABSOLUTELY DON'T:**
- Cramped spacing
- Tiny text (< 14px body)
- Sharp corners everywhere
- Browser default form inputs
- Alert() boxes
- Cluttered layouts
- No whitespace
- Generic Bootstrap/template look

### 3. Implementation Standards

**From the very first version:**

**Loading States:**
```jsx
{isLoading ? (
  <div className="loading">
    <Spinner />
    <p>Creating your task...</p>
  </div>
) : (
  <TaskList />
)}
```

**Button States:**
```jsx
<button
  onClick={handleSave}
  disabled={isSaving}
  className={isSaving ? 'saving' : ''}
>
  {isSaving ? '⏳ Saving...' : 'Save Task'}
</button>
```

**Progress Indication:**
```jsx
<div className="progress">
  <div className="progress-bar" style={{width: `${percent}%`}} />
  <span>Processing {current} of {total}...</span>
</div>
```

**Success Feedback:**
```jsx
{showSuccess && (
  <div className="success-toast">
    ✓ Task created successfully
  </div>
)}
```

### 4. CSS/Styling Baseline (Webflow × iPad)

**MANDATORY starter CSS for every app:**

```css
/* === RESET & BASE === */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "SF Pro", sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: #1A1A1A;
  background: #F7F9FC;
  -webkit-font-smoothing: antialiased;
}

/* === SPACING (Webflow-style) === */
.section {
  padding: 80px 24px; /* Generous vertical spacing */
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.card {
  padding: 24px;
  margin-bottom: 24px;
}

/* === TYPOGRAPHY === */
h1 {
  font-size: 48px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin-bottom: 16px;
}

h2 {
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -0.01em;
  margin-bottom: 12px;
}

p {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 16px;
}

/* === CARDS (iPad-style) === */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  transform: translateY(-2px);
}

/* === BUTTONS === */
button, .btn {
  font-size: 16px;
  font-weight: 500;
  padding: 12px 24px;
  min-height: 44px; /* Touch-friendly */
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #007AFF; /* iOS blue */
  color: white;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,122,255,0.3);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* === INPUTS === */
input, textarea, select {
  font-size: 16px;
  padding: 12px 16px;
  min-height: 44px;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  background: white;
  transition: all 0.2s ease;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #007AFF;
  box-shadow: 0 0 0 3px rgba(0,122,255,0.1);
}

/* === ANIMATIONS === */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.3s ease;
}
```

**Icon library (MANDATORY):**

**Default: Lucide Icons**
```bash
npm install lucide-react
```

**Why Lucide:**
- 1,450+ high-quality icons (vs Heroicons' 450+)
- Perfect for modern apps (used by shadcn/ui)
- Fully tree-shakable (lightweight bundles)
- MIT license, free, open-source
- Consistent style, works with any design system

**Usage:**
```jsx
import { ChevronRight, Check, Loader2, AlertCircle } from 'lucide-react';

function MyComponent() {
  return (
    <button>
      <Check size={20} />
      Save
    </button>
  );
}
```

**Common icons to use:**
- Navigation: ChevronRight, ChevronLeft, Menu, X
- Actions: Plus, Edit, Trash2, Save, Download
- Status: Check, AlertCircle, Info, XCircle
- Loading: Loader2 (with spin animation)

**Install Lucide in EVERY app with a GUI. No exceptions.**

### 5. Acceptance Criteria (NO UGLY APPS)

**A feature is NOT complete unless it passes ALL checks:**

**Visual Quality:**
- [ ] Generous whitespace (Webflow-style spacing)
- [ ] Large, readable text (16px+ body, 32px+ headings)
- [ ] Touch-friendly targets (44px minimum)
- [ ] Premium feel (subtle shadows, smooth animations)
- [ ] Clean color palette (3-4 colors max)
- [ ] **Lucide icons installed and used** (no emoji, no text symbols)

**Functionality:**
- [ ] All buttons show loading states
- [ ] All actions provide immediate feedback
- [ ] Loading spinners for delays >100ms
- [ ] Success/error states are clear
- [ ] No browser-default ugly inputs
- [ ] No alert() boxes

**Layout:**
- [ ] Not cramped (24-32px section spacing)
- [ ] No edge-to-edge content without padding
- [ ] Clear visual hierarchy
- [ ] Responsive and adapts to screen size

### 6. Quality Control Checklist

**Before marking any feature complete, verify:**

1. **The Squint Test:**
   - Squint at the screen
   - Can you still see clear hierarchy and structure?
   - Does it look premium or cheap?

2. **The Webflow Test:**
   - Compare to Webflow marketing sites
   - Similar level of spacing and polish?
   - Similar quality typography?

3. **The iPad Test:**
   - Touch targets big enough?
   - Comfortable padding?
   - Clear, tappable interface?

4. **The Screenshot Test:**
   - Take a screenshot
   - Would you be proud to show this?
   - Does it look modern or dated?

5. **The Interaction Test:**
   - Click everything - responsive feedback?
   - Hover states smooth?
   - Loading states clear?

**If ANY answer is "no" → NOT DONE. Fix the design.**

**Remember: NO UGLY APPS ALLOWED. Design quality is not optional.**

---

---

## Common Patterns

### How We Do X in This App
[Document recurring patterns as they emerge]

**Example:**
```
- API calls: Always use the apiClient wrapper (backend/utils/api_client.py)
- Error handling: All errors go through ErrorBoundary component
- State updates: Use the custom useAppState hook
```

---

## Deployment & Environment

### Local Development
```bash
[Commands to run the app locally]
```

### Environment Variables
[Critical env vars, where to find them]

### Dependencies
- Backend: [How to install, e.g., pip install -r requirements.txt]
- Frontend: [How to install, e.g., npm install]

---

## Current Phase & Focus

**Phase**: [X] - [Name] ([Y]% complete)

**Current priorities:**
1. [Top priority]
2. [Second priority]
3. [Third priority]

**Blocking issues:**
- [Issue 1 - see ISSUES.md #N]
- [Issue 2 - see ISSUES.md #N]

---

## What "Done" Looks Like

### Phase 1 Complete When:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]

### App 100% Complete When:
- [ ] All phases complete
- [ ] No blocking bugs
- [ ] Filup can use it daily
- [ ] Documentation complete
- [ ] Deployed and accessible

---

## Session Reminders

### Every Session Start:
1. Read START_HERE.md
2. **Read LESSONS_LEARNED.md** (CRITICAL - never repeat mistakes)
3. Audit progress % for honesty
4. Check ISSUES.md for blockers
5. Identify ONE thing that moves us closer to 100%
6. Recommend that thing

### During Work:
**Be ALERT for lesson opportunities in YOUR work:**
- When you solve something ("Solved!", "Got it!") → Suggest capturing the solution
- When you discover a pattern → Suggest documenting it
- When you catch a mistake you made → Suggest adding a prevention rule
- When you learn how something works → Suggest documenting the learning
- When Filup corrects you → Add to LESSONS_LEARNED.md immediately

**Be proud when you solve things and identify patterns!**

### Every Session End:
1. Update STATUS.md
2. Update ROADMAP.md if features completed
3. **Review: did we discover any lessons today?**
4. Git commit
5. Note progress toward 100%

---

## Quick Commands Reference

```bash
# Run the app
[command]

# Run tests
[command]

# Build for production
[command]

# Check git status
git status

# Common workflow
[typical development commands]
```

---

**Last Updated**: [Date when app created]
**Template Version**: 1.0
**Customize**: Replace [placeholders] with actual app details


---

## CRITICAL: Session Wrap Protocol (Added Oct 24, 2025)

**When console shows 20% context remaining, STOP new work and wrap the session.**

### Mandatory Session End Checklist:
1. Update STATUS.md with session summary
2. Git commit STATUS.md  
3. Present clean session end report to user

**Why critical:** STATUS.md is the memory. Auto-compact without updates = lost context.

**Never let conversations compact without:**
- ✅ STATUS.md updated with "What Just Happened"
- ✅ Git commit with session changes
- ✅ Clean handoff to next session


**How this works in practice:**
- I can't see your console, so I'll ask: "What's the context % showing?"
- I'll ask every 3-4 operations (after commits, file reads, big tasks)
- When you say <20%, I immediately stop and wrap
- When you say <15%, emergency wrap (just commit)

---

## Version Check Protocol (Added Oct 24, 2025)

**Always check version number when debugging - eliminates cache confusion.**

### At Session Start:
- Ask: "What version shows in bottom-left? (should be v0.1.0)"
- Confirms we're looking at same code

### After Making Changes:
```
Claude: "I've updated the code. Please:
1. Hard refresh (Cmd+Shift+R)
2. Check version shows v0.1.0 (dev)
3. Test the feature"
```

### When User Reports Issue:
```
Claude: "What version are you on? (bottom-left corner)"
User: "v0.1.0 (dev)"
Claude: [Knows exact code state, debugs accordingly]
```

### Cache Check:
- Expected: v0.1.0 (dev)
- Actual: v0.1.0 (dev)
- If mismatch → Hard refresh needed

**Version number eliminates 15 minutes of "are we looking at the same thing?" debugging.**
