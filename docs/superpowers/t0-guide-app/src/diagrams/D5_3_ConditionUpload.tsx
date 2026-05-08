import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node, DBNode } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        On every tick, <code>ConditionUploadAPI.findUploadable()</code>{" "}
        queries <code>T0DataSvcDB</code> for payload rows in state{" "}
        <code>READY</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        For each row, it looks up the tag policy: which target tag in
        Frontier this payload should be appended to, and what IOV (interval
        of validity) range it covers.
      </>
    ),
  },
  {
    caption: (
      <>
        It POSTs the payload to the Frontier upload endpoint with auth
        credentials. Frontier returns an HTTP 200 with the new IOV.
      </>
    ),
  },
  {
    caption: (
      <>
        On success, <code>markUploaded()</code> flips the row from{" "}
        <code>READY</code> to <code>UPLOADED</code> in T0DataSvcDB. On
        failure, the row stays in <code>READY</code> — the next tick retries.
      </>
    ),
  },
  {
    caption: (
      <>
        Meanwhile, <code>PopConLogDB</code> (if configured) gets a row per
        upload attempt for audit / replay.
      </>
    ),
  },
];

export function D5_3_ConditionUpload() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });
  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D5.3 — Condition upload"
      title="ConditionUploadAPI's tick-loop"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 880 320"
    >
      <ArrowheadDefs />

      <Node x={32} y={140} label="ConditionUploadAPI" sublabel="every tick" state={tl.step >= 0 ? "active" : "hidden"} />

      <DBNode x={260} y={50} label="T0DataSvcDB" sublabel="READY rows" state={stateAt(0)} />
      <Node x={260} y={150} label="Tag policy" sublabel="from RunConfig" state={stateAt(1)} />
      <Node x={500} y={150} label="Frontier" sublabel="POST upload" state={stateAt(2)} variant="external" />
      <DBNode x={260} y={250} label="T0DataSvcDB" sublabel="UPLOADED rows" state={stateAt(3)} />
      <DBNode x={720} y={250} label="PopConLogDB" sublabel="audit log" state={stateAt(4)} />

      <Arrow d="M 164 158 C 200 158, 240 90, 258 80" show={tl.step >= 0} highlight={tl.step === 0} label="query" labelPos={{ x: 220, y: 110 }} />
      <Arrow d="M 164 168 L 256 178" show={tl.step >= 1} highlight={tl.step === 1} />
      <Arrow d="M 392 178 L 498 178" show={tl.step >= 2} highlight={tl.step === 2} label="POST" labelPos={{ x: 444, y: 168 }} />
      <Arrow d="M 562 210 C 562 240, 400 280, 392 280" show={tl.step >= 3} highlight={tl.step === 3} label="markUploaded" labelPos={{ x: 470, y: 268 }} />
      <Arrow d="M 562 210 C 600 220, 700 270, 718 280" show={tl.step >= 4} highlight={tl.step === 4} />
    </DiagramShell>
  );
}
