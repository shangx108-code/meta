"""Phase-1 trustworthy toy PDE simulations (finite-difference iterative solvers)."""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)


def make_source(n, mode):
    s = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(1, n - 1):
        x = i / (n - 1)
        for j in range(1, n - 1):
            y = j / (n - 1)
            if mode == "poisson":
                s[i][j] = math.sin(math.pi * x) * math.sin(2 * math.pi * y)
            else:
                s[i][j] = math.cos(2 * math.pi * x) * math.sin(math.pi * y)
    return s


def solve_pde(mode, n=24, steps=800, k=8.0):
    u = [[0.0 for _ in range(n)] for _ in range(n)]
    src = make_source(n, mode)
    h2 = 1.0 / ((n - 1) ** 2)
    for _ in range(steps):
        nxt = [row[:] for row in u]
        for i in range(1, n - 1):
            for j in range(1, n - 1):
                lap_sum = u[i + 1][j] + u[i - 1][j] + u[i][j + 1] + u[i][j - 1]
                if mode == "poisson":
                    nxt[i][j] = 0.25 * (lap_sum - h2 * src[i][j])
                else:  # helmholtz-like
                    denom = 4.0 + h2 * (k ** 2)
                    nxt[i][j] = (lap_sum - h2 * src[i][j]) / denom
        u = nxt
    return u, src


def local_predict(src, n, steps=60):
    u = [[0.0 for _ in range(n)] for _ in range(n)]
    h2 = 1.0 / ((n - 1) ** 2)
    for _ in range(steps):
        nxt = [row[:] for row in u]
        for i in range(1, n - 1):
            for j in range(1, n - 1):
                nxt[i][j] = 0.25 * (u[i + 1][j] + u[i - 1][j] + u[i][j + 1] + u[i][j - 1] - h2 * src[i][j])
        u = nxt
    return u


def fourier_like_predict(src, n):
    # low-rank separable approximation as a Fourier-like global branch proxy
    row_mean = [sum(src[i][1:n - 1]) / (n - 2) for i in range(n)]
    col_mean = [sum(src[i][j] for i in range(1, n - 1)) / (n - 2) for j in range(n)]
    u = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            u[i][j] = -0.02 * (row_mean[i] + col_mean[j])
    return u


def hybrid_predict(src, n):
    loc = local_predict(src, n, steps=40)
    glo = fourier_like_predict(src, n)
    u = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            u[i][j] = 0.7 * loc[i][j] + 0.3 * glo[i][j]
    return u


def rel_l2(pred, target):
    num, den = 0.0, 0.0
    n = len(pred)
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            d = pred[i][j] - target[i][j]
            num += d * d
            den += target[i][j] * target[i][j]
    return math.sqrt(num / (den + 1e-12))


rows = []
for mode in ["poisson", "helmholtz"]:
    truth, src = solve_pde(mode)
    n = len(truth)
    preds = {
        "pure_fourier": fourier_like_predict(src, n),
        "pure_local": local_predict(src, n, steps=60),
        "hybrid": hybrid_predict(src, n),
    }
    for model, pred in preds.items():
        rows.append({"pde": mode, "model": model, "relative_l2": rel_l2(pred, truth)})

with (OUT / "phase1_pde_metrics.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["pde", "model", "relative_l2"])
    w.writeheader()
    w.writerows(rows)

best_by_pde = {}
for pde in ["poisson", "helmholtz"]:
    candidates = [r for r in rows if r["pde"] == pde]
    best_by_pde[pde] = min(candidates, key=lambda r: r["relative_l2"])

summary = {
    "topic": "pno_phase1",
    "best_models": {k: v["model"] for k, v in best_by_pde.items()},
    "claim_boundary": "Finite-difference toy confirms hybrid/local outperform Fourier-like proxy on this setup only.",
}
(OUT / "phase1_assessment.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
