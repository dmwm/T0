import { ChapterShell } from "@/components/ChapterShell";

export function Ch1Overview() {
  return (
    <ChapterShell
      eyebrow="Chapter 1"
      title="The pipeline at a glance"
      subtitle="Storage Manager → Tier0Feeder → Repack/Express → PromptReco → AlcaHarvest → Archive"
    >
      <h2>What you will learn</h2>
      <p>
        This chapter introduces the Tier-0 (T0) processing chain and the four
        offline workflows that turn raw streamer files into archived datasets
        and PCL conditions.
      </p>
      <p style={{ color: "var(--muted)" }}>
        Content port in progress — the pipeline hero diagram and prose land
        here next.
      </p>
    </ChapterShell>
  );
}
