import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, StateBubble } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Streams are nested under runs. Their state machine is simpler — four
        states that follow the splitting lifecycle.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>OPEN</strong>: <code>RUN_STREAM_*</code> rows are configured;
        no streamers yet. The agent is waiting.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>SPLITTING</strong>: at least one streamer arrived. The
        splitter is producing <code>WMBS_JOB</code> rows.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>SPLIT_DONE</strong>: Storage Manager confirmed no more
        streamers (end-of-run). The last streamer has been split.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>CLOSED</strong>: <code>CloseStream(run, stream)</code> ran.
        This stream is no longer a closeout signal source.
      </>
    ),
  },
];

const STATES = [
  { id: "open", x: 110, y: 140, label: "OPEN", step: 1 },
  { id: "splitting", x: 320, y: 140, label: "SPLITTING", step: 2 },
  { id: "split-done", x: 530, y: 140, label: "SPLIT_DONE", step: 3 },
  { id: "closed", x: 740, y: 140, label: "CLOSED", step: 4 },
];

const TRANSITIONS = [
  { from: "open", to: "splitting", label: "first streamer" },
  { from: "splitting", to: "split-done", label: "no more streamers" },
  { from: "split-done", to: "closed", label: "feeder closes" },
];

export function D2_3_StreamStates() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });

  return (
    <DiagramShell
      tag="D2.3 — Stream state machine"
      title="Four states per (run, stream) row"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 880 240"
    >
      <ArrowheadDefs />

      {TRANSITIONS.map((t, i) => {
        const from = STATES.find((s) => s.id === t.from)!;
        const to = STATES.find((s) => s.id === t.to)!;
        const targetIdx = STATES.findIndex((s) => s.id === t.to);
        const stepActive = tl.step >= targetIdx + 1;
        const isCurrent = tl.step === targetIdx + 1;
        const d = `M ${from.x + 36} ${from.y} L ${to.x - 36} ${to.y}`;
        return (
          <g key={i}>
            <Arrow d={d} show={stepActive} highlight={isCurrent} />
            <text
              x={(from.x + to.x) / 2}
              y={from.y - 12}
              textAnchor="middle"
              fontSize={10.5}
              fontWeight={500}
              fill={isCurrent ? "var(--accent)" : "var(--muted)"}
              opacity={stepActive ? 1 : 0.3}
            >
              {t.label}
            </text>
          </g>
        );
      })}

      {STATES.map((s) => {
        const idx = STATES.findIndex((x) => x.id === s.id);
        const isActive = tl.step === idx + 1;
        const wasVisited = tl.step > idx + 1;
        return (
          <StateBubble
            key={s.id}
            x={s.x}
            y={s.y}
            r={40}
            label={s.label}
            active={isActive}
            visited={wasVisited}
          />
        );
      })}
    </DiagramShell>
  );
}
