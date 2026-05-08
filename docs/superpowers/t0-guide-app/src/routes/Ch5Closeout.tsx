import { ChapterShell } from "@/components/ChapterShell";
import { CloseoutSim } from "@/simulators/CloseoutSim";
import { D5_1_CloseoutFlow } from "@/diagrams/D5_1_CloseoutFlow";

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

      <h2>From AlcaHarvest output to PCL conditions</h2>
      <p>
        The AlcaHarvest workflow aggregates per-run histograms into{" "}
        <em>condition payloads</em>. The <code>ConditionUploadAPI</code>{" "}
        picks them up, normalises tag names, and posts them to Frontier — the
        production conditions database. PromptReco can then consume them.
      </p>

      <p style={{ color: "var(--muted)" }}>
        D5.2 (AlcaHarvest pipe) and D5.3 (Condition upload) land here next.
      </p>
    </ChapterShell>
  );
}
