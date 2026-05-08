import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";

const COMMANDS = [
  { id: "start", label: "--start-agent", hint: "kick off Tier0Feeder", x: 60, y: 70, step: 1 },
  { id: "stop", label: "--stop-agent", hint: "graceful shutdown", x: 60, y: 150, step: 2 },
  { id: "update", label: "--update-t0=<ver>", hint: "pip install + restart", x: 60, y: 230, step: 3 },
  { id: "tarball", label: "--get-tarball=<job>", hint: "download condor sandbox", x: 320, y: 70, step: 4 },
  { id: "clear", label: "--clear-deployment", hint: "wipe /data/tier0/", x: 320, y: 150, step: 5 },
  { id: "status", label: "--status", hint: "agent health check", x: 320, y: 230, step: 6 },
];

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        <code>bin/t0</code> is the operator CLI on each deploy host. All
        operational tasks go through it — there is no web UI, no admin
        console.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>--start-agent</code> launches <code>Tier0Feeder</code> via the
        WMAgent harness. Reads the config from <code>/data/tier0/</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>--stop-agent</code> gracefully drains in-flight ticks and
        stops the worker thread.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>--update-t0=&lt;ver&gt;</code> installs the named PyPI release
        and restarts the agent. Used for both planned upgrades and rollbacks.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>--get-tarball=&lt;job&gt;</code> pulls the condor sandbox for a
        failed job — the operator-side debugger.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>--clear-deployment</code> wipes <code>/data/tier0/</code>{" "}
        before a clean redeploy. Destructive — operator confirms.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>--status</code> prints WMAgent health: thread state, last tick
        timestamp, oracle connectivity. First-line diagnostic.
      </>
    ),
  },
];

export function D6_1_OperatorCLI() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });

  return (
    <DiagramShell
      tag="D6.1 — Operator CLI surface"
      title="bin/t0 — every operational task on every deploy host"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 600 320"
    >
      <ArrowheadDefs />

      <Node
        x={232}
        y={20}
        label="bin/t0"
        sublabel="operator CLI"
        state={tl.step >= 0 ? "active" : "hidden"}
      />

      {COMMANDS.map((c) => (
        <g key={c.id}>
          <Node
            x={c.x}
            y={c.y}
            label={c.label}
            sublabel={c.hint}
            state={tl.step > c.step ? "visited" : tl.step === c.step ? "active" : "hidden"}
          />
          <Arrow
            d={`M ${298} ${78} L ${c.x + 66} ${c.y - 4}`}
            show={tl.step >= c.step}
            highlight={tl.step === c.step}
          />
        </g>
      ))}
    </DiagramShell>
  );
}
