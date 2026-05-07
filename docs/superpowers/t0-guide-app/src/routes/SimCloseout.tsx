import { ChapterShell } from "@/components/ChapterShell";
import { CloseoutSim } from "@/simulators/CloseoutSim";

export function SimCloseout() {
  return (
    <ChapterShell
      eyebrow="Simulator"
      title="Closeout convergence"
      subtitle="Toggle four signals; see exactly when closeout fires"
      showPrevNext={false}
    >
      <p>
        Run closeout in T0 is a <strong>convergence pattern</strong>: the
        Tier0Feeder is checking, on every tick, whether four independent
        signals have all flipped to "ready" for a given run. The moment they
        all line up, the run is marked closed and downstream cleanup
        proceeds.
      </p>

      <CloseoutSim />

      <h2>Why convergence (not orchestration)</h2>
      <p>
        The agent never <em>orchestrates</em> closeout — it only checks
        invariants. This is robust against partial failures: if any one
        signal disappears (e.g. a re-released CMSSW version, or a streamer
        arriving late from Storage Manager), the run automatically falls
        back into "waiting" and resumes when the signal returns.
      </p>

      <h2>What each signal really is</h2>
      <ul>
        <li>
          <strong>All streams closed</strong> — every stream has its end-of-run
          row in <code>STREAMER</code> and <code>RUN_STREAM_DONE</code>; the
          Storage Manager has reported "no more for this run".
        </li>
        <li>
          <strong>AlcaHarvest finished</strong> — the AlcaHarvest workflow
          for the run has succeeded, and condition payloads are sitting in
          the upload queue.
        </li>
        <li>
          <strong>Conditions uploaded</strong> — <code>ConditionUploadAPI</code>{" "}
          has handed every payload to Frontier; reflected in T0DataSvcDB.
        </li>
        <li>
          <strong>Release announced</strong> — a CMSSW release for the run is
          available, gating PromptReco and AOD/MINIAOD finalisation.
        </li>
      </ul>
    </ChapterShell>
  );
}
