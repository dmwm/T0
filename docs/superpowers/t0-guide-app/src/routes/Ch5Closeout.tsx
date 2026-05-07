import { ChapterShell } from "@/components/ChapterShell";
import { CloseoutSim } from "@/simulators/CloseoutSim";

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
        <em>detects</em> it. On each tick, the Tier0Feeder checks four
        independent signals; the moment they all line up, the run is closed.
      </p>

      <CloseoutSim />

      <h2>From AlcaHarvest output to PCL conditions</h2>
      <p>
        The AlcaHarvest workflow aggregates per-run histograms into{" "}
        <em>condition payloads</em>. The <code>ConditionUploadAPI</code> picks
        them up, normalises tag names, and posts them to Frontier — the
        production conditions database. PromptReco can then consume them.
      </p>

      <p style={{ color: "var(--muted)" }}>Content port in progress.</p>
    </ChapterShell>
  );
}
