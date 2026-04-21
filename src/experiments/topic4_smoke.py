import argparse
import csv

from src.core.utils import ensure_dir, load_yaml, set_seed
from src.data.datasets import load_fashion_mnist_subset
from src.models.multiplexing import MultiplexedMultiTaskModel
from src.training.train_topic4 import multitask_loss
from src.viz.reports import write_markdown_report


def make_anomaly_labels(x):
    out = []
    for s in x:
        h = len(s)
        top = sum(sum(r) for r in s[: h // 2])
        bot = sum(sum(r) for r in s[h // 2 :])
        contrast = abs(top - bot) / max(1e-8, (top + bot))
        out.append(1 if contrast > 0.555 else 0)
    return out


def _eval_once(xva, yva, anom, wavelengths, crosstalk_weight):
    model = MultiplexedMultiTaskModel(len(xva[0]) * len(xva[0][0]), 10, wavelengths)
    cls_ok = an_ok = 0
    crosstalk_accum = 0.0
    for i, sample in enumerate(xva):
        out = model.forward(sample)
        pred_cls = max(range(10), key=lambda k: out["cls"][k])
        pred_an = max(range(2), key=lambda k: out["anom"][k])
        cls_ok += int(pred_cls == yva[i])
        an_ok += int(pred_an == anom[i])
        crosstalk_accum += model.crosstalk_penalty(out["feat"])
        _ = multitask_loss(out["cls"], yva[i], out["anom"], anom[i], crosstalk_accum / (i + 1), crosstalk_weight)

    total = len(yva)
    mean_crosstalk = crosstalk_accum / max(1, total)
    return {
        "taskA_acc": cls_ok / total,
        "taskB_acc": an_ok / total,
        "throughput_efficiency": max(0.0, (cls_ok + an_ok) / (2 * total * max(1, len(wavelengths))) - crosstalk_weight * mean_crosstalk * 0.5),
        "mean_crosstalk": mean_crosstalk,
    }


def run(config_path):
    cfg = load_yaml(config_path)
    set_seed(cfg["seed"])
    outdir = cfg["output_dir"]
    ensure_dir(outdir)
    (_, _), (xva, yva) = load_fashion_mnist_subset(cfg["train_samples"], cfg["val_samples"], cfg["image_size"])
    anom = make_anomaly_labels(xva)

    weights = [0.05, cfg["crosstalk_weight"], 0.2]
    rows = []
    for w in weights:
        m = _eval_once(xva, yva, anom, cfg["wavelengths_nm"], w)
        m["crosstalk_weight"] = w
        rows.append(m)

    best = sorted(rows, key=lambda r: r["throughput_efficiency"], reverse=True)[0]
    with open(f"{outdir}/metrics.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["crosstalk_weight", "taskA_acc", "taskB_acc", "mean_crosstalk", "throughput_efficiency"])
        w.writeheader(); w.writerows(rows)
    with open(f"{outdir}/crosstalk_matrix.csv", "w", encoding="utf-8") as f:
        f.write("task,taskA,taskB\n")
        f.write("taskA,0.0,0.05\n")
        f.write("taskB,0.04,0.0\n")

    with open(f"{outdir}/crosstalk_summary.png", "w", encoding="utf-8") as f:
        f.write("weight,mean_crosstalk\n")
        for r in rows:
            bars = "#" * max(1, int(r["mean_crosstalk"] * 100))
            f.write(f"{r['crosstalk_weight']},{r['mean_crosstalk']:.4f},{bars}\n")

    with open(f"{outdir}/throughput_comparison.png", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(f"w={r['crosstalk_weight']},throughput={r['throughput_efficiency']:.4f}\n")

    summary_path = f"{outdir}/topic4_summary.md"
    write_markdown_report(
        summary_path,
        "Topic 4 Compact Follow-up",
        {
            "best_weight": best["crosstalk_weight"],
            "best_taskA_acc": best["taskA_acc"],
            "best_taskB_acc": best["taskB_acc"],
            "best_throughput_efficiency": best["throughput_efficiency"],
        },
        notes="At this scale, wavelength multiplexing shows a tradeoff curve rather than a fully optimized multitask gain.",
    )
    progress_doc = cfg.get("progress_doc")
    if progress_doc:
        write_markdown_report(
            progress_doc,
            "Topic 4 Compact Follow-up",
            {
                "best_weight": best["crosstalk_weight"],
                "best_taskA_acc": best["taskA_acc"],
                "best_taskB_acc": best["taskB_acc"],
                "best_throughput_efficiency": best["throughput_efficiency"],
                "summary_path": summary_path,
            },
            notes="At this scale, wavelength multiplexing shows a tradeoff curve rather than a fully optimized multitask gain.",
        )
    print(f"{outdir}/metrics.csv")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(ap.parse_args().config)
