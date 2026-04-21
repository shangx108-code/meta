import csv
import json
import random
from pathlib import Path

random.seed(7)
root = Path(__file__).resolve().parents[1]
results = root / "results"
results.mkdir(parents=True, exist_ok=True)

fractions = [0.05, 0.1, 0.2, 0.4, 0.8]
rows = []
for f in fractions:
    recovery = 0.45 + 0.55 * (1 - (2.71828 ** (-3 * f))) + random.uniform(-0.01, 0.01)
    cost = 0.1 + 1.4 * f + random.uniform(-0.015, 0.015)
    rows.append({"programmable_fraction": f, "recovery_ratio": recovery, "update_cost": cost})

with (results / "phase0_recovery_cost.csv").open("w", newline="", encoding="utf-8") as fp:
    writer = csv.DictWriter(fp, fieldnames=["programmable_fraction", "recovery_ratio", "update_cost"])
    writer.writeheader()
    writer.writerows(rows)

fr90 = next((r["programmable_fraction"] for r in rows if r["recovery_ratio"] >= 0.9), fractions[-1])
best_idx = max(range(len(rows)), key=lambda i: rows[i]["recovery_ratio"] - 0.25 * rows[i]["update_cost"])
summary = {
    "topic": "meta_adapt_phase0",
    "fraction_at_90pct_recovery": fr90,
    "best_pareto_index": best_idx,
    "note": "Synthetic adaptation tradeoff scan for pipeline validation only; not a scientific claim."
}
(results / "metrics_phase0.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
