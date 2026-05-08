import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        An operator wants to test a config change before it lands in
        production. They open a PR with the proposed change.
      </>
    ),
  },
  {
    caption: (
      <>
        The operator types <code>may I replay?</code> as a PR comment.
        GitHub fires the <code>issue_comment</code> event into our
        workflow.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>deployReplayPR.yaml</code> checks the comment author against{" "}
        <code>AUTHORIZED_USERS</code> and prints current default replay
        parameters in a reply comment.
      </>
    ),
  },
  {
    caption: (
      <>
        Operator iterates. Once happy, they comment{" "}
        <code>run autoreplay</code> — the workflow deploys the PR's branch
        to a replay node from <code>ALLOWED_NODES</code>.
      </>
    ),
  },
  {
    caption: (
      <>
        On the replay node, <code>00_pypi_deploy_replay.sh</code> installs the
        T0 PyPI version pinned in the PR and starts a Tier0Feeder against
        the replay config.
      </>
    ),
  },
  {
    caption: (
      <>
        The replay runs against archived streamers; the operator monitors
        through Grafana. If it passes, the PR can merge to{" "}
        <code>master</code>.
      </>
    ),
  },
];

export function D6_2_ReplayByPR() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });
  const stateAt = (n: number) =>
    tl.step > n ? "visited" : tl.step === n ? "active" : "hidden";

  return (
    <DiagramShell
      tag="D6.2 — Replay by PR comment"
      title="From PR comment to replay running on a vocms node"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 920 320"
    >
      <ArrowheadDefs />

      <Node x={20} y={130} label="Operator" sublabel="opens PR" state={stateAt(0)} variant="external" />
      <Node x={200} y={130} label="GitHub PR" sublabel="comment trigger" state={stateAt(1)} />
      <Node x={400} y={50} label="deployReplayPR.yaml" sublabel="GitHub Actions" state={stateAt(2)} />
      <Node x={400} y={210} label="ALLOWED_NODES" sublabel="vocms* whitelist" state={stateAt(3)} />
      <Node x={620} y={130} label="00_pypi_deploy_replay.sh" sublabel="on replay node" state={stateAt(4)} />
      <Node x={830} y={130} label="Tier0Feeder" sublabel="replay run" state={stateAt(5)} />

      <Arrow d="M 152 158 L 198 158" show={tl.step >= 1} highlight={tl.step === 1} label="comment" labelPos={{ x: 175, y: 148 }} />
      <Arrow d="M 332 138 C 360 138, 380 100, 398 80" show={tl.step >= 2} highlight={tl.step === 2} label="trigger" labelPos={{ x: 366, y: 110 }} />
      <Arrow d="M 332 168 C 360 168, 380 200, 398 218" show={tl.step >= 3} highlight={tl.step === 3} label="autoreplay" labelPos={{ x: 366, y: 200 }} />
      <Arrow d="M 532 80 C 580 80, 600 130, 618 138" show={tl.step >= 4} highlight={tl.step === 4} />
      <Arrow d="M 532 238 C 580 238, 600 158, 618 158" show={tl.step >= 4} highlight={tl.step === 4} />
      <Arrow d="M 752 158 L 826 158" show={tl.step >= 5} highlight={tl.step === 5} />
    </DiagramShell>
  );
}
