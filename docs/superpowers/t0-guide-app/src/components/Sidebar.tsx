import { useState } from "react";
import { NavLink } from "react-router-dom";
import { CHAPTERS_LINKED, SIMULATORS, REFERENCE, HOME } from "@/lib/routes";
import { useVisited } from "@/lib/visited";
import { ThemeToggle } from "./ThemeToggle";
import styles from "./Sidebar.module.css";

interface SidebarProps {
  onOpenPalette: () => void;
}

export function Sidebar({ onOpenPalette }: SidebarProps) {
  const [open, setOpen] = useState(false);
  const visited = useVisited();

  const isMac =
    typeof navigator !== "undefined" && /Mac|iPhone|iPad/.test(navigator.platform);
  const cmdKey = isMac ? "⌘" : "Ctrl";

  return (
    <>
      <button
        className={styles.toggleBtn}
        onClick={() => setOpen((v) => !v)}
        aria-label="Toggle sidebar"
      >
        ☰
      </button>
      <aside className={`${styles.sidebar} ${open ? styles.sidebarOpen : ""}`}>
        <NavLink
          to={HOME.path}
          className={styles.brand}
          onClick={() => setOpen(false)}
        >
          <span className={styles.mark}>T0</span>
          <span className={styles.brandText}>
            <span>Architecture</span>
            <small>CMS Tier-0 guide</small>
          </span>
        </NavLink>

        <button
          onClick={() => {
            onOpenPalette();
            setOpen(false);
          }}
          className={styles.link}
          style={{
            background: "var(--code-bg)",
            border: "1px solid var(--rule)",
            cursor: "pointer",
            justifyContent: "space-between",
          }}
        >
          <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <span style={{ opacity: 0.6 }}>⌕</span>
            <span style={{ color: "var(--muted)", fontWeight: 500 }}>
              Quick jump…
            </span>
          </span>
          <span className={styles.kbd}>
            {cmdKey} K
          </span>
        </button>

        <div className={styles.section}>
          <div className={styles.label}>Chapters</div>
          {CHAPTERS_LINKED.map((c) => (
            <NavLink
              key={c.path}
              to={c.path}
              className={({ isActive }) =>
                `${styles.link} ${isActive ? styles.linkActive : ""}`
              }
              onClick={() => setOpen(false)}
            >
              {({ isActive }) => (
                <>
                  <span
                    className={`${styles.bullet} ${
                      isActive
                        ? styles.bulletActive
                        : visited.has(c.path)
                        ? styles.bulletVisited
                        : ""
                    }`}
                  />
                  <span>{c.shortTitle}</span>
                  {visited.has(c.path) && !isActive ? (
                    <span className={styles.checkmark}>✓</span>
                  ) : null}
                </>
              )}
            </NavLink>
          ))}
        </div>

        <div className={styles.section}>
          <div className={styles.label}>Simulators</div>
          {SIMULATORS.map((s) => (
            <NavLink
              key={s.path}
              to={s.path}
              className={({ isActive }) =>
                `${styles.link} ${isActive ? styles.linkActive : ""}`
              }
              onClick={() => setOpen(false)}
            >
              {({ isActive }) => (
                <>
                  <span
                    className={`${styles.bullet} ${
                      isActive ? styles.bulletActive : ""
                    }`}
                  />
                  <span>{s.shortTitle}</span>
                </>
              )}
            </NavLink>
          ))}
        </div>

        <div className={styles.section}>
          <div className={styles.label}>Reference</div>
          {REFERENCE.map((r) => (
            <NavLink
              key={r.path}
              to={r.path}
              className={({ isActive }) =>
                `${styles.link} ${isActive ? styles.linkActive : ""}`
              }
              onClick={() => setOpen(false)}
            >
              {({ isActive }) => (
                <>
                  <span
                    className={`${styles.bullet} ${
                      isActive ? styles.bulletActive : ""
                    }`}
                  />
                  <span>{r.shortTitle}</span>
                </>
              )}
            </NavLink>
          ))}
        </div>

        <div className={styles.footer}>
          <ThemeToggle />
          <div className={styles.kbdHint}>
            <span className={styles.kbd}>{cmdKey} K</span>
            <span>quick jump</span>
          </div>
          <div className={styles.kbdHint}>
            <span className={styles.kbd}>← →</span>
            <span>step diagrams</span>
          </div>
        </div>
      </aside>
    </>
  );
}
