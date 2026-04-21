import random


def make_mode_mapping_dataset(n, size=32, num_classes=4):
    xs, ys = [], []
    centers = [(8, 8), (24, 8), (8, 24), (24, 24)]
    for i in range(n):
        c = i % num_classes
        cx, cy = centers[c]
        img = []
        for y in range(size):
            row = []
            for x in range(size):
                d2 = (x - cx) ** 2 + (y - cy) ** 2
                row.append(max(0.0, 1.0 - d2 / 200.0 + random.uniform(-0.02, 0.02)))
            img.append(row)
        xs.append(img)
        ys.append(c)
    return xs, ys
