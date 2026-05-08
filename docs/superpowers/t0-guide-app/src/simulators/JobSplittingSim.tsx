import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import styles from "./JobSplittingSim.module.css";

type Mode = "repack" | "express";

interface ModeConfig {
  defaultLumiCap: number;
  defaultEventCap: number;
  defaultSizeCap: number;
  lumiRange: [number, number];
  eventRange: [number, number];
  sizeRange: [number, number];
  description: string;
}

const MODES: Record<Mode, ModeConfig> = {
  repack: {
    defaultLumiCap: 8,
    defaultEventCap: 2_000_000,
    defaultSizeCap: 16_000,
    lumiRange: [1, 20],
    eventRange: [200_000, 5_000_000],
    sizeRange: [1_000, 50_000],
    description:
      "Repack groups streamer files by lumi until either a lumi or event cap is hit, then emits a job.",
  },
  express: {
    defaultLumiCap: 4,
    defaultEventCap: 800_000,
    defaultSizeCap: 8_000,
    lumiRange: [1, 10],
    eventRange: [200_000, 2_000_000],
    sizeRange: [500, 30_000],
    description:
      "Express uses tighter caps so AlCa and DQM can consume small jobs quickly.",
  },
};

interface Streamer {
  id: number;
  lumis: number;
  events: number;
  sizeMB: number;
}

interface Job {
  id: number;
  mode: Mode;
  streamerCount: number;
  lumis: number;
  events: number;
  sizeMB: number;
  reason: "lumi cap" | "event cap" | "size cap";
}

const STREAMER_LIMIT = 200;
const JOB_LIMIT = 40;

function randomStreamer(idSeed: number): Streamer {
  return {
    id: idSeed,
    lumis: 1 + Math.floor(Math.random() * 3),
    events: Math.floor(80_000 + Math.random() * 220_000),
    sizeMB: Math.floor(800 + Math.random() * 1_400),
  };
}

export function JobSplittingSim() {
  const [mode, setMode] = useState<Mode>("repack");
  const cfg = MODES[mode];

  const [lumiCap, setLumiCap] = useState(cfg.defaultLumiCap);
  const [eventCap, setEventCap] = useState(cfg.defaultEventCap);
  const [sizeCap, setSizeCap] = useState(cfg.defaultSizeCap);

  const [bucket, setBucket] = useState<{
    lumis: number;
    events: number;
    sizeMB: number;
    streamerCount: number;
  }>({ lumis: 0, events: 0, sizeMB: 0, streamerCount: 0 });

  const [jobs, setJobs] = useState<Job[]>([]);
  const [streamers, setStreamers] = useState<Streamer[]>([]);
  const [auto, setAuto] = useState(false);
  const [streamersSeen, setStreamersSeen] = useState(0);
  const idRef = useRef(0);
  const jobIdRef = useRef(0);

  function changeMode(m: Mode) {
    setMode(m);
    const c = MODES[m];
    setLumiCap(c.defaultLumiCap);
    setEventCap(c.defaultEventCap);
    setSizeCap(c.defaultSizeCap);
    reset();
  }

  function reset() {
    setBucket({ lumis: 0, events: 0, sizeMB: 0, streamerCount: 0 });
    setJobs([]);
    setStreamers([]);
    setStreamersSeen(0);
    idRef.current = 0;
    jobIdRef.current = 0;
  }

  function send() {
    idRef.current += 1;
    const s = randomStreamer(idRef.current);
    setStreamers((prev) => [...prev, s].slice(-STREAMER_LIMIT));
    setStreamersSeen((n) => n + 1);

    setBucket((b) => {
      const next = {
        lumis: b.lumis + s.lumis,
        events: b.events + s.events,
        sizeMB: b.sizeMB + s.sizeMB,
        streamerCount: b.streamerCount + 1,
      };
      if (
        next.lumis >= lumiCap ||
        next.events >= eventCap ||
        next.sizeMB >= sizeCap
      ) {
        const reason: Job["reason"] =
          next.lumis >= lumiCap
            ? "lumi cap"
            : next.events >= eventCap
            ? "event cap"
            : "size cap";
        jobIdRef.current += 1;
        const job: Job = {
          id: jobIdRef.current,
          mode,
          streamerCount: next.streamerCount,
          lumis: next.lumis,
          events: next.events,
          sizeMB: next.sizeMB,
          reason,
        };
        setJobs((prev) => [job, ...prev].slice(0, JOB_LIMIT));
        return { lumis: 0, events: 0, sizeMB: 0, streamerCount: 0 };
      }
      return next;
    });
  }

  useEffect(() => {
    if (!auto) return;
    const id = window.setInterval(send, 600);
    return () => clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [auto, lumiCap, eventCap, sizeCap, mode]);

  const lumiPct = Math.min(100, (bucket.lumis / lumiCap) * 100);
  const eventPct = Math.min(100, (bucket.events / eventCap) * 100);
  const sizePct = Math.min(100, (bucket.sizeMB / sizeCap) * 100);

  const totalStreamersInJobs = jobs.reduce((s, j) => s + j.streamerCount, 0);
  const avgStreamersPerJob =
    jobs.length === 0
      ? 0
      : Math.round((totalStreamersInJobs / jobs.length) * 10) / 10;
  const avgEventsPerJob =
    jobs.length === 0
      ? 0
      : Math.round(jobs.reduce((s, j) => s + j.events, 0) / jobs.length);

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <div>
          <span className={styles.tag}>Simulator — JobSplitting</span>
          <div className={styles.title}>
            Tweak caps and watch streamers cut into jobs in real time.
          </div>
        </div>
        <div className={styles.modePicker}>
          {(["repack", "express"] as Mode[]).map((m) => (
            <button
              key={m}
              className={`${styles.modeBtn} ${
                mode === m ? styles.modeBtnActive : ""
              }`}
              onClick={() => changeMode(m)}
            >
              {m === "repack" ? "Repack" : "Express"}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.body}>
        <div className={styles.controls}>
          <div className={styles.sliderGroup}>
            <div className={styles.sliderLabel}>
              <span>Lumi cap</span>
              <span className={styles.sliderValue}>{lumiCap}</span>
            </div>
            <input
              type="range"
              min={cfg.lumiRange[0]}
              max={cfg.lumiRange[1]}
              value={lumiCap}
              onChange={(e) => setLumiCap(Number(e.target.value))}
              className={styles.slider}
            />
            <span className={styles.sliderHint}>
              max lumi sections per job
            </span>
          </div>

          <div className={styles.sliderGroup}>
            <div className={styles.sliderLabel}>
              <span>Event cap</span>
              <span className={styles.sliderValue}>
                {(eventCap / 1_000_000).toFixed(1)}M
              </span>
            </div>
            <input
              type="range"
              min={cfg.eventRange[0]}
              max={cfg.eventRange[1]}
              step={50_000}
              value={eventCap}
              onChange={(e) => setEventCap(Number(e.target.value))}
              className={styles.slider}
            />
            <span className={styles.sliderHint}>max events per job</span>
          </div>

          <div className={styles.sliderGroup}>
            <div className={styles.sliderLabel}>
              <span>Size cap</span>
              <span className={styles.sliderValue}>
                {(sizeCap / 1_000).toFixed(1)} GB
              </span>
            </div>
            <input
              type="range"
              min={cfg.sizeRange[0]}
              max={cfg.sizeRange[1]}
              step={500}
              value={sizeCap}
              onChange={(e) => setSizeCap(Number(e.target.value))}
              className={styles.slider}
            />
            <span className={styles.sliderHint}>max payload per job</span>
          </div>

          <p
            style={{
              fontSize: 11.5,
              color: "var(--muted)",
              lineHeight: 1.5,
              margin: 0,
            }}
          >
            {cfg.description}
          </p>
        </div>

        <div className={styles.canvas}>
          <span className={styles.canvasLabel}>Streamer feed</span>
          <div className={styles.streamerLane}>
            <AnimatePresence>
              {streamers.slice(-12).map((s, i) => (
                <motion.div
                  key={s.id}
                  className={styles.streamerToken}
                  initial={{ x: -80, opacity: 0 }}
                  animate={{
                    x: i * 56,
                    opacity: 1,
                  }}
                  exit={{ opacity: 0, scale: 0.7 }}
                  transition={{
                    type: "spring",
                    stiffness: 320,
                    damping: 28,
                  }}
                >
                  s{s.id}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          <span className={styles.canvasLabel}>Current bucket</span>
          <div className={styles.bucketWrap}>
            <div className={styles.bucketTrack}>
              <motion.div
                className={styles.bucketFill}
                initial={false}
                animate={{
                  width: `${Math.max(lumiPct, eventPct, sizePct)}%`,
                }}
                transition={{ type: "spring", stiffness: 220, damping: 28 }}
              />
              <div className={styles.bucketText}>
                {bucket.streamerCount} streamers · {bucket.lumis} lumis ·{" "}
                {(bucket.events / 1_000_000).toFixed(1)}M events
              </div>
            </div>
            <div
              style={{
                fontSize: 10.5,
                color: "var(--muted)",
                display: "flex",
                gap: 12,
              }}
            >
              <span>lumi {lumiPct.toFixed(0)}%</span>
              <span>events {eventPct.toFixed(0)}%</span>
              <span>size {sizePct.toFixed(0)}%</span>
            </div>
          </div>

          <span className={styles.canvasLabel}>Emitted jobs</span>
          <div className={styles.jobsList}>
            <AnimatePresence initial={false}>
              {jobs.map((j) => (
                <motion.div
                  key={j.id}
                  className={styles.jobCard}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.25 }}
                >
                  <span className={styles.jobN}>
                    {j.mode === "repack" ? "Repack" : "Express"} job #{j.id}
                  </span>
                  <span className={styles.jobMeta}>
                    {j.streamerCount} streamers · {j.lumis} lumis ·{" "}
                    {(j.events / 1_000_000).toFixed(2)}M events ·{" "}
                    {(j.sizeMB / 1000).toFixed(2)} GB · cut by {j.reason}
                  </span>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>

        <div className={styles.stats}>
          <div className={styles.stat}>
            <div className={styles.statN}>{jobs.length}</div>
            <div className={styles.statLabel}>jobs emitted</div>
          </div>
          <div className={styles.stat}>
            <div className={styles.statN}>{streamersSeen}</div>
            <div className={styles.statLabel}>streamers seen</div>
          </div>
          <div className={styles.stat}>
            <div className={styles.statN}>{avgStreamersPerJob}</div>
            <div className={styles.statLabel}>avg streamers / job</div>
            <div className={styles.statHint}>
              fewer streamers per job = tighter cap window
            </div>
          </div>
          <div className={styles.stat}>
            <div className={styles.statN}>
              {(avgEventsPerJob / 1_000_000).toFixed(2)}M
            </div>
            <div className={styles.statLabel}>avg events / job</div>
          </div>
        </div>
      </div>

      <div className={styles.footer}>
        <button
          className={`${styles.btn} ${styles.btnPrimary}`}
          onClick={send}
        >
          ▶ Send streamer
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
          Auto-send
        </label>
        <button className={styles.btn} onClick={reset}>
          ⟲ Reset
        </button>
        <span
          style={{
            marginLeft: "auto",
            fontSize: 11.5,
            color: "var(--muted)",
          }}
        >
          tip — turn on Auto-send and slide the caps to feel the splitter shape
        </span>
      </div>
    </div>
  );
}
