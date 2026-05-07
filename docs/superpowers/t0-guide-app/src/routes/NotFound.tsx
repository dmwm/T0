import { Link } from "react-router-dom";
import { ChapterShell } from "@/components/ChapterShell";

export function NotFound() {
  return (
    <ChapterShell
      eyebrow="404"
      title="Route not found"
      subtitle="That URL is not part of the guide."
      showPrevNext={false}
    >
      <p>
        Try the <Link to="/">home page</Link> or use{" "}
        <kbd>⌘ K</kbd> / <kbd>Ctrl K</kbd> to jump anywhere.
      </p>
    </ChapterShell>
  );
}
