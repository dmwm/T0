import { Command } from "cmdk";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { CHAPTERS, SIMULATORS, REFERENCE } from "@/lib/routes";
import styles from "./CommandPalette.module.css";

interface Props {
  open: boolean;
  onClose: () => void;
}

export function CommandPalette({ open, onClose }: Props) {
  const navigate = useNavigate();

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  const go = (path: string) => {
    navigate(path);
    onClose();
  };

  return (
    <AnimatePresence>
      {open ? (
        <motion.div
          className={styles.scrim}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.15 }}
          onClick={onClose}
        >
          <motion.div
            className={styles.dialog}
            initial={{ y: -8, opacity: 0, scale: 0.97 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            exit={{ y: -8, opacity: 0, scale: 0.97 }}
            transition={{ type: "spring", stiffness: 500, damping: 32 }}
            onClick={(e) => e.stopPropagation()}
          >
            <Command label="Quick jump" loop>
              <Command.Input
                className={styles.input}
                autoFocus
                placeholder="Jump to a chapter, simulator, glossary entry…"
              />
              <Command.List className={styles.list}>
                <Command.Empty className={styles.empty}>
                  No matches.
                </Command.Empty>

                <Command.Group heading="Chapters" className={styles.group}>
                  {CHAPTERS.map((c) => (
                    <Command.Item
                      key={c.path}
                      value={`${c.title} ${c.hint ?? ""}`}
                      onSelect={() => go(c.path)}
                      className={styles.item}
                    >
                      <span className={styles.icon}>📖</span>
                      <span className={styles.title}>{c.title}</span>
                      <span className={styles.hint}>{c.path}</span>
                    </Command.Item>
                  ))}
                </Command.Group>

                <Command.Group heading="Simulators" className={styles.group}>
                  {SIMULATORS.map((s) => (
                    <Command.Item
                      key={s.path}
                      value={`${s.title} ${s.hint ?? ""}`}
                      onSelect={() => go(s.path)}
                      className={styles.item}
                    >
                      <span className={styles.icon}>▶</span>
                      <span className={styles.title}>{s.title}</span>
                      <span className={styles.hint}>{s.path}</span>
                    </Command.Item>
                  ))}
                </Command.Group>

                <Command.Group heading="Reference" className={styles.group}>
                  {REFERENCE.map((r) => (
                    <Command.Item
                      key={r.path}
                      value={r.title}
                      onSelect={() => go(r.path)}
                      className={styles.item}
                    >
                      <span className={styles.icon}>📚</span>
                      <span className={styles.title}>{r.title}</span>
                      <span className={styles.hint}>{r.path}</span>
                    </Command.Item>
                  ))}
                </Command.Group>
              </Command.List>
            </Command>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}
