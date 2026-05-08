import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Express splitting is where Tier-0 cuts deeper for latency. The
        algorithm is similar to Repack but with tighter caps and an extra
        AlCa skim emission step.
      </>
    ),
  },
  {
    caption: (
      <>
        Same loop structure: walk pending streamers in lumi order, accumulate
        a bucket. Inputs include the lumi count and event count per
        streamer.
      </>
    ),
  },
  {
    caption: (
      <>
        Express caps are tighter — typically half of Repack's lumi cap and a
        third of the event cap. It also has a dedicated{" "}
        <code>maxLatency</code> cap (wall-clock).
      </>
    ),
  },
  {
    caption: (
      <>
        On cap hit, the splitter emits both an{" "}
        <strong>Express job</strong> (for the fast reco) and an{" "}
        <strong>AlCa skim job</strong> with the same input streamers.
      </>
    ),
  },
  {
    caption: (
      <>
        Express jobs feed the prompt monitoring path; AlCa jobs feed the
        AlcaHarvest workflow that we saw in Chapter 5.
      </>
    ),
  },
];

const NODES = [
  { id: "loop", x: 40, y: 130, label: "walk streamers", hint: "lumi-ordered", step: 0 },
  { id: "tally", x: 240, y: 130, label: "accumulate", hint: "lumis / events / latency", step: 1 },
  { id: "caps", x: 440, y: 130, label: "Express caps", hint: "tighter than Repack", step: 2 },
  { id: "express", x: 660, y: 50, label: "WMBS_JOB", hint: "Express fast reco", step: 3 },
  { id: "alca", x: 660, y: 210, label: "WMBS_JOB", hint: "AlCa skim → harvest", step: 3 },
];

export function D4_3_ExpressSplitter() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });
  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D4.3 — Express splitter"
      title="Inside ExpressJobSplitter.split() — emits two jobs per cap hit"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 840 320"
    >
      <ArrowheadDefs />

      {NODES.map((n) => (
        <Node
          key={n.id}
          x={n.x}
          y={n.y}
          label={n.label}
          sublabel={n.hint}
          state={stateAt(n.step)}
        />
      ))}

      <Arrow d="M 172 158 L 238 158" show={tl.step >= 1} highlight={tl.step === 1} />
      <Arrow d="M 372 158 L 438 158" show={tl.step >= 2} highlight={tl.step === 2} />
      <Arrow d="M 572 138 C 600 138, 620 90, 658 78" show={tl.step >= 3} highlight={tl.step === 3} label="emit Express" labelPos={{ x: 612, y: 100 }} />
      <Arrow d="M 572 178 C 600 178, 620 220, 658 240" show={tl.step >= 3} highlight={tl.step === 3} label="emit AlCa" labelPos={{ x: 612, y: 220 }} />

      {tl.step >= 4 ? (
        <>
          <text x={730} y={36} fontSize={10.5} fontWeight={600} fill="var(--accent)" letterSpacing="0.05em" textAnchor="middle">→ MONITORING / DQM</text>
          <text x={730} y={282} fontSize={10.5} fontWeight={600} fill="var(--accent)" letterSpacing="0.05em" textAnchor="middle">→ ALCAHARVEST → CONDITIONS</text>
        </>
      ) : null}
    </DiagramShell>
  );
}
