# T0 Guide App v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace v1 single-HTML guide with a Vite + React + Framer Motion local SPA — 6 chapter routes, all 22 diagrams as step-through React+SVG components, 4 hands-on simulators.

**Architecture:** Vite dev server, React Router for routing, Framer Motion for animation, Shiki for syntax highlighting. New directory `docs/superpowers/t0-guide-app/`. v1 HTML kept as fallback until acceptance, then deleted.

**Tech Stack:** Vite 5 · React 18 · React Router 6 · TypeScript strict · Framer Motion 11 · Shiki · cmdk · CSS Modules

---

## Task 0 — Scaffold Vite project

**Files:**
- Create: `docs/superpowers/t0-guide-app/package.json`
- Create: `docs/superpowers/t0-guide-app/vite.config.ts`
- Create: `docs/superpowers/t0-guide-app/tsconfig.json`, `tsconfig.node.json`
- Create: `docs/superpowers/t0-guide-app/index.html`
- Create: `docs/superpowers/t0-guide-app/.gitignore`
- Create: `docs/superpowers/t0-guide-app/src/main.tsx`, `src/App.tsx`
- Create: `docs/superpowers/t0-guide-app/src/styles/theme.css`, `src/styles/globals.css`

- [ ] Step 1: Write all scaffold files
- [ ] Step 2: `cd docs/superpowers/t0-guide-app && npm install`
- [ ] Step 3: `npm run dev` — verify it serves on `http://localhost:5173`
- [ ] Step 4: Commit `feat(t0-guide): scaffold Vite + React + TS project`

## Task 1 — Shell & routing

**Files:**
- `src/lib/routes.ts` — route metadata (path, title, prevPath, nextPath)
- `src/components/Sidebar.tsx`, `Sidebar.module.css`
- `src/components/ThemeToggle.tsx`, `ThemeToggle.module.css`
- `src/components/CommandPalette.tsx` (cmdk)
- `src/components/PrevNextNav.tsx`
- `src/components/ChapterShell.tsx` — wraps chapter content with right TOC + Prev/Next
- `src/components/RightTOC.tsx` — auto-builds TOC from headings, scrollspy
- `src/App.tsx` — wires React Router with sidebar + outlets

- [ ] All 6 chapter routes render placeholder content with sidebar visible
- [ ] Theme toggle works, persists in localStorage
- [ ] Cmd+K palette lists chapters and navigates
- [ ] Visited markers persist
- [ ] Commit `feat(t0-guide): shell — sidebar, theming, routing, command palette`

## Task 2 — Diagram framework

**Files:**
- `src/diagrams/shared/useTimeline.ts`
- `src/diagrams/shared/DiagramShell.tsx`, `DiagramShell.module.css`
- `src/diagrams/shared/primitives.tsx` — Node, DBNode, Arrow, Cluster, StateBubble, Lane, Tick
- `src/diagrams/shared/motion-presets.ts`

- [ ] `useTimeline` exposes `{step, totalSteps, isPlaying, play, pause, next, prev, reset}`
- [ ] DiagramShell renders controls + caption + fullscreen + keyboard nav + reduced-motion support
- [ ] Primitives accept `active`/`dim`/`highlighted` props that drive Framer Motion animations
- [ ] Commit `feat(t0-guide): diagram framework — shell, timeline, primitives`

## Task 3 — Example diagram (proof of concept)

**Files:**
- `src/diagrams/D1_1_PipelineHero.tsx`

- [ ] One full step-through diagram showing the pipeline (Storage Manager → Tier0Feeder → Repack/Express → PromptReco → AlcaHarvest → Archive)
- [ ] 7 steps, each draws an arrow + lights up next node + updates caption
- [ ] Embedded on landing page `/` and on Chapter 1
- [ ] Visual smoke check via dev server
- [ ] Commit `feat(t0-guide): pipeline hero diagram`

## Task 4 — Example simulator (proof of concept)

**Files:**
- `src/simulators/CloseoutSim.tsx`

- [ ] Four toggles, animated convergence ring, fires only when all four are on
- [ ] Embedded at `/sim/closeout` and inside Ch5
- [ ] Commit `feat(t0-guide): closeout simulator`

## Task 5 — Remaining 21 diagrams

Build in 4 batches by chapter:
- Batch A: D1.x (3) + D2.x (4)
- Batch B: D3.x (4) + D4.x (4)
- Batch C: D5.x (4)
- Batch D: D6.x (3)

For each diagram: hand-authored SVG, declarative `step-spec`, embedded in correct chapter route.

- [ ] Batch A committed
- [ ] Batch B committed
- [ ] Batch C committed
- [ ] Batch D committed

## Task 6 — Remaining 3 simulators

- [ ] `Tier0FeederTickSim` — 5 phases, tick button + auto-tick + speed slider, DAO log
- [ ] `LifecycleSim` — Run/Stream/Job state machine, buttons, DAO trace
- [ ] `JobSplittingSim` — sliders, animated tokens, running counts

Commit each separately.

## Task 7 — Content port (Chapters 1–6)

For each chapter route:
- [ ] Prose ported from v1 HTML
- [ ] All chapter diagrams referenced
- [ ] Code excerpts loaded via `<CodeBlock src= lines=>`
- [ ] Self-check questions in `<SelfCheck>` component
- [ ] Owning simulator embedded in correct chapter

Commit per chapter.

## Task 8 — Glossary + landing polish

- [ ] `/glossary` route with terms grouped (architecture, processing, deployment)
- [ ] Landing page hero animation + chapter card grid + CTA
- [ ] All chapter card thumbnails are mini-versions of the chapter's hero diagram
- [ ] Commit `feat(t0-guide): glossary + landing polish`

## Task 9 — Verification harness

**Files:**
- `docs/superpowers/scripts/verify_app.py`
- `docs/superpowers/scripts/test_verify_app.py`

- [ ] All 8 checks implemented (see spec §G)
- [ ] All 8 unit tests pass
- [ ] `verify_app.py` exits 0
- [ ] Commit `feat(t0-guide): verification harness`

## Task 10 — Final acceptance + cleanup

- [ ] `npm run build` succeeds, produces `dist/`
- [ ] All routes load on dev server
- [ ] All diagrams animate
- [ ] All simulators interactive
- [ ] Theme toggle persists
- [ ] Delete `docs/superpowers/t0-architecture-guide.html`
- [ ] Delete `docs/superpowers/scripts/verify_guide.py` and `test_verify_guide.py`
- [ ] Update CLAUDE.md notes if needed
- [ ] Commit `chore(t0-guide): retire v1, accept v2`
