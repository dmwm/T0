import { ChapterShell } from "@/components/ChapterShell";
import { Tier0FeederTickSim } from "@/simulators/Tier0FeederTickSim";

export function Ch3Tier0Feeder() {
  return (
    <ChapterShell
      eyebrow="Chapter 3"
      title="The Tier0Feeder heartbeat"
      subtitle="What happens on each tick of the feeder loop"
    >
      <h2>The five-phase tick</h2>
      <p>
        <code>T0Component.Tier0Feeder.Tier0FeederPoller.algorithm</code> is the
        heart of the agent. It runs every poll interval (default 30s) and
        fires the same five phases. Press <strong>Tick</strong> below to see
        a single iteration; <strong>Auto-tick</strong> to watch the loop run.
      </p>

      <Tier0FeederTickSim />

      <h2>Idempotency by design</h2>
      <p>
        Each phase looks for <em>work that hasn't been done yet</em> in T0AST
        and writes a state row only if needed. Crash recovery is therefore
        free — the next tick will re-run the queries and pick up where it
        left off.
      </p>

      <h2>Multi-DB connectivity</h2>
      <p>
        The Tier0Feeder talks to several Oracle databases on every tick:
        T0AST (local agent state), HLTConfDB (which streams exist for which
        runs), the Storage Manager DB (streamer files), and optionally
        SMNotifyDB / PopConLogDB / T0DataSvcDB depending on configuration.
      </p>

      <p style={{ color: "var(--muted)" }}>
        D3.1 phase flow + D3.2 multi-DB layout + D3.3 Main vs Helper agent
        diagrams land here next.
      </p>
    </ChapterShell>
  );
}
