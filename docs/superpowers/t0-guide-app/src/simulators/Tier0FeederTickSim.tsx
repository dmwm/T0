import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import styles from "./Tier0FeederTickSim.module.css";

interface Phase {
  id: string;
  label: string;
  hint: string;
  icon: string;
  daos: { call: string; comment?: string }[];
}

const PHASES: Phase[] = [
  {
    id: "configure",
    label: "Configure runs / streams",
    hint: "Pick up newly active runs from T0AST",
    icon: "⚙",
    daos: [
      {
        call: "FindNewRuns()",
        comment: "rows in RUN with no run_config row yet",
      },
      {
        call: "FindNewRunStreams()",
        comment: "new (run, stream) pairs from HLT config",
      },
      { call: "RunConfigAPI.configureRun(run)", comment: "writes RUN_CONFIG" },
      {
        call: "RunConfigAPI.configureRunStream(run, stream)",
        comment: "writes RUN_STREAM_CMSSW_VER and friends",
      },
    ],
  },
  {
    id: "splitter",
    label: "Feed splitters",
    hint: "Streamer files become Repack / Express jobs",
    icon: "✂",
    daos: [
      {
        call: 'SplitterFactory(package="T0.JobSplitting").get("Repack")',
        comment: "lookup plugin",
      },
      {
        call: "RepackJobSplitter.split(streamers)",
        comment: "by lumi cap and event count",
      },
      {
        call: "ExpressJobSplitter.split(streamers)",
        comment: "fast reco partition",
      },
      {
        call: "InsertSplitJobs(jobs)",
        comment: "rows into WMBS_JOB",
      },
    ],
  },
  {
    id: "reco",
    label: "Release PromptReco",
    hint: "Once a CMSSW release is announced",
    icon: "▶",
    daos: [
      {
        call: "FindNewlyReleasedRuns()",
        comment: "checks RELEASE_VERSION_ANNOUNCE",
      },
      {
        call: "RunConfigAPI.releasePromptReco(run)",
        comment: "creates PromptReco workflows",
      },
    ],
  },
  {
    id: "closeout",
    label: "Drive closeout",
    hint: "Convergence: streams, AlcaHarvest, conditions, release",
    icon: "✓",
    daos: [
      {
        call: "FindActiveStreamerRuns()",
        comment: "still expecting streamers?",
      },
      {
        call: "CheckAlcaHarvestStatus(run)",
        comment: "harvest workflow done?",
      },
      {
        call: "CloseRun(run)",
        comment: "fires only if ALL four signals are on",
      },
    ],
  },
  {
    id: "upload",
    label: "Upload conditions",
    hint: "PCL payloads → Frontier",
    icon: "☁",
    daos: [
      {
        call: "ConditionUploadAPI.findUploadable()",
        comment: "from T0DataSvcDB",
      },
      {
        call: "ConditionUploadAPI.uploadPayloads()",
        comment: "POST to Frontier",
      },
      {
        call: "ConditionUploadAPI.markUploaded()",
        comment: "ack + state transition",
      },
    ],
  },
];

interface LogEntry {
  id: number;
  tick: number;
  phaseId: string;
  call: string;
  comment?: string;
}

const SPEEDS = [1, 2, 4];

export function Tier0FeederTickSim() {
  const [tickCount, setTickCount] = useState(0);
  const [activePhaseIdx, setActivePhaseIdx] = useState(-1);
  const [completedPhases, setCompletedPhases] = useState(0);
  const [auto, setAuto] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [log, setLog] = useState<LogEntry[]>([]);
  const [running, setRunning] = useState(false);

  const seqRef = useRef(0);
  const timerRef = useRef<number | null>(null);
  const cancelRef = useRef(false);

  const cancelAll = () => {
    cancelRef.current = true;
    if (timerRef.current != null) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  };

  const runOneTick = async () => {
    if (running) return;
    setRunning(true);
    setActivePhaseIdx(-1);
    setCompletedPhases(0);
    cancelRef.current = false;
    const tickN = tickCount + 1;
    setTickCount(tickN);

    const wait = (ms: number) =>
      new Promise<void>((resolve) => {
        timerRef.current = window.setTimeout(resolve, ms);
      });

    for (let i = 0; i < PHASES.length; i++) {
      if (cancelRef.current) break;
      const phase = PHASES[i];
      setActivePhaseIdx(i);
      const newEntries: LogEntry[] = phase.daos.map((d) => ({
        id: ++seqRef.current,
        tick: tickN,
        phaseId: phase.id,
        call: d.call,
        comment: d.comment,
      }));
      setLog((prev) => [...prev, ...newEntries].slice(-60));
      await wait(700 / speed);
      setCompletedPhases(i + 1);
      await wait(80 / speed);
    }
    setActivePhaseIdx(-1);
    setRunning(false);
  };

  useEffect(() => {
    if (!auto || running) return;
    const id = window.setTimeout(() => {
      runOneTick();
    }, 600 / speed);
    return () => clearTimeout(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [auto, running, tickCount]);

  useEffect(() => () => cancelAll(), []);

  const reset = () => {
    cancelAll();
    setRunning(false);
    setAuto(false);
    setTickCount(0);
    setActivePhaseIdx(-1);
    setCompletedPhases(0);
    setLog([]);
  };

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <span className={styles.tag}>Simulator — Tier0Feeder tick</span>
          <span className={styles.title}>
            Watch the heartbeat fire all five phases in order
          </span>
        </div>
        <div className={styles.tickPill}>
          <span
            className={`${styles.tickDot} ${
              running ? styles.tickDotActive : ""
            }`}
          />
          tick #{tickCount}
        </div>
      </div>

      <div className={styles.phases}>
        {PHASES.map((p, i) => {
          const isActive = activePhaseIdx === i;
          const isDone = i < completedPhases;
          return (
            <motion.div
              key={p.id}
              className={`${styles.phase} ${isDone ? styles.phaseDone : ""} ${
                isActive ? styles.phaseActive : ""
              }`}
              animate={{
                scale: isActive ? 1.02 : 1,
              }}
            >
              <span className={styles.phaseN}>PHASE {i + 1}</span>
              <span className={styles.phaseIcon}>{p.icon}</span>
              <span className={styles.phaseLabel}>{p.label}</span>
              <span className={styles.phaseHint}>{p.hint}</span>
              {i < PHASES.length - 1 ? (
                <span
                  className={`${styles.phaseConn} ${
                    isDone ? styles.phaseConnDone : ""
                  }`}
                  aria-hidden="true"
                />
              ) : null}
            </motion.div>
          );
        })}
      </div>

      <div className={styles.log}>
        {log.length === 0 ? (
          <div className={styles.logEmpty}>
            DAO calls will appear here once you fire a tick.
          </div>
        ) : (
          log.map((e) => (
            <motion.div
              key={e.id}
              className={styles.logEntry}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            >
              <span className={styles.logTick}>t{e.tick}</span>
              <span className={styles.logPhase}>{e.phaseId.toUpperCase()}</span>
              <span className={styles.logCall}>
                <span>{e.call}</span>
                {e.comment ? (
                  <span className={styles.logComment}>// {e.comment}</span>
                ) : null}
              </span>
            </motion.div>
          ))
        )}
      </div>

      <div className={styles.controls}>
        <button
          className={`${styles.btn} ${styles.btnPrimary}`}
          onClick={runOneTick}
          disabled={running || auto}
        >
          ▶ Tick
        </button>
        <label className={styles.autoToggle}>
          <span
            className={`${styles.toggle} ${auto ? styles.toggleActive : ""}`}
            aria-hidden="true"
          >
            <motion.span
              className={styles.thumb}
              animate={{ x: auto ? 14 : 0 }}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          </span>
          <input
            type="checkbox"
            checked={auto}
            onChange={(e) => setAuto(e.target.checked)}
            style={{ display: "none" }}
          />
          Auto-tick
        </label>
        <button
          className={styles.btn}
          onClick={reset}
          disabled={running}
        >
          ⟲ Reset
        </button>
        <div className={styles.speed}>
          {SPEEDS.map((s) => (
            <button
              key={s}
              className={`${styles.speedBtn} ${
                speed === s ? styles.speedBtnActive : ""
              }`}
              onClick={() => setSpeed(s)}
            >
              {s}×
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
