import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowheadDefs } from "@/diagrams/shared/primitives";
import styles from "./LifecycleSim.module.css";

type Mode = "run" | "stream" | "job";

interface Transition {
  from: string;
  to: string;
  label: string;
  daos: string[];
}

interface MachineSpec {
  states: { id: string; label: string; x: number; y: number }[];
  transitions: Transition[];
  initial: string;
  hint: Record<string, string>;
}

const RUN_MACHINE: MachineSpec = {
  initial: "new",
  states: [
    { id: "new", label: "new", x: 60, y: 130 },
    { id: "configured", label: "configured", x: 200, y: 130 },
    { id: "active", label: "active", x: 340, y: 130 },
    { id: "released", label: "release\nannounced", x: 480, y: 50 },
    { id: "closed", label: "closed", x: 480, y: 210 },
  ],
  transitions: [
    {
      from: "new",
      to: "configured",
      label: "configureRun",
      daos: ["FindNewRuns", "RunConfigAPI.configureRun(run)", "InsertRun(run)"],
    },
    {
      from: "configured",
      to: "active",
      label: "first streamer",
      daos: ["InsertRunStream(run, stream)", "InsertStreamer(streamer)"],
    },
    {
      from: "active",
      to: "released",
      label: "CMSSW announced",
      daos: [
        "FindNewlyReleasedRuns()",
        "RunConfigAPI.releasePromptReco(run)",
      ],
    },
    {
      from: "active",
      to: "closed",
      label: "all four signals",
      daos: ["CheckClosable(run)", "CloseRun(run)", "MarkRunClosed"],
    },
    {
      from: "released",
      to: "closed",
      label: "closeout converges",
      daos: ["CloseRun(run)"],
    },
  ],
  hint: {
    new: "Run row exists in T0AST but no run-config row yet.",
    configured: "Run-config and run-stream rows are written.",
    active: "Streamers arriving; splitters are partitioning into jobs.",
    released:
      "PromptReco workflows have been created; AOD/MINIAOD release pending.",
    closed:
      "Closeout convergence fired. The run is done from Tier-0's perspective.",
  },
};

const STREAM_MACHINE: MachineSpec = {
  initial: "open",
  states: [
    { id: "open", label: "open", x: 90, y: 130 },
    { id: "splitting", label: "splitting", x: 250, y: 130 },
    { id: "split-done", label: "split done", x: 410, y: 130 },
    { id: "closed", label: "closed", x: 570, y: 130 },
  ],
  transitions: [
    {
      from: "open",
      to: "splitting",
      label: "first streamer",
      daos: [
        'SplitterFactory("T0.JobSplitting").get("Repack")',
        "InsertSplitJobs(jobs)",
      ],
    },
    {
      from: "splitting",
      to: "split-done",
      label: "no more streamers",
      daos: ["FindActiveStreams(run)", "MarkSplitDone(run, stream)"],
    },
    {
      from: "split-done",
      to: "closed",
      label: "feeder closes",
      daos: ["CloseStream(run, stream)"],
    },
  ],
  hint: {
    open: "Stream is configured; awaiting first streamer.",
    splitting: "Splitter is consuming streamers and writing WMBS_JOB rows.",
    "split-done":
      "Storage Manager ack'd no more streamers. Splitting is done.",
    closed: "Stream contributes no further work to closeout convergence.",
  },
};

const JOB_MACHINE: MachineSpec = {
  initial: "new",
  states: [
    { id: "new", label: "new", x: 70, y: 130 },
    { id: "executing", label: "executing", x: 220, y: 130 },
    { id: "complete", label: "complete", x: 370, y: 130 },
    { id: "merged", label: "merged", x: 520, y: 50 },
    { id: "fts-acked", label: "FTS ack'd", x: 520, y: 210 },
  ],
  transitions: [
    {
      from: "new",
      to: "executing",
      label: "WMAgent runs",
      daos: ["JobSubmitter.submit(job)", "InsertExecuting(job)"],
    },
    {
      from: "executing",
      to: "complete",
      label: "exit code 0",
      daos: ["MarkComplete(job)", "InsertOutput(file)"],
    },
    {
      from: "complete",
      to: "merged",
      label: "merge step",
      daos: ["MergeJobSplitter.split", "MarkMerged(job)"],
    },
    {
      from: "complete",
      to: "fts-acked",
      label: "transfer ack",
      daos: ["FTSAck(file)", "MarkFtsAcked(job)"],
    },
  ],
  hint: {
    new: "Job is in WMBS_JOB but not yet submitted.",
    executing: "WMAgent has the job; condor / batch is running it.",
    complete: "Job finished; output files registered in WMBS.",
    merged: "Output passed through the merge splitter.",
    "fts-acked":
      "FTS confirmed file transfer; downstream stages can consume it.",
  },
};

const MACHINES: Record<Mode, MachineSpec> = {
  run: RUN_MACHINE,
  stream: STREAM_MACHINE,
  job: JOB_MACHINE,
};

interface DAOEntry {
  id: number;
  transition: string;
  call: string;
}

export function LifecycleSim() {
  const [mode, setMode] = useState<Mode>("run");
  const [state, setState] = useState<string>(MACHINES.run.initial);
  const [history, setHistory] = useState<string[]>([MACHINES.run.initial]);
  const [trace, setTrace] = useState<DAOEntry[]>([]);
  const [seq, setSeq] = useState(0);

  const machine = MACHINES[mode];
  const outgoing = machine.transitions.filter((t) => t.from === state);

  const switchMode = (m: Mode) => {
    setMode(m);
    setState(MACHINES[m].initial);
    setHistory([MACHINES[m].initial]);
    setTrace([]);
  };

  const fire = (t: Transition) => {
    setState(t.to);
    setHistory((h) => [...h, t.to]);
    const transitionLabel = `${t.from.toUpperCase()} → ${t.to.toUpperCase()}`;
    const newEntries: DAOEntry[] = t.daos.map((call) => {
      const id = seq + 1 + Math.random();
      return { id, transition: transitionLabel, call };
    });
    setSeq((s) => s + t.daos.length);
    setTrace((tr) => [...tr, ...newEntries].slice(-30));
  };

  const reset = () => {
    setState(machine.initial);
    setHistory([machine.initial]);
    setTrace([]);
  };

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <div>
          <span className={styles.tag}>Simulator — Lifecycle state machine</span>
          <div className={styles.title}>
            Step a {mode} through its states; see DAOs fire on each transition.
          </div>
        </div>
        <div className={styles.modePicker}>
          {(["run", "stream", "job"] as Mode[]).map((m) => (
            <button
              key={m}
              className={`${styles.modeBtn} ${
                mode === m ? styles.modeBtnActive : ""
              }`}
              onClick={() => switchMode(m)}
            >
              {m.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.body}>
        <div className={styles.canvas}>
          <svg
            viewBox="0 0 640 280"
            className={styles.svg}
            preserveAspectRatio="xMidYMid meet"
          >
            <ArrowheadDefs />
            {machine.transitions.map((t, i) => {
              const from = machine.states.find((s) => s.id === t.from)!;
              const to = machine.states.find((s) => s.id === t.to)!;
              const fromActive = state === t.from;
              const wasUsed = history.some(
                (s, idx) =>
                  idx > 0 && history[idx - 1] === t.from && s === t.to,
              );
              const sameRow = Math.abs(from.y - to.y) < 8;
              const ctrl = sameRow
                ? `${(from.x + to.x) / 2} ${from.y}`
                : `${from.x + 60} ${(from.y + to.y) / 2}`;
              const d = `M ${from.x + 36} ${from.y} Q ${ctrl} ${to.x - 36} ${to.y}`;
              return (
                <motion.path
                  key={i}
                  d={d}
                  fill="none"
                  stroke={
                    wasUsed
                      ? "color-mix(in srgb, var(--accent) 60%, transparent)"
                      : fromActive
                      ? "var(--accent)"
                      : "var(--rule)"
                  }
                  strokeWidth={fromActive || wasUsed ? 2.2 : 1.4}
                  markerEnd={
                    fromActive || wasUsed
                      ? "url(#arrowhead-active)"
                      : "url(#arrowhead)"
                  }
                  strokeDasharray={fromActive ? "0" : wasUsed ? "0" : "4 4"}
                  initial={false}
                  animate={{ opacity: fromActive ? 1 : wasUsed ? 0.85 : 0.4 }}
                />
              );
            })}
            {machine.transitions.map((t, i) => {
              const from = machine.states.find((s) => s.id === t.from)!;
              const to = machine.states.find((s) => s.id === t.to)!;
              const lx = (from.x + to.x) / 2;
              const ly = (from.y + to.y) / 2 - 6;
              const fromActive = state === t.from;
              return (
                <text
                  key={`l${i}`}
                  x={lx}
                  y={ly}
                  textAnchor="middle"
                  fontSize={10}
                  fontWeight={500}
                  fill={fromActive ? "var(--accent)" : "var(--muted)"}
                  opacity={fromActive ? 1 : 0.55}
                >
                  {t.label}
                </text>
              );
            })}
            {machine.states.map((s) => {
              const isActive = s.id === state;
              const wasVisited = history.includes(s.id);
              return (
                <motion.g
                  key={s.id}
                  initial={false}
                  animate={{ scale: isActive ? 1.07 : 1 }}
                  transition={{ type: "spring", stiffness: 300, damping: 22 }}
                  style={{ transformOrigin: `${s.x}px ${s.y}px` }}
                >
                  <motion.circle
                    cx={s.x}
                    cy={s.y}
                    r={36}
                    fill={isActive ? "var(--accent-soft)" : "var(--bg-elevated)"}
                    animate={{
                      stroke: isActive
                        ? "var(--accent)"
                        : wasVisited
                        ? "color-mix(in srgb, var(--accent) 55%, transparent)"
                        : "var(--rule)",
                      strokeWidth: isActive ? 2.5 : 1.5,
                    }}
                  />
                  {isActive ? (
                    <motion.circle
                      cx={s.x}
                      cy={s.y}
                      r={36}
                      fill="none"
                      stroke="var(--accent)"
                      strokeWidth={1.5}
                      animate={{ scale: [1, 1.18, 1], opacity: [0.5, 0, 0.5] }}
                      transition={{
                        duration: 1.6,
                        repeat: Infinity,
                        ease: "easeInOut",
                      }}
                      style={{
                        transformOrigin: `${s.x}px ${s.y}px`,
                      }}
                    />
                  ) : null}
                  {s.label.split("\n").map((line, li, arr) => (
                    <text
                      key={li}
                      x={s.x}
                      y={s.y + 4 + (li - (arr.length - 1) / 2) * 12}
                      textAnchor="middle"
                      fontSize={11}
                      fontWeight={600}
                      fill="var(--fg)"
                    >
                      {line}
                    </text>
                  ))}
                </motion.g>
              );
            })}
          </svg>
        </div>

        <div className={styles.right}>
          <div className={styles.summary}>
            <div className={styles.summaryLabel}>Current state</div>
            <div className={styles.summaryState}>{state.toUpperCase()}</div>
            <div className={styles.summaryHint}>
              {machine.hint[state] ?? ""}
            </div>
          </div>

          <div className={styles.actions}>
            {outgoing.length === 0 ? (
              <div
                style={{
                  fontSize: 12,
                  color: "var(--muted)",
                  padding: "6px 4px",
                  fontStyle: "italic",
                }}
              >
                Terminal state — reset to try a different path.
              </div>
            ) : (
              outgoing.map((t, i) => (
                <button
                  key={i}
                  className={styles.actionBtn}
                  onClick={() => fire(t)}
                >
                  <span className={styles.actionIcon}>→</span>
                  <span className={styles.actionLabel}>
                    {t.label}
                    <div className={styles.actionHint}>→ {t.to}</div>
                  </span>
                </button>
              ))
            )}
          </div>

          <div className={styles.daoTrace}>
            {trace.length === 0 ? (
              <div className={styles.daoEmpty}>
                DAOs fired by transitions appear here.
              </div>
            ) : (
              trace.map((e) => (
                <motion.div
                  key={e.id}
                  className={styles.daoEntry}
                  initial={{ opacity: 0, x: -6 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <span className={styles.daoTransition}>{e.transition}</span>
                  <span className={styles.daoCall}>{e.call}</span>
                </motion.div>
              ))
            )}
          </div>
        </div>
      </div>

      <div className={styles.footer}>
        <button className={styles.btn} onClick={reset}>
          ⟲ Reset
        </button>
      </div>
    </div>
  );
}
