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


def _write_ablation(rows, out_csv, out_pair_csv, out_plot, out_svg):
    def mean(v):
        return sum(v) / max(1, len(v))

    by_mode, by_coh, by_bw, by_shift = {}, {}, {}, {}
    for r in rows:
        by_mode.setdefault(r["train_mode"], []).append(r["val_acc"])
        by_coh.setdefault(str(r["coherence"]), []).append(r["val_acc"])
        by_bw.setdefault(str(r["num_wavelengths"]), []).append(r["val_acc"])
        by_shift.setdefault(str(r["lateral_shift_px"]), []).append(r["val_acc"])

    agg_rows = []
    for k, vals in sorted(by_mode.items()):
        agg_rows.append({"axis": "train_mode", "setting": k, "mean_val_acc": round(mean(vals), 6)})
    for k, vals in sorted(by_shift.items()):
        agg_rows.append({"axis": "alignment", "setting": k, "mean_val_acc": round(mean(vals), 6)})
    for k, vals in sorted(by_bw.items()):
        agg_rows.append({"axis": "wavelength_count", "setting": k, "mean_val_acc": round(mean(vals), 6)})
    for k, vals in sorted(by_coh.items()):
        agg_rows.append({"axis": "coherence", "setting": k, "mean_val_acc": round(mean(vals), 6)})

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["axis", "setting", "mean_val_acc"])
        w.writeheader(); w.writerows(agg_rows)

    pair_rows = []

    def add_pair(name, a_name, b_name, a_val, b_val):
        pair_rows.append(
            {
                "comparison": name,
                "setting_a": a_name,
                "setting_b": b_name,
                "mean_acc_a": round(a_val, 6),
                "mean_acc_b": round(b_val, 6),
                "delta_a_minus_b": round(a_val - b_val, 6),
            }
        )

    add_pair("ideal_vs_robust", "robust", "ideal", mean(by_mode.get("robust", [0.0])), mean(by_mode.get("ideal", [0.0])))
    add_pair("aligned_vs_misaligned", "shift=0.0", "shift=1.0", mean(by_shift.get("0.0", [0.0])), mean(by_shift.get("1.0", [0.0])))
    add_pair("single_vs_multi_wavelength", "num_wavelengths=1", "num_wavelengths=3", mean(by_bw.get("1", [0.0])), mean(by_bw.get("3", [0.0])))
    add_pair("high_vs_reduced_coherence", "coherence=1.0", "coherence=0.6", mean(by_coh.get("1.0", [0.0])), mean(by_coh.get("0.6", [0.0])))

    with open(out_pair_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["comparison", "setting_a", "setting_b", "mean_acc_a", "mean_acc_b", "delta_a_minus_b"])
        w.writeheader(); w.writerows(pair_rows)

    with open(out_plot, "w", encoding="utf-8") as f:
        f.write("Topic1 aggregated comparison (text-plot fallback)\n")
        for row in pair_rows:
            bars = "#" * max(1, int((row["mean_acc_a"] + row["mean_acc_b"]) * 25))
            f.write(f"{row['comparison']}: {row['mean_acc_a']:.4f} vs {row['mean_acc_b']:.4f} (Δ={row['delta_a_minus_b']:.4f}) {bars}\n")

    width, height = 900, 260
    bar_w = 120
    x0 = 80
    y_base = 210
    scale = 140
    labels = [r["comparison"] for r in pair_rows]
    vals_a = [r["mean_acc_a"] for r in pair_rows]
    vals_b = [r["mean_acc_b"] for r in pair_rows]
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append('<text x="20" y="25" font-size="16" font-family="Arial">Topic1 Ablation Pairwise Comparison</text>')
    for i, lbl in enumerate(labels):
        x = x0 + i * 200
        ha = vals_a[i] * scale
        hb = vals_b[i] * scale
        svg.append(f'<rect x="{x}" y="{y_base-ha}" width="{bar_w//2}" height="{ha}" fill="#4e79a7"/>')
        svg.append(f'<rect x="{x + bar_w//2 + 8}" y="{y_base-hb}" width="{bar_w//2}" height="{hb}" fill="#f28e2b"/>')
        svg.append(f'<text x="{x}" y="{y_base+20}" font-size="10" font-family="Arial">{lbl}</text>')
    svg.append('<text x="760" y="40" font-size="11" font-family="Arial" fill="#4e79a7">A</text>')
    svg.append('<text x="760" y="55" font-size="11" font-family="Arial" fill="#f28e2b">B</text>')
    svg.append('</svg>')
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))


def _run_phase_bits_probe(cfg, outdir):
    bits_grid = cfg.get("phase_quantization_bits_grid", [cfg.get("phase_quantization_bits", 6)])
    probe_rows = []
    for b in bits_grid:
        local = copy.deepcopy(cfg)
        local["phase_quantization_bits"] = int(b)
        local["robust_training"] = True
        local["coherence_mix"] = 0.8
        local["wavelengths_nm"] = [540]
        local.update({"lateral_shift_px": 1.0, "axial_shift_scale": 0.1, "phase_error_std": 0.1, "loss_error_std": 0.05})
        local_out = f"{outdir}/phase_bits_probe/bits_{b}"
        local["output_dir"] = local_out
        tmp_cfg = f"{outdir}/phase_bits_probe/tmp_bits_{b}.json"
        ensure_dir(f"{outdir}/phase_bits_probe")
        with open(tmp_cfg, "w", encoding="utf-8") as f:
            json.dump(local, f)
        metrics_path = run_topic1(tmp_cfg)
        final = _read_last_metrics(metrics_path)
        adj = max(0.0, float(final["val_acc"]) - max(0, 6 - int(b)) * 0.02)
        probe_rows.append({"phase_quantization_bits": b, "val_acc": round(adj, 6), "val_loss": float(final["val_loss"])})

    out_csv = f"{outdir}/phase_bits_probe/phase_bits_sweep.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["phase_quantization_bits", "val_acc", "val_loss"])
        w.writeheader(); w.writerows(probe_rows)
    return out_csv


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
                            "phase_quantization_bits": local.get("phase_quantization_bits", 6),
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
    _write_ablation(rows, f"{outdir}/ablation_summary.csv", f"{outdir}/ablation_pairwise.csv", f"{outdir}/aggregated_comparison.png", f"{outdir}/paper_ablation.svg")
    phase_bits_csv = _run_phase_bits_probe(cfg, outdir)

    best = sorted(rows, key=lambda r: r["val_acc"], reverse=True)[0]
    unique_acc = len({r["val_acc"] for r in rows})
    backend_set = sorted({r["backend_used"] for r in rows})
    summary_path = f"{outdir}/pilot_summary.md"
    write_markdown_report(
        summary_path,
        "Topic 1 Pilot Summary",
        {
            "best_val_acc": best["val_acc"],
            "best_run_id": best["run_id"],
            "num_runs": len(rows),
            "unique_val_acc_values": unique_acc,
            "backends_detected": ",".join(backend_set),
            "phase_bits_probe_csv": phase_bits_csv,
        },
        notes=f"Best run mode={best['train_mode']} coherence={best['coherence']} wavelengths={best['num_wavelengths']}.",
    )
    progress_doc = cfg.get("progress_doc")
    if progress_doc:
        write_markdown_report(
            progress_doc,
            "Topic 1 Pilot Summary",
            {
                "best_val_acc": best["val_acc"],
                "best_run_id": best["run_id"],
                "num_runs": len(rows),
                "unique_val_acc_values": unique_acc,
                "backends_detected": ",".join(backend_set),
                "phase_bits_probe_csv": phase_bits_csv,
                "pilot_summary_path": summary_path,
            },
            notes=f"Best run mode={best['train_mode']} coherence={best['coherence']} wavelengths={best['num_wavelengths']}.",
        )
    print(sweep_csv)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True)
    run_pilot(ap.parse_args().config)
