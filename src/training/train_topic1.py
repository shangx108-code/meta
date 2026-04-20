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
from src.training.losses import efficiency_regularization


def _build_perturb(cfg):
    return {
        "lateral_shift_px": cfg.get("lateral_shift_px", 0.0),
        "axial_shift_scale": cfg.get("axial_shift_scale", 0.0),
        "phase_quantization_bits": cfg.get("phase_quantization_bits", 0),
        "phase_error_std": cfg.get("phase_error_std", 0.0),
        "loss_error_std": cfg.get("loss_error_std", 0.0),
    }


def _forward_sample(model, wavelengths, sample, perturb, coherence_mix, noise_sigma):
    ints = [model.forward_wavelength(sample, wl, perturb) for wl in wavelengths]
    mixed = mix_coherent_partially_coherent(ints, coherence_mix)
    return detector_noise(mixed, noise_sigma)


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
        train_loss = 0.0
        perturb = _build_perturb(cfg)
        for sample, label in zip(xtr, ytr):
            intensity = _forward_sample(model, wavelengths, sample, perturb, cfg.get("coherence_mix", 1.0), cfg.get("noise_sigma", 0.0))
            cls_loss = head.train_step(intensity, label, lr=cfg.get("lr", 0.01))
            eff_loss = cfg.get("efficiency_weight", 0.05) * efficiency_regularization(optical_efficiency(intensity))
            train_loss += cls_loss + eff_loss

            # Robust mode: extra perturbation-aware update improves mismatched settings.
            if cfg.get("robust_training", False):
                perturb_aug = dict(perturb)
                perturb_aug["lateral_shift_px"] = perturb_aug.get("lateral_shift_px", 0.0) + 1.0
                perturb_aug["phase_error_std"] = perturb_aug.get("phase_error_std", 0.0) + 0.05
                perturb_aug["loss_error_std"] = perturb_aug.get("loss_error_std", 0.0) + 0.03
                intensity_aug = _forward_sample(model, wavelengths, sample, perturb_aug, max(0.4, cfg.get("coherence_mix", 1.0) - 0.2), cfg.get("noise_sigma", 0.0) * 1.2)
                train_loss += cfg.get("robust_weight", 0.1) * head.train_step(intensity_aug, label, lr=cfg.get("lr", 0.01))

        logits_list = []
        for sample in xva:
            val_int = _forward_sample(model, wavelengths, sample, perturb, cfg.get("coherence_mix", 1.0), cfg.get("noise_sigma", 0.0))
            logits_list.append(head.forward(val_int))
        acc = accuracy(logits_list, yva)
        row = {
            "epoch": epoch,
            "train_loss": round(train_loss / max(1, len(xtr)), 6),
            "val_loss": round(1 - acc, 6),
            "val_acc": round(acc, 6),
        }
        rows.append(row)

    metrics_csv = f"{outdir}/metrics.csv"
    with open(metrics_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["epoch", "train_loss", "val_loss", "val_acc"])
        w.writeheader(); w.writerows(rows)
    with open(f"{outdir}/checkpoints/final.pt", "w", encoding="utf-8") as f:
        json.dump({"cfg": cfg, "head": {"weights": head.weights, "bias": head.bias}}, f)
    return metrics_csv


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    print(run_topic1(args.config))
