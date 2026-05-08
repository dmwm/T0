import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node, DBNode } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Express jobs produce calibration histograms (the AlCa skim) alongside
        their fast-reco output. AlcaHarvest is the workflow that aggregates
        them across all Express jobs of a run.
      </>
    ),
  },
  {
    caption: (
      <>
        Each Express job writes an AlCa output to <code>WMBS_FILE</code>;
        Tier0Feeder marks them ready in <code>ALCA_HARVEST</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        Once a stream's Express jobs are done, AlcaHarvest is released as a
        separate WMAgent workflow. It runs a single job that reads all the
        per-job AlCa files.
      </>
    ),
  },
  {
    caption: (
      <>
        The AlcaHarvest job emits condition payloads — pickled IOV records
        keyed by tag. They land in <code>T0DataSvcDB</code> via{" "}
        <code>ConditionUploadAPI</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        On the next tick, the upload phase picks up payloads from{" "}
        <code>T0DataSvcDB</code> and POSTs them to Frontier — the production
        conditions backend.
      </>
    ),
  },
];

export function D5_2_AlcaHarvestPipe() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });
  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D5.2 — AlcaHarvest pipeline"
      title="From Express AlCa output to Frontier conditions"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 920 280"
    >
      <ArrowheadDefs />

      <Node x={20} y={120} label="Express jobs" sublabel="N per stream" state={stateAt(0)} />
      <DBNode x={200} y={120} label="ALCA_HARVEST" sublabel="ready rows" state={stateAt(1)} />
      <Node x={372} y={120} label="AlcaHarvest" sublabel="one job per run" state={stateAt(2)} />
      <DBNode x={550} y={120} label="T0DataSvcDB" sublabel="payloads" state={stateAt(3)} />
      <Node x={732} y={120} label="ConditionUpload" sublabel="POST to Frontier" state={stateAt(4)} variant="external" />

      <Arrow d="M 152 148 L 198 148" show={tl.step >= 1} highlight={tl.step === 1} label="register" labelPos={{ x: 175, y: 138 }} />
      <Arrow d="M 312 148 L 370 148" show={tl.step >= 2} highlight={tl.step === 2} label="release" labelPos={{ x: 340, y: 138 }} />
      <Arrow d="M 504 148 L 550 148" show={tl.step >= 3} highlight={tl.step === 3} label="payloads" labelPos={{ x: 528, y: 138 }} />
      <Arrow d="M 660 148 L 730 148" show={tl.step >= 4} highlight={tl.step === 4} label="upload" labelPos={{ x: 695, y: 138 }} />

      <text x={460} y={222} textAnchor="middle" fontSize={11} fill="var(--muted)" letterSpacing="0.06em" fontWeight={600}>
        EVERY WMBS_FILE → AGGREGATED → IOV PAYLOADS → FRONTIER
      </text>
    </DiagramShell>
  );
}
