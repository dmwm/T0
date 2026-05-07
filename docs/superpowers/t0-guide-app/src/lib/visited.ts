import { useEffect, useState } from "react";

const KEY = "t0-visited";

function read(): Set<string> {
  if (typeof window === "undefined") return new Set();
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return new Set();
    return new Set(JSON.parse(raw) as string[]);
  } catch {
    return new Set();
  }
}

function write(set: Set<string>) {
  if (typeof window === "undefined") return;
  localStorage.setItem(KEY, JSON.stringify([...set]));
}

let listeners: Array<() => void> = [];
function emit() {
  for (const fn of listeners) fn();
}

export function markVisited(path: string) {
  const set = read();
  if (set.has(path)) return;
  set.add(path);
  write(set);
  emit();
}

export function useVisited(): Set<string> {
  const [snap, setSnap] = useState<Set<string>>(() => read());
  useEffect(() => {
    const update = () => setSnap(read());
    listeners.push(update);
    return () => {
      listeners = listeners.filter((f) => f !== update);
    };
  }, []);
  return snap;
}
