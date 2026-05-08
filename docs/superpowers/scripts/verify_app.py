"""Verify the T0 guide v2 app is well-formed.

Checks:
1. All 22 expected diagram files are present
2. All 4 simulator files are present
3. All routes (Home + 6 chapters + 4 sims + glossary) are registered in lib/routes.ts and App.tsx
4. tsc --noEmit returns 0
5. No console.error( calls in src/

Heavy checks gated behind --full:
6. npm run build returns 0
7. Dev server returns 200 on every route

Run from the repo root or anywhere — paths are anchored to the script.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
APP_DIR = REPO_ROOT / "docs" / "superpowers" / "t0-guide-app"
SRC = APP_DIR / "src"

EXPECTED_DIAGRAMS = [
    "D1_1_PipelineHero",
    "D1_2_TwoDBLayout",
    "D1_3_MultiDBConnectivity",
    "D1_4_DeployTopology",
    "D2_1_RunConfigFlow",
    "D2_2_RunStates",
    "D2_3_StreamStates",
    "D2_4_DSLTimeline",
    "D3_1_Tier0FeederTick",
    "D3_2_MultiAgentSplit",
    "D3_3_StorageManagerPolling",
    "D4_1_SplitterFactory",
    "D4_2_RepackSplitter",
    "D4_3_ExpressSplitter",
    "D4_4_SplitterMatrix",
    "D5_1_CloseoutFlow",
    "D5_2_AlcaHarvestPipe",
    "D5_3_ConditionUpload",
    "D5_4_CloseoutTiming",
    "D6_1_OperatorCLI",
    "D6_2_ReplayByPR",
    "D6_3_DeployScript",
]

EXPECTED_SIMULATORS = [
    "Tier0FeederTickSim",
    "LifecycleSim",
    "JobSplittingSim",
    "CloseoutSim",
]

EXPECTED_ROUTES = [
    "/",
    "/ch1",
    "/ch2",
    "/ch3",
    "/ch4",
    "/ch5",
    "/ch6",
    "/sim/tier0-feeder-tick",
    "/sim/lifecycle",
    "/sim/jobsplitting",
    "/sim/closeout",
    "/glossary",
]


def check_diagrams() -> list[str]:
    issues = []
    diag_dir = SRC / "diagrams"
    for name in EXPECTED_DIAGRAMS:
        path = diag_dir / f"{name}.tsx"
        if not path.exists():
            issues.append(f"missing diagram file: {path.relative_to(REPO_ROOT)}")
    return issues


def check_simulators() -> list[str]:
    issues = []
    sim_dir = SRC / "simulators"
    for name in EXPECTED_SIMULATORS:
        path = sim_dir / f"{name}.tsx"
        if not path.exists():
            issues.append(f"missing simulator file: {path.relative_to(REPO_ROOT)}")
    return issues


def check_routes() -> list[str]:
    issues = []
    routes_ts = (SRC / "lib" / "routes.ts").read_text()
    app_tsx = (SRC / "App.tsx").read_text()
    for path in EXPECTED_ROUTES:
        # In routes.ts the path appears as a string literal; in App.tsx as path="..."
        if path == "/":
            # HOME is keyed by literal "/"
            if "HOME" not in routes_ts or 'path: "/"' not in routes_ts:
                issues.append("HOME route missing from lib/routes.ts")
            if 'path="/"' not in app_tsx:
                issues.append("App.tsx has no <Route path=\"/\" />")
        else:
            if f'path: "{path}"' not in routes_ts:
                issues.append(f"route metadata missing for {path}")
            if f'path="{path}"' not in app_tsx:
                issues.append(f"App.tsx <Route> missing for {path}")
    return issues


def check_typecheck() -> list[str]:
    tsc = APP_DIR / "node_modules" / ".bin" / "tsc"
    if not tsc.exists():
        return [f"tsc binary not found at {tsc.relative_to(REPO_ROOT)} — run npm install"]
    proc = subprocess.run(
        [str(tsc), "--noEmit"],
        cwd=APP_DIR,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return [f"tsc --noEmit failed:\n{proc.stdout}\n{proc.stderr}"]
    return []


def check_no_console_error() -> list[str]:
    issues = []
    for path in SRC.rglob("*.ts*"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text()
        for i, line in enumerate(text.splitlines(), start=1):
            if re.search(r"\bconsole\.error\s*\(", line):
                rel = path.relative_to(REPO_ROOT)
                issues.append(f"console.error at {rel}:{i}")
    return issues


def check_build() -> list[str]:
    npm = "npm"
    proc = subprocess.run(
        [npm, "run", "build"],
        cwd=APP_DIR,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return [f"npm run build failed:\n{proc.stdout[-1000:]}\n{proc.stderr[-1000:]}"]
    dist = APP_DIR / "dist"
    if not (dist / "index.html").exists():
        return ["npm run build succeeded but dist/index.html is missing"]
    return []


def check_dev_server() -> list[str]:
    issues: list[str] = []
    vite = APP_DIR / "node_modules" / ".bin" / "vite"
    if not vite.exists():
        return [f"vite binary not found at {vite.relative_to(REPO_ROOT)}"]
    # Pick an unlikely port to avoid clashes
    port = 5180
    proc = subprocess.Popen(
        [str(vite), "--port", str(port), "--host", "127.0.0.1"],
        cwd=APP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    try:
        # Wait for server to come up (poll /)
        deadline = time.time() + 20
        ready = False
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/", timeout=2
                ) as r:
                    if r.status == 200:
                        ready = True
                        break
            except (urllib.error.URLError, ConnectionError, TimeoutError):
                time.sleep(0.5)
        if not ready:
            return ["dev server did not respond within 20s"]
        for path in EXPECTED_ROUTES:
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}{path}", timeout=5
                ) as r:
                    if r.status != 200:
                        issues.append(f"{path}: HTTP {r.status}")
            except urllib.error.URLError as e:
                issues.append(f"{path}: error {e}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    return issues


CHECKS_FAST = [
    ("diagrams present", check_diagrams),
    ("simulators present", check_simulators),
    ("routes registered", check_routes),
    ("tsc --noEmit clean", check_typecheck),
    ("no console.error in src", check_no_console_error),
]

CHECKS_HEAVY = [
    ("npm run build", check_build),
    ("dev server smoke test", check_dev_server),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="also run heavy checks (npm run build, dev server)",
    )
    args = parser.parse_args()

    checks = CHECKS_FAST + (CHECKS_HEAVY if args.full else [])
    failed = 0
    for label, fn in checks:
        issues = fn()
        if issues:
            failed += 1
            print(f"FAIL  {label}")
            for issue in issues:
                print(f"      - {issue}")
        else:
            print(f"OK    {label}")
    print()
    if failed:
        print(f"{failed}/{len(checks)} check(s) failed")
        return 1
    print(f"All {len(checks)} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
