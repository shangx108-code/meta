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


def _read_backend_used(metrics_csv):
    ckpt = metrics_csv.replace("metrics.csv", "checkpoints/final.pt")
    try:
        with open(ckpt, "r", encoding="utf-8") as f:
            payload = json.load(f)
        return payload.get("backend_used", "unknown")
    except Exception:
        return "unknown"


def _write_robustness_summary_plot(rows, out_path):
    groups = {}
    for r in rows:
        key = (r["train_mode"], r["coherence"], r["num_wavelengths"], r["lateral_shift_px"])
        groups.setdefault(key, []).append(r["val_acc"])
    lines = ["Topic1 robustness trend summary", "mode,coherence,num_wavelengths,lateral_shift,mean_acc"]
    for key, vals in sorted(groups.items()):
        lines.append(f"{key[0]},{key[1]},{key[2]},{key[3]},{sum(vals)/len(vals):.6f}")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def _write_ablation(rows, out_csv, out_plot):
    def mean(v):
        return sum(v) / max(1, len(v))

    by_mode = {}
    by_coh = {}
    by_bw = {}
    by_shift = {}
    for r in rows:
        by_mode.setdefault(r["train_mode"], []).append(r["val_acc"])
        by_coh.setdefault(str(r["coherence"]), []).append(r["val_acc"])
        by_bw.setdefault(str(r["num_wavelengths"]), []).append(r["val_acc"])
        by_shift.setdefault(str(r["lateral_shift_px"]), []).append(r["val_acc"])

    ablation_rows = []
    for k, vals in sorted(by_mode.items()):
        ablation_rows.append({"axis": "train_mode", "setting": k, "mean_val_acc": round(mean(vals), 6)})
    for k, vals in sorted(by_coh.items()):
        ablation_rows.append({"axis": "coherence", "setting": k, "mean_val_acc": round(mean(vals), 6)})
    for k, vals in sorted(by_bw.items()):
        ablation_rows.append({"axis": "num_wavelengths", "setting": k, "mean_val_acc": round(mean(vals), 6)})
    for k, vals in sorted(by_shift.items()):
        ablation_rows.append({"axis": "lateral_shift_px", "setting": k, "mean_val_acc": round(mean(vals), 6)})

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["axis", "setting", "mean_val_acc"])
        w.writeheader(); w.writerows(ablation_rows)

    with open(out_plot, "w", encoding="utf-8") as f:
        f.write("Topic1 aggregated comparison (text-plot fallback)\n")
        for row in ablation_rows:
            bars = "#" * max(1, int(row["mean_val_acc"] * 40))
            f.write(f"{row['axis']}={row['setting']}: {row['mean_val_acc']:.4f} {bars}\n")


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
                    rows.append(
                        {
                            "run_id": run_id,
                            "train_mode": train_mode,
                            "coherence": coh,
                            "num_wavelengths": len(bw),
                            "lateral_shift_px": mis["lateral_shift_px"],
                            "val_acc": float(final["val_acc"]),
                            "val_loss": float(final["val_loss"]),
                            "backend_used": _read_backend_used(metrics_path),
                            "metrics_csv": metrics_path,
                        }
                    )
                    plot_metric_curves(metrics_path, f"{local_out}/curve.png", y="val_acc")
                    run_id += 1

    sweep_csv = f"{outdir}/pilot_sweep.csv"
    with open(sweep_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    _write_robustness_summary_plot(rows, f"{outdir}/robustness_trends.png")
    _write_ablation(rows, f"{outdir}/ablation_summary.csv", f"{outdir}/aggregated_comparison.png")

    best = sorted(rows, key=lambda r: r["val_acc"], reverse=True)[0]
    unique_acc = len({r["val_acc"] for r in rows})
    backend_set = sorted({r["backend_used"] for r in rows})
    write_markdown_report(
        "docs/progress/topic1_pilot_summary.md",
        "Topic 1 Pilot Summary",
        {
            "best_val_acc": best["val_acc"],
            "best_run_id": best["run_id"],
            "num_runs": len(rows),
            "unique_val_acc_values": unique_acc,
            "backends_detected": ",".join(backend_set),
        },
        notes=f"Best run mode={best['train_mode']} coherence={best['coherence']} wavelengths={best['num_wavelengths']}.",
    )
    print(sweep_csv)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run_pilot(ap.parse_args().config)
