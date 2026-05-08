import { ChapterShell } from "@/components/ChapterShell";
import { Tier0FeederTickSim } from "@/simulators/Tier0FeederTickSim";
import { D3_1_Tier0FeederTick } from "@/diagrams/D3_1_Tier0FeederTick";
import { D3_2_MultiAgentSplit } from "@/diagrams/D3_2_MultiAgentSplit";

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
        fires the same five phases — the diagram below walks through them
        one at a time, and the simulator below it lets you fire ticks live.
      </p>

      <D3_1_Tier0FeederTick />

      <Tier0FeederTickSim />

      <h2>Idempotency by design</h2>
      <p>
        Each phase looks for <em>work that hasn't been done yet</em> in T0AST
        and writes a state row only if needed. Crash recovery is therefore
        free — the next tick will re-run the queries and pick up where it
        left off.
      </p>

      <h2>The Main / Helper agent split</h2>
      <p>
        Tier-0 doesn't run as a single agent — it runs as one Main agent
        plus N Helper agents. The split is declared in the Tier0Config:{" "}
        <code>HelperAgentStreams</code> maps each Helper to the streams it
        owns, and Main takes everything else. Each agent is a separate
        process on a separate <code>vocms</code> host.
      </p>

      <D3_2_MultiAgentSplit />

      <h2>Multi-DB connectivity</h2>
      <p>
        Every tick may reach into up to six Oracle DBs (we covered them in
        Chapter 1). All connections are configured at agent start; the
        Tier0Feeder caches them and re-uses them across ticks.
      </p>

      <p style={{ color: "var(--muted)" }}>
        D3.3 (Storage Manager polling) and D3.4 (splitter dispatch detail)
        land here next.
      </p>
    </ChapterShell>
  );
}
