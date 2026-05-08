import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node, DBNode } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Tier-0 keeps two distinct database "halves". <strong>T0AST</strong> is
        the agent's run / stream / closeout state. <strong>WMBS</strong> is
        the WMAgent's job-execution database — the same schema every CMS
        agent uses.
      </>
    ),
  },
  {
    caption: (
      <>
        The agent <code>Tier0Feeder</code> writes T0AST: run config, stream
        configuration, run-stream state, splitter results.
      </>
    ),
  },
  {
    caption: (
      <>
        The Tier0Feeder also writes WMBS: job creations from splitters land
        in <code>WMBS_JOB</code>, files in <code>WMBS_FILE</code>, filesets
        in <code>WMBS_FILESET</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        WMAgent's <code>JobSubmitter</code> and friends read WMBS to dispatch
        jobs to HTCondor — they have no awareness of T0AST.
      </>
    ),
  },
  {
    caption: (
      <>
        T0AST is the "Tier-0 brain"; WMBS is the "execution engine". Both are
        durable Oracle schemas. The split is what lets us reuse WMAgent.
      </>
    ),
  },
];

export function D1_2_TwoDBLayout() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });
  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D1.2 — Two-database layout"
      title="T0AST and WMBS — Tier-0's two state halves"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 800 280"
    >
      <ArrowheadDefs />

      <Node x={324} y={30} label="Tier0Feeder" sublabel="agent.algorithm()" state={stateAt(0)} />

      <DBNode x={70} y={130} label="T0AST" sublabel="Tier-0 state" state={stateAt(1)} />
      <text x={125} y={216} fontSize={10} textAnchor="middle" fill="var(--muted)">RUN, RUN_STREAM_*</text>
      <text x={125} y={228} fontSize={10} textAnchor="middle" fill="var(--muted)">RUN_PRIMDS, ALCA_HARVEST</text>

      <DBNode x={620} y={130} label="WMBS" sublabel="job exec" state={stateAt(2)} />
      <text x={675} y={216} fontSize={10} textAnchor="middle" fill="var(--muted)">WMBS_JOB, WMBS_FILE</text>
      <text x={675} y={228} fontSize={10} textAnchor="middle" fill="var(--muted)">WMBS_FILESET, WORKFLOW</text>

      <Node x={324} y={130} label="WMAgent" sublabel="JobSubmitter" state={stateAt(3)} variant="external" />

      <Arrow d="M 324 76 C 240 76, 200 130, 180 138" show={tl.step >= 1} highlight={tl.step === 1} label="writes" labelPos={{ x: 240, y: 92 }} />
      <Arrow d="M 456 76 C 540 76, 600 130, 620 138" show={tl.step >= 2} highlight={tl.step === 2} label="writes" labelPos={{ x: 562, y: 92 }} />
      <Arrow d="M 456 158 L 620 158" show={tl.step >= 3} highlight={tl.step === 3} label="reads" labelPos={{ x: 540, y: 152 }} />
    </DiagramShell>
  );
}
