import argparse
import copy
import csv
import json

from src.core.utils import ensure_dir, load_yaml
from src.training.train_topic1 import run_topic1
from src.viz.plots import plot_metric_curves
from src.viz.reports import write_markdown_report


def _read_last_metrics(path):
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[-1]


def run_pilot(config_path):
    cfg = load_yaml(config_path)
    outdir = cfg["output_dir"]
    ensure_dir(outdir)
    rows = []
    run_id = 0
    for train_mode in ["ideal", "robust"]:
        for coh in cfg["coherence_grid"]:
            for bw in cfg["bandwidth_grid"]:
                for mis in cfg["misalignment_grid"]:
                    local = copy.deepcopy(cfg)
                    local["coherence_mix"] = coh
                    local["wavelengths_nm"] = bw
                    local.update(mis)
                    local["robust_training"] = train_mode == "robust"
                    local_out = f"{outdir}/runs/run_{run_id}_{train_mode}_coh{coh}_bw{len(bw)}"
                    local["output_dir"] = local_out
                    tmp_cfg = f"{outdir}/tmp_run_{run_id}.json"
                    with open(tmp_cfg, "w", encoding="utf-8") as f:
                        json.dump(local, f)
                    metrics_path = run_topic1(tmp_cfg)
                    final = _read_last_metrics(metrics_path)
                    rows.append({
                        "run_id": run_id,
                        "train_mode": train_mode,
                        "coherence": coh,
                        "num_wavelengths": len(bw),
                        "lateral_shift_px": mis["lateral_shift_px"],
                        "val_acc": float(final["val_acc"]),
                        "val_loss": float(final["val_loss"]),
                        "metrics_csv": metrics_path,
                    })
                    plot_metric_curves(metrics_path, f"{local_out}/curve.png", y="val_acc")
                    run_id += 1
    sweep_csv = f"{outdir}/pilot_sweep.csv"
    with open(sweep_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    best = sorted(rows, key=lambda r: r["val_acc"], reverse=True)[0]
    write_markdown_report("docs/progress/topic1_pilot_summary.md", "Topic 1 Pilot Summary", {"best_val_acc": best["val_acc"], "best_run_id": best["run_id"], "num_runs": len(rows)}, notes=f"Best run mode={best['train_mode']} coherence={best['coherence']} wavelengths={best['num_wavelengths']}")
    print(sweep_csv)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run_pilot(ap.parse_args().config)
