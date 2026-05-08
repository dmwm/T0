import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Job splitting is plugin-based. The Tier0Feeder doesn't know about
        Repack or Express specifically — it asks{" "}
        <code>SplitterFactory</code> for a splitter by name.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>SplitterFactory(package="T0.JobSplitting")</code> looks at every
        Python module in <code>src/python/T0/JobSplitting/</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>.get("Repack")</code> finds <code>RepackJobSplitter</code> in{" "}
        <code>RepackJobSplitter.py</code>, instantiates it, returns the
        instance.
      </>
    ),
  },
  {
    caption: (
      <>
        Same code path for Express, Merge, RepackMerge, ExpressMerge — each
        is just another file in <code>T0.JobSplitting</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        Adding a new splitter is a drop-in: write a new file with a class
        named for the splitter, and the factory finds it without code
        changes elsewhere.
      </>
    ),
  },
];

const SPLITTERS = [
  { id: "Repack", x: 580, y: 30, step: 3 },
  { id: "Express", x: 580, y: 110, step: 4 },
  { id: "Merge", x: 580, y: 190, step: 4 },
  { id: "RepackMerge", x: 580, y: 270, step: 4 },
];

export function D4_1_SplitterFactory() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });

  return (
    <DiagramShell
      tag="D4.1 — SplitterFactory dispatch"
      title="Plugin pattern: pick a splitter by name"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 800 340"
    >
      <ArrowheadDefs />

      <Node x={40} y={150} label="Tier0Feeder" sublabel="splitter call" state={tl.step >= 0 ? "active" : "hidden"} />

      <Node
        x={300}
        y={150}
        label="SplitterFactory"
        sublabel='package="T0.JobSplitting"'
        state={tl.step >= 1 ? (tl.step === 1 ? "active" : "visited") : "hidden"}
      />

      {SPLITTERS.map((s) => (
        <Node
          key={s.id}
          x={s.x}
          y={s.y}
          label={`${s.id}JobSplitter`}
          sublabel={`${s.id}JobSplitter.py`}
          state={
            tl.step >= s.step ? (tl.step === s.step ? "active" : "visited") : "hidden"
          }
        />
      ))}

      <Arrow d="M 172 178 L 296 178" show={tl.step >= 1} highlight={tl.step === 1} label='get("Repack")' labelPos={{ x: 230, y: 168 }} />

      {SPLITTERS.map((s) => {
        const startX = 432;
        const startY = 178;
        const endX = s.x;
        const endY = s.y + 28;
        const ctrlX = (startX + endX) / 2;
        const d = `M ${startX} ${startY} C ${ctrlX} ${startY}, ${ctrlX} ${endY}, ${endX - 4} ${endY}`;
        return (
          <Arrow
            key={`arr-${s.id}`}
            d={d}
            show={tl.step >= s.step}
            highlight={tl.step === s.step}
          />
        );
      })}
    </DiagramShell>
  );
}
