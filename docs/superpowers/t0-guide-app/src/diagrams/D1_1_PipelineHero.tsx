import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import {
  ArrowheadDefs,
  Arrow,
  Node,
  type NodeState,
} from "./shared/primitives";

interface NodeSpec {
  id: string;
  x: number;
  y: number;
  label: string;
  sublabel?: string;
  variant?: "default" | "external" | "process" | "db";
}

const NODES: NodeSpec[] = [
  { id: "sm", x: 30, y: 110, label: "Storage Manager", sublabel: "online DB", variant: "external" },
  { id: "feeder", x: 220, y: 110, label: "Tier0Feeder", sublabel: "agent" },
  { id: "repack", x: 410, y: 50, label: "Repack", sublabel: "RAW packing" },
  { id: "express", x: 410, y: 170, label: "Express", sublabel: "fast reco" },
  { id: "reco", x: 600, y: 50, label: "PromptReco", sublabel: "AOD/MINIAOD" },
  { id: "alca", x: 600, y: 170, label: "AlcaHarvest", sublabel: "PCL inputs" },
  { id: "cond", x: 790, y: 170, label: "Cond. Upload", sublabel: "→ Frontier", variant: "external" },
  { id: "archive", x: 790, y: 50, label: "Archive", sublabel: "CASTOR/EOS", variant: "external" },
];

interface ArrowSpec {
  id: string;
  from: string;
  to: string;
  d: string;
  step: number;
  label?: string;
  labelPos?: { x: number; y: number };
}

function nodeRight(n: NodeSpec) {
  return { x: n.x + 132, y: n.y + 28 };
}
function nodeLeft(n: NodeSpec) {
  return { x: n.x, y: n.y + 28 };
}

const N = Object.fromEntries(NODES.map((n) => [n.id, n]));

const ARROWS: ArrowSpec[] = [
  {
    id: "sm-feeder",
    from: "sm",
    to: "feeder",
    d: `M ${nodeRight(N.sm).x} ${nodeRight(N.sm).y} L ${nodeLeft(N.feeder).x - 4} ${nodeLeft(N.feeder).y}`,
    step: 1,
    label: "polls each tick",
    labelPos: { x: 176, y: 130 },
  },
  {
    id: "feeder-repack",
    from: "feeder",
    to: "repack",
    d: `M ${nodeRight(N.feeder).x} ${nodeRight(N.feeder).y - 4} C 392 138, 392 78, ${nodeLeft(N.repack).x - 4} ${nodeLeft(N.repack).y}`,
    step: 2,
    label: "Repack splits",
    labelPos: { x: 318, y: 92 },
  },
  {
    id: "feeder-express",
    from: "feeder",
    to: "express",
    d: `M ${nodeRight(N.feeder).x} ${nodeRight(N.feeder).y + 4} C 392 158, 392 198, ${nodeLeft(N.express).x - 4} ${nodeLeft(N.express).y}`,
    step: 3,
    label: "Express splits",
    labelPos: { x: 318, y: 188 },
  },
  {
    id: "repack-reco",
    from: "repack",
    to: "reco",
    d: `M ${nodeRight(N.repack).x} ${nodeRight(N.repack).y} L ${nodeLeft(N.reco).x - 4} ${nodeLeft(N.reco).y}`,
    step: 4,
    label: "after release announce",
    labelPos: { x: 558, y: 70 },
  },
  {
    id: "express-alca",
    from: "express",
    to: "alca",
    d: `M ${nodeRight(N.express).x} ${nodeRight(N.express).y} L ${nodeLeft(N.alca).x - 4} ${nodeLeft(N.alca).y}`,
    step: 5,
    label: "harvest histograms",
    labelPos: { x: 558, y: 190 },
  },
  {
    id: "reco-archive",
    from: "reco",
    to: "archive",
    d: `M ${nodeRight(N.reco).x} ${nodeRight(N.reco).y} L ${nodeLeft(N.archive).x - 4} ${nodeLeft(N.archive).y}`,
    step: 6,
    label: "archive",
    labelPos: { x: 748, y: 70 },
  },
  {
    id: "alca-cond",
    from: "alca",
    to: "cond",
    d: `M ${nodeRight(N.alca).x} ${nodeRight(N.alca).y} L ${nodeLeft(N.cond).x - 4} ${nodeLeft(N.cond).y}`,
    step: 6,
    label: "PCL upload",
    labelPos: { x: 748, y: 190 },
  },
];

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Data taking is in progress. Streamer files (~16 MB blobs of HLT-accepted
        events) accumulate in the <strong>Storage Manager</strong> database at
        Point 5.
      </>
    ),
  },
  {
    caption: (
      <>
        Each heartbeat, <code>Tier0Feeder</code> polls the Storage Manager for
        new streamer files using <code>FindNewRunStreamers</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        For physics streams, <strong>Repack</strong> jobs pack the streamers
        into RAW datasets. Driven by <code>SplitterFactory</code> with the
        Repack plugin.
      </>
    ),
  },
  {
    caption: (
      <>
        In parallel, <strong>Express</strong> runs a fast reconstruction —
        crucial for prompt monitoring and the AlCa stream.
      </>
    ),
  },
  {
    caption: (
      <>
        Once a CMSSW release for the run is announced,{" "}
        <strong>PromptReco</strong> workflows release and produce AOD /
        MINIAOD from the RAW datasets.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>AlcaHarvest</strong> aggregates calibration histograms from
        Express and PromptReco runs into condition payloads.
      </>
    ),
  },
  {
    caption: (
      <>
        Final outputs: archived RAW/AOD/MINIAOD on CASTOR/EOS, and PCL
        conditions uploaded via <code>ConditionUploadAPI</code> to Frontier.
      </>
    ),
  },
];

export function D1_1_PipelineHero() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1500 });

  function nodeState(activeAtStep: number): NodeState {
    if (tl.step > activeAtStep) return "visited";
    if (tl.step === activeAtStep) return "active";
    return "hidden";
  }

  // Each node becomes active on its primary step
  const nodeActiveStep: Record<string, number> = {
    sm: 0,
    feeder: 1,
    repack: 2,
    express: 3,
    reco: 4,
    alca: 5,
    cond: 6,
    archive: 6,
  };

  return (
    <DiagramShell
      tag="D1.1 — Pipeline overview"
      title="From streamers to archive"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 940 240"
    >
      <ArrowheadDefs />

      {ARROWS.map((a) => (
        <Arrow
          key={a.id}
          d={a.d}
          show={tl.step >= a.step}
          highlight={tl.step === a.step}
          label={a.label}
          labelPos={a.labelPos}
        />
      ))}

      {NODES.map((n) => (
        <Node
          key={n.id}
          x={n.x}
          y={n.y}
          label={n.label}
          sublabel={n.sublabel}
          variant={n.variant ?? "default"}
          state={nodeState(nodeActiveStep[n.id])}
        />
      ))}
    </DiagramShell>
  );
}
