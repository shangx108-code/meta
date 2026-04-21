import csv
import json
import random
from pathlib import Path

random.seed(42)
root = Path(__file__).resolve().parents[1]
results = root / "results"
results.mkdir(parents=True, exist_ok=True)

fourier_depth = [1, 2, 3, 4]
local_strength = [0.0, 0.25, 0.5, 0.75, 1.0]
rows = []
best = None

for d in fourier_depth:
    for l in local_strength:
        base = 0.12 - 0.01 * d - 0.02 * l
        penalty = 0.015 if (d > 3 and l > 0.8) else 0.0
        noise = random.uniform(-0.002, 0.002)
        rel_l2 = max(base + penalty + noise, 0.03)
        item = {"fourier_depth": d, "local_strength": l, "relative_l2": rel_l2}
        rows.append(item)
        best = item if best is None or rel_l2 < best["relative_l2"] else best

with (results / "phase0_structure_error_map.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["fourier_depth", "local_strength", "relative_l2"])
    writer.writeheader()
    writer.writerows(rows)

summary = {
    "topic": "pno_phase0",
    "best_fourier_depth": best["fourier_depth"],
    "best_local_strength": best["local_strength"],
    "best_relative_l2": best["relative_l2"],
    "note": "Synthetic phase-0 scan for pipeline validation only; not a scientific claim."
}
(results / "metrics_phase0.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
