import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Node } from "./shared/primitives";
import { motion } from "framer-motion";

interface SetterCall {
  call: string;
  hint: string;
  step: number;
  field: string;
}

const CALLS: SetterCall[] = [
  {
    call: 'setAcquisitionEra("Run2026D")',
    hint: "stamp the acquisition era on every dataset",
    step: 1,
    field: "tier0Config.Global.AcquisitionEra",
  },
  {
    call: 'setProcessingSite("T0_CH_CERN")',
    hint: "where the offline jobs run",
    step: 2,
    field: "tier0Config.Global.ProcessingSite",
  },
  {
    call: 'addDataset("HLTPhysics", scenario="ppRun3")',
    hint: "register a primary dataset with its scenario",
    step: 3,
    field: "tier0Config.Datasets[]",
  },
  {
    call: 'addRepackConfig(maxSizeSingleLumi=4*GB, ...)',
    hint: "Repack splitter caps for this dataset",
    step: 4,
    field: "tier0Config.Datasets[].Repack",
  },
  {
    call: 'addExpressConfig(scenario, alcaSkims=[...])',
    hint: "Express config + AlCa harvest skims",
    step: 5,
    field: "tier0Config.Datasets[].Express",
  },
  {
    call: 'setHelperAgentStreams({"agent2": ["AlCaPhi"]})',
    hint: "helper-agent stream partition",
    step: 6,
    field: "tier0Config.Global.HelperAgentStreams",
  },
];

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Tier0Config is built top-down: each setter mutates a different field
        of the in-memory config tree. The setters are just Python functions
        defined in <code>src/python/T0/RunConfig/Tier0Config.py</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>setAcquisitionEra</code> stamps a label that propagates onto
        every output dataset name.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>setProcessingSite</code> picks the destination CMS site for
        offline processing — usually <code>T0_CH_CERN</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>addDataset</code> registers a primary dataset (PD) and the
        reconstruction scenario it should use.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>addRepackConfig</code> attaches Repack splitter caps to the
        most recently added dataset — note the implicit "current dataset"
        state in the DSL.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>addExpressConfig</code> does the same for Express. AlCa skim
        names live here.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>setHelperAgentStreams</code> finally tells the agent which
        streams Main owns and which ones each Helper takes.
      </>
    ),
  },
];

export function D2_4_DSLTimeline() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });

  return (
    <DiagramShell
      tag="D2.4 — DSL setter timeline"
      title="A typical ProdOfflineConfiguration.py — top to bottom"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 880 360"
    >
      <ArrowheadDefs />

      <Node
        x={356}
        y={20}
        label="Tier0Config tree"
        sublabel="in-memory dict"
        state={tl.step >= 0 ? "active" : "hidden"}
      />

      {CALLS.map((c, i) => {
        const isActive = tl.step === c.step;
        const isDone = tl.step > c.step;
        const y = 100 + i * 40;
        return (
          <motion.g
            key={c.step}
            initial={false}
            animate={{ opacity: isDone || isActive ? 1 : 0.25 }}
          >
            <text
              x={20}
              y={y + 14}
              fontSize={11.5}
              fontFamily="SF Mono, Menlo, monospace"
              fontWeight={isActive ? 600 : 500}
              fill={isActive ? "var(--accent)" : isDone ? "var(--fg)" : "var(--muted)"}
            >
              <tspan opacity={0.5}>{(i + 1).toString().padStart(2, "0")}  </tspan>
              {c.call}
            </text>
            <text
              x={28}
              y={y + 28}
              fontSize={10.5}
              fill="var(--muted)"
              fontStyle="italic"
            >
              // {c.hint}
            </text>
            {(isActive || isDone) ? (
              <motion.path
                d={`M 480 ${y + 14} C 540 ${y + 14}, 580 ${y + 14}, 620 60`}
                stroke={isActive ? "var(--accent)" : "color-mix(in srgb, var(--accent) 50%, transparent)"}
                strokeWidth={isActive ? 1.8 : 1.2}
                fill="none"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: isActive ? 1 : 0.5 }}
                transition={{ duration: 0.5 }}
                markerEnd={isActive ? "url(#arrowhead-active)" : "url(#arrowhead)"}
              />
            ) : null}
            {isActive ? (
              <text
                x={620}
                y={y + 14}
                fontSize={10}
                fontFamily="SF Mono, Menlo, monospace"
                fill="var(--accent)"
              >
                {c.field}
              </text>
            ) : null}
          </motion.g>
        );
      })}
    </DiagramShell>
  );
}
