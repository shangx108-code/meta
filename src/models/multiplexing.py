class MultiplexedMultiTaskModel:
    def __init__(self, in_dim, num_classes, wavelengths):
        self.in_dim = in_dim
        self.num_classes = num_classes
        self.wavelengths = wavelengths

    def forward(self, sample):
        m = sum(sum(r) for r in sample) / max(1, len(sample) * len(sample[0]))
        cls = [m * (i + 1) for i in range(self.num_classes)]
        anom = [1 - m, m]
        feat = [m, m * 0.5, m * 1.5, m * 0.8]
        return {"cls": cls, "anom": anom, "feat": feat}

    @staticmethod
    def crosstalk_penalty(feat):
        mean = sum(feat) / len(feat)
        return sum(abs(v - mean) for v in feat) / len(feat)
