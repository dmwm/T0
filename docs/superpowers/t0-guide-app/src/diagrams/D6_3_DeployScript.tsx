import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        <code>00_pypi_deploy_prod.sh</code> is the single deploy entry point
        on each production host. Step through to see what it does in order.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>1.</strong> Reads the pinned versions at the top of the
        script — <code>WMAGENT_TAG</code> and <code>TIER0_VERSION</code>.
        Hard-coded here, not derived from <code>__init__.py</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>2.</strong> Sources the WMAgent install. This sets up the
        Python environment with the correct WMCore version.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>3.</strong> Runs <code>pip install T0=={"<TIER0_VERSION>"}</code> from
        the CMS PyPI mirror. This is the line that actually decides what
        Tier-0 code runs.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>4.</strong> Sources <code>00_pypi_patches.sh</code> — a list
        of <code>curl … | patch</code> commands cherry-picking WMCore / T0
        PRs. These are <em>live operational state</em>, not committed
        source.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>5.</strong> Runs the WMAgent setup script to generate the
        agent config under <code>/data/tier0/&lt;agent_name&gt;</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        <strong>6.</strong> Hands off to <code>bin/t0 --start-agent</code>;
        the Tier0Feeder begins ticking.
      </>
    ),
  },
];

const NODES = [
  { id: "pin", x: 40, y: 30, label: "version pin", hint: "WMAGENT_TAG / TIER0_VERSION", step: 1 },
  { id: "wmagent", x: 40, y: 130, label: "Source WMAgent", hint: "set Python env", step: 2 },
  { id: "pip", x: 280, y: 30, label: "pip install T0==…", hint: "from CMS PyPI", step: 3 },
  { id: "patches", x: 280, y: 130, label: "00_pypi_patches.sh", hint: "curl|patch cherry-picks", step: 4 },
  { id: "config", x: 520, y: 30, label: "wmagent-mod-config", hint: "/data/tier0/<name>/", step: 5 },
  { id: "start", x: 520, y: 130, label: "bin/t0 --start-agent", hint: "Tier0Feeder live", step: 6 },
];

export function D6_3_DeployScript() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });

  return (
    <DiagramShell
      tag="D6.3 — Deploy script flow"
      title="Inside 00_pypi_deploy_prod.sh"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 720 240"
    >
      <ArrowheadDefs />

      {NODES.map((n) => (
        <Node
          key={n.id}
          x={n.x}
          y={n.y}
          label={n.label}
          sublabel={n.hint}
          state={tl.step > n.step ? "visited" : tl.step === n.step ? "active" : "hidden"}
        />
      ))}

      <Arrow d="M 106 86 L 106 130" show={tl.step >= 2} highlight={tl.step === 2} />
      <Arrow d="M 172 158 C 220 158, 240 90, 278 60" show={tl.step >= 3} highlight={tl.step === 3} />
      <Arrow d="M 346 86 L 346 130" show={tl.step >= 4} highlight={tl.step === 4} />
      <Arrow d="M 412 158 C 460 158, 480 90, 518 60" show={tl.step >= 5} highlight={tl.step === 5} />
      <Arrow d="M 586 86 L 586 130" show={tl.step >= 6} highlight={tl.step === 6} />
    </DiagramShell>
  );
}
