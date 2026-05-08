import { useTimeline } from "./shared/useTimeline";
import { DiagramShell, type StepSpec } from "./shared/DiagramShell";
import { ArrowheadDefs } from "./shared/primitives";
import { motion } from "framer-motion";

const SIGNALS = [
  { id: "data", label: "Data taking", color: "#5b8cff", startPct: 0, endPct: 0.18 },
  { id: "express", label: "Express done", color: "#36b37e", startPct: 0.18, endPct: 0.32 },
  { id: "alca", label: "AlcaHarvest done", color: "#9c5dff", startPct: 0.30, endPct: 0.50 },
  { id: "cond", label: "Conditions uploaded", color: "#ff9f43", startPct: 0.50, endPct: 0.62 },
  { id: "release", label: "CMSSW release announced", color: "#ff5b6e", startPct: 0.45, endPct: 0.85 },
  { id: "reco", label: "PromptReco done", color: "#22c8b8", startPct: 0.55, endPct: 0.98 },
];

const STEPS: StepSpec[] = [
  {
    caption: (
      <>
        Closeout doesn't fire as soon as data taking ends — it waits for
        downstream pipelines. Step through to see when each signal lands
        on a typical run timeline.
      </>
    ),
  },
  { caption: <><strong>t = 0</strong>: data taking starts. Streamers stream into the Storage Manager.</> },
  { caption: <><strong>t ≈ end-of-run + 5 min</strong>: Express jobs complete. AlCa skim files registered.</> },
  { caption: <><strong>t ≈ end-of-run + 30 min</strong>: AlcaHarvest workflow finishes; payloads land in T0DataSvcDB.</> },
  { caption: <><strong>t ≈ end-of-run + 1 h</strong>: ConditionUploadAPI POSTs payloads to Frontier; UPLOADED rows committed.</> },
  { caption: <><strong>t ≈ end-of-run + 6–24 h</strong>: a CMSSW release for the run is announced (manual step by experts).</> },
  { caption: <><strong>t ≈ end-of-run + days</strong>: PromptReco completes for all primary datasets.</> },
  {
    caption: (
      <>
        Only when <em>all</em> four convergence signals (streams, alca,
        conds, release) are present does <code>CloseRun</code> fire.
        PromptReco completion is downstream of closeout, not part of it.
      </>
    ),
  },
];

export function D5_4_CloseoutTiming() {
  const tl = useTimeline({ totalSteps: STEPS.length, msPerStep: 1100 });
  const baseX = 60;
  const baseY = 60;
  const trackWidth = 740;
  const rowH = 30;

  return (
    <DiagramShell
      tag="D5.4 — Closeout timing"
      title="When each signal lands on a typical run timeline"
      timeline={tl}
      steps={STEPS}
      viewBox="0 0 880 280"
    >
      <ArrowheadDefs />

      {/* Time axis */}
      <line x1={baseX} y1={250} x2={baseX + trackWidth} y2={250} stroke="var(--rule)" strokeWidth={1.5} />
      {[0, 0.25, 0.5, 0.75, 1].map((t) => (
        <g key={t}>
          <line
            x1={baseX + t * trackWidth}
            y1={246}
            x2={baseX + t * trackWidth}
            y2={254}
            stroke="var(--rule)"
            strokeWidth={1.5}
          />
          <text
            x={baseX + t * trackWidth}
            y={266}
            fontSize={10}
            textAnchor="middle"
            fill="var(--muted)"
          >
            {t === 0 ? "t = 0" : t === 1 ? "+24 h" : `+${Math.round(t * 24)} h`}
          </text>
        </g>
      ))}

      {SIGNALS.map((s, i) => {
        const visible = tl.step >= i + 1;
        const isActive = tl.step === i + 1;
        const startX = baseX + s.startPct * trackWidth;
        const endX = baseX + s.endPct * trackWidth;
        const y = baseY + i * rowH;
        return (
          <motion.g
            key={s.id}
            initial={false}
            animate={{ opacity: visible ? 1 : 0.2 }}
            transition={{ duration: 0.4 }}
          >
            <text
              x={baseX - 10}
              y={y + 14}
              fontSize={11}
              fontWeight={500}
              textAnchor="end"
              fill={isActive ? "var(--accent)" : "var(--fg)"}
            >
              {s.label}
            </text>
            <motion.rect
              x={startX}
              y={y + 2}
              width={endX - startX}
              height={rowH - 8}
              rx={4}
              fill={s.color}
              stroke={isActive ? "var(--accent)" : "transparent"}
              strokeWidth={2}
              initial={{ opacity: 0, scaleX: 0.4 }}
              animate={{
                opacity: visible ? 0.85 : 0.2,
                scaleX: visible ? 1 : 0.4,
              }}
              style={{ transformOrigin: `${startX}px ${y + 14}px` }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            />
          </motion.g>
        );
      })}

      {tl.step >= 7 ? (
        <motion.g
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4 }}
        >
          <line
            x1={baseX + 0.62 * trackWidth}
            y1={50}
            x2={baseX + 0.62 * trackWidth}
            y2={246}
            stroke="var(--accent)"
            strokeWidth={2}
            strokeDasharray="6 4"
          />
          <text
            x={baseX + 0.62 * trackWidth}
            y={42}
            textAnchor="middle"
            fontSize={11}
            fontWeight={600}
            fill="var(--accent)"
            letterSpacing="0.06em"
          >
            CLOSEOUT FIRES
          </text>
        </motion.g>
      ) : null}
    </DiagramShell>
  );
}
