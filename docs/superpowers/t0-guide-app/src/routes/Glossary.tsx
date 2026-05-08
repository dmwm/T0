import { useMemo, useState } from "react";
import { ChapterShell } from "@/components/ChapterShell";
import styles from "./Glossary.module.css";

interface Entry {
  term: string;
  aka?: string;
  def: React.ReactNode;
  ref?: string;
  group: "Architecture" | "Processing" | "Deploy" | "Conventions";
}

const ENTRIES: Entry[] = [
  {
    term: "T0AST",
    aka: "Tier-0 Agent State",
    def: "The agent's own Oracle schema — runs, streams, splitter state, closeout signals, condition upload state. Distinct from WMBS.",
    ref: "src/python/T0/WMBS/Oracle/Create",
    group: "Architecture",
  },
  {
    term: "WMBS",
    aka: "Workload Management Database System",
    def: "WMAgent's standard execution database — jobs, files, filesets, workflows. Tier-0 writes splitter results here; WMAgent's submitters read it.",
    group: "Architecture",
  },
  {
    term: "Tier0Feeder",
    def: "The active WMAgent component (T0Component.Tier0Feeder.Tier0FeederPoller) whose algorithm() runs every poll interval and drives the whole pipeline.",
    ref: "src/python/T0Component/Tier0Feeder/",
    group: "Architecture",
  },
  {
    term: "Tier0Config",
    aka: "DSL",
    def: "The Python module operators edit. Setter functions on a singleton object; parsed by WMAgent's loadConfigurationFile.",
    ref: "src/python/T0/RunConfig/Tier0Config.py",
    group: "Architecture",
  },
  {
    term: "Helper agent",
    def: "An additional Tier0Feeder process on a separate vocms host. Its assignment is declared by HelperAgentStreams in Tier0Config; it polls only those streams.",
    group: "Architecture",
  },
  {
    term: "Streamer",
    def: "A binary blob (~16 MB) of HLT-accepted events from one stream of one run. Originates at Point 5; named in Storage Manager DB.",
    group: "Processing",
  },
  {
    term: "Repack",
    def: "Splitter that packs streamer files into RAW datasets, partitioned by primary dataset. Produces RAW for archive and downstream PromptReco.",
    ref: "src/python/T0/JobSplitting/RepackJobSplitter.py",
    group: "Processing",
  },
  {
    term: "Express",
    def: "Splitter that runs a fast reconstruction immediately. Produces fast-reco AOD plus AlCa skims that feed AlcaHarvest.",
    ref: "src/python/T0/JobSplitting/ExpressJobSplitter.py",
    group: "Processing",
  },
  {
    term: "PromptReco",
    def: "Full-blown reconstruction workflow. Released for a run only after a CMSSW release for the run is announced.",
    group: "Processing",
  },
  {
    term: "AlcaHarvest",
    def: "Workflow that aggregates per-run calibration histograms (from Express AlCa skims) into condition payloads.",
    group: "Processing",
  },
  {
    term: "PCL",
    aka: "Prompt Calibration Loop",
    def: "The per-run calibration pipeline: Express → AlcaHarvest → ConditionUpload → Frontier. Conditions are then visible to PromptReco for that run.",
    group: "Processing",
  },
  {
    term: "Frontier",
    def: "CMS's production conditions database. ConditionUploadAPI POSTs payloads to its upload endpoint; PromptReco / offline jobs read from it.",
    group: "Processing",
  },
  {
    term: "Closeout",
    def: "The point at which a run is marked closed in T0AST. Fires only when all four convergence signals (streams closed, AlcaHarvest done, conditions uploaded, release announced) are present.",
    group: "Processing",
  },
  {
    term: "DAOFactory",
    def: "WMCore pattern for accessing Oracle stored-procedure-like Python modules. Tier-0 uses DAOFactory(package=\"T0.WMBS\", classname=\"<area>.<name>\").",
    group: "Conventions",
  },
  {
    term: "SplitterFactory",
    def: "Plugin lookup pattern for splitters. SplitterFactory(package=\"T0.JobSplitting\").get(\"Repack\") → instance of RepackJobSplitter.",
    group: "Conventions",
  },
  {
    term: "vocms",
    def: "The CERN naming pattern for CMS production hosts. Tier-0 runs on vocms047 (Main) and vocms0500 / 05011 / 05012 (Helpers) as the cmst0 user.",
    group: "Deploy",
  },
  {
    term: "bin/t0",
    def: "The operator CLI on each deploy host. --start-agent, --stop-agent, --update-t0=<ver>, --get-tarball, --clear-deployment, --status.",
    ref: "bin/t0",
    group: "Deploy",
  },
  {
    term: "TIER0_VERSION",
    def: "The pinned Tier-0 PyPI version, hard-coded at the top of bin/00_pypi_deploy_*.sh. Drifts independently from src/python/T0/__init__.py:__version__.",
    group: "Deploy",
  },
  {
    term: "00_pypi_patches.sh",
    def: "Shell script of curl … | patch commands cherry-picking WMCore / T0 PRs at deploy time. Live operational state — rotated frequently, not committed source.",
    ref: "bin/00_pypi_patches.sh",
    group: "Deploy",
  },
  {
    term: "Replay",
    def: "Re-running Tier-0 against archived data with a candidate config. Triggered via PR comments on deployReplayPR.yaml; runs on whitelisted vocms nodes.",
    group: "Deploy",
  },
];

const GROUPS: Entry["group"][] = [
  "Architecture",
  "Processing",
  "Deploy",
  "Conventions",
];

export function Glossary() {
  const [query, setQuery] = useState("");
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return ENTRIES;
    return ENTRIES.filter((e) => {
      const haystack = `${e.term} ${e.aka ?? ""} ${e.ref ?? ""}`.toLowerCase();
      return haystack.includes(q);
    });
  }, [query]);

  return (
    <ChapterShell
      eyebrow="Reference"
      title="Glossary"
      subtitle="Quick lookup for the terminology that runs through the guide"
      showPrevNext={false}
    >
      <input
        type="search"
        placeholder="Filter terms (try 'Frontier', 'splitter', 'vocms'…)"
        className={styles.search}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {GROUPS.map((g) => {
        const items = filtered.filter((e) => e.group === g);
        if (items.length === 0) return null;
        return (
          <section key={g} className={styles.section}>
            <div className={styles.sectionTitle}>{g}</div>
            <div className={styles.grid}>
              {items.map((e) => (
                <div key={e.term} className={styles.entry}>
                  <div>
                    <span className={styles.term}>{e.term}</span>
                    {e.aka ? <span className={styles.aka}>aka {e.aka}</span> : null}
                  </div>
                  <div className={styles.def}>{e.def}</div>
                  {e.ref ? <div className={styles.ref}>{e.ref}</div> : null}
                </div>
              ))}
            </div>
          </section>
        );
      })}

      {filtered.length === 0 ? (
        <div className={styles.empty}>
          No glossary entries match "{query}".
        </div>
      ) : null}
    </ChapterShell>
  );
}
