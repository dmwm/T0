export interface RouteEntry {
  path: string;
  title: string;
  shortTitle: string;
  group: "guide" | "chapter" | "simulator" | "reference";
  hint?: string;
  prevPath?: string;
  nextPath?: string;
}

export const CHAPTERS: RouteEntry[] = [
  {
    path: "/ch1",
    title: "Chapter 1 — The pipeline at a glance",
    shortTitle: "1. Pipeline overview",
    group: "chapter",
    hint: "Storage Manager → Repack → Express → PromptReco → AlcaHarvest → Archive",
  },
  {
    path: "/ch2",
    title: "Chapter 2 — RunConfig and the Tier0Config DSL",
    shortTitle: "2. RunConfig",
    group: "chapter",
    hint: "How operator-edited configs become T0AST rows",
  },
  {
    path: "/ch3",
    title: "Chapter 3 — The Tier0Feeder heartbeat",
    shortTitle: "3. Tier0Feeder",
    group: "chapter",
    hint: "What happens on each tick of the feeder loop",
  },
  {
    path: "/ch4",
    title: "Chapter 4 — JobSplitting",
    shortTitle: "4. JobSplitting",
    group: "chapter",
    hint: "Repack and Express splitter algorithms",
  },
  {
    path: "/ch5",
    title: "Chapter 5 — Closeout and condition uploads",
    shortTitle: "5. Closeout",
    group: "chapter",
    hint: "Convergence of streams, AlcaHarvest, conditions, releases",
  },
  {
    path: "/ch6",
    title: "Chapter 6 — Operator surface and recap",
    shortTitle: "6. Operator surface",
    group: "chapter",
    hint: "bin/t0, replay-by-PR, multi-agent split",
  },
];

export const SIMULATORS: RouteEntry[] = [
  {
    path: "/sim/tier0-feeder-tick",
    title: "Simulator — Tier0Feeder tick",
    shortTitle: "Tier0Feeder tick",
    group: "simulator",
    hint: "Watch the heartbeat fire all 5 phases in order",
  },
  {
    path: "/sim/lifecycle",
    title: "Simulator — Run/Stream/Job lifecycle",
    shortTitle: "Lifecycle state machine",
    group: "simulator",
    hint: "Step a run through each state; see DAOs fire",
  },
  {
    path: "/sim/jobsplitting",
    title: "Simulator — JobSplitting",
    shortTitle: "JobSplitting",
    group: "simulator",
    hint: "Tweak caps and watch streamers cut into jobs",
  },
  {
    path: "/sim/closeout",
    title: "Simulator — Closeout convergence",
    shortTitle: "Closeout convergence",
    group: "simulator",
    hint: "Toggle four signals; see when closeout fires",
  },
];

export const REFERENCE: RouteEntry[] = [
  {
    path: "/glossary",
    title: "Glossary",
    shortTitle: "Glossary",
    group: "reference",
    hint: "Repack, Express, AlcaHarvest, PCL, T0AST…",
  },
];

export const HOME: RouteEntry = {
  path: "/",
  title: "T0 Architecture Guide",
  shortTitle: "Home",
  group: "guide",
};

export const ALL_ROUTES: RouteEntry[] = [
  HOME,
  ...CHAPTERS,
  ...SIMULATORS,
  ...REFERENCE,
];

const linkedChapters: RouteEntry[] = CHAPTERS.map((ch, i) => ({
  ...ch,
  prevPath: i === 0 ? "/" : CHAPTERS[i - 1].path,
  nextPath: i === CHAPTERS.length - 1 ? undefined : CHAPTERS[i + 1].path,
}));

export const CHAPTERS_LINKED = linkedChapters;

export function findRoute(path: string): RouteEntry | undefined {
  return ALL_ROUTES.find((r) => r.path === path);
}

export function findChapter(path: string): RouteEntry | undefined {
  return CHAPTERS_LINKED.find((c) => c.path === path);
}
