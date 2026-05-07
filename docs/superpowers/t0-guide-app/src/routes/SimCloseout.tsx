import { ChapterShell } from "@/components/ChapterShell";

export function SimCloseout() {
  return (
    <ChapterShell
      eyebrow="Simulator"
      title="Closeout convergence"
      subtitle="Toggle four signals; see exactly when closeout fires"
      showPrevNext={false}
    >
      <p style={{ color: "var(--muted)" }}>Simulator implementation pending.</p>
    </ChapterShell>
  );
}
