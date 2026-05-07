import { useCallback, useEffect, useRef, useState } from "react";

interface UseTimelineOpts {
  totalSteps: number;
  msPerStep?: number;
  loop?: boolean;
}

export interface Timeline {
  step: number;
  totalSteps: number;
  isPlaying: boolean;
  speed: number;
  setSpeed: (s: number) => void;
  play: () => void;
  pause: () => void;
  toggle: () => void;
  next: () => void;
  prev: () => void;
  reset: () => void;
  goTo: (n: number) => void;
}

export function useTimeline({
  totalSteps,
  msPerStep = 800,
  loop = false,
}: UseTimelineOpts): Timeline {
  const [step, setStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const lastTickRef = useRef<number>(0);
  const rafRef = useRef<number | null>(null);

  const stop = useCallback(() => {
    if (rafRef.current != null) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
  }, []);

  const tick = useCallback(
    (now: number) => {
      if (document.hidden) {
        rafRef.current = requestAnimationFrame(tick);
        return;
      }
      if (lastTickRef.current === 0) lastTickRef.current = now;
      const elapsed = now - lastTickRef.current;
      const interval = msPerStep / speed;
      if (elapsed >= interval) {
        lastTickRef.current = now;
        setStep((s) => {
          if (s >= totalSteps - 1) {
            if (loop) return 0;
            setIsPlaying(false);
            return s;
          }
          return s + 1;
        });
      }
      rafRef.current = requestAnimationFrame(tick);
    },
    [msPerStep, speed, totalSteps, loop],
  );

  useEffect(() => {
    if (isPlaying) {
      lastTickRef.current = 0;
      rafRef.current = requestAnimationFrame(tick);
    } else {
      stop();
    }
    return stop;
  }, [isPlaying, tick, stop]);

  const play = useCallback(() => setIsPlaying(true), []);
  const pause = useCallback(() => setIsPlaying(false), []);
  const toggle = useCallback(() => setIsPlaying((v) => !v), []);
  const next = useCallback(() => {
    setIsPlaying(false);
    setStep((s) => Math.min(totalSteps - 1, s + 1));
  }, [totalSteps]);
  const prev = useCallback(() => {
    setIsPlaying(false);
    setStep((s) => Math.max(0, s - 1));
  }, []);
  const reset = useCallback(() => {
    setIsPlaying(false);
    setStep(0);
  }, []);
  const goTo = useCallback(
    (n: number) => {
      setIsPlaying(false);
      setStep(Math.max(0, Math.min(totalSteps - 1, n)));
    },
    [totalSteps],
  );

  return {
    step,
    totalSteps,
    isPlaying,
    speed,
    setSpeed,
    play,
    pause,
    toggle,
    next,
    prev,
    reset,
    goTo,
  };
}
