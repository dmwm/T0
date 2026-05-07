# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

CMS **Tier-0 (T0)** — the workload-management agent that runs CMS data taking at CERN. It is built on top of [WMCore](https://github.com/dmwm/WMCore)'s `WMAgent` framework and distributed as the PyPI package `T0`. The agent ingests streamer files from the online Storage Manager database, drives the offline processing chain (Repack → Express → PromptReco → AlcaHarvest), and uploads PCL conditions. This repo holds both the Python library code *and* the operational shell scripts/configs the T0 operators use on the deploy hosts.

`__version__` lives in `src/python/T0/__init__.py` (currently `3.5.5`). Pushing a change to that file to `master` triggers `create_tag_and_release.yaml` (tag + GitHub release) and `pypi_build_publish_template.yaml` (PyPI publish via twine).

## Build, dev, and validation commands

```bash
# Set PYTHONPATH / PATH / T0_ROOT for in-place dev (must be eval'd, not just run)
eval `python setup.py -q env`

# Build the PyPI sdist (CI uses setup_template.py + tools/build_pypi_packages.sh; this is the local equivalent)
python setup_t0.py sdist
sh tools/build_pypi_packages.sh T0       # full CI-equivalent build + twine upload

# Tier0Config unit tests — the ONLY tests that run without WMCore + Oracle + Couch
python -m unittest test.python.T0_t.RunConfig_t.Tier0Config_t

# Configuration validation (what CI runs on PRs that touch etc/*ProdOfflineConfiguration.py)
python -m py_compile etc/ProdOfflineConfiguration.py
flake8 --select=ISC001,F821,F811,E999,W605 etc/ProdOfflineConfiguration.py
python test/python/validate_config.py etc/ProdOfflineConfiguration.py
```

Everything else under `test/python/` (Tier0Feeder, JobSplitting, RunConfig DAO tests) uses `WMQuality.TestInit` and requires:
- `WMCore` importable on `PYTHONPATH`
- `WMAGENT_CONFIG` env var pointing at a real WMAgent config
- A reachable Oracle T0AST schema *and* CouchDB

There is **no pytest, lint, or formatter configuration** beyond the narrow flake8 rule subset above. Don't introduce one without being asked.

## Architecture

### Two source roots
- `src/python/T0/` — pure libraries (no WMAgent harness): `RunConfig` (incl. `Tier0Config.py`, the public DSL used by `etc/*OfflineConfiguration.py`), `JobSplitting`, `RunLumiCloseout`, `ConditionUpload`, `StorageManager`, `WMSpec`, and the DAO tree under `WMBS/Oracle/`.
- `src/python/T0Component/` — WMAgent components (subclasses of `WMCore.Agent.Harness`): `Tier0Feeder` is the active one; `Tier0Auditor` is a stub.

### How a run flows through the system

`T0Component.Tier0Feeder.Tier0FeederPoller.algorithm` is the heartbeat. Each tick it:

1. Connects to several Oracle DBs simultaneously: local **T0AST**, **HLTConfDB**, **StorageManagerDB**, and optionally `SMNotifyDB` / `PopConLogDB` / `T0DataSvcDB` (each is a separate `DBFactory`/`DAOFactory` and only enabled if the corresponding `config.<...>Database` block exists).
2. Discovers new runs/streams (`T0.WMBS.Oracle.Tier0Feeder.FindNewRuns`, `FindNewRunStreams`) and configures them via `T0.RunConfig.RunConfigAPI.configureRun` / `configureRunStream` — these are the entry points that parse the `Tier0Config` DSL into rows in T0AST.
3. Hands streamer files to the Repack / Express splitters in `T0.JobSplitting/` (loaded via `SplitterFactory(package="T0.JobSplitting")`), which create WMBS jobs.
4. Releases PromptReco workflows once a CMSSW release is announced (`RunConfigAPI.releasePromptReco`).
5. Drives AlcaHarvest closeout and condition uploads (`T0.ConditionUpload.ConditionUploadAPI`).

DAOs are *all* under `src/python/T0/WMBS/Oracle/<area>/` and are accessed via `DAOFactory(package="T0.WMBS", classname="<area>.<Name>")`. Schema bootstrap is `T0.WMBS.Oracle.Create`. There is no SQLite/MySQL backend — Oracle only.

### Multi-agent split (Main + Helpers)

`Tier0FeederPoller` instantiates either `MainAgent` or `HelperAgent` (both in `T0Component/Tier0Feeder/MultipleAgents/`) based on `config.Tier0Feeder.agentName`. The mapping comes from the **Tier0Config**, not the WMAgent config:

```python
tier0Config.Global.HelperAgentStreams = {'SecondAgent': ['stream_a', 'stream_b'], ...}
```

`HelperAgent` only processes streams listed for its name; `MainAgent` processes everything *not* listed in any helper. Touching this code requires keeping `findUnwantedStreams`, `filterStreamerFiles`, and `filterHltConfigStreams` consistent on both sides.

### The `Tier0Config` DSL

`src/python/T0/RunConfig/Tier0Config.py` defines the public surface that operator-edited configs in `etc/` import: `createTier0Config`, `addDataset`, `addRepackConfig`, `addExpressConfig`, `setAcquisitionEra`, `setInjectRuns`, `setBackfill`, `setProcessingSite`, `addSiteConfig`, `setHelperAgentStreams`, `specifyStreams`, etc. The top-of-file docstring is the canonical schema reference — update it when adding a setter. The same module is consumed by both the WMAgent (at runtime, via `WMCore.Configuration.loadConfigurationFile`) and by `bin/t0` for tarball-path lookups.

## Operational layer (this matters — most PRs touch it)

The repo doubles as the source of truth for what runs on the production deploy hosts (`vocms047`, `vocms0500`, `vocms05011`, `vocms05012` under user `cmst0`). On those hosts the shell scripts live in `/data/tier0/`; `bin/pypi_update.sh` re-pulls them from `master`.

- `bin/00_pypi_deploy_replay.sh` and `00_pypi_deploy_prod.sh` are the deploy entry points. Each **pins its own `WMAGENT_TAG` and `TIER0_VERSION`** at the top of the file. These pins drift from `src/python/T0/__init__.py:__version__` — the `__init__` version controls what is *published* to PyPI; the deploy scripts control what is *installed*. When asked "what version is in production?" check the deploy script, not `__init__.py`.
- `bin/00_pypi_patches.sh` cherry-picks WMCore/T0 PRs from contributor forks via `curl … | patch` at deploy time. Treat patches in that file as live operational state, not committed source — they get rotated frequently.
- `bin/t0` is the operator CLI on the deploy host (`t0 --start-agent`, `--stop-agent`, `--update-t0=<version>`, `--clear-deployment`, `--get-tarball`, etc.). It hardcodes `/data/tier0/` paths.
- `etc/ReplayOfflineConfiguration.py` is rewritten frequently and is treated as scratch state for the next replay. The HI/OXY/XeXe variants are for special data-taking eras. Production configs (`etc/*ProdOfflineConfiguration.py`) are gated by `validate-config.yaml` CI.

### Replay-by-PR-comment workflow

`.github/workflows/deployReplayPR.yaml` lets authorized operators deploy a replay from a PR comment. Triggers (case-sensitive substrings):

| Comment | Action |
| --- | --- |
| `may I replay?` | Posts the current default parameters and node availability |
| `verify nodes` | Posts node status (HTCondor queue depth) |
| `run autoreplay` | Actually deploys the PR's replay config to a node |

Authorization is a hardcoded list (`AUTHORIZED_USERS`) and node whitelist (`ALLOWED_NODES`) in the workflow's `env:` block. Defaults for T0 version, WMCore version, target node, etc. also live there and drift independently of the deploy scripts. When updating defaults, update the workflow `env:` — there is no other source.

### CI workflows summary

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `validate-config.yaml` | PR touching `etc/*ProdOfflineConfiguration.py` | py_compile → narrow flake8 → `validate_config.py` (dataset family gap detection) |
| `create_tag_and_release.yaml` | push to master touching `src/python/T0/__init__.py` | git tag + GitHub release at the new version |
| `pypi_build_publish_template.yaml` | push to master touching `src/python/T0/__init__.py` | sdist + `twine upload` to PyPI |
| `deployReplayPR.yaml` | issue_comment on a PR | Operator-driven replay deployment (see above) |
