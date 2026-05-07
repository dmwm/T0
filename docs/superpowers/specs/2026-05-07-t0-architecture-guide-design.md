# T0 Architecture Guide — Design Spec

**Date:** 2026-05-07
**Status:** Approved (brainstorming complete)
**Author:** Pair-designed with Claude Code

## Goal

Produce a single self-contained interactive HTML file, **`t0-architecture-guide.html`**, that explains the CMS Tier-0 (T0) system end-to-end — both architecture and code — to a senior engineer who is **brand new to T0**. The artifact is sized for ~6 days of reading at ~5 hours/day (~30 hours total content).

## Audience and assumptions

The reader is assumed to have:
- Strong general software-engineering background (Python, SQL, polling/agent patterns, distributed-system vocabulary).
- **No** prior knowledge of CMS, HEP physics computing, WMCore, WMAgent, or T0 itself.
- No interest in hands-on practice during this read. The artifact is for *deep passive understanding*, not skill drilling.

Every CMS- or WMCore-specific term is introduced before being used. Every code excerpt is annotated.

## Out of scope (explicit)

- No PDF version.
- No Anki deck or other spaced-repetition artifact.
- No multi-page static site — exactly one HTML file (CDN dependencies are fine).
- No exercises, hands-on labs, SSH walkthroughs, or query-the-DB tasks.
- No video or audio narration.
- No coverage of: WMCore internals beyond what T0 directly consumes, the CMSSW (offline reconstruction software) build/runtime, the Storage Manager / online DAQ side, dropbox/Frontier conditions infrastructure beyond ConditionUpload's interface to it.

## Deliverable shape

A single file checked into the repo (likely under `docs/superpowers/` or a sibling location to be decided in implementation): one HTML document with all CSS inline (or in a single `<style>`), Mermaid diagrams rendered client-side via CDN, and code excerpts highlighted via a CDN syntax-highlighter (Prism.js or highlight.js). The file must work fully offline once its CDN assets cache (i.e., it is a *static* artifact — no build step required by the reader).

### Visual / UX requirements

- **Sticky TOC sidebar** with 1- and 2-level nav, current-section highlighting on scroll.
- **Dark-mode-friendly** palette (single theme is acceptable; toggle is optional).
- **Collapsible "deeper dive" blocks** via `<details>`/`<summary>` for advanced/optional content per chapter.
- **Reading time** estimate at the top of each chapter.
- **No JavaScript framework** — vanilla JS only. Acceptable libraries: Mermaid (CDN), Prism.js or highlight.js (CDN), nothing else.
- Internal anchor links between chapters (e.g., chapter 4 references "see Chapter 2's `addRepackConfig` walk-through").
- Source-code excerpts must show the file path and starting line number, e.g., `src/python/T0/RunConfig/RunConfigAPI.py:120-145`.

## Chapter structure

Six chapters, mapped to ~5 hours of reading each:

### Chapter 1 — Foundations

What it covers:
- One-page CMS context: the LHC → detector → DAQ → Storage Manager → Tier-0 pipeline, in plain English. Defines streamer file, run, lumi-section, stream, dataset, primary dataset.
- WMAgent / `WMCore.Agent.Harness` primer: what an agent is, what `BaseWorkerThread` does, the `DAOFactory(package=…, classname=…)` pattern.
- T0 repo map: `src/python/T0/` (libraries) vs `src/python/T0Component/` (agent components), the Oracle DAO tree, where `etc/` and `bin/` fit.
- The chain in one picture: Storage Manager → Repack → Express → PromptReco → AlcaHarvest → ConditionUpload, with the database stops along the way.

Diagrams:
- D1.1 The CMS data flow at 30,000 ft.
- D1.2 WMAgent component anatomy (Harness → BaseWorkerThread → DAOFactory).
- D1.3 The T0 database topology (T0AST + HLTConfDB + StorageManagerDB + optional SMNotifyDB / PopConLogDB / T0DataSvcDB).

Sources:
- `CLAUDE.md`
- `src/python/T0/__init__.py`
- `src/python/T0Component/Tier0Feeder/Tier0Feeder.py`
- `src/python/T0Component/Tier0Feeder/Tier0FeederPoller.py:1-120` (just the constructor for the DB topology view)

### Chapter 2 — The Tier0Config DSL

What it covers:
- The Tier0Config object hierarchy (Sites / Global / Streams / Datasets) — using the canonical docstring at the top of `T0/RunConfig/Tier0Config.py` as the spec.
- Walk-through of a real `etc/ReplayOfflineConfiguration.py` line by line. Each setter linked to its definition in `Tier0Config.py`.
- How `RunConfigAPI.configureRun` and `configureRunStream` translate the in-memory Tier0Config object into rows in T0AST. The DSL → schema mapping.
- A mental model for which T0AST tables back which DSL concepts.

Diagrams:
- D2.1 Tier0Config object tree (rendered from the docstring).
- D2.2 Setter → T0AST table mapping for the most common settings (`addDataset`, `addRepackConfig`, `addExpressConfig`, `setInjectRuns`).
- D2.3 `configureRun` sequence diagram.

Sources:
- `src/python/T0/RunConfig/Tier0Config.py` (esp. lines 1–270 for the docstring, plus key setters: `addDataset`, `addRepackConfig`, `addExpressConfig`, `setHelperAgentStreams`)
- `src/python/T0/RunConfig/RunConfigAPI.py:configureRun`, `configureRunStream`
- `etc/ReplayOfflineConfiguration.py`
- A representative subset of DAOs in `src/python/T0/WMBS/Oracle/RunConfig/` (esp. `InsertRun.py`, `InsertStream.py`, `InsertRepackConfig.py`, `InsertDatasetScenario.py`)

### Chapter 3 — The Tier0Feeder heartbeat

What it covers:
- The polling component lifecycle: how `Tier0Feeder(Harness)` registers `Tier0FeederPoller` with the worker-thread manager, how `algorithm()` is invoked every `pollInterval` seconds.
- A guided read of `Tier0FeederPoller.algorithm` from top to bottom — what each block does, in order, with named DAOs.
- The DAO layer convention: `T0/WMBS/Oracle/<area>/<Verb><Noun>.py`. How a DAO maps to one parameterised SQL statement.
- The Main / Helper agent split: how `tier0Config.Global.HelperAgentStreams` plus `config.Tier0Feeder.agentName` decides which `BaseAgent` subclass instantiates, and how `filterStreamerFiles` / `filterHltConfigStreams` keep the two agents from stepping on each other.

Diagrams:
- D3.1 `Tier0FeederPoller.algorithm` per-tick flowchart (the canonical "what one tick does").
- D3.2 DAO call graph for one tick.
- D3.3 Main/Helper agent stream routing.

Sources:
- `src/python/T0Component/Tier0Feeder/Tier0FeederPoller.py` (full file)
- `src/python/T0Component/Tier0Feeder/MultipleAgents/{BaseAgent.py,MainAgent.py,HelperAgent.py}`
- `src/python/T0/WMBS/Oracle/Tier0Feeder/` (FindNewRuns, FindNewRunStreams, FeedStreamers, MarkWorkflowsInjected — pick ~5 representative DAOs)
- `src/python/T0/WMBS/Oracle/Create.py` (schema bootstrap, brief mention)

### Chapter 4 — JobSplitting

What it covers:
- The WMCore `SplitterFactory` plugin pattern: how `SplitterFactory(package="T0.JobSplitting")` discovers the T0 splitters at runtime.
- Repack vs RepackMerge: the size/lumi/file thresholds that decide when to split a fileset, and what RepackMerge does after.
- Express vs ExpressMerge: latency-driven splitting; why Express usually does not merge.
- The simpler splitters: `Condition.py`, `AlcaHarvest.py`.
- WMBS job state machine (subscription → fileset → jobgroup → job → completed) at the level needed to understand splitter outputs.

Diagrams:
- D4.1 Repack splitter decision tree (when to split, when to wait, when to merge).
- D4.2 Express splitter decision tree (latency-driven).
- D4.3 WMBS job state machine.

Sources:
- `src/python/T0/JobSplitting/{Repack.py,RepackMerge.py,Express.py,ExpressMerge.py,Condition.py,AlcaHarvest.py}`
- `src/python/T0/WMBS/Oracle/JobSplitting/{InsertSplitLumis.py,InsertPromptCalibrationFile.py}`
- A pointer to `WMCore.JobSplitting.SplitterFactory` (external reference, no quoted code)

### Chapter 5 — Closeout

What it covers:
- PromptReco release: how `RunConfigAPI.releasePromptReco` waits for a CMSSW release announcement (via `PopConLogDatabase`) and then converts deferred PromptReco configs into live workflows.
- AlcaHarvest splitter and the time-trigger fallback (`AlcaHarvestTimeout`).
- ConditionUpload: how the dropbox upload works, validation mode vs prompt-reco mode, the difference between local-file-staging and HTTP submission to the conditions dropbox.
- RunLumi closeout: when a run is considered "done" — every stream's fileset closed, conditions uploaded, AlcaHarvest finished. The state model for "active vs closed-out vs archived".

Diagrams:
- D5.1 Run closeout state machine.
- D5.2 ConditionUpload sequence diagram (Tier0Feeder → ConditionUploadAPI → dropbox).
- D5.3 Where in the chain each closeout signal originates.

Sources:
- `src/python/T0/RunConfig/RunConfigAPI.py:releasePromptReco`
- `src/python/T0/JobSplitting/AlcaHarvest.py`
- `src/python/T0/RunLumiCloseout/RunLumiCloseoutAPI.py`
- `src/python/T0/ConditionUpload/{ConditionUploadAPI.py,upload.py}`
- Relevant DAOs in `src/python/T0/WMBS/Oracle/{RunLumiCloseout,ConditionUpload,Tier0Feeder}/`

### Chapter 6 — Operator surface and reference

What it covers:
- The `bin/00_pypi_*.sh` scripts that live on `/data/tier0/` on the deploy hosts, what each does, and the `bin/pypi_update.sh` mechanism that syncs them from `master`.
- The `bin/t0` operator CLI.
- The replay-by-PR-comment workflow (`.github/workflows/deployReplayPR.yaml`): triggers, authorization, node whitelist, what each step does.
- The CI workflow trio (`validate-config.yaml`, `create_tag_and_release.yaml`, `pypi_build_publish_template.yaml`).
- A one-page recap mind-map summarising every preceding chapter — the "everything in one picture" capstone.

Diagrams:
- D6.1 Deploy script call graph (how `00_pypi_deploy_replay.sh` orchestrates the others).
- D6.2 The replay-by-comment workflow flow.
- D6.3 Recap mind-map: every concept covered in chapters 1–5, in one diagram, with cross-links.

Sources:
- `bin/00_pypi_deploy_replay.sh`, `00_pypi_deploy_prod.sh`, `00_pypi_start_agent.sh`, `00_pypi_stop_agent.sh`, `00_pypi_patches.sh`, `pypi_update.sh`, `bin/t0`
- `.github/workflows/deployReplayPR.yaml`, `validate-config.yaml`, `create_tag_and_release.yaml`, `pypi_build_publish_template.yaml`
- The completed chapters 1–5

## Per-chapter content shape (standardised)

Every chapter is structured the same way, top to bottom:

1. **Header** — chapter number, title, estimated reading time, a one-sentence "what you'll know by the end".
2. **Setup prose** (~200–400 words) — the framing. Why this layer exists. What problem it solves. What you're about to read.
3. **Architecture diagram(s)** — Mermaid-rendered. Each diagram is followed by a 100–200 word caption that *narrates* the diagram (don't make the reader figure it out).
4. **Annotated code walk-throughs** — real excerpts from the repo with `file:line` headers, line-prefix annotations or post-block bullet annotations explaining what each block does.
5. **Deeper-dive `<details>` blocks** — optional advanced material (e.g., the obscure `extraStreamDatasetMap` DSL setting, or the SMNotifyDB optional path) tucked into collapsibles so the main flow stays linear.
6. **Key takeaways** — 3–6 bullets summarising the chapter's load-bearing ideas.
7. **Self-check questions** — 3–5 open-ended questions the reader should be able to answer. *No answer key.* The point is to surface gaps, not to grade.

## Diagrams summary

15 diagrams total across the 6 chapters (D1.1–D1.3, D2.1–D2.3, D3.1–D3.3, D4.1–D4.3, D5.1–D5.3, D6.1–D6.3). All Mermaid (flowcharts, sequence, state, mind-map). No raster images; everything renders client-side.

## Acceptance criteria

The artifact is "done" when:

1. The HTML file opens cleanly in Chrome/Safari/Firefox with no console errors.
2. All 15 diagrams render.
3. All 6 chapters are present, each with the standard 7-section shape.
4. Every code excerpt has a correct `file:line` header that matches the current state of the repo.
5. The TOC sidebar correctly anchors to every section.
6. A reader who completes all 6 chapters can answer a "what does Tier0Feeder do in one tick?" question (Chapter 3 self-check) and a "when does run N archive?" question (Chapter 5 self-check) without re-opening the source.
7. The file is committed to the repo at `docs/superpowers/t0-architecture-guide.html`. The existing `doc/` directory is reserved for Sphinx output and is not used.

## Risks and how the design mitigates them

- **Architecture-first risk** (knowledge stays shallow because not tied to a concrete instance) — mitigated by anchoring every chapter with real code excerpts and by Chapter 6's recap mind-map that forces synthesis.
- **WMCore-knowledge gap** — mitigated by the Chapter 1 primer; further WMCore specifics introduced just-in-time as they appear in T0 code.
- **Drift from real code** — addressed by the acceptance criterion that all `file:line` references match the current repo. The implementation plan will pin a specific commit SHA so the guide describes a known state.
- **Over-scope** — the explicit out-of-scope list keeps the artifact from sprawling into WMCore internals or CMSSW physics. If scope creeps during implementation, cut to keep the 6-day reading budget realistic.

## Next step

Hand this spec to the `superpowers:writing-plans` skill to produce an implementation plan that walks through how to actually generate `t0-architecture-guide.html` (chapter-by-chapter source-gathering, diagram drafting, HTML scaffolding, polish, verification).
