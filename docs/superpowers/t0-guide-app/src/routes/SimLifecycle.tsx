import { ChapterShell } from "@/components/ChapterShell";
import { LifecycleSim } from "@/simulators/LifecycleSim";

export function SimLifecycle() {
  return (
    <ChapterShell
      eyebrow="Simulator"
      title="Run / Stream / Job lifecycle"
      subtitle="Step a run through each state; see DAOs fire on each transition"
      showPrevNext={false}
    >
      <p>
        Three nested state machines drive Tier-0: the <strong>run</strong> at
        the top, <strong>streams</strong> within a run, and{" "}
        <strong>jobs</strong> within streams. Each state lives as a row in
        T0AST; every transition is one or more DAO writes. Pick a machine and
        click an outgoing transition to fire it.
      </p>

      <LifecycleSim />

      <h2>Why three machines, not one</h2>
      <p>
        The agent decomposes the work this way for two reasons. First, runs
        have very different lifetimes from jobs (hours / days vs seconds /
        minutes), so they need different polling cadences. Second, the
        Main / Helper agent split partitions <em>streams</em>, not runs — so
        the stream machine has to be self-contained.
      </p>

      <h2>What you can read along with this</h2>
      <p>
        The DAO names in the trace correspond to files under{" "}
        <code>src/python/T0/WMBS/Oracle/</code>. The state-changing logic is
        in <code>src/python/T0/RunConfig/RunConfigAPI.py</code> and{" "}
        <code>T0Component/Tier0Feeder/Tier0FeederPoller.py</code>.
      </p>
    </ChapterShell>
  );
}
