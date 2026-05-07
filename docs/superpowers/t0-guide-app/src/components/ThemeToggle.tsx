import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import styles from "./ThemeToggle.module.css";

type Theme = "light" | "dark" | "auto";

const STORAGE_KEY = "t0-theme";

function readStored(): Theme {
  if (typeof window === "undefined") return "auto";
  const v = localStorage.getItem(STORAGE_KEY);
  return v === "light" || v === "dark" ? v : "auto";
}

function apply(theme: Theme) {
  const root = document.documentElement;
  if (theme === "auto") {
    delete root.dataset.theme;
    localStorage.removeItem(STORAGE_KEY);
  } else {
    root.dataset.theme = theme;
    localStorage.setItem(STORAGE_KEY, theme);
  }
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(readStored);

  useEffect(() => {
    apply(theme);
  }, [theme]);

  const options: { value: Theme; label: string; icon: string }[] = [
    { value: "light", label: "Light", icon: "☀" },
    { value: "auto", label: "Auto", icon: "◐" },
    { value: "dark", label: "Dark", icon: "☾" },
  ];

  const activeIndex = options.findIndex((o) => o.value === theme);

  return (
    <div className={styles.toggle} role="radiogroup" aria-label="Theme">
      <motion.div
        className={styles.indicator}
        animate={{
          left: `calc(3px + ${activeIndex} * (100% - 6px) / 3)`,
          width: "calc((100% - 6px) / 3)",
        }}
        transition={{ type: "spring", stiffness: 500, damping: 35 }}
      />
      {options.map((o) => (
        <button
          key={o.value}
          role="radio"
          aria-checked={theme === o.value}
          className={`${styles.option} ${
            theme === o.value ? styles.optionActive : ""
          }`}
          onClick={() => setTheme(o.value)}
        >
          <span aria-hidden="true">{o.icon}</span>
          <span>{o.label}</span>
        </button>
      ))}
    </div>
  );
}
