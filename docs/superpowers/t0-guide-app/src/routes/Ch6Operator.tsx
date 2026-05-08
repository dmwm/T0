import { ChapterShell } from "@/components/ChapterShell";
import { D6_1_OperatorCLI } from "@/diagrams/D6_1_OperatorCLI";

export function Ch6Operator() {
  return (
    <ChapterShell
      eyebrow="Chapter 6"
      title="Operator surface and recap"
      subtitle="bin/t0, replay-by-PR, multi-agent split"
    >
      <h2>The operator CLI</h2>
      <p>
        Every operational task on a deploy host is a <code>bin/t0</code>{" "}
        invocation. There is no web admin console; the CLI is the surface.
      </p>

      <D6_1_OperatorCLI />

      <h2>Replay by PR comment</h2>
      <p>
        For pre-production validation, operators run replays — re-processing
        archived data with new code. The workflow{" "}
        <code>.github/workflows/deployReplayPR.yaml</code> turns this into a
        PR-comment interaction:
      </p>
      <ul>
        <li>
          <code>may I replay?</code> — bot replies with current default
          parameters and node availability
        </li>
        <li>
          <code>verify nodes</code> — bot prints HTCondor queue depth on
          each replay node
        </li>
        <li>
          <code>run autoreplay</code> — bot deploys the PR's replay config
          and starts the replay
        </li>
      </ul>
      <p>
        Authorisation is a hard-coded list of GitHub usernames (the{" "}
        <code>AUTHORIZED_USERS</code> env var in the workflow); only those
        users can trigger a deploy.
      </p>

      <h2>Recap</h2>
      <p>
        You should now have a mental model for: the four offline workflows
        and how they hand off; the heartbeat loop's five phases; how the
        Tier0Config DSL becomes T0AST rows; how splitters cut streamers
        into jobs; how closeout converges. The remaining chapters of the
        guide and the simulators are reinforcement — come back to whichever
        one is the most fuzzy.
      </p>

      <p style={{ color: "var(--muted)" }}>
        D6.2 (replay-by-PR workflow) and D6.3 (deploy script flow) land
        here next.
      </p>
    </ChapterShell>
  );
}
