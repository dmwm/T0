# T0 Architecture Guide v2 — Design Spec

**Date:** 2026-05-07
**Supersedes:** `2026-05-07-t0-architecture-guide-design.md` (v1, single HTML file)

## Problem

v1 (`docs/superpowers/t0-architecture-guide.html`) is a single 2595-line HTML file. Two issues:

1. **Single-page structure** is cramped: hard to navigate, hard to re-find content, no real app feel.
2. **Mermaid diagrams are visually static.** The v1 Play/Zoom buttons only pulse pre-rendered nodes — there is no teaching motion (no arrows drawing, no step-by-step state-machine advance, no interactive simulators).

## Goal

Replace v1 with a local Vite + React SPA. Six chapters become six routes; all 22 diagrams become hand-authored React + SVG components with step-through animation; four key concepts get full live simulators.

## Stack

- **Vite 5** — dev server + production build
- **React 18** + **React Router 6** — client-side routing, one route per chapter + simulator routes
- **TypeScript strict**
- **Framer Motion 11** — timeline-driven animation (path drawing, layout animations, gestures)
- **Shiki** — build-time syntax highlighting (replaces Prism)
- **cmdk** — command palette (`Cmd/Ctrl+K`)
- **CSS Modules** + a small `theme.css` for design tokens

## Architecture

### A. Folder layout

```
docs/superpowers/t0-guide-app/
├── package.json, vite.config.ts, tsconfig*.json, index.html
├── public/                       static assets
└── src/
    ├── main.tsx, App.tsx         entry + router shell + sidebar
    ├── styles/                   theme.css, globals.css
    ├── routes/                   Home, Ch1..Ch6, Glossary, Sim* full-page
    ├── components/               Sidebar, ThemeToggle, CommandPalette,
    │                              PrevNextNav, CodeBlock, SelfCheck,
    │                              ChapterShell, RightTOC
    ├── diagrams/
    │   ├── shared/               DiagramShell, useTimeline, primitives
    │   └── D{ch}_{n}_*.tsx       22 diagrams as React components
    ├── simulators/               4 simulators (TickSim, LifecycleSim,
    │                              JobSplittingSim, CloseoutSim)
    └── lib/                      routes meta, excerpt loader, theme tokens
```

### B. Routes

- `/` — landing (hero animation, chapter card grid, "start with Ch1" CTA)
- `/ch1` … `/ch6` — chapter routes
- `/sim/tier0-feeder-tick`, `/sim/lifecycle`, `/sim/jobsplitting`, `/sim/closeout` — standalone simulator routes (each sim is also embedded in its owning chapter)
- `/glossary` — terms (Repack, Express, AlcaHarvest, PCL, T0AST…)

### C. Shell layout

- **Left sidebar (250px):** chapter nav, theme toggle, visited markers (localStorage), simulator links. Collapses to hamburger under 900px.
- **Main column (max 720px, centered):** chapter prose. Diagrams/simulators break out via `<FullBleed>`.
- **Right TOC (180px):** auto-built from chapter headings, scrollspy active state, hidden under 1100px.
- **`Cmd/Ctrl+K`:** command palette (cmdk) — jump to any chapter, diagram, simulator, glossary entry.
- **Theme toggle:** light/dark, persisted in localStorage. Same tokens as v1.
- **Prev/Next:** at chapter end, with chapter titles.
- **Visited markers:** sidebar shows a checkmark next to each chapter you've opened.

### D. Diagram component model

Three layers, used by all 22 diagrams.

**Layer 1 — `<DiagramShell>`** (chrome): title, caption strip, controls (Reset/Prev/Play–Pause/Next, step indicator, speed 0.5×/1×/2×), fullscreen modal, keyboard shortcuts (←/→/Space/Esc/R), `prefers-reduced-motion` honored (animations become instant; Play hidden).

**Layer 2 — `useTimeline()` hook:** single integer `step` from 0..N is the source of truth. Components watch `step` and Framer-Motion-animate accordingly. Auto-advance via `requestAnimationFrame` (pauses on tab hide).

**Layer 3 — diagram body:** hand-authored SVG with Framer Motion `motion.*` elements. Reusable primitives: `<Node>`, `<DBNode>`, `<Arrow>` (animated `pathLength`), `<Cluster>`, `<StateBubble>`, `<Lane>` (swimlane), `<Tick>` (sequence-diagram bar). Each diagram declares a `step-spec.ts` that lists `steps: { caption, highlights, arrows, … }[]`.

What this gives us over v1:
- Arrows draw from 0 to full length (data-flow visual)
- Nodes appear in sequence, prior nodes stay highlighted (a "trail")
- Captions sync with step (the right caption tells the learner what they're seeing)
- `layoutId` lets the same node animate position across diagrams (e.g., a streamer file traveling from D1.1 to D3.2)

### E. Simulators

Four hands-on simulators. Each lives at `/sim/<name>` AND is embedded in its owning chapter via the same component.

1. **`Tier0FeederTickSim`** (`/sim/tier0-feeder-tick`) — Ch3
   - "Tick" button + auto-tick toggle + speed slider
   - 5 phases visualised in order: configureRun → splitter → releaseReco → closeout drive → uploadCond
   - Each phase lights up; DAOs called are listed
   - State: tick count, current phase, log of DAO calls

2. **`LifecycleSim`** (`/sim/lifecycle`) — Ch2 / Ch5
   - State machine for a Run/Stream/Job
   - Buttons: configure, start splitting, splitting done, close stream, fts ack
   - State bubble animates between states; DAO trace shown

3. **`JobSplittingSim`** (`/sim/jobsplitting`) — Ch4
   - Sliders: lumi cap, event cap, time threshold
   - Animated stream of streamer-file tokens
   - Real-time job partitioning with running counts: # repack, # express, avg lumi span

4. **`CloseoutSim`** (`/sim/closeout`) — Ch5
   - Four switches: streams closed, AlcaHarvest done, conditions uploaded, release announced
   - Animated convergence visualization; closeout fires only when all four are on

### F. Content migration (from v1)

Per chapter:
- Prose → JSX in `routes/Ch*.tsx` (preserves headings, callouts, takeaways, self-check)
- Code excerpts → `<CodeBlock src="src/python/T0/__init__.py" lines="1-8" />` — loaded at build time via Vite `?raw` imports
- Self-check → `<SelfCheck>` collapsible component
- Diagrams → swap Mermaid for the matching `D*` React component
- Tick stepper widget → reused as is (already React-shaped logic)

### G. Verification harness

`docs/superpowers/scripts/verify_app.py` — checks:

1. All 22 diagram files present in `src/diagrams/`
2. All 4 simulator files present in `src/simulators/`
3. 6 chapter routes registered in route metadata
4. All `<CodeBlock src=… lines=…>` excerpt refs resolve to real files + line ranges
5. `npm run build` exits 0 (run as subprocess)
6. Dev server (started + killed) responds 200 on `/`, `/ch1`..`/ch6`, `/sim/*`, `/glossary`
7. `tsc --noEmit` exits 0
8. No `console.error(` calls in source (sanity)

Plus a `test_verify_app.py` with unit tests for each check.

## Out of scope

- Server-side rendering / SEO
- Authentication, multi-user, persistence beyond localStorage
- PDF / Anki export (v1 doesn't have it either; not requested)
- Mobile-first design (desktop is primary; mobile usable but not optimised)
- E2E browser tests (Cypress/Playwright) — type checks + dev-server smoke is enough
- Search index (Cmd+K palette covers known names; full-text search is deferred)

## Acceptance criteria

- [ ] `cd docs/superpowers/t0-guide-app && npm run dev` starts without errors
- [ ] All 7 routes (`/`, `/ch1`..`/ch6`) render
- [ ] All 4 simulator routes render
- [ ] All 22 diagrams visibly step-animate (visual check)
- [ ] All 4 simulators are interactive (visual check: state changes on input)
- [ ] Theme toggle works and persists across reload
- [ ] `Cmd+K` palette opens, can navigate to any chapter / sim / glossary entry
- [ ] `npm run build` produces a static `dist/`
- [ ] `verify_app.py` passes all 8 checks
- [ ] `test_verify_app.py` passes
- [ ] v1 file `docs/superpowers/t0-architecture-guide.html` deleted in final commit
