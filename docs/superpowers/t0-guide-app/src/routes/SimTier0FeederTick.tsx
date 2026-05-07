import { ChapterShell } from "@/components/ChapterShell";
import { Tier0FeederTickSim } from "@/simulators/Tier0FeederTickSim";

export function SimTier0FeederTick() {
  return (
    <ChapterShell
      eyebrow="Simulator"
      title="Tier0Feeder tick"
      subtitle="Watch the heartbeat fire all five phases in order"
      showPrevNext={false}
    >
      <p>
        The agent's main loop is{" "}
        <code>
          T0Component.Tier0Feeder.Tier0FeederPoller.algorithm
        </code>
        . On every heartbeat it fires the same five phases — each one a
        lookup against T0AST, then a DAO write. Press <strong>Tick</strong>{" "}
        to step through one iteration, or flip <strong>Auto-tick</strong>{" "}
        on to see the loop run continuously.
      </p>

      <Tier0FeederTickSim />

      <h2>Why this design holds up</h2>
      <p>
        Notice that every phase is idempotent: it queries for{" "}
        <em>work that hasn't been done yet</em> and writes a row only if
        needed. A crash mid-tick is harmless — the next tick re-runs the
        query and continues. There is no in-memory queue: T0AST is the only
        durable state.
      </p>

      <h2>What the DAO log shows you</h2>
      <p>
        Every call in the log corresponds to a real DAO under{" "}
        <code>src/python/T0/WMBS/Oracle/&lt;area&gt;/&lt;Verb&gt;&lt;Noun&gt;.py</code>{" "}
        accessed through{" "}
        <code>DAOFactory(package="T0.WMBS", classname=...)</code>. Read those
        files alongside this simulator and the loop becomes very concrete.
      </p>
    </ChapterShell>
  );
}
