# Recovery Round 2026-04-29

## Durable updates
- Confirmed blocker: the current scheduled-run workspace contains the Majorana project memory, but not the executable three-terminal benchmark scripts or the historical benchmark outputs needed for a real rerun. [active blocker]
- Recovered the three-terminal benchmark provenance into `/workspace/output/three-terminal-benchmark/RECOVERY_MANIFEST.md`. [verified]
- Recovered a machine-readable expected-asset list into `/workspace/output/three-terminal-benchmark/provenance_manifest.json`. [verified]
- Updated the project bottleneck from a generic "missing rerun" description to a concrete missing-bundle recovery state. [verified]
- Added a runnable recovery bootstrap at `/workspace/memory/majorana-diagnostic-natphys/code/majorana_recovery_bootstrap.py` that rebuilds the recovery folder and audits the scheduled-run environment. [verified]
- Re-ran the recovery bootstrap and regenerated `RECOVERY_MANIFEST.md`, `provenance_manifest.json`, `environment_audit.json`, and `missing_assets.json` in the current workspace. [verified]
- Expanded the recovery search across the live workspace/container and connected Google Drive metadata, and did not recover `three_terminal_benchmark.py` or any of the nine expected bundle assets. [verified]
- Confirmed that the current scheduled-run environment imports `numpy` and `pandas` but is missing `scipy` and `matplotlib`, so the benchmark rerun environment is still incomplete even before historical data restoration. [active blocker]
- Confirmed that no three-terminal benchmark entry script is present at the searched recovery paths and that all nine expected benchmark assets remain absent from the current workspace. [active blocker]
- Executed a direct environment-recovery attempt with `python -m pip install scipy matplotlib`, and the install failed because the scheduled container cannot reach the configured package index proxy (`403 Forbidden`), so dependency restoration is currently blocked upstream of the benchmark rerun. [active blocker]
- Re-ran `majorana_recovery_bootstrap.py` once more in the current scheduled run and reconfirmed the same recovery state: 9 missing benchmark assets and no ready rerun path. [verified]
- Repeated a targeted connected-Google-Drive search for `majorana three terminal benchmark` and `majorana three terminal figures`, and both queries returned no recoverable archive result. [verified]

## Rejected from long-term state
- Any claim that the three-terminal numerical bundle itself has been regenerated. [unverified - do not commit]
- Any claim that `nu_ring` or `P_topo` were recomputed in this round. [unverified - do not commit]
- Any manuscript-strength interpretation upgrade based only on the recovered provenance files. [unverified - do not commit]
- Any claim that the environment is now fully ready for the three-terminal rerun. [unverified - do not commit]
- Any claim that the missing dependencies can be fixed from this scheduled container by a normal online `pip install` path. [unverified - do not commit]

## Current stable bottleneck
- The current workspace still lacks the shared three-terminal benchmark entry script and all historical bundle assets, and the scheduled-run Python environment still lacks `scipy` and `matplotlib`; this round additionally verified that the container cannot fetch those packages from its configured package index proxy, so both code recovery and dependency restoration remain blocked before the full-device topology rerun can start.
- A fresh targeted connected-Google-Drive search also failed to expose the missing script or bundle, so the persistent-source recovery path is now narrowed to storage that is not mounted here and not discoverable through the current Drive index.

## Next durable action
- Restore the shared three-terminal benchmark script and historical bundle from a persistent source that is not yet mounted into the current workspace or indexed in connected Google Drive search, and pair that recovery with an offline or prebundled path for `scipy` and `matplotlib` before attempting the matched transport-plus-topology rerun.
