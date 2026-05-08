import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        <code>RepackJobSplitter.split()</code> runs once per active stream
        per tick. It walks streamers in lumi order and decides where to cut.
      </>
    ),
  },
  {
    caption: (
      <>
        Each iteration reads the next streamer's <em>lumi count</em>,{" "}
        <em>event count</em>, and <em>file size</em>. They're added to a
        running tally for the current bucket.
      </>
    ),
  },
  {
    caption: (
      <>
        After every streamer, the splitter checks all caps:{" "}
        <code>maxSizeSingleLumi</code>, <code>maxEdmSize</code>,{" "}
        <code>maxOverSize</code>, …
      </>
    ),
  },
  {
    caption: (
      <>
        If any cap fires, the splitter emits one <code>WMBS_JOB</code> row
        for the current bucket and resets the tallies for the next one.
      </>
    ),
  },
  {
    caption: (
      <>
        At end of stream, the splitter emits any leftover bucket (even if
        no cap fired). The remaining streamers will be split on the next
        tick.
      </>
    ),
  },
];

const NODES = [
  { id: "loop", x: 40, y: 130, label: "for streamer in pending", hint: "lumi-ordered iteration", step: 0 },
  { id: "tally", x: 250, y: 50, label: "add to bucket", hint: "lumis += / events +=", step: 1 },
  { id: "checks", x: 470, y: 50, label: "check caps", hint: "any threshold hit?", step: 2 },
  { id: "emit", x: 470, y: 200, label: "emit WMBS_JOB", hint: "and reset bucket", step: 3 },
  { id: "leftover", x: 690, y: 130, label: "flush leftover", hint: "end of stream", step: 4 },
];

export function D4_2_RepackSplitter() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });
  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D4.2 — Repack splitter"
      title="Inside RepackJobSplitter.split()"
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

      <Arrow d="M 172 158 C 200 158, 230 90, 248 78" show={tl.step >= 1} highlight={tl.step === 1} />
      <Arrow d="M 382 78 L 468 78" show={tl.step >= 2} highlight={tl.step === 2} />
      <Arrow d="M 536 106 L 536 200" show={tl.step >= 3} highlight={tl.step === 3} label="cap hit" labelPos={{ x: 555, y: 156 }} />
      <Arrow d="M 470 226 C 360 226, 200 226, 106 158" show={tl.step >= 3} highlight={tl.step === 3} label="reset + continue" labelPos={{ x: 290, y: 218 }} />
      <Arrow d="M 602 78 C 660 78, 690 110, 690 130" show={tl.step >= 4} highlight={tl.step === 4} label="end-of-stream" labelPos={{ x: 660, y: 100 }} />
    </DiagramShell>
  );
}
