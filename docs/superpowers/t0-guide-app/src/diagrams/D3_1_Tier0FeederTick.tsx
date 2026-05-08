import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";

interface PhaseNode {
  id: string;
  x: number;
  y: number;
  label: string;
  hint: string;
}

const PHASES: PhaseNode[] = [
  { id: "configure", x: 30, y: 110, label: "Configure", hint: "runs / streams" },
  { id: "split", x: 200, y: 110, label: "Splitters", hint: "Repack + Express" },
  { id: "release", x: 370, y: 110, label: "Release", hint: "PromptReco" },
  { id: "closeout", x: 540, y: 110, label: "Closeout", hint: "convergence" },
  { id: "upload", x: 710, y: 110, label: "Upload", hint: "PCL → Frontier" },
];

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        <strong>algorithm()</strong> is invoked by{" "}
        <code>WorkerThreadManager</code> on the configured poll interval
        (default 30s).
      </>
    ),
  },
  {
    caption: (
      <>
        Phase 1 — pick up newly active runs/streams from T0AST and write run /
        run-stream config rows via <code>RunConfigAPI</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        Phase 2 — call splitter plugins via{" "}
        <code>SplitterFactory("T0.JobSplitting")</code>; each plugin emits
        WMBS_JOB rows for its stream.
      </>
    ),
  },
  {
    caption: (
      <>
        Phase 3 — once a CMSSW release is announced, release PromptReco
        workflows for runs that are otherwise complete.
      </>
    ),
  },
  {
    caption: (
      <>
        Phase 4 — drive closeout: check the four convergence signals and mark
        runs / streams closed in T0AST.
      </>
    ),
  },
  {
    caption: (
      <>
        Phase 5 — pick up new condition payloads and POST them to Frontier via{" "}
        <code>ConditionUploadAPI</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        ↻ Loop back. The next tick repeats the same five phases — every run /
        stream / job state lives in T0AST, so a crash mid-tick is a no-op.
      </>
    ),
  },
];

export function D3_1_Tier0FeederTick() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });

  function phaseState(phaseIdx: number) {
    const target = phaseIdx + 1; // step 0 is "algorithm()", phase i lights at step i+1
    if (tl.step > target) return "visited" as const;
    if (tl.step === target) return "active" as const;
    return "hidden" as const;
  }

  return (
    <DiagramShell
      tag="D3.1 — Tier0Feeder heartbeat"
      title="Five phases on every poll tick"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 880 260"
    >
      <ArrowheadDefs />

      <rect
        x={10}
        y={86}
        width={840}
        height={108}
        rx={16}
        fill="color-mix(in srgb, var(--accent) 4%, transparent)"
        stroke="var(--rule)"
        strokeDasharray="4 4"
      />
      <text
        x={22}
        y={104}
        fontSize={11}
        fontWeight={600}
        fill="var(--muted)"
        letterSpacing="0.06em"
      >
        TIER0FEEDERPOLLER.ALGORITHM()
      </text>

      {PHASES.map((p, i) => {
        const next = PHASES[i + 1];
        if (!next) return null;
        const fromX = p.x + 132;
        const fromY = p.y + 28;
        const toX = next.x;
        const toY = next.y + 28;
        return (
          <Arrow
            key={`${p.id}-${next.id}`}
            d={`M ${fromX} ${fromY} L ${toX - 4} ${toY}`}
            show={tl.step >= i + 2}
            highlight={tl.step === i + 2}
          />
        );
      })}

      <Arrow
        d={`M ${PHASES[4].x + 66} ${PHASES[4].y + 56} C 778 230, 60 230, ${PHASES[0].x + 66} ${PHASES[0].y + 56}`}
        show={tl.step === STEPS.length - 1}
        highlight={tl.step === STEPS.length - 1}
        label="next tick — same five phases"
        labelPos={{ x: 440, y: 250 }}
      />

      {PHASES.map((p, i) => (
        <Node
          key={p.id}
          x={p.x}
          y={p.y}
          label={p.label}
          sublabel={p.hint}
          state={phaseState(i)}
        />
      ))}
    </DiagramShell>
  );
}
