from src.training.losses import classification_loss


def multitask_loss(logits_cls, y_cls, logits_anom, y_anom, crosstalk, weight=0.1):
    return classification_loss(logits_cls, y_cls) + classification_loss(logits_anom, y_anom) + weight * crosstalk
