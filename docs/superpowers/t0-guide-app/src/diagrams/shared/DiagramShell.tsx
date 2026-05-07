import { useEffect, useState, type ReactNode } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Timeline } from "./useTimeline";
import styles from "./DiagramShell.module.css";

export interface StepSpec {
  caption: ReactNode;
}

interface Props {
  tag?: string;
  title: string;
  timeline: Timeline;
  steps: StepSpec[];
  viewBox: string;
  children: ReactNode;
  showCaption?: boolean;
}

const SPEEDS = [0.5, 1, 2];

export function DiagramShell({
  tag,
  title,
  timeline,
  steps,
  viewBox,
  children,
  showCaption = true,
}: Props) {
  const [zoomed, setZoomed] = useState(false);
  const [hovered, setHovered] = useState(false);
  const { step, totalSteps, isPlaying, speed, setSpeed, toggle, next, prev, reset, goTo } =
    timeline;

  const atEnd = step === totalSteps - 1;

  useEffect(() => {
    if (!hovered && !zoomed) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight") {
        e.preventDefault();
        next();
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        prev();
      } else if (e.key === " ") {
        e.preventDefault();
        toggle();
      } else if (e.key === "r" || e.key === "R") {
        e.preventDefault();
        reset();
      } else if (e.key === "Escape") {
        if (zoomed) setZoomed(false);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [hovered, zoomed, next, prev, toggle, reset]);

  const renderShell = (inZoom: boolean) => (
    <div
      className={styles.shell}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className={styles.header}>
        <div className={styles.headerText}>
          {tag ? <span className={styles.tag}>{tag}</span> : null}
          <span className={styles.title}>{title}</span>
        </div>
        {!inZoom ? (
          <button
            className={styles.zoomBtn}
            onClick={() => setZoomed(true)}
            aria-label="Zoom in"
          >
            ⛶ Fullscreen
          </button>
        ) : null}
      </div>

      <div className={styles.canvas}>
        <svg
          viewBox={viewBox}
          className={styles.svg}
          preserveAspectRatio="xMidYMid meet"
          aria-hidden="true"
        >
          {children}
        </svg>
      </div>

      <div className={styles.controls}>
        <button
          className={styles.btn}
          onClick={reset}
          aria-label="Reset"
          title="Reset (R)"
        >
          ⏮
        </button>
        <button
          className={styles.btn}
          onClick={prev}
          disabled={step === 0}
          aria-label="Previous step"
          title="Previous (←)"
        >
          ◀
        </button>
        <button
          className={`${styles.btn} ${styles.btnPlay}`}
          onClick={() => {
            if (atEnd && !isPlaying) {
              reset();
              setTimeout(toggle, 50);
            } else {
              toggle();
            }
          }}
          aria-label={isPlaying ? "Pause" : "Play"}
          title="Play/Pause (Space)"
        >
          {isPlaying ? "⏸ Pause" : atEnd ? "↻ Replay" : "▶ Play"}
        </button>
        <button
          className={styles.btn}
          onClick={next}
          disabled={atEnd}
          aria-label="Next step"
          title="Next (→)"
        >
          ▶
        </button>

        <div className={styles.stepIndicator}>
          {steps.map((_, i) => (
            <button
              key={i}
              className={`${styles.dot} ${
                i === step
                  ? styles.dotActive
                  : i < step
                  ? styles.dotVisited
                  : ""
              }`}
              onClick={() => goTo(i)}
              aria-label={`Go to step ${i + 1}`}
            />
          ))}
        </div>

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

      {showCaption ? (
        <div className={styles.caption}>
          <div className={styles.captionLabel}>
            <span className={styles.captionN}>
              {step + 1} / {totalSteps}
            </span>
            Step caption
          </div>
          <AnimatePresence mode="wait">
            <motion.div
              key={step}
              className={styles.captionText}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.18 }}
            >
              {steps[step]?.caption ?? null}
            </motion.div>
          </AnimatePresence>
        </div>
      ) : null}
    </div>
  );

  return (
    <>
      {renderShell(false)}
      <AnimatePresence>
        {zoomed ? (
          <motion.div
            className={styles.zoomScrim}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={() => setZoomed(false)}
          >
            <motion.div
              className={styles.zoomDialog}
              initial={{ scale: 0.96, y: 8 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.96, y: 8 }}
              transition={{ type: "spring", stiffness: 320, damping: 28 }}
              onClick={(e) => e.stopPropagation()}
              style={{ position: "relative" }}
            >
              <button
                className={styles.zoomCloseBtn}
                onClick={() => setZoomed(false)}
                aria-label="Close fullscreen"
              >
                ×
              </button>
              {renderShell(true)}
            </motion.div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </>
  );
}
