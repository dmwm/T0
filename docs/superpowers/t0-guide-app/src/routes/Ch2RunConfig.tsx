import { ChapterShell } from "@/components/ChapterShell";

export function Ch2RunConfig() {
  return (
    <ChapterShell
      eyebrow="Chapter 2"
      title="RunConfig and the Tier0Config DSL"
      subtitle="How operator-edited configs become T0AST rows"
    >
      <h2>What you will learn</h2>
      <p>
        How <code>etc/*OfflineConfiguration.py</code> turns into rows in the T0AST
        schema, what the DSL is, and how <code>configureRun</code> /
        <code> configureRunStream</code> translate Python objects into DAOs.
      </p>
      <p style={{ color: "var(--muted)" }}>Content port in progress.</p>
    </ChapterShell>
  );
}
