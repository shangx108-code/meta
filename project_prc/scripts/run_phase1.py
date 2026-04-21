"""Phase-1 reservoir simulation for memory/capacity trends."""
import csv
import json
import math
import random
from pathlib import Path

random.seed(123)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)


def tanh(x):
    ex = math.exp(max(min(x, 20), -20))
    enx = math.exp(max(min(-x, 20), -20))
    return (ex - enx) / (ex + enx)


def generate_u(T=1200):
    return [random.uniform(0, 0.5) for _ in range(T)]


def run_reservoir(u, gain=0.6, beta=0.8):
    x = 0.0
    states = []
    for t in range(len(u)):
        x = tanh(gain * x + beta * u[t])
        states.append(x)
    return states


def corr(a, b):
    n = len(a)
    ma = sum(a) / n
    mb = sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if va <= 1e-12 or vb <= 1e-12:
        return 0.0
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    return cov / math.sqrt(va * vb)


def memory_capacity(u, states, max_lag=20):
    caps = []
    for k in range(1, max_lag + 1):
        a = states[k:]
        b = u[:-k]
        c = corr(a, b)
        caps.append(c * c)
    return sum(caps)


def narma10(u):
    y = [0.0 for _ in u]
    for t in range(10, len(u) - 1):
        y[t + 1] = 0.3 * y[t] + 0.05 * y[t] * sum(y[t - i] for i in range(10)) + 1.5 * u[t - 9] * u[t] + 0.1
    return y


def fit_poly2(x, y):
    # least squares for y = a + b*x + c*x^2
    n = len(x)
    s1 = n
    sx = sum(x)
    sx2 = sum(v * v for v in x)
    sx3 = sum(v ** 3 for v in x)
    sx4 = sum(v ** 4 for v in x)
    sy = sum(y)
    sxy = sum(x[i] * y[i] for i in range(n))
    sx2y = sum((x[i] ** 2) * y[i] for i in range(n))

    A = [[s1, sx, sx2], [sx, sx2, sx3], [sx2, sx3, sx4]]
    b = [sy, sxy, sx2y]

    # gaussian elimination
    for i in range(3):
        piv = A[i][i] if abs(A[i][i]) > 1e-12 else 1e-12
        for j in range(i, 3):
            A[i][j] /= piv
        b[i] /= piv
        for r in range(3):
            if r == i:
                continue
            f = A[r][i]
            for c in range(i, 3):
                A[r][c] -= f * A[i][c]
            b[r] -= f * b[i]
    return b  # a,b,c


def narma_nrmse(states, target):
    split = int(0.7 * len(states))
    a, b, c = fit_poly2(states[:split], target[:split])
    pred = [a + b * s + c * (s ** 2) for s in states[split:]]
    truth = target[split:]
    mse = sum((pred[i] - truth[i]) ** 2 for i in range(len(pred))) / len(pred)
    mean = sum(truth) / len(truth)
    var = sum((v - mean) ** 2 for v in truth) / len(truth)
    return math.sqrt(mse / (var + 1e-12))


u = generate_u()
y = narma10(u)
rows = []
for g in [0.2, 0.4, 0.6, 0.8, 1.0]:
    st = run_reservoir(u, gain=g)
    mc = memory_capacity(u, st, max_lag=20)
    err = narma_nrmse(st, y)
    rows.append({"feedback_gain": g, "memory_capacity": mc, "narma10_nrmse": err})

with (OUT / "phase1_reservoir_metrics.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["feedback_gain", "memory_capacity", "narma10_nrmse"])
    w.writeheader()
    w.writerows(rows)

best_mem = max(rows, key=lambda r: r["memory_capacity"])
best_task = min(rows, key=lambda r: r["narma10_nrmse"])
summary = {
    "topic": "prc_phase1",
    "best_memory_gain": best_mem["feedback_gain"],
    "best_task_gain": best_task["feedback_gain"],
    "claim_boundary": "This toy run provides executable capacity/task metrics; WDM and multi-task effects remain untested.",
}
(OUT / "phase1_assessment.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
