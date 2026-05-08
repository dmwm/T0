import { ChapterShell } from "@/components/ChapterShell";
import { D1_1_PipelineHero } from "@/diagrams/D1_1_PipelineHero";
import { D1_2_TwoDBLayout } from "@/diagrams/D1_2_TwoDBLayout";
import { D1_3_MultiDBConnectivity } from "@/diagrams/D1_3_MultiDBConnectivity";
import { D1_4_DeployTopology } from "@/diagrams/D1_4_DeployTopology";

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
        workflows that turn them into archived datasets and PCL conditions
        for Frontier. By the end of this chapter you should be able to
        describe end-to-end how one streamer's content lands in CASTOR and
        how its calibration histograms reach Frontier.
      </p>

      <p>
        Press <strong>Play</strong> on the diagram below — or step through
        with the arrow keys — to see one streamer's journey through the
        chain.
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

      <h2>Two databases — one for the agent, one for the jobs</h2>
      <p>
        Tier-0 uses two distinct Oracle schemas. <strong>T0AST</strong> holds
        Tier-0's own state (runs, streams, closeout signals).{" "}
        <strong>WMBS</strong> is the standard WMAgent execution database
        (jobs, files, filesets). The Tier0Feeder writes to both; WMAgent's
        job submitters read only WMBS.
      </p>

      <D1_2_TwoDBLayout />

      <h2>How many databases really?</h2>
      <p>
        On every tick the Tier0Feeder may also reach out to up to four
        additional Oracle DBs — three mandatory read paths (HLT config,
        Storage Manager files, …) and three optional write paths
        (notification, audit, monitoring). Each is a separate{" "}
        <code>DBFactory</code> in the agent config.
      </p>

      <D1_3_MultiDBConnectivity />

      <h2>Where this actually runs</h2>
      <p>
        Production Tier-0 runs on four <code>vocms</code> hosts at CERN as
        the <code>cmst0</code> user. <code>vocms047</code> is the Main agent;
        the other three are Helpers (which we'll explain in Chapter 3).
        Source of truth is the <code>master</code> branch of this repo, and
        each host pins its own <code>TIER0_VERSION</code>.
      </p>

      <D1_4_DeployTopology />

      <h2>What is in T0AST</h2>
      <p>
        Every state transition the agent makes is durable in the{" "}
        <strong>T0AST</strong> Oracle schema. There is no in-memory queue —
        a crash in the agent is a no-op for the pipeline; a restart picks up
        from the last committed row. We will see this pattern again and
        again.
      </p>

      <h2>Where to go next</h2>
      <p>
        Chapter 2 unpacks the <code>Tier0Config</code> DSL — how operators
        encode "what should happen for this run" in Python and how the agent
        translates that into T0AST rows. Chapter 3 then dives into the
        Tier0Feeder heartbeat itself.
      </p>
    </ChapterShell>
  );
}
