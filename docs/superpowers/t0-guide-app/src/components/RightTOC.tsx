import { useEffect, useState } from "react";
import styles from "./RightTOC.module.css";

interface Heading {
  id: string;
  text: string;
  level: number;
}

interface Props {
  scopeRef: React.RefObject<HTMLElement>;
}

export function RightTOC({ scopeRef }: Props) {
  const [headings, setHeadings] = useState<Heading[]>([]);
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    const root = scopeRef.current;
    if (!root) return;
    const nodes = Array.from(root.querySelectorAll("h2, h3")) as HTMLElement[];
    const items: Heading[] = nodes.map((n, i) => {
      let id = n.id;
      if (!id) {
        id = `h-${i}-${(n.textContent ?? "")
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .slice(0, 40)}`;
        n.id = id;
      }
      return {
        id,
        text: n.textContent ?? "",
        level: n.tagName === "H2" ? 2 : 3,
      };
    });
    setHeadings(items);

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) setActiveId(visible[0].target.id);
      },
      { rootMargin: "-72px 0px -60% 0px", threshold: [0, 1] },
    );
    nodes.forEach((n) => observer.observe(n));
    return () => observer.disconnect();
  }, [scopeRef]);

  if (headings.length === 0) return null;

  return (
    <nav className={styles.toc} aria-label="On this page">
      <div className={styles.label}>On this page</div>
      <div className={styles.list}>
        {headings.map((h) => (
          <a
            key={h.id}
            href={`#${h.id}`}
            className={`${styles.link} ${
              activeId === h.id ? styles.linkActive : ""
            } ${h.level === 3 ? styles.h3 : ""}`}
          >
            {h.text}
          </a>
        ))}
      </div>
    </nav>
  );
}
