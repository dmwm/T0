import { ChapterShell } from "@/components/ChapterShell";
import { D1_1_PipelineHero } from "@/diagrams/D1_1_PipelineHero";

export function Ch1Overview() {
  return (
    <ChapterShell
      eyebrow="Chapter 1"
      title="The pipeline at a glance"
      subtitle="Storage Manager → Tier0Feeder → Repack/Express → PromptReco → AlcaHarvest → Archive"
    >
      <h2>What you will learn</h2>
      <p>
        Tier-0 (T0) ingests <em>streamer files</em> from the online{" "}
        <strong>Storage Manager</strong> at Point 5 and drives four offline
        workflows that turn them into archived datasets and PCL conditions for
        Frontier.
      </p>

      <p>
        Press <strong>Play</strong> on the diagram below — or step through with
        the arrow keys — to see one streamer's journey through the chain.
      </p>

      <D1_1_PipelineHero />

      <h2>The four offline workflows</h2>
      <p>
        Each workflow is a WMAgent <em>spec</em> instantiated per
        run / stream / dataset:
      </p>
      <ul>
        <li>
          <strong>Repack</strong> — packs streamer files into RAW
          datasets, partitioned by primary dataset.
        </li>
        <li>
          <strong>Express</strong> — fast reconstruction for monitoring,
          alignment streams, and the AlCa input.
        </li>
        <li>
          <strong>PromptReco</strong> — full reconstruction; releases once a
          CMSSW release is announced for the run.
        </li>
        <li>
          <strong>AlcaHarvest</strong> — aggregates calibration histograms;
          its outputs feed the PCL condition uploads.
        </li>
      </ul>

      <h2>What is in T0AST</h2>
      <p>
        Every state transition the agent makes is durable in the{" "}
        <strong>T0AST</strong> Oracle schema. There is no in-memory queue —
        a crash in the agent is a no-op for the pipeline; a restart picks up
        from the last committed row. We will see this pattern again and again.
      </p>

      <p style={{ color: "var(--muted)" }}>
        More content in this chapter lands as we port from v1.
      </p>
    </ChapterShell>
  );
}
