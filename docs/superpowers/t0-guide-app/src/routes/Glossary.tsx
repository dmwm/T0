import { ChapterShell } from "@/components/ChapterShell";

export function Glossary() {
  return (
    <ChapterShell
      eyebrow="Reference"
      title="Glossary"
      subtitle="Quick lookup for the terminology that runs through the guide"
      showPrevNext={false}
    >
      <p style={{ color: "var(--muted)" }}>
        Terms grouped by area land here (architecture, processing, deploy).
      </p>
    </ChapterShell>
  );
}
