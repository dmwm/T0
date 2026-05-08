import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node, DBNode } from "./shared/primitives";

interface DBSpec {
  id: string;
  x: number;
  y: number;
  label: string;
  hint: string;
  optional: boolean;
  step: number;
}

const DBS: DBSpec[] = [
  { id: "t0ast", x: 60, y: 30, label: "T0AST", hint: "Tier-0 state", optional: false, step: 1 },
  { id: "hltconf", x: 60, y: 130, label: "HLTConfDB", hint: "stream config", optional: false, step: 2 },
  { id: "smdb", x: 60, y: 230, label: "StorageMgr DB", hint: "streamer files", optional: false, step: 3 },
  { id: "smnotify", x: 660, y: 30, label: "SMNotifyDB", hint: "online notify", optional: true, step: 4 },
  { id: "popcon", x: 660, y: 130, label: "PopConLogDB", hint: "PCL upload log", optional: true, step: 5 },
  { id: "datasvc", x: 660, y: 230, label: "T0DataSvcDB", hint: "monitoring", optional: true, step: 6 },
];

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        On every tick, the Tier0Feeder may talk to up to six Oracle
        databases. Three are mandatory; three are optional, gated on
        whether their config block exists.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>T0AST</strong> — the agent's own state. RUN, RUN_STREAM_*,
        WMBS_*, ALCA_HARVEST, etc. Always required.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>HLTConfDB</strong> — read-only. Tells us which streams exist
        for which run from the online HLT configuration.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>StorageManager DB</strong> — read-only. Lists the streamer
        files Tier-0 should pull and process.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>SMNotifyDB</strong> (optional) — write back to Storage
        Manager when Tier-0 finishes consuming streamer batches.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>PopConLogDB</strong> (optional) — log condition uploads for
        replay / audit.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>T0DataSvcDB</strong> (optional) — monitoring telemetry the
        Tier-0 dashboard reads.
      </>
    ),
  },
];

export function D1_3_MultiDBConnectivity() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });

  const stateAt = (target: number) =>
    tl.step > target ? "visited" : tl.step === target ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D1.3 — Multi-DB connectivity"
      title="Six databases the Tier0Feeder may touch"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 820 320"
    >
      <ArrowheadDefs />

      <Node
        x={344}
        y={130}
        label="Tier0Feeder"
        sublabel="agent.algorithm()"
        state={tl.step >= 0 ? "active" : "hidden"}
      />

      {DBS.map((db) => {
        const left = db.x < 400;
        const startX = left ? db.x + 110 : db.x;
        const startY = db.y + 32;
        const endX = left ? 344 : 476;
        const endY = 158;
        const ctrlX = (startX + endX) / 2;
        const ctrlY = (startY + endY) / 2;
        const d = `M ${startX} ${startY} Q ${ctrlX} ${ctrlY}, ${endX} ${endY}`;
        const labelPos = { x: (startX + endX) / 2, y: (startY + endY) / 2 - 6 };
        return (
          <g key={db.id}>
            <DBNode
              x={db.x}
              y={db.y}
              label={db.label}
              sublabel={db.hint}
              state={stateAt(db.step)}
            />
            {db.optional ? (
              <text
                x={db.x + 110}
                y={db.y + 8}
                fontSize={9.5}
                fontWeight={600}
                fill="var(--muted)"
                letterSpacing="0.06em"
              >
                OPT
              </text>
            ) : null}
            <Arrow
              d={d}
              show={tl.step >= db.step}
              highlight={tl.step === db.step}
              label={db.optional ? "optional" : ""}
              labelPos={db.optional ? labelPos : undefined}
            />
          </g>
        );
      })}
    </DiagramShell>
  );
}
