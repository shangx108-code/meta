def classification_loss(logits, y):
    target = y if isinstance(y, int) else int(y)
    margin = max(logits) - logits[target]
    return max(0.0, margin)


def efficiency_regularization(efficiency):
    return 1.0 - efficiency


def robustness_regularization(logits_nom, logits_perturbed):
    return sum((a - b) ** 2 for a, b in zip(logits_nom, logits_perturbed)) / len(logits_nom)
