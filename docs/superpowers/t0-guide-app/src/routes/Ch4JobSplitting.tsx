import { ChapterShell } from "@/components/ChapterShell";
import { JobSplittingSim } from "@/simulators/JobSplittingSim";

export function Ch4JobSplitting() {
  return (
    <ChapterShell
      eyebrow="Chapter 4"
      title="JobSplitting"
      subtitle="Repack and Express splitter algorithms"
    >
      <h2>The cap-then-cut idea</h2>
      <p>
        Splitters batch streamer files until <em>any</em> cap is hit (lumi,
        event count, payload size), then emit a job and start a fresh bucket.
        Switch between Repack and Express below to see how default caps
        differ.
      </p>

      <JobSplittingSim />

      <h2>How dispatch works</h2>
      <p>
        On each tick, the Tier0Feeder calls{" "}
        <code>SplitterFactory(package="T0.JobSplitting").get(name)</code>{" "}
        for each stream's configured splitter and invokes{" "}
        <code>split(streamers, …)</code>. The splitter decides job boundaries;
        the Tier0Feeder writes the resulting jobs into <code>WMBS_JOB</code>.
      </p>

      <p style={{ color: "var(--muted)" }}>
        D4.x splitter detail diagrams and the Repack vs Express comparison
        land here next.
      </p>
    </ChapterShell>
  );
}
