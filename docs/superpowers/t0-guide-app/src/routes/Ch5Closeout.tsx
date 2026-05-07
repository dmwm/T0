import { ChapterShell } from "@/components/ChapterShell";

export function Ch5Closeout() {
  return (
    <ChapterShell
      eyebrow="Chapter 5"
      title="Closeout and condition uploads"
      subtitle="Convergence of streams, AlcaHarvest, conditions, releases"
    >
      <h2>What you will learn</h2>
      <p>
        The four-signal convergence pattern that gates closeout, plus how
        AlcaHarvest output becomes PCL conditions via{" "}
        <code>ConditionUploadAPI</code>.
      </p>
      <p style={{ color: "var(--muted)" }}>
        The Closeout simulator embeds here.
      </p>
    </ChapterShell>
  );
}
