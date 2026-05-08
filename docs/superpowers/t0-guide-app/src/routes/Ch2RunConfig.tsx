import { ChapterShell } from "@/components/ChapterShell";
import { D2_1_RunConfigFlow } from "@/diagrams/D2_1_RunConfigFlow";
import { LifecycleSim } from "@/simulators/LifecycleSim";

export function Ch2RunConfig() {
  return (
    <ChapterShell
      eyebrow="Chapter 2"
      title="RunConfig and the Tier0Config DSL"
      subtitle="How operator-edited configs become T0AST rows"
    >
      <h2>The DSL is just Python</h2>
      <p>
        <code>etc/ProdOfflineConfiguration.py</code> looks like a Python
        script — and it is. It calls a small set of setter functions defined
        in <code>src/python/T0/RunConfig/Tier0Config.py</code>. WMAgent loads
        it, executes it, and ends up with an in-memory tree of run / stream
        configuration. The Tier0Feeder then translates that tree into T0AST
        rows on the run's first appearance.
      </p>

      <D2_1_RunConfigFlow />

      <h2>The run / stream / job state machine</h2>
      <p>
        Once the run row exists in T0AST, every later state transition lives
        as another row in T0AST. The simulator below lets you step a run, a
        stream, or a job through every state and watch the DAOs fire.
      </p>

      <LifecycleSim />

      <p style={{ color: "var(--muted)" }}>
        D2.2 / D2.3 / D2.4 detail diagrams (state machine, DSL setter
        timeline) land here next.
      </p>
    </ChapterShell>
  );
}
