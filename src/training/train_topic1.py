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


def _run_topic1_surrogate(cfg):
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
        rows.append({"epoch": epoch, "train_loss": round(train_loss / max(1, len(xtr)), 6), "val_loss": round(1 - acc, 6), "val_acc": round(acc, 6)})

    metrics_csv = f"{outdir}/metrics.csv"
    with open(metrics_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["epoch", "train_loss", "val_loss", "val_acc"])
        w.writeheader(); w.writerows(rows)
    with open(f"{outdir}/checkpoints/final.pt", "w", encoding="utf-8") as f:
        json.dump({"cfg": cfg, "backend_used": "surrogate", "head": {"weights": head.weights, "bias": head.bias}}, f)
    return metrics_csv


def _run_topic1_torch(cfg):
    import torch

    outdir = cfg["output_dir"]
    ensure_dir(outdir)
    ensure_dir(f"{outdir}/checkpoints")

    (xtr_f, ytr_f), (xva, yva) = load_fashion_mnist_subset(cfg["train_samples"], cfg["val_samples"], cfg["image_size"])
    xtr = torch.tensor(xtr_f, dtype=torch.float32)
    ytr = torch.tensor(ytr_f, dtype=torch.long)
    xva = torch.tensor(xva, dtype=torch.float32)
    yva = torch.tensor(yva, dtype=torch.long)

    # Compact tensorized baseline: perturbation-aware optical-like feature extractor + linear readout.
    feature = torch.nn.Sequential(
        torch.nn.Conv2d(1, 8, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.AvgPool2d(2),
        torch.nn.Conv2d(8, 8, kernel_size=3, padding=1),
        torch.nn.ReLU(),
        torch.nn.AdaptiveAvgPool2d((4, 4)),
        torch.nn.Flatten(),
    )
    head = torch.nn.Linear(8 * 4 * 4, 10)
    opt = torch.optim.Adam(list(feature.parameters()) + list(head.parameters()), lr=cfg.get("lr", 0.01))
    loss_fn = torch.nn.CrossEntropyLoss()

    def apply_setting_perturb(x):
        # Differentiate coherence/bandwidth/misalignment effects.
        coh = float(cfg.get("coherence_mix", 1.0))
        wl_factor = 1.0 - 0.04 * max(0, len(cfg.get("wavelengths_nm", [530])) - 1)
        shift = int(cfg.get("lateral_shift_px", 0.0))
        phase_err = float(cfg.get("phase_error_std", 0.0))
        loss_err = float(cfg.get("loss_error_std", 0.0))
        x2 = x.clone() * (0.85 + 0.15 * coh) * wl_factor
        if shift:
            x2 = torch.roll(x2, shifts=(shift, -shift), dims=(-2, -1))
        if phase_err > 0:
            x2 = x2 + phase_err * 0.05 * torch.randn_like(x2)
        if loss_err > 0:
            x2 = x2 * (1.0 - min(0.5, loss_err))
        return torch.clamp(x2, 0.0, 1.0)

    rows = []
    bs = int(cfg.get("batch_size", 16))
    for epoch in range(int(cfg.get("epochs", 1))):
        perm = torch.randperm(xtr.size(0))
        xtr_e = xtr[perm]
        ytr_e = ytr[perm]
        total_loss = 0.0
        for i in range(0, xtr_e.size(0), bs):
            xb = xtr_e[i : i + bs].unsqueeze(1)
            yb = ytr_e[i : i + bs]
            xb = apply_setting_perturb(xb)
            logits = head(feature(xb))
            loss = loss_fn(logits, yb)
            if cfg.get("robust_training", False):
                xb_aug = torch.roll(xb, shifts=(1, -1), dims=(-2, -1))
                logits_aug = head(feature(xb_aug))
                loss = loss + float(cfg.get("robust_weight", 0.1)) * loss_fn(logits_aug, yb)
            opt.zero_grad(); loss.backward(); opt.step()
            total_loss += float(loss.item())

        with torch.no_grad():
            xv = apply_setting_perturb(xva.unsqueeze(1))
            val_logits = head(feature(xv))
            val_acc = float((val_logits.argmax(1) == yva).float().mean().item())
        rows.append({"epoch": epoch, "train_loss": round(total_loss / max(1, xtr.size(0) // bs), 6), "val_loss": round(1 - val_acc, 6), "val_acc": round(val_acc, 6)})

    metrics_csv = f"{outdir}/metrics.csv"
    with open(metrics_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["epoch", "train_loss", "val_loss", "val_acc"])
        w.writeheader(); w.writerows(rows)
    torch.save({"cfg": cfg, "backend_used": "torch", "feature": feature.state_dict(), "head": head.state_dict()}, f"{outdir}/checkpoints/final.pt")
    return metrics_csv


def run_topic1(config_path):
    cfg = load_yaml(config_path)
    set_seed(int(cfg.get("seed", 1)))
    backend = cfg.get("backend", "auto")
    torch_available = False
    if backend in ("auto", "torch"):
        try:
            import torch  # noqa: F401

            torch_available = True
        except Exception:
            torch_available = False

    if backend == "torch" and not torch_available:
        raise RuntimeError("backend=torch requested but PyTorch is unavailable")
    if backend == "auto" and torch_available:
        return _run_topic1_torch(cfg)
    if backend == "torch":
        return _run_topic1_torch(cfg)
    return _run_topic1_surrogate(cfg)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    print(run_topic1(args.config))
