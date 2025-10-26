# Feature Roadmap

<!--
═══════════════════════════════════════════════════════════════════
HOW TO UPDATE THIS FILE
═══════════════════════════════════════════════════════════════════

WHEN TO UPDATE:
- When feature is completed (check the box)
- When phase % changes
- When priorities shift
- When new features identified
- When timeline estimates change

HOW TO CHECK OFF FEATURES:
1. Change [ ] to [x] when feature is FULLY working end-to-end
2. Update phase % at top: [X% COMPLETE]
3. Update STATUS.md to match
4. Only mark complete when Filup can actually USE it

PHASE % CALCULATION:
Phase % = (Completed features in phase / Total features in phase) × 100

DO NOT mark feature complete if:
- Only backend exists (need frontend too)
- App hasn't been run with this feature
- Feature not tested
- Data connectors exist but no real data synced

HOW TO ADD NEW FEATURES:
1. Determine which phase it belongs to
2. Categorize as: Must Have / Should Have / Nice to Have
3. Add checkbox and description
4. Update phase dependencies if needed

HOW TO REORDER PRIORITIES:
1. Move features between phases if needed
2. Update timeline estimates
3. Document reason in git commit
4. Update dependencies section

FORMATTING RULES:
- Keep features as checkboxes: - [ ] or - [x]
- Indent details under feature with 2 spaces
- Update phase % in square brackets: [45% COMPLETE]
- Use consistent priority labels: CRITICAL/HIGH/MEDIUM/LOW
- Timeline format: Week X or Month X

═══════════════════════════════════════════════════════════════════
-->

All features, priorities, and timeline for this app.

---

## Phase 1: Backend Core [100% COMPLETE] ✓

**Timeline**: Week 1-2 (COMPLETE)
**Goal**: Build screenplay parsing and AI analysis engine

### Must Have
- [x] PDF/Fountain parser (parses screenplay files)
- [x] Scene-by-scene extraction
- [x] Entity tracking (characters, locations, relationships)
- [x] Memory management system (compresses old scenes, keeps key info)
- [x] Question tracking (tracks narrative questions raised/answered)
- [x] AI reviewer personas (multiple personality types)
- [x] Emotional state tracking
- [x] Feedback generation engine
- [x] Horror Brain personas (Jordan Peele, James Gunn, Sam Raimi, etc.)

### Should Have
- [x] Test suite (~5K lines backend code)
- [x] Bad Hombres screenplay for testing

**Priority**: CRITICAL
**Dependencies**: None
**Success Criteria**: Backend can analyze full screenplay with AI feedback ✓

---

## Phase 2: GUI Frontend [0% COMPLETE]

**Timeline**: Week 3
**Goal**: Build clean, modern web interface for screenplay analysis

### Must Have
- [ ] React + Vite + TypeScript setup
- [ ] shadcn/ui component library installed
- [ ] Lucide icons installed
- [ ] Upload screenplay interface
- [ ] Select reviewer personas
- [ ] Display scene-by-scene feedback
- [ ] Show emotional tracking graphs
- [ ] Character analysis view
- [ ] Question tracking view

### Should Have
- [ ] Dark mode
- [ ] Progress indicators during analysis
- [ ] Export feedback to PDF/Markdown
- [ ] Save/load analysis sessions

### Nice to Have
- [ ] Side-by-side screenplay + feedback view
- [ ] Highlight key moments visually
- [ ] Compare feedback from multiple reviewers

**Priority**: CRITICAL
**Dependencies**: Phase 1 complete ✓
**Success Criteria**: Can upload screenplay, see full AI analysis in polished GUI

---

## Phase 3: API Layer [0% COMPLETE]

**Timeline**: Week 3-4
**Goal**: Connect frontend to backend with FastAPI

### Must Have
- [ ] FastAPI setup
- [ ] POST /analyze endpoint (upload screenplay)
- [ ] GET /analysis/{id} endpoint (retrieve results)
- [ ] WebSocket for real-time progress
- [ ] File upload handling
- [ ] Error handling

### Should Have
- [ ] Authentication (simple token-based)
- [ ] Rate limiting
- [ ] Caching analyzed screenplays

**Priority**: HIGH
**Dependencies**: Phase 2 in progress
**Success Criteria**: Frontend can communicate with backend, full analysis flow works

---

## Phase 4: Polish & Deploy [0% COMPLETE]

**Timeline**: Week 5
**Goal**: Production-ready app

### Must Have
- [ ] End-to-end testing with multiple screenplays
- [ ] Error handling for bad inputs
- [ ] Loading states for long operations
- [ ] Success/error notifications
- [ ] Documentation for users

### Should Have
- [ ] Docker containerization
- [ ] Environment config (dev/prod)
- [ ] Logging system
- [ ] Performance optimization

### Nice to Have
- [ ] Deploy to cloud (Render, Railway, etc.)
- [ ] Custom Horror Brain training
- [ ] Batch analysis (multiple screenplays)

**Priority**: MEDIUM
**Dependencies**: Phase 3 complete
**Success Criteria**: Filup can use it to analyze any screenplay, end-to-end

---

## Priority Matrix

| Feature | User Value | Effort | Priority |
|---------|-----------|--------|----------|
| GUI Frontend | Critical | Medium | P0 |
| API Layer | Critical | Low | P0 |
| Upload/Display Flow | Critical | Low | P0 |
| Export feedback | High | Low | P1 |
| Dark mode | Medium | Low | P2 |
| Cloud deployment | Medium | High | P2 |

**P0** = This week (critical)
**P1** = This month (important)
**P2** = Next month (nice to have)
**P3** = Future/Maybe

---

## Non-Goals

Features explicitly NOT building:

### ❌ Screenplay editing
**Why**: Focus is analysis/feedback, not writing tool

### ❌ Collaboration features
**Why**: MVP is single-user, can add later

### ❌ Mobile apps
**Why**: Web-first, responsive design covers mobile

---

## Success Metrics

### Phase 1 Success ✓
- [x] Parse full screenplay (Bad Hombres)
- [x] Generate AI feedback scene-by-scene
- [x] Track emotions, characters, questions

### Phase 2 Success
- [ ] Upload screenplay via GUI
- [ ] See analysis results beautifully displayed
- [ ] Export feedback

### Ultimate Success
Filup can upload ANY screenplay, get insightful scene-by-scene AI feedback from multiple Horror Brain personas, review emotional tracking/character arcs/narrative questions - all in a polished, fast, reliable GUI.

---

## Decision Framework

When prioritizing, ask:
1. Did user explicitly request this?
2. Does it solve the core problem?
3. Is it blocking other work?
4. Is it a nice-to-have?

---

**Last Updated**: Oct 24, 2025
**Next Review**: After Phase 2 complete
