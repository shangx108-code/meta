"""Phase-1 non-stationary adaptation simulation with fixed trunk + programmable gains."""
import csv
import json
import math
import random
from pathlib import Path

random.seed(7)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

DIM = 8
W = [random.uniform(-1, 1) for _ in range(DIM)]


def make_data(n=400, shifted=False):
    xs, ys = [], []
    for i in range(n):
        label = 1 if i % 2 == 0 else 0
        mu = 0.9 if label == 1 else -0.9
        x = [random.gauss(mu, 0.7) for _ in range(DIM)]
        if shifted:
            x = [0.6 * v + 0.3 * math.sin(j + 1) + random.gauss(0, 0.2) for j, v in enumerate(x)]
        xs.append(x)
        ys.append(label)
    return xs, ys


def score(x, gains):
    return sum(gains[i] * W[i] * x[i] for i in range(DIM))


def choose_threshold(xs, ys, gains):
    scores = [score(x, gains) for x in xs]
    # midpoint between class means
    pos = [s for s, y in zip(scores, ys) if y == 1]
    neg = [s for s, y in zip(scores, ys) if y == 0]
    th = (sum(pos) / len(pos) + sum(neg) / len(neg)) / 2
    sign = 1 if sum(pos) > sum(neg) else -1
    return th, sign


def evaluate(xs, ys, gains, th=0.0, sign=1):
    ok = 0
    for x, y in zip(xs, ys):
        s = sign * score(x, gains)
        pred = 1 if s > th else 0
        ok += 1 if pred == y else 0
    return ok / len(xs)


def tune(xs, ys, gains, idx, steps=120, lr=0.03):
    g = gains[:]
    for _ in range(steps):
        for i in idx:
            grad = 0.0
            for x, y in zip(xs[:150], ys[:150]):
                z = score(x, g)
                p = 1 / (1 + math.exp(-max(min(z, 20), -20)))
                grad += (p - y) * W[i] * x[i]
            g[i] -= lr * grad / 150.0
    return g


src_x, src_y = make_data(shifted=False)
shf_x, shf_y = make_data(shifted=True)
base = [1.0 for _ in range(DIM)]
th0, sign0 = choose_threshold(src_x, src_y, base)
acc_source = evaluate(src_x, src_y, base, th=th0, sign=sign0)
acc_shift = evaluate(shf_x, shf_y, base, th=th0, sign=sign0)

k = max(1, int(DIM * 0.25))
local_idx = sorted(range(DIM), key=lambda i: abs(W[i]), reverse=True)[:k]
all_idx = list(range(DIM))
local_g = tune(shf_x, shf_y, base, local_idx, steps=120)
global_g = tune(shf_x, shf_y, base, all_idx, steps=160)

th_e, sign_e = choose_threshold(shf_x[:150], shf_y[:150], base)
th_l, sign_l = choose_threshold(shf_x[:150], shf_y[:150], local_g)
th_g, sign_g = choose_threshold(shf_x[:150], shf_y[:150], global_g)

acc_elec = evaluate(shf_x, shf_y, base, th=th_e, sign=sign_e)
acc_local = evaluate(shf_x, shf_y, local_g, th=th_l, sign=sign_l)
acc_global = evaluate(shf_x, shf_y, global_g, th=th_g, sign=sign_g)


def recovery(acc):
    gap = max(acc_source - acc_shift, 1e-12)
    return (acc - acc_shift) / gap


rows = [
    {"strategy": "none", "shifted_accuracy": acc_shift, "recovery_ratio": 0.0, "cost_proxy": 0.0},
    {"strategy": "electronic_comp", "shifted_accuracy": acc_elec, "recovery_ratio": recovery(acc_elec), "cost_proxy": 0.2},
    {"strategy": "local_tuning", "shifted_accuracy": acc_local, "recovery_ratio": recovery(acc_local), "cost_proxy": 0.4},
    {"strategy": "global_retrain", "shifted_accuracy": acc_global, "recovery_ratio": recovery(acc_global), "cost_proxy": 1.0},
]

with (OUT / "phase1_adaptation_metrics.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["strategy", "shifted_accuracy", "recovery_ratio", "cost_proxy"])
    w.writeheader()
    w.writerows(rows)

summary = {
    "topic": "meta_adapt_phase1",
    "source_accuracy": acc_source,
    "shifted_accuracy": acc_shift,
    "best_accuracy_strategy": max(rows[1:], key=lambda r: r["shifted_accuracy"])["strategy"],
    "best_cost_effective_strategy": max(rows[1:], key=lambda r: r["recovery_ratio"] - 0.3 * r["cost_proxy"])["strategy"],
    "claim_boundary": "Local tuning/global retrain tradeoff is scenario-dependent in this toy setup.",
}
(OUT / "phase1_assessment.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
