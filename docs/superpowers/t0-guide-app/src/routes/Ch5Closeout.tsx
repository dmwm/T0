import { ChapterShell } from "@/components/ChapterShell";
import { CloseoutSim } from "@/simulators/CloseoutSim";
import { D5_1_CloseoutFlow } from "@/diagrams/D5_1_CloseoutFlow";
import { D5_2_AlcaHarvestPipe } from "@/diagrams/D5_2_AlcaHarvestPipe";
import { D5_3_ConditionUpload } from "@/diagrams/D5_3_ConditionUpload";
import { D5_4_CloseoutTiming } from "@/diagrams/D5_4_CloseoutTiming";

export function Ch5Closeout() {
  return (
    <ChapterShell
      eyebrow="Chapter 5"
      title="Closeout and condition uploads"
      subtitle="Convergence of streams, AlcaHarvest, conditions, releases"
    >
      <h2>Closeout is a convergence pattern</h2>
      <p>
        Tier-0 does not <em>orchestrate</em> the end of a run — it{" "}
        <em>detects</em> it. On every tick, the Tier0Feeder polls four
        independent signals; the moment all four are ready, the run is
        closed. The diagram below shows the convergence visually; the
        simulator below it lets you flip signals individually.
      </p>

      <D5_1_CloseoutFlow />

      <CloseoutSim />

      <h2>AlcaHarvest: from Express output to condition payloads</h2>
      <p>
        The AlcaHarvest workflow aggregates per-run histograms emitted by
        Express jobs into <em>condition payloads</em>. Each payload is a
        pickled IOV record keyed by tag.
      </p>

      <D5_2_AlcaHarvestPipe />

      <h2>The upload tick-loop</h2>
      <p>
        On each tick, <code>ConditionUploadAPI</code> picks up payloads in{" "}
        <code>READY</code> state and POSTs them to Frontier — the production
        conditions database. PromptReco can then consume them.
      </p>

      <D5_3_ConditionUpload />

      <h2>When does closeout actually fire?</h2>
      <p>
        Closeout doesn't fire as soon as data taking ends — it has to wait
        for downstream pipelines (Express, AlcaHarvest, ConditionUpload, plus
        the manual CMSSW release announcement). The timing diagram below
        sketches a typical run.
      </p>

      <D5_4_CloseoutTiming />
    </ChapterShell>
  );
}
