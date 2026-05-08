import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs } from "./shared/primitives";
import { motion } from "framer-motion";

interface Row {
  feature: string;
  repack: string;
  express: string;
  step: number;
}

const ROWS: Row[] = [
  { feature: "Goal", repack: "RAW packing", express: "fast reco", step: 1 },
  { feature: "Lumi cap", repack: "8 lumis", express: "4 lumis", step: 2 },
  { feature: "Event cap", repack: "2M events", express: "800K events", step: 3 },
  { feature: "Size cap", repack: "16 GB", express: "8 GB", step: 4 },
  { feature: "Latency", repack: "minutes", express: "seconds", step: 5 },
  { feature: "Output", repack: "RAW dataset", express: "AOD/AlCa", step: 6 },
  { feature: "Source file", repack: "RepackJobSplitter.py", express: "ExpressJobSplitter.py", step: 7 },
];

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Repack and Express share the same cap-then-cut machinery, but with
        very different defaults. Step through to see them side by side.
      </>
    ),
  },
  {
    caption: <><strong>Goal</strong> — Repack packs streamers into RAW; Express runs a fast reco for monitoring + AlCa.</>,
  },
  {
    caption: <><strong>Lumi cap</strong> — Express is tighter so AlCa skims emerge sooner.</>,
  },
  {
    caption: <><strong>Event cap</strong> — both bound the per-job runtime; Express is tighter for latency.</>,
  },
  {
    caption: <><strong>Size cap</strong> — protects transfer queues; matters most for Express output to AlCa.</>,
  },
  {
    caption: <><strong>Latency</strong> — Repack jobs run in minutes; Express lands seconds after the streamer arrives.</>,
  },
  {
    caption: <><strong>Output</strong> — Repack writes one RAW dataset row; Express writes AOD plus AlCa skims.</>,
  },
  {
    caption: <>The implementations live next to each other in <code>src/python/T0/JobSplitting/</code> — <code>Repack</code>, <code>Express</code>, plus <code>Merge</code> variants for both.</>,
  },
];

export function D4_4_SplitterMatrix() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1000 });

  const colW = [180, 250, 250];
  const x0 = 40;
  const y0 = 30;
  const rowH = 42;

  return (
    <DiagramShell
      tag="D4.4 — Splitter feature matrix"
      title="Repack vs Express — same machinery, different caps"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 760 360"
    >
      <ArrowheadDefs />

      <g>
        <rect x={x0} y={y0} width={colW[0]} height={rowH} fill="var(--code-bg)" stroke="var(--rule)" />
        <rect x={x0 + colW[0]} y={y0} width={colW[1]} height={rowH} fill="var(--accent-soft)" stroke="var(--rule)" />
        <rect x={x0 + colW[0] + colW[1]} y={y0} width={colW[2]} height={rowH} fill="color-mix(in srgb, var(--accent) 4%, var(--bg-elevated))" stroke="var(--rule)" />

        <text x={x0 + 14} y={y0 + 26} fontSize={12} fontWeight={600} fill="var(--muted)" letterSpacing="0.06em">FEATURE</text>
        <text x={x0 + colW[0] + 14} y={y0 + 26} fontSize={13} fontWeight={700} fill="var(--accent)">REPACK</text>
        <text x={x0 + colW[0] + colW[1] + 14} y={y0 + 26} fontSize={13} fontWeight={700} fill="var(--accent)">EXPRESS</text>
      </g>

      {ROWS.map((row, i) => {
        const y = y0 + (i + 1) * rowH;
        const visible = tl.step >= row.step;
        const isActive = tl.step === row.step;
        return (
          <motion.g
            key={row.feature}
            initial={false}
            animate={{ opacity: visible ? 1 : 0.25 }}
            transition={{ duration: 0.3 }}
          >
            <rect
              x={x0}
              y={y}
              width={colW[0] + colW[1] + colW[2]}
              height={rowH}
              fill={isActive ? "var(--accent-soft)" : i % 2 === 0 ? "transparent" : "var(--code-bg)"}
              stroke="var(--rule)"
              strokeWidth={isActive ? 1.5 : 0.6}
            />
            <text x={x0 + 14} y={y + 26} fontSize={12} fontWeight={600} fill="var(--fg)">
              {row.feature}
            </text>
            <text x={x0 + colW[0] + 14} y={y + 26} fontSize={12} fontFamily="SF Mono, Menlo, monospace" fill="var(--fg)">
              {row.repack}
            </text>
            <text x={x0 + colW[0] + colW[1] + 14} y={y + 26} fontSize={12} fontFamily="SF Mono, Menlo, monospace" fill="var(--fg)">
              {row.express}
            </text>
          </motion.g>
        );
      })}
    </DiagramShell>
  );
}
