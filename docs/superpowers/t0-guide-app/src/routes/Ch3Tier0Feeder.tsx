import { ChapterShell } from "@/components/ChapterShell";

export function Ch3Tier0Feeder() {
  return (
    <ChapterShell
      eyebrow="Chapter 3"
      title="The Tier0Feeder heartbeat"
      subtitle="What happens on each tick of the feeder loop"
    >
      <h2>What you will learn</h2>
      <p>
        The five phases of <code>Tier0FeederPoller.algorithm</code>: configure
        runs/streams, feed splitters, release PromptReco, drive closeout,
        upload conditions.
      </p>
      <p style={{ color: "var(--muted)" }}>
        The Tier0Feeder tick simulator embeds here.
      </p>
    </ChapterShell>
  );
}
