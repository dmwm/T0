import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import styles from "./CloseoutSim.module.css";

interface Signal {
  id: string;
  label: string;
  hint: string;
  icon: string;
}

const SIGNALS: Signal[] = [
  {
    id: "streams",
    label: "All streams closed",
    hint: "End-of-run record + every Storage Manager streamer received",
    icon: "⏹",
  },
  {
    id: "alca",
    label: "AlcaHarvest finished",
    hint: "Histogram aggregation done; PCL inputs are ready",
    icon: "📊",
  },
  {
    id: "cond",
    label: "Conditions uploaded",
    hint: "ConditionUploadAPI dropped payloads to Frontier",
    icon: "📤",
  },
  {
    id: "release",
    label: "CMSSW release announced",
    hint: "PromptReco can finalise (also gates AOD/MINIAOD release)",
    icon: "📦",
  },
];

const CIRCUMFERENCE = 2 * Math.PI * 70;
const ARC = CIRCUMFERENCE / SIGNALS.length;
const GAP = 6;

export function CloseoutSim() {
  const [active, setActive] = useState<Record<string, boolean>>({
    streams: false,
    alca: false,
    cond: false,
    release: false,
  });
  const [fireCount, setFireCount] = useState(0);

  const onCount = SIGNALS.filter((s) => active[s.id]).length;
  const allOn = onCount === SIGNALS.length;
  const wasFired = fireCount > 0;

  useEffect(() => {
    if (allOn) {
      setFireCount((n) => n + 1);
    }
  }, [allOn]);

  const reset = () =>
    setActive({ streams: false, alca: false, cond: false, release: false });
  const lightAll = () =>
    setActive({ streams: true, alca: true, cond: true, release: true });

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <div className={styles.tag}>Simulator — Closeout convergence</div>
        <div className={styles.title}>
          Closeout fires only when all four signals are present
        </div>
      </div>

      <div className={styles.body}>
        <div className={styles.signals}>
          {SIGNALS.map((s) => {
            const isOn = active[s.id];
            return (
              <button
                key={s.id}
                className={`${styles.signal} ${
                  isOn ? styles.signalActive : ""
                }`}
                onClick={() =>
                  setActive((prev) => ({ ...prev, [s.id]: !prev[s.id] }))
                }
                aria-pressed={isOn}
              >
                <span className={styles.signalIcon}>{s.icon}</span>
                <span className={styles.signalText}>
                  <span className={styles.signalLabel}>{s.label}</span>
                  <span className={styles.signalHint}>{s.hint}</span>
                </span>
                <span
                  className={`${styles.toggle} ${
                    isOn ? styles.toggleActive : ""
                  }`}
                  aria-hidden="true"
                >
                  <motion.span
                    className={styles.thumb}
                    animate={{ x: isOn ? 16 : 0 }}
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                </span>
              </button>
            );
          })}
        </div>

        <div className={styles.viz}>
          <svg
            className={styles.svg}
            width="180"
            height="180"
            viewBox="0 0 180 180"
          >
            <circle
              cx="90"
              cy="90"
              r="70"
              fill="none"
              stroke="var(--rule)"
              strokeWidth="10"
              strokeDasharray={`${ARC - GAP} ${GAP}`}
              transform="rotate(-90 90 90)"
            />
            {SIGNALS.map((s, i) => {
              const isOn = active[s.id];
              const offset = -i * ARC;
              return (
                <motion.circle
                  key={s.id}
                  cx="90"
                  cy="90"
                  r="70"
                  fill="none"
                  stroke="var(--accent)"
                  strokeWidth="10"
                  strokeLinecap="butt"
                  strokeDasharray={`${ARC - GAP} ${CIRCUMFERENCE}`}
                  initial={false}
                  animate={{
                    strokeDashoffset: isOn
                      ? offset
                      : offset + (ARC - GAP),
                    opacity: isOn ? 1 : 0,
                  }}
                  transition={{
                    duration: 0.55,
                    ease: [0.16, 1, 0.3, 1],
                  }}
                  style={{ transform: "rotate(-90deg)", transformOrigin: "90px 90px" }}
                />
              );
            })}
            <AnimatePresence>
              {allOn ? (
                <motion.g
                  key="fired"
                  initial={{ scale: 0.7, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0.7, opacity: 0 }}
                  transition={{ type: "spring", stiffness: 320, damping: 22 }}
                  style={{ transformOrigin: "90px 90px" }}
                >
                  <circle cx="90" cy="90" r="48" fill="var(--accent)" />
                  <text
                    x="90"
                    y="86"
                    textAnchor="middle"
                    fontSize="11"
                    fontWeight={600}
                    fill="#fff"
                    letterSpacing="0.1em"
                  >
                    CLOSEOUT
                  </text>
                  <text
                    x="90"
                    y="100"
                    textAnchor="middle"
                    fontSize="13"
                    fontWeight={700}
                    fill="#fff"
                  >
                    FIRED
                  </text>
                </motion.g>
              ) : (
                <motion.text
                  key="counting"
                  x="90"
                  y="96"
                  textAnchor="middle"
                  fontSize="22"
                  fontWeight={700}
                  fill="var(--fg)"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  {onCount} / {SIGNALS.length}
                </motion.text>
              )}
            </AnimatePresence>
          </svg>

          <div
            className={`${styles.statusCard} ${
              allOn ? styles.statusFired : ""
            }`}
          >
            {allOn ? (
              <>
                Run closeout fires
                <div className={styles.statusFiredHint}>
                  Tier0Feeder marks the run closed in T0AST; helper agents
                  release.
                </div>
              </>
            ) : (
              <>
                Waiting on{" "}
                {SIGNALS.length - onCount} more signal
                {SIGNALS.length - onCount !== 1 ? "s" : ""}
              </>
            )}
          </div>
        </div>
      </div>

      <div className={styles.footer}>
        <button className={styles.btn} onClick={reset}>
          ⟲ Reset
        </button>
        <button className={styles.btn} onClick={lightAll}>
          ⚡ Light all four
        </button>
        <span className={styles.counter}>
          Closeout has fired{" "}
          <strong>{fireCount}</strong> time{fireCount !== 1 ? "s" : ""}
          {wasFired ? " in this session" : ""}
        </span>
      </div>
    </div>
  );
}
