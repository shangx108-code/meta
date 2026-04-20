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
            for y in range(self.image_size):
                for x in range(self.image_size):
                    phase = layer[y][x] + random.gauss(0, perturb.get("phase_error_std", 0.0))
                    if qbits > 0:
                        levels = 2**qbits
                        phase = round((phase % (2 * math.pi)) / (2 * math.pi) * (levels - 1)) / (levels - 1) * (2 * math.pi)
                    field[y][x] *= 0.5 + 0.5 * math.cos(phase)
            if shifted:
                field = field[-shifted:] + field[:-shifted]
            z = self.propagation_distance * (1 + perturb.get("axial_shift_scale", 0.0))
            field = angular_spectrum_propagate(field, wavelength_m, z, self.pixel_size)
        intensity = [[v * v for v in row] for row in field]
        return apply_absorption(intensity, perturb.get("loss_error_std", 0.0))


class DetectorHead:
    def __init__(self, image_size, num_classes):
        self.image_size = image_size
        self.num_classes = num_classes

    def forward(self, intensity):
        s = sum(sum(r) for r in intensity) / (self.image_size * self.image_size)
        return [s * (k + 1) * 0.1 for k in range(self.num_classes)]
