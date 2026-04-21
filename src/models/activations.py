from dataclasses import dataclass
import math


@dataclass
class ActivationParams:
    insertion_loss: float = 0.1
    slope: float = 1.0
    saturation_threshold: float = 0.5
    dynamic_range: float = 1.0
    smoothness: float = 1.0


def saturable_absorber(x, p):
    return (1 - p.insertion_loss) * x / (1 + (x / (p.saturation_threshold + 1e-6)) ** p.smoothness)


def microring_like(x, p):
    return (1 - p.insertion_loss) * (1 / (1 + math.exp(-p.slope * (x - p.saturation_threshold)))) * p.dynamic_range


def thermal_like(x, p):
    return (1 - p.insertion_loss) * math.tanh(p.slope * x / (p.saturation_threshold + 1e-6)) * p.dynamic_range


def oe_hybrid_like(x, p):
    z = p.slope * (x - p.saturation_threshold)
    return (1 - p.insertion_loss) * math.log(1 + math.exp(z)) / max(p.smoothness, 1e-6)


def nfom_like(acc, throughput, energy_proxy, insertion_loss):
    return (acc * throughput) / (energy_proxy * (1 + insertion_loss) + 1e-8)
