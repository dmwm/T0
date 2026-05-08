import { ChapterShell } from "@/components/ChapterShell";
import { D2_1_RunConfigFlow } from "@/diagrams/D2_1_RunConfigFlow";
import { D2_2_RunStates } from "@/diagrams/D2_2_RunStates";
import { D2_3_StreamStates } from "@/diagrams/D2_3_StreamStates";
import { D2_4_DSLTimeline } from "@/diagrams/D2_4_DSLTimeline";
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

      <h2>What the setters look like in practice</h2>
      <p>
        A typical <code>ProdOfflineConfiguration.py</code> reads top-down:
        global settings, dataset list, per-dataset Repack / Express config,
        helper-agent partition. The diagram below walks through one such
        file and shows which field of <code>Tier0Config</code> each setter
        mutates.
      </p>

      <D2_4_DSLTimeline />

      <h2>The run / stream / job state machine</h2>
      <p>
        Once the run row exists in T0AST, every later state transition lives
        as another row in T0AST. The simulator below lets you step a run, a
        stream, or a job through every state and watch the DAOs fire.
      </p>

      <LifecycleSim />

      <h2>Run state machine reference</h2>
      <p>
        Five states a run passes through. The simulator above lets you fire
        them interactively; the diagram below shows them all together.
      </p>

      <D2_2_RunStates />

      <h2>Stream state machine reference</h2>
      <p>
        Streams have a flatter four-state shape. The Storage Manager's
        end-of-run record is what triggers the SPLITTING → SPLIT_DONE
        transition.
      </p>

      <D2_3_StreamStates />
    </ChapterShell>
  );
}
