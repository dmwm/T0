import { ChapterShell } from "@/components/ChapterShell";
import { JobSplittingSim } from "@/simulators/JobSplittingSim";

export function SimJobSplitting() {
  return (
    <ChapterShell
      eyebrow="Simulator"
      title="JobSplitting"
      subtitle="Tweak caps and watch streamers cut into Repack / Express jobs"
      showPrevNext={false}
    >
      <p>
        Splitter plugins under <code>src/python/T0/JobSplitting/</code> decide
        how a stream of streamer files becomes a queue of WMBS jobs. The same
        cap-then-cut idea runs both <strong>Repack</strong> (RAW packing) and{" "}
        <strong>Express</strong> (fast reconstruction), with different
        defaults. Slide the caps to see the trade-off.
      </p>

      <JobSplittingSim />

      <h2>What you should notice</h2>
      <ul>
        <li>
          Tighter <strong>lumi</strong> caps cut more jobs, each with fewer
          events — better latency, more overhead.
        </li>
        <li>
          Tighter <strong>event</strong> caps protect downstream agents from
          jobs that take too long.
        </li>
        <li>
          Tighter <strong>size</strong> caps protect transfer queues —
          relevant for Express where outputs go to the AlCa stream quickly.
        </li>
      </ul>

      <h2>Where this lives in the code</h2>
      <p>
        Each splitter is a class registered with{" "}
        <code>SplitterFactory(package="T0.JobSplitting")</code>. The Tier0Feeder
        looks up the right plugin per stream and calls{" "}
        <code>split(streamers, ...)</code>. Read{" "}
        <code>RepackJobSplitter.py</code> and{" "}
        <code>ExpressJobSplitter.py</code> alongside this simulator.
      </p>
    </ChapterShell>
  );
}
