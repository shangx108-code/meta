import argparse
import csv

from src.core.utils import ensure_dir, load_yaml, set_seed
from src.data.datasets import load_fashion_mnist_subset
from src.models.activations import ActivationParams, nfom_like
from src.training.train_topic2 import ACTS
from src.viz.plots import plot_bar
from src.viz.reports import write_markdown_report


def run(config_path):
    cfg = load_yaml(config_path)
    set_seed(cfg["seed"])
    outdir = cfg["output_dir"]
    ensure_dir(outdir)
    (_, _), (xva, yva) = load_fashion_mnist_subset(cfg["train_samples"], cfg["val_samples"], cfg["image_size"])

    params_by_activation = {
        "saturable": ActivationParams(insertion_loss=0.05, slope=1.0, saturation_threshold=0.35, dynamic_range=1.1, smoothness=1.6),
        "microring": ActivationParams(insertion_loss=0.08, slope=1.4, saturation_threshold=0.45, dynamic_range=1.0, smoothness=1.2),
        "thermal": ActivationParams(insertion_loss=0.12, slope=0.9, saturation_threshold=0.50, dynamic_range=0.95, smoothness=1.8),
        "oe_hybrid": ActivationParams(insertion_loss=0.10, slope=1.8, saturation_threshold=0.40, dynamic_range=1.05, smoothness=1.1),
    }

    rows = []
    for name, fn in ACTS.items():
        p = params_by_activation[name]
        score = 0.0
        for i, sample in enumerate(xva):
            feat = sum(sum(r) for r in sample) / (cfg["image_size"] ** 2)
            out = fn(feat, p)
            pred = int(abs((out + 0.03 * (i % 5)) * 13)) % 10
            score += 1.0 if pred == yva[i] else 0.0
        acc = score / len(yva)
        rows.append({"activation": name, "acc": acc, "nfom": nfom_like(acc, 1.0 + 0.1 * p.dynamic_range, 1.0 + 0.2 * p.slope, p.insertion_loss)})

    rows.sort(key=lambda r: r["nfom"], reverse=True)
    csv_path = f"{outdir}/activation_ranking.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["activation", "acc", "nfom"])
        w.writeheader(); w.writerows(rows)
    plot_bar(rows, x="activation", y="nfom", out_png=f"{outdir}/activation_nfom.png", title="Topic2 NFOM ranking")
    write_markdown_report("docs/progress/topic2_smoke_summary.md", "Topic 2 Smoke", {"best_nfom": rows[0]["nfom"]}, notes="NFOM=(acc*throughput)/(energy*(1+insertion_loss)).")
    print(csv_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run(ap.parse_args().config)
