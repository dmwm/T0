import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Tier-0 production runs on four <code>vocms</code> hosts as the{" "}
        <code>cmst0</code> user. <strong>vocms047</strong> is the Main agent;
        the other three are Helpers.
      </>
    ),
  },
  {
    caption: (
      <>
        Source of truth: the <code>master</code> branch of{" "}
        <code>github.com/dmwm/T0</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        On every push to master that touches{" "}
        <code>src/python/T0/__init__.py</code>, CI publishes a new tag and
        sdist to PyPI.
      </>
    ),
  },
  {
    caption: (
      <>
        Each host pins its own <code>TIER0_VERSION</code> in{" "}
        <code>bin/00_pypi_deploy_*.sh</code>. The version drift between hosts
        is intentional — Helpers can run a lagging release.
      </>
    ),
  },
  {
    caption: (
      <>
        The shell scripts on the host live under <code>/data/tier0/</code>;{" "}
        <code>bin/pypi_update.sh</code> re-pulls them from{" "}
        <code>master</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        Operators drive each host with the <code>bin/t0</code> CLI:{" "}
        <code>--start-agent</code>, <code>--stop-agent</code>,{" "}
        <code>--update-t0=&lt;ver&gt;</code>, etc.
      </>
    ),
  },
];

export function D1_4_DeployTopology() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });
  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D1.4 — Deploy topology"
      title="Where Tier-0 actually runs in production"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 920 320"
    >
      <ArrowheadDefs />

      <Node x={40} y={50} label="github.com/dmwm/T0" sublabel="master branch" state={stateAt(1)} variant="external" />
      <Node x={40} y={170} label="PyPI: T0" sublabel="sdist + tags" state={stateAt(2)} variant="external" />

      <rect x={300} y={20} width={580} height={280} rx={14} fill="color-mix(in srgb, var(--accent) 4%, transparent)" stroke="var(--rule)" strokeDasharray="4 4" />
      <text x={314} y={40} fontSize={11} fontWeight={600} fill="var(--muted)" letterSpacing="0.06em">CMST0 PRODUCTION HOSTS</text>

      <Node x={330} y={70} label="vocms047" sublabel="Main agent" state={stateAt(0)} />
      <Node x={486} y={70} label="vocms0500" sublabel="Helper agent" state={stateAt(0)} />
      <Node x={642} y={70} label="vocms05011" sublabel="Helper agent" state={stateAt(0)} />
      <Node x={742} y={170} label="vocms05012" sublabel="Helper agent" state={stateAt(0)} />

      <Node x={486} y={170} label="bin/00_pypi_deploy_prod.sh" sublabel="pins TIER0_VERSION" state={stateAt(3)} />
      <Node x={330} y={170} label="/data/tier0/" sublabel="installed scripts" state={stateAt(4)} />
      <Node x={486} y={250} label="bin/t0 CLI" sublabel="operator interface" state={stateAt(5)} />

      <Arrow d="M 172 78 L 328 78" show={tl.step >= 1} highlight={tl.step === 1} />
      <Arrow d="M 172 198 L 328 198" show={tl.step >= 4} highlight={tl.step === 4} label="pypi_update.sh" labelPos={{ x: 248, y: 188 }} />
      <Arrow d="M 172 198 C 230 198, 280 200, 340 200" show={false} />
      <Arrow d="M 172 198 L 484 198" show={tl.step >= 2} highlight={tl.step === 2} />
      <Arrow d="M 552 230 L 552 248" show={tl.step >= 5} highlight={tl.step === 5} />
      <Arrow d="M 462 270 C 400 270, 360 102, 396 100" show={tl.step >= 5} highlight={tl.step === 5} />
      <Arrow d="M 552 250 C 720 250, 720 102, 706 100" show={tl.step >= 5} highlight={tl.step === 5} />
    </DiagramShell>
  );
}
