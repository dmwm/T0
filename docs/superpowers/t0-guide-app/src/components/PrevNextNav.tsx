import { Link } from "react-router-dom";
import { findChapter, findRoute } from "@/lib/routes";
import styles from "./PrevNextNav.module.css";

interface Props {
  currentPath: string;
}

export function PrevNextNav({ currentPath }: Props) {
  const ch = findChapter(currentPath);
  if (!ch) return null;

  const prev = ch.prevPath ? findRoute(ch.prevPath) : undefined;
  const next = ch.nextPath ? findRoute(ch.nextPath) : undefined;

  return (
    <nav className={styles.nav} aria-label="Chapter navigation">
      {prev ? (
        <Link to={prev.path} className={styles.card}>
          <span className={styles.dir}>← Previous</span>
          <span className={styles.title}>{prev.title}</span>
        </Link>
      ) : (
        <span className={`${styles.card} ${styles.spacer}`} aria-hidden="true" />
      )}
      {next ? (
        <Link to={next.path} className={`${styles.card} ${styles.next}`}>
          <span className={styles.dir}>Next →</span>
          <span className={styles.title}>{next.title}</span>
        </Link>
      ) : (
        <span className={`${styles.card} ${styles.spacer}`} aria-hidden="true" />
      )}
    </nav>
  );
}
