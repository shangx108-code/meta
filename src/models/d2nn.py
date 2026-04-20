import math
import random

from src.core.noise import apply_absorption
from src.core.propagation import angular_spectrum_propagate


class D2NN:
    def __init__(self, image_size, num_layers, propagation_distance, pixel_size):
        self.image_size = image_size
        self.num_layers = num_layers
        self.propagation_distance = propagation_distance
        self.pixel_size = pixel_size
        self.phases = [
            [[random.uniform(0, 2 * math.pi) for _ in range(image_size)] for _ in range(image_size)]
            for _ in range(num_layers)
        ]

    def forward_wavelength(self, amp, wavelength_m, perturb):
        field = [row[:] for row in amp]
        for layer in self.phases:
            qbits = int(perturb.get("phase_quantization_bits", 0))
            shifted = int(perturb.get("lateral_shift_px", 0.0))
            phase_err = perturb.get("phase_error_std", 0.0)
            for y in range(self.image_size):
                for x in range(self.image_size):
                    phase = layer[y][x] + random.gauss(0, phase_err)
                    if qbits > 0:
                        levels = max(2, 2**qbits)
                        phase = round((phase % (2 * math.pi)) / (2 * math.pi) * (levels - 1)) / (levels - 1) * (2 * math.pi)
                    # Include wavelength dependence in phase response.
                    phase_scale = 0.7 + 0.3 * math.cos(2 * math.pi * wavelength_m / 600e-9)
                    field[y][x] *= max(0.0, 0.45 + 0.55 * math.cos(phase * phase_scale))
            if shifted:
                field = field[-shifted:] + field[:-shifted]
                for row in field:
                    row[:] = row[-shifted:] + row[:-shifted]
            z = self.propagation_distance * (1 + perturb.get("axial_shift_scale", 0.0))
            field = angular_spectrum_propagate(field, wavelength_m, z, self.pixel_size)
        intensity = [[v * v for v in row] for row in field]
        return apply_absorption(intensity, perturb.get("loss_error_std", 0.0))


class DetectorHead:
    """Simple trainable linear readout over physically motivated intensity features."""

    def __init__(self, image_size, num_classes):
        self.image_size = image_size
        self.num_classes = num_classes
        self.feature_dim = 8
        self.weights = [[random.uniform(-0.02, 0.02) for _ in range(self.feature_dim)] for _ in range(num_classes)]
        self.bias = [0.0 for _ in range(num_classes)]

    def extract_features(self, intensity):
        h = len(intensity)
        w = len(intensity[0])
        midy, midx = h // 2, w // 2
        q1 = sum(sum(r[:midx]) for r in intensity[:midy])
        q2 = sum(sum(r[midx:]) for r in intensity[:midy])
        q3 = sum(sum(r[:midx]) for r in intensity[midy:])
        q4 = sum(sum(r[midx:]) for r in intensity[midy:])
        total = q1 + q2 + q3 + q4 + 1e-8
        mean = total / (h * w)
        var = sum((v - mean) ** 2 for row in intensity for v in row) / (h * w)
        # Horizontal/vertical imbalance and concentration proxy.
        h_diff = (q1 + q3 - q2 - q4) / total
        v_diff = (q1 + q2 - q3 - q4) / total
        center = sum(sum(intensity[y][w // 4 : 3 * w // 4]) for y in range(h // 4, 3 * h // 4)) / total
        return [q1 / total, q2 / total, q3 / total, q4 / total, mean, var, h_diff + 0.5, v_diff + center]

    def forward(self, intensity):
        f = self.extract_features(intensity)
        return [sum(w * x for w, x in zip(row, f)) + b for row, b in zip(self.weights, self.bias)]

    def train_step(self, intensity, label, lr):
        f = self.extract_features(intensity)
        logits = self.forward(intensity)
        exps = [math.exp(max(-40.0, min(40.0, z))) for z in logits]
        zsum = sum(exps) + 1e-12
        probs = [z / zsum for z in exps]
        for c in range(self.num_classes):
            err = probs[c] - (1.0 if c == label else 0.0)
            for j in range(self.feature_dim):
                self.weights[c][j] -= lr * err * f[j]
            self.bias[c] -= lr * err
        return -math.log(max(1e-12, probs[label]))
