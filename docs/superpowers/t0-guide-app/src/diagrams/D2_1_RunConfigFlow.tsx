import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node, DBNode } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Operator edits <code>etc/ProdOfflineConfiguration.py</code>: a Python
        file that calls Tier0Config setters like <code>addDataset</code>,{" "}
        <code>setAcquisitionEra</code>, <code>setHelperAgentStreams</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        WMAgent loads the config via{" "}
        <code>loadConfigurationFile</code>, which executes the Python and
        builds an in-memory <code>Tier0Config</code> tree.
      </>
    ),
  },
  {
    caption: (
      <>
        On each tick, <code>Tier0FeederPoller</code> resolves the current
        run's row in <code>RUN</code> and looks up the corresponding{" "}
        <code>Tier0Config</code> object.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>RunConfigAPI.configureRun(run, tier0Config)</code> reads the
        DSL tree and writes one row per related table —{" "}
        <code>RUN_PRIMDS_SCENARIO_ASSOC</code>,{" "}
        <code>RUN_STREAM_CMSSW_VER</code>, <code>RUN_HELPER_AGENT</code> —
        idempotently.
      </>
    ),
  },
  {
    caption: (
      <>
        Every later phase (splitting, closeout, condition upload) consults
        these T0AST rows. T0AST is the durable boundary: once written,
        config-driven behavior is decided.
      </>
    ),
  },
];

export function D2_1_RunConfigFlow() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });

  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D2.1 — RunConfig flow"
      title="From DSL file to T0AST rows"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 920 290"
    >
      <ArrowheadDefs />

      <rect
        x={10}
        y={20}
        width={300}
        height={250}
        rx={14}
        fill="color-mix(in srgb, var(--accent) 4%, transparent)"
        stroke="var(--rule)"
        strokeDasharray="4 4"
      />
      <text x={24} y={40} fontSize={11} fontWeight={600} fill="var(--muted)" letterSpacing="0.06em">
        OPERATOR-EDITED CONFIG
      </text>

      <rect
        x={330}
        y={20}
        width={280}
        height={250}
        rx={14}
        fill="color-mix(in srgb, var(--accent) 4%, transparent)"
        stroke="var(--rule)"
        strokeDasharray="4 4"
      />
      <text x={344} y={40} fontSize={11} fontWeight={600} fill="var(--muted)" letterSpacing="0.06em">
        AGENT — IN MEMORY
      </text>

      <rect
        x={630}
        y={20}
        width={280}
        height={250}
        rx={14}
        fill="color-mix(in srgb, var(--accent) 4%, transparent)"
        stroke="var(--rule)"
        strokeDasharray="4 4"
      />
      <text x={644} y={40} fontSize={11} fontWeight={600} fill="var(--muted)" letterSpacing="0.06em">
        T0AST — DURABLE
      </text>

      <Node
        x={50}
        y={70}
        label="ProdOfflineConfiguration.py"
        sublabel="Tier0Config DSL"
        state={stateAt(0)}
      />
      <Node
        x={50}
        y={170}
        label="addDataset / setStream / …"
        sublabel="DSL setters"
        state={stateAt(0)}
      />

      <Node
        x={356}
        y={70}
        label="loadConfigurationFile"
        sublabel="WMCore"
        state={stateAt(1)}
      />
      <Node
        x={356}
        y={170}
        label="Tier0Config tree"
        sublabel="in-memory dict"
        state={stateAt(2)}
      />

      <DBNode
        x={672}
        y={70}
        label="RUN"
        sublabel="run_config?"
        state={stateAt(3)}
      />
      <DBNode
        x={672}
        y={170}
        label="RUN_STREAM_*"
        sublabel="config rows"
        state={stateAt(3)}
      />
      <DBNode
        x={802}
        y={170}
        label="RUN_HELPER"
        sublabel="agent assign"
        state={stateAt(3)}
      />
      <DBNode
        x={802}
        y={70}
        label="RUN_PRIMDS"
        sublabel="scenarios"
        state={stateAt(3)}
      />

      <Arrow
        d="M 182 98 L 354 98"
        show={tl.step >= 1}
        highlight={tl.step === 1}
      />
      <Arrow
        d="M 182 198 L 354 198"
        show={tl.step >= 2}
        highlight={tl.step === 2}
      />
      <Arrow
        d="M 488 98 L 670 98"
        show={tl.step >= 3}
        highlight={tl.step === 3}
        label="configureRun"
        labelPos={{ x: 580, y: 88 }}
      />
      <Arrow
        d="M 488 198 L 670 198"
        show={tl.step >= 3}
        highlight={tl.step === 3}
      />
      <Arrow
        d="M 782 102 L 800 90"
        show={tl.step >= 3}
        highlight={tl.step === 3}
      />
      <Arrow
        d="M 782 200 L 800 188"
        show={tl.step >= 3}
        highlight={tl.step === 3}
      />
    </DiagramShell>
  );
}
