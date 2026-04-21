"""Compact scalar propagation surrogate for restricted environments."""


def angular_spectrum_propagate(field, wavelength_m, distance_m, pixel_size_m):
    # Surrogate blur-like update.
    h, w = len(field), len(field[0])
    out = [[0.0 for _ in range(w)] for _ in range(h)]
    alpha = min(0.49, max(0.01, distance_m / (wavelength_m * 1e6 + 1e-9)))
    for y in range(h):
        for x in range(w):
            c = field[y][x]
            n = field[y - 1][x] if y > 0 else c
            s = field[y + 1][x] if y < h - 1 else c
            e = field[y][x + 1] if x < w - 1 else c
            wv = field[y][x - 1] if x > 0 else c
            out[y][x] = (1 - alpha) * c + alpha * 0.25 * (n + s + e + wv)
    return out


def fresnel_propagate(field, wavelength_m, distance_m, pixel_size_m):
    return angular_spectrum_propagate(field, wavelength_m, distance_m, pixel_size_m)
