import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { CHAPTERS, SIMULATORS } from "@/lib/routes";
import { D1_1_PipelineHero } from "@/diagrams/D1_1_PipelineHero";
import styles from "./Home.module.css";

const stagger = {
  show: { transition: { staggerChildren: 0.06 } },
  hidden: {},
};
const item = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.16, 1, 0.3, 1] } },
};

export function Home() {
  return (
    <>
      <section className={styles.hero}>
        <div className={styles.heroInner}>
          <motion.div
            className={styles.eyebrow}
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <span className={styles.dot} />
            CMS Tier-0 — interactive architecture guide
          </motion.div>
          <motion.h1
            className={styles.title}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.05 }}
          >
            Learn how Tier-0 turns CMS detector data into archived datasets.
          </motion.h1>
          <motion.p
            className={styles.subtitle}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.12 }}
          >
            Six chapters, twenty-two animated diagrams, and four hands-on
            simulators. Step through the heartbeat, build a mental model of the
            run lifecycle, and play with the splitter and closeout logic.
          </motion.p>
          <motion.div
            className={styles.ctas}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.18 }}
          >
            <Link to="/ch1" className={styles.btnPrimary}>
              Start with Chapter 1 →
            </Link>
            <Link to="/sim/tier0-feeder-tick" className={styles.btnSecondary}>
              Or try a simulator
            </Link>
          </motion.div>
        </div>
      </section>

      <div className={styles.body}>
        <div className={styles.sectionLabel}>The whole pipeline at a glance</div>
        <D1_1_PipelineHero />

        <div className={styles.sectionLabel} style={{ marginTop: 56 }}>
          The six chapters
        </div>
        <motion.div
          className={styles.grid}
          variants={stagger}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-80px" }}
        >
          {CHAPTERS.map((c, i) => (
            <motion.div key={c.path} variants={item}>
              <Link to={c.path} className={styles.card}>
                <span className={styles.cardN}>0{i + 1}</span>
                <span className={styles.cardTitle}>{c.shortTitle}</span>
                <span className={styles.cardHint}>{c.hint}</span>
                <span className={styles.cardArrow}>Open chapter →</span>
              </Link>
            </motion.div>
          ))}
        </motion.div>

        <div className={styles.simSection}>
          <div className={styles.sectionLabel}>Hands-on simulators</div>
          <div className={styles.simGrid}>
            {SIMULATORS.map((s) => (
              <Link key={s.path} to={s.path} className={styles.simCard}>
                <span className={styles.simIcon}>▶</span>
                <span className={styles.simBody}>
                  <span className={styles.simTitle}>{s.shortTitle}</span>
                  <span className={styles.simHint}>{s.hint}</span>
                </span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
