import { ChapterShell } from "@/components/ChapterShell";

export function Ch4JobSplitting() {
  return (
    <ChapterShell
      eyebrow="Chapter 4"
      title="JobSplitting"
      subtitle="Repack and Express splitter algorithms"
    >
      <h2>What you will learn</h2>
      <p>
        How <code>SplitterFactory(package="T0.JobSplitting")</code> dispatches
        to splitter plugins, how Repack vs Express differ, and what the lumi /
        event / time thresholds do.
      </p>
      <p style={{ color: "var(--muted)" }}>
        The JobSplitting simulator embeds here.
      </p>
    </ChapterShell>
  );
}
