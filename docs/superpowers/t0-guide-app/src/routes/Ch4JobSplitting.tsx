import { ChapterShell } from "@/components/ChapterShell";
import { JobSplittingSim } from "@/simulators/JobSplittingSim";
import { D4_1_SplitterFactory } from "@/diagrams/D4_1_SplitterFactory";
import { D4_4_SplitterMatrix } from "@/diagrams/D4_4_SplitterMatrix";

export function Ch4JobSplitting() {
  return (
    <ChapterShell
      eyebrow="Chapter 4"
      title="JobSplitting"
      subtitle="Repack and Express splitter algorithms"
    >
      <h2>The plugin pattern</h2>
      <p>
        Job splitting in Tier-0 is plugin-based. The Tier0Feeder doesn't know
        anything specific about Repack or Express — it asks{" "}
        <code>SplitterFactory(package="T0.JobSplitting")</code> for a
        splitter by name and calls <code>split(streamers, …)</code> on
        whatever comes back. This is what lets us add new splitters
        (RepackMerge, ExpressMerge, …) without touching the core agent.
      </p>

      <D4_1_SplitterFactory />

      <h2>The cap-then-cut idea</h2>
      <p>
        Splitters batch streamer files until <em>any</em> cap is hit (lumi,
        event count, payload size), then emit a job and start a fresh bucket.
        Switch between Repack and Express below to see how default caps
        differ in practice.
      </p>

      <JobSplittingSim />

      <h2>Side by side</h2>
      <p>
        Repack and Express share machinery but use very different defaults
        because they serve different purposes. The matrix below shows the
        contrasts.
      </p>

      <D4_4_SplitterMatrix />

      <p style={{ color: "var(--muted)" }}>
        D4.2 (Repack splitter detail) and D4.3 (Express splitter detail)
        land here next.
      </p>
    </ChapterShell>
  );
}
