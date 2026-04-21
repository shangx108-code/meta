import csv
import json
import random
from pathlib import Path

random.seed(123)
root = Path(__file__).resolve().parents[1]
results = root / "results"
results.mkdir(parents=True, exist_ok=True)

gains = [0.1, 0.3, 0.5, 0.7, 0.9]
rows = []
for g in gains:
    memory_cap = 0.3 + 0.7 * (1 - abs(g - 0.55)) + random.uniform(-0.01, 0.01)
    nonlinear_cap = 0.25 + 0.6 * g - 0.25 * (g ** 2) + random.uniform(-0.01, 0.01)
    rows.append({"feedback_gain": g, "memory_capacity": memory_cap, "nonlinear_capacity": nonlinear_cap})

with (results / "phase0_capacity_curves.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["feedback_gain", "memory_capacity", "nonlinear_capacity"])
    writer.writeheader()
    writer.writerows(rows)

best_memory = max(rows, key=lambda r: r["memory_capacity"])
best_nonlinear = max(rows, key=lambda r: r["nonlinear_capacity"])
summary = {
    "topic": "prc_phase0",
    "best_memory_gain": best_memory["feedback_gain"],
    "best_nonlinearity_gain": best_nonlinear["feedback_gain"],
    "tcf_proxy": sum((r["memory_capacity"] + r["nonlinear_capacity"]) / 2 for r in rows) / len(rows),
    "note": "Synthetic phase-0 dynamic scan for pipeline validation only; not a scientific claim."
}
(results / "metrics_phase0.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
