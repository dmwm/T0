import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs, Arrow, Node } from "./shared/primitives";
import { motion } from "framer-motion";

interface Stream {
  id: string;
  label: string;
  owner: "main" | "helper2" | "helper3";
  step: number;
}

const STREAMS: Stream[] = [
  { id: "Physics", label: "Physics", owner: "main", step: 1 },
  { id: "Express", label: "Express", owner: "main", step: 1 },
  { id: "AlCaPhi", label: "AlCaPhi", owner: "helper2", step: 2 },
  { id: "AlCaLumi", label: "AlCaLumi", owner: "helper2", step: 2 },
  { id: "DQM", label: "DQM", owner: "helper3", step: 3 },
  { id: "EventDisplay", label: "EventDisplay", owner: "helper3", step: 3 },
];

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Tier-0 runs as <strong>multiple agents</strong>. The Main agent on
        vocms047 owns most streams; one or more Helper agents take a
        configured subset. The split is declared in the Tier0Config.
      </>
    ),
  },
  {
    caption: (
      <>
        Streams not listed in <code>HelperAgentStreams</code> belong to the{" "}
        <strong>Main</strong> agent: <code>Physics</code>,{" "}
        <code>Express</code>, …
      </>
    ),
  },
  {
    caption: (
      <>
        <code>HelperAgentStreams[helper2]</code> = ['AlCaPhi', 'AlCaLumi'].
        Helper 2 polls T0AST for those streams only.
      </>
    ),
  },
  {
    caption: (
      <>
        <code>HelperAgentStreams[helper3]</code> = ['DQM', 'EventDisplay'].
        Each helper agent has its own deploy host and own WMAgent process.
      </>
    ),
  },
  {
    caption: (
      <>
        Why split? Express and DQM streams have very different cadences;
        running them in different processes lets one stall without halting
        the others.
      </>
    ),
  },
];

export function D3_2_MultiAgentSplit() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1300 });

  const colorOf: Record<Stream["owner"], string> = {
    main: "var(--accent)",
    helper2: "#4f86ff",
    helper3: "#36b37e",
  };

  return (
    <DiagramShell
      tag="D3.2 — Main vs Helper agents"
      title="HelperAgentStreams partitions the work across agents"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 920 320"
    >
      <ArrowheadDefs />

      <text x={20} y={36} fontSize={11} fontWeight={600} fill="var(--muted)" letterSpacing="0.06em">
        STREAMS IN T0AST
      </text>

      {STREAMS.map((s, i) => {
        const visible = tl.step >= s.step;
        const isActive = tl.step === s.step;
        const x = 20 + (i % 3) * 130;
        const y = 56 + Math.floor(i / 3) * 56;
        return (
          <motion.g
            key={s.id}
            initial={false}
            animate={{ opacity: visible ? 1 : 0.2 }}
            transition={{ duration: 0.4 }}
          >
            <rect
              x={x}
              y={y}
              width={120}
              height={42}
              rx={9}
              fill="var(--bg-elevated)"
              stroke={visible ? colorOf[s.owner] : "var(--rule)"}
              strokeWidth={isActive ? 2.4 : 1.5}
            />
            <text
              x={x + 60}
              y={y + 18}
              textAnchor="middle"
              fontSize={11.5}
              fontWeight={600}
              fill="var(--fg)"
            >
              {s.label}
            </text>
            <text
              x={x + 60}
              y={y + 32}
              textAnchor="middle"
              fontSize={9.5}
              fill={visible ? colorOf[s.owner] : "var(--muted)"}
              letterSpacing="0.06em"
            >
              → {s.owner.toUpperCase()}
            </text>
          </motion.g>
        );
      })}

      <g>
        <Node x={500} y={50} label="Main agent" sublabel="vocms047" state={tl.step >= 1 ? "active" : "hidden"} />
        <Node x={500} y={140} label="Helper #2" sublabel="vocms0500" state={tl.step >= 2 ? "active" : "hidden"} />
        <Node x={500} y={230} label="Helper #3" sublabel="vocms05011" state={tl.step >= 3 ? "active" : "hidden"} />
      </g>

      {STREAMS.map((s, i) => {
        const visible = tl.step >= s.step;
        const x = 20 + (i % 3) * 130 + 120;
        const y = 56 + Math.floor(i / 3) * 56 + 22;
        const targetY = s.owner === "main" ? 78 : s.owner === "helper2" ? 168 : 258;
        const d = `M ${x} ${y} C ${(x + 500) / 2} ${y}, ${(x + 500) / 2} ${targetY}, 500 ${targetY}`;
        return (
          <Arrow
            key={`arr-${s.id}`}
            d={d}
            show={visible}
            highlight={tl.step === s.step}
          />
        );
      })}

      {tl.step >= 4 ? (
        <motion.g
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <text x={680} y={50} fontSize={11} fontWeight={600} fill="var(--muted)" letterSpacing="0.06em">
            ISOLATION BENEFIT
          </text>
          <text x={680} y={80} fontSize={12} fill="var(--fg)">Express stalls →</text>
          <text x={680} y={98} fontSize={12} fill="var(--fg)">Main paused</text>
          <text x={680} y={130} fontSize={12} fill="var(--fg)">Helpers keep</text>
          <text x={680} y={148} fontSize={12} fill="var(--fg)">making progress</text>
        </motion.g>
      ) : null}
    </DiagramShell>
  );
}
