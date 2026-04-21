import random

from src.data.synthetic_optics import make_mode_mapping_dataset


def _pattern_image(label, image_size):
    img = [[0.02 * random.random() for _ in range(image_size)] for _ in range(image_size)]
    half = image_size // 2
    # Map label to region + orientation pattern to make learnable but nontrivial.
    region = label % 4
    orient = (label // 4) % 3
    y0 = 0 if region in (0, 1) else half
    y1 = half if region in (0, 1) else image_size
    x0 = 0 if region in (0, 2) else half
    x1 = half if region in (0, 2) else image_size
    for y in range(y0, y1):
        for x in range(x0, x1):
            img[y][x] += 0.35
    for y in range(image_size):
        for x in range(image_size):
            if orient == 0 and (x % 4 == 0):
                img[y][x] += 0.25
            elif orient == 1 and (y % 4 == 0):
                img[y][x] += 0.25
            elif orient == 2 and ((x + y) % 5 == 0):
                img[y][x] += 0.25
            img[y][x] = min(1.0, img[y][x])
    return img


def _pseudo_fashion(n, image_size=32):
    xs, ys = [], []
    for i in range(n):
        label = i % 10
        xs.append(_pattern_image(label, image_size))
        ys.append(label)
    return xs, ys


def load_fashion_mnist_subset(train_samples, val_samples, image_size=32):
    return _pseudo_fashion(train_samples, image_size), _pseudo_fashion(val_samples, image_size)


def load_synthetic_optics(train_samples, val_samples, image_size=32):
    return make_mode_mapping_dataset(train_samples, image_size), make_mode_mapping_dataset(val_samples, image_size)
