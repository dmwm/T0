import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import { Sidebar } from "@/components/Sidebar";
import { CommandPalette } from "@/components/CommandPalette";
import { Home } from "@/routes/Home";
import { Ch1Overview } from "@/routes/Ch1Overview";
import { Ch2RunConfig } from "@/routes/Ch2RunConfig";
import { Ch3Tier0Feeder } from "@/routes/Ch3Tier0Feeder";
import { Ch4JobSplitting } from "@/routes/Ch4JobSplitting";
import { Ch5Closeout } from "@/routes/Ch5Closeout";
import { Ch6Operator } from "@/routes/Ch6Operator";
import { Glossary } from "@/routes/Glossary";
import { SimTier0FeederTick } from "@/routes/SimTier0FeederTick";
import { SimLifecycle } from "@/routes/SimLifecycle";
import { SimJobSplitting } from "@/routes/SimJobSplitting";
import { SimCloseout } from "@/routes/SimCloseout";
import { NotFound } from "@/routes/NotFound";
import styles from "./components/AppFrame.module.css";

export default function App() {
  const [paletteOpen, setPaletteOpen] = useState(false);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen((v) => !v);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <div className={styles.app}>
      <Sidebar onOpenPalette={() => setPaletteOpen(true)} />
      <main className={styles.main}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ch1" element={<Ch1Overview />} />
          <Route path="/ch2" element={<Ch2RunConfig />} />
          <Route path="/ch3" element={<Ch3Tier0Feeder />} />
          <Route path="/ch4" element={<Ch4JobSplitting />} />
          <Route path="/ch5" element={<Ch5Closeout />} />
          <Route path="/ch6" element={<Ch6Operator />} />
          <Route path="/glossary" element={<Glossary />} />
          <Route
            path="/sim/tier0-feeder-tick"
            element={<SimTier0FeederTick />}
          />
          <Route path="/sim/lifecycle" element={<SimLifecycle />} />
          <Route path="/sim/jobsplitting" element={<SimJobSplitting />} />
          <Route path="/sim/closeout" element={<SimCloseout />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <CommandPalette
        open={paletteOpen}
        onClose={() => setPaletteOpen(false)}
      />
    </div>
  );
}
