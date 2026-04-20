import random

from src.data.synthetic_optics import make_mode_mapping_dataset


def _pseudo_fashion(n, image_size=32):
    xs, ys = [], []
    for i in range(n):
        label = i % 10
        img = []
        for y in range(image_size):
            row = []
            for x in range(image_size):
                base = ((x + y + label * 3) % image_size) / image_size
                row.append(max(0.0, min(1.0, base + random.uniform(-0.05, 0.05))))
            img.append(row)
        xs.append(img)
        ys.append(label)
    return xs, ys


def load_fashion_mnist_subset(train_samples, val_samples, image_size=32):
    return _pseudo_fashion(train_samples, image_size), _pseudo_fashion(val_samples, image_size)


def load_synthetic_optics(train_samples, val_samples, image_size=32):
    return make_mode_mapping_dataset(train_samples, image_size), make_mode_mapping_dataset(val_samples, image_size)
