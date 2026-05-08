import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node, DBNode } from "./shared/primitives";
import { motion } from "framer-motion";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Streamer files don't push into Tier-0 — Tier-0 pulls them. Each tick
        runs <code>FindNewStreamers</code> to discover any files added to
        the Storage Manager DB since the last successful read.
      </>
    ),
  },
  {
    caption: (
      <>
        The query joins the SM DB <code>STREAMER</code> table with T0AST's
        own <code>STREAMER</code> table. Anything in the SM table without a
        T0AST row is "new".
      </>
    ),
  },
  {
    caption: (
      <>
        Each new streamer is inserted into T0AST's <code>STREAMER</code>{" "}
        table with state <code>NEW</code>. This is the durable hand-off
        boundary — once written, the agent owns it.
      </>
    ),
  },
  {
    caption: (
      <>
        Now the splitter sees those rows. The same row will move through
        states <code>NEW → SPLIT → DONE</code> as the splitter picks it up
        and packs it into a job.
      </>
    ),
  },
  {
    caption: (
      <>
        If the agent crashes mid-tick, the Storage Manager row is unchanged
        and the T0AST row hasn't been written. The next tick's{" "}
        <code>FindNewStreamers</code> will find the same set again.
      </>
    ),
  },
];

export function D3_3_StorageManagerPolling() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });
  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D3.3 — Storage Manager polling"
      title="FindNewStreamers — the pull boundary"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 880 320"
    >
      <ArrowheadDefs />

      <DBNode x={32} y={130} label="StorageMgr" sublabel="STREAMER" state={tl.step >= 0 ? "active" : "hidden"} />
      <Node x={224} y={130} label="FindNewStreamers" sublabel="DAO" state={stateAt(0)} />
      <DBNode x={420} y={50} label="T0AST" sublabel="STREAMER (state=NEW)" state={stateAt(2)} />
      <DBNode x={420} y={210} label="T0AST" sublabel="STREAMER (state=SPLIT/DONE)" state={stateAt(3)} />
      <Node x={680} y={210} label="Splitter" sublabel="moves state forward" state={stateAt(3)} />

      <Arrow d="M 142 158 L 222 158" show={tl.step >= 0} highlight={tl.step === 0} label="poll" labelPos={{ x: 182, y: 148 }} />
      <Arrow d="M 356 158 C 380 158, 400 90, 420 80" show={tl.step >= 1} highlight={tl.step === 1} label="left-anti join" labelPos={{ x: 380, y: 116 }} />
      <Arrow d="M 528 78 C 460 80, 460 220, 422 240" show={tl.step >= 2} highlight={tl.step === 2} label="insert NEW" labelPos={{ x: 470, y: 152 }} />
      <Arrow d="M 528 240 L 678 240" show={tl.step >= 3} highlight={tl.step === 3} label="split jobs" labelPos={{ x: 600, y: 230 }} />

      {tl.step >= 4 ? (
        <motion.text
          x={440}
          y={302}
          textAnchor="middle"
          fontSize={11}
          fontWeight={600}
          fill="var(--accent)"
          letterSpacing="0.05em"
          initial={{ opacity: 0, y: 296 }}
          animate={{ opacity: 1, y: 302 }}
        >
          CRASH MID-TICK = NO-OP. NEXT TICK FINDS THE SAME SET AGAIN.
        </motion.text>
      ) : null}
    </DiagramShell>
  );
}
