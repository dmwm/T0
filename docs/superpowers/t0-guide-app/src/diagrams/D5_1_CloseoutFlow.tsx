import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node, StateBubble } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Run closeout in T0 is an <strong>AND</strong> over four independent
        signals — there is no orchestrator that "decides" when a run is
        done.
      </>
    ),
  },
  {
    caption: (
      <>
        Signal 1 — <strong>All streams closed</strong>. Every stream has its
        end-of-run row in <code>STREAMER</code>; the Storage Manager
        confirmed "no more for this run".
      </>
    ),
  },
  {
    caption: (
      <>
        Signal 2 — <strong>AlcaHarvest done</strong>. The harvest workflow
        for the run completed and condition payloads are in the upload queue.
      </>
    ),
  },
  {
    caption: (
      <>
        Signal 3 — <strong>Conditions uploaded</strong>.{" "}
        <code>ConditionUploadAPI</code> pushed every payload into Frontier;
        T0DataSvcDB has the ack rows.
      </>
    ),
  },
  {
    caption: (
      <>
        Signal 4 — <strong>CMSSW release announced</strong>. PromptReco can
        finalise the run; AOD / MINIAOD release.
      </>
    ),
  },
  {
    caption: (
      <>
        Tier0Feeder polls these signals on every tick. When all four flip
        to ready, <code>CloseRun</code> fires — and the run is done from
        the agent's perspective.
      </>
    ),
  },
];

export function D5_1_CloseoutFlow() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });

  return (
    <DiagramShell
      tag="D5.1 — Closeout convergence"
      title="Four independent signals → one AND gate → run closed"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 800 280"
    >
      <ArrowheadDefs />

      <StateBubble x={120} y={60} r={32} label="streams" active={tl.step === 1} visited={tl.step > 1} />
      <StateBubble x={120} y={140} r={32} label="alca" active={tl.step === 2} visited={tl.step > 2} />
      <StateBubble x={120} y={220} r={32} label="cond" active={tl.step === 3} visited={tl.step > 3} />
      <StateBubble x={300} y={140} r={32} label="release" active={tl.step === 4} visited={tl.step > 4} />

      <g>
        <rect x={420} y={92} width={140} height={96} rx={16} fill={tl.step >= 5 ? "var(--accent-soft)" : "var(--bg-elevated)"} stroke={tl.step >= 5 ? "var(--accent)" : "var(--rule)"} strokeWidth={tl.step >= 5 ? 2.4 : 1.5} />
        <text x={490} y={132} textAnchor="middle" fontSize={13} fontWeight={700} fill="var(--fg)">AND</text>
        <text x={490} y={156} textAnchor="middle" fontSize={11} fill="var(--muted)">all four signals</text>
      </g>

      <Arrow d="M 152 60 C 290 60, 350 110, 418 122" show={tl.step >= 1} highlight={tl.step === 1} />
      <Arrow d="M 152 140 L 418 140" show={tl.step >= 2} highlight={tl.step === 2} />
      <Arrow d="M 152 220 C 290 220, 350 170, 418 158" show={tl.step >= 3} highlight={tl.step === 3} />
      <Arrow d="M 332 140 L 418 140" show={tl.step >= 4} highlight={tl.step === 4} />

      <Node x={628} y={112} label="CloseRun(run)" sublabel="DAO" state={tl.step >= 5 ? "active" : "hidden"} />

      <Arrow d="M 560 140 L 624 140" show={tl.step >= 5} highlight={tl.step === 5} label="fires" labelPos={{ x: 592, y: 132 }} />
    </DiagramShell>
  );
}
