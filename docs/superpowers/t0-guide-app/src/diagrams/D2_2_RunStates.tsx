import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, StateBubble } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Every run goes through five states in T0AST. The transitions are not
        time-based — they fire when DAOs detect their preconditions.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>NEW</strong>: a row exists in <code>RUN</code> but no
        run-config row yet. <code>FindNewRuns()</code> picks it up on the
        next tick.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>CONFIGURED</strong>: <code>RUN_CONFIG</code> and{" "}
        <code>RUN_STREAM_CMSSW_VER</code> rows are written by{" "}
        <code>RunConfigAPI.configureRun</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>ACTIVE</strong>: streamers are arriving for at least one
        stream of this run. Splitter is producing jobs.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>RELEASE_ANNOUNCED</strong>: a CMSSW release for the run
        becomes available. <code>releasePromptReco(run)</code> creates the
        PromptReco workflow.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>CLOSED</strong>: closeout convergence fired —{" "}
        <code>CloseRun(run)</code> committed. The run is done from the
        agent's perspective.
      </>
    ),
  },
];

const STATES = [
  { id: "new", x: 90, y: 140, label: "NEW", step: 1 },
  { id: "configured", x: 260, y: 140, label: "CONFIGURED", step: 2 },
  { id: "active", x: 440, y: 140, label: "ACTIVE", step: 3 },
  { id: "release", x: 620, y: 60, label: "RELEASE_\nANNOUNCED", step: 4 },
  { id: "closed", x: 620, y: 220, label: "CLOSED", step: 5 },
];

const TRANSITIONS = [
  { from: "new", to: "configured", label: "configureRun" },
  { from: "configured", to: "active", label: "first streamer" },
  { from: "active", to: "release", label: "release announce" },
  { from: "active", to: "closed", label: "closeout (no reco)" },
  { from: "release", to: "closed", label: "closeout fires" },
];

export function D2_2_RunStates() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });

  return (
    <DiagramShell
      tag="D2.2 — Run state machine"
      title="Five states a run passes through in T0AST"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 800 320"
    >
      <ArrowheadDefs />

      {TRANSITIONS.map((t, i) => {
        const from = STATES.find((s) => s.id === t.from)!;
        const to = STATES.find((s) => s.id === t.to)!;
        const sameRow = Math.abs(from.y - to.y) < 8;
        const ctrl = sameRow
          ? `${(from.x + to.x) / 2} ${from.y - 24}`
          : `${(from.x + to.x) / 2} ${(from.y + to.y) / 2}`;
        const d = `M ${from.x + 36} ${from.y} Q ${ctrl}, ${to.x - 36} ${to.y}`;
        const stepActive = tl.step >= STATES.findIndex((s) => s.id === t.to) + 1;
        const isCurrentTransition = tl.step === STATES.findIndex((s) => s.id === t.to) + 1;
        return (
          <g key={i}>
            <Arrow d={d} show={stepActive} highlight={isCurrentTransition} />
            <text
              x={(from.x + to.x) / 2}
              y={Math.min(from.y, to.y) - 8}
              textAnchor="middle"
              fontSize={10.5}
              fontWeight={500}
              fill={isCurrentTransition ? "var(--accent)" : "var(--muted)"}
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
        return s.label.includes("\n") ? (
          <g key={s.id}>
            <StateBubble
              x={s.x}
              y={s.y}
              r={36}
              label=""
              active={isActive}
              visited={wasVisited}
            />
            {s.label.split("\n").map((line, li) => (
              <text
                key={li}
                x={s.x}
                y={s.y + 4 + (li - 0.5) * 11}
                textAnchor="middle"
                fontSize={10}
                fontWeight={600}
                fill="var(--fg)"
              >
                {line}
              </text>
            ))}
          </g>
        ) : (
          <StateBubble
            key={s.id}
            x={s.x}
            y={s.y}
            r={36}
            label={s.label}
            active={isActive}
            visited={wasVisited}
          />
        );
      })}
    </DiagramShell>
  );
}
