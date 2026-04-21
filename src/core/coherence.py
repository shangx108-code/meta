def mix_coherent_partially_coherent(intensities, coherence_mix):
    # intensities: list of 2D lists
    h, w = len(intensities[0]), len(intensities[0][0])
    out = [[0.0 for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            vals = [im[y][x] for im in intensities]
            incoh = sum(vals) / len(vals)
            coh = (sum(v ** 0.5 for v in vals) / len(vals)) ** 2
            out[y][x] = coherence_mix * coh + (1 - coherence_mix) * incoh
    return out
