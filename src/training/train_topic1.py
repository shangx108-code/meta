import argparse
import csv
import json

from src.core.coherence import mix_coherent_partially_coherent
from src.core.metrics import accuracy, optical_efficiency
from src.core.noise import detector_noise
from src.core.utils import ensure_dir, load_yaml, set_seed
from src.core.wavelengths import nm_to_m
from src.data.datasets import load_fashion_mnist_subset, load_synthetic_optics
from src.models.d2nn import D2NN, DetectorHead
from src.training.losses import classification_loss, efficiency_regularization, robustness_regularization


def run_topic1(config_path):
    cfg = load_yaml(config_path)
    set_seed(int(cfg.get("seed", 1)))
    outdir = cfg["output_dir"]
    ensure_dir(outdir)
    ensure_dir(f"{outdir}/checkpoints")

    (xtr_f, ytr_f), (xva, yva) = load_fashion_mnist_subset(cfg["train_samples"], cfg["val_samples"], cfg["image_size"])
    (xtr_s, ytr_s), _ = load_synthetic_optics(cfg["train_samples"], max(16, cfg["val_samples"] // 2), cfg["image_size"])
    xtr, ytr = xtr_f + xtr_s, ytr_f + [y % 10 for y in ytr_s]

    model = D2NN(cfg["image_size"], cfg["num_layers"], cfg["propagation_distance"], cfg["pixel_size"])
    head = DetectorHead(cfg["image_size"], 10)
    wavelengths = nm_to_m(cfg["wavelengths_nm"])

    rows = []
    for epoch in range(cfg["epochs"]):
        for i in range(len(xtr)):
            perturb = {
                "lateral_shift_px": cfg.get("lateral_shift_px", 0.0),
                "axial_shift_scale": cfg.get("axial_shift_scale", 0.0),
                "phase_quantization_bits": cfg.get("phase_quantization_bits", 0),
                "phase_error_std": cfg.get("phase_error_std", 0.0),
                "loss_error_std": cfg.get("loss_error_std", 0.0),
            }
            ints = [model.forward_wavelength(xtr[i], wl, perturb) for wl in wavelengths]
            mixed = mix_coherent_partially_coherent(ints, cfg.get("coherence_mix", 1.0))
            noisy = detector_noise(mixed, cfg.get("noise_sigma", 0.0))
            logits = head.forward(noisy)
            _ = classification_loss(logits, ytr[i]) + cfg.get("efficiency_weight", 0.05) * efficiency_regularization(optical_efficiency(noisy))
            if cfg.get("robust_training", False):
                p2 = dict(perturb)
                p2["lateral_shift_px"] = perturb.get("lateral_shift_px", 0.0) + 1
                logits2 = head.forward(detector_noise(mix_coherent_partially_coherent([model.forward_wavelength(xtr[i], wl, p2) for wl in wavelengths], cfg.get("coherence_mix", 1.0)), cfg.get("noise_sigma", 0.0)))
                _ += cfg.get("robust_weight", 0.1) * robustness_regularization(logits, logits2)

        logits_list = []
        for sample in xva:
            ints = [model.forward_wavelength(sample, wl, {"phase_quantization_bits": cfg.get("phase_quantization_bits", 0)}) for wl in wavelengths]
            mixed = mix_coherent_partially_coherent(ints, cfg.get("coherence_mix", 1.0))
            logits_list.append(head.forward(mixed))
        acc = accuracy(logits_list, yva)
        rows.append({"epoch": epoch, "val_loss": round(1 - acc, 6), "val_acc": round(acc, 6)})

    metrics_csv = f"{outdir}/metrics.csv"
    with open(metrics_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["epoch", "val_loss", "val_acc"])
        w.writeheader(); w.writerows(rows)
    with open(f"{outdir}/checkpoints/final.pt", "w", encoding="utf-8") as f:
        json.dump({"cfg": cfg, "note": "lightweight checkpoint"}, f)
    return metrics_csv


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    print(run_topic1(args.config))
