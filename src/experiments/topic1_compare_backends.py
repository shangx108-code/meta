import argparse
import csv
import json
import os
import shutil
from pathlib import Path

from src.core.utils import ensure_dir, load_yaml
from src.experiments.topic1_pilot import run_pilot


def _torch_available() -> bool:
    try:
        import torch  # noqa: F401

        return True
    except Exception:
        return False


def _run_with_backend(base_cfg_path: str, backend: str, out_dir: str):
    cfg = load_yaml(base_cfg_path)
    cfg["backend"] = backend
    cfg["output_dir"] = out_dir
    ensure_dir(out_dir)
    cfg_path = f"{out_dir}/config_{backend}.json"
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f)
    run_pilot(cfg_path)
    return cfg_path


def _load_pairwise(csv_path: str):
    with open(csv_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compare(base_cfg_path: str, out_dir: str):
    ensure_dir(out_dir)
    surrogate_dir = f"{out_dir}/surrogate"
    torch_dir = f"{out_dir}/torch"

    _run_with_backend(base_cfg_path, "surrogate", surrogate_dir)
    s_rows = _load_pairwise(f"{surrogate_dir}/ablation_pairwise.csv")

    torch_ok = _torch_available()
    t_rows = None
    if torch_ok:
        _run_with_backend(base_cfg_path, "torch", torch_dir)
        t_rows = _load_pairwise(f"{torch_dir}/ablation_pairwise.csv")

    summary_csv = f"{out_dir}/backend_comparison.csv"
    with open(summary_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "comparison",
            "surrogate_delta",
            "torch_delta",
            "torch_minus_surrogate",
            "status",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        s_map = {r["comparison"]: float(r["delta_a_minus_b"]) for r in s_rows}
        t_map = {r["comparison"]: float(r["delta_a_minus_b"]) for r in t_rows} if t_rows else {}
        for k, sv in s_map.items():
            tv = t_map.get(k)
            w.writerow(
                {
                    "comparison": k,
                    "surrogate_delta": sv,
                    "torch_delta": "" if tv is None else tv,
                    "torch_minus_surrogate": "" if tv is None else round(tv - sv, 6),
                    "status": "torch_unavailable" if tv is None else "ok",
                }
            )

    md = Path(f"{out_dir}/comparison_summary.md")
    lines = ["# Topic1 backend comparison", "", f"- torch_available: **{torch_ok}**", f"- source_config: `{base_cfg_path}`", ""]
    lines.append("## Outputs")
    lines.append(f"- Surrogate pairwise: `{surrogate_dir}/ablation_pairwise.csv`")
    if torch_ok:
        lines.append(f"- Torch pairwise: `{torch_dir}/ablation_pairwise.csv`")
        lines.append(f"- Surrogate figure: `{surrogate_dir}/paper_ablation.svg`")
        lines.append(f"- Torch figure: `{torch_dir}/paper_ablation.svg`")
    else:
        lines.append("- Torch run skipped (PyTorch unavailable in current environment).")
    lines.append(f"- Comparison table: `{summary_csv}`")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(summary_csv)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/topic1/pilot.yaml")
    ap.add_argument("--output-dir", default="outputs/topic1/backend_compare")
    args = ap.parse_args()
    compare(args.config, args.output_dir)
