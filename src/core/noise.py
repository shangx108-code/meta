import random


def detector_noise(x, sigma=0.01):
    if sigma <= 0:
        return x
    out = []
    for row in x:
        out.append([max(0.0, v + random.gauss(0.0, sigma)) for v in row])
    return out


def apply_absorption(x, loss_error_std=0.0):
    if loss_error_std <= 0:
        return x
    factor = max(0.0, 1.0 - abs(random.gauss(0.0, loss_error_std)))
    return [[v * factor for v in row] for row in x]
