import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { findChapter } from "@/lib/routes";
import { markVisited } from "@/lib/visited";
import { PrevNextNav } from "./PrevNextNav";
import { RightTOC } from "./RightTOC";
import styles from "./ChapterShell.module.css";

interface Props {
  eyebrow?: string;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  showPrevNext?: boolean;
}

export function ChapterShell({
  eyebrow,
  title,
  subtitle,
  children,
  showPrevNext = true,
}: Props) {
  const ref = useRef<HTMLElement>(null);
  const { pathname } = useLocation();

  useEffect(() => {
    if (findChapter(pathname)) markVisited(pathname);
    window.scrollTo({ top: 0, behavior: "auto" });
  }, [pathname]);

  return (
    <>
      <motion.header
        className={styles.heroBand}
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      >
        <div className={styles.heroBandInner}>
          {eyebrow ? <div className={styles.eyebrow}>{eyebrow}</div> : null}
          <h1 className={styles.title}>{title}</h1>
          {subtitle ? <p className={styles.subtitle}>{subtitle}</p> : null}
        </div>
      </motion.header>

      <div className={styles.layout}>
        <motion.article
          ref={ref}
          className={styles.body}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.05, ease: [0.16, 1, 0.3, 1] }}
        >
          {children}
          {showPrevNext ? <PrevNextNav currentPath={pathname} /> : null}
        </motion.article>
        <RightTOC scopeRef={ref} />
      </div>
    </>
  );
}
