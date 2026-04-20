class MultiplexedMultiTaskModel:
    def __init__(self, in_dim, num_classes, wavelengths):
        self.in_dim = in_dim
        self.num_classes = num_classes
        self.wavelengths = wavelengths

    def forward(self, sample):
        h = len(sample)
        w = len(sample[0])
        m = sum(sum(r) for r in sample) / max(1, h * w)
        top = sum(sum(r) for r in sample[: h // 2]) / max(1, (h // 2) * w)
        bot = sum(sum(r) for r in sample[h // 2 :]) / max(1, (h - h // 2) * w)
        contrast = top - bot
        cls = [m * (i + 1) + 0.1 * contrast * (i % 2 * 2 - 1) for i in range(self.num_classes)]
        raw = 1.2 * abs(contrast) - 0.15 + 0.1 * m
        anom_score = min(1.0, max(0.0, raw))
        anom = [1 - anom_score, anom_score]
        feat = [m, top, bot, contrast]
        return {"cls": cls, "anom": anom, "feat": feat}

    @staticmethod
    def crosstalk_penalty(feat):
        mean = sum(feat) / len(feat)
        return sum(abs(v - mean) for v in feat) / len(feat)
