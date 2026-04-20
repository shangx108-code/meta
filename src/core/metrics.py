def accuracy(logits, y):
    correct = 0
    for i, row in enumerate(logits):
        pred = max(range(len(row)), key=lambda k: row[k])
        if pred == y[i]:
            correct += 1
    return correct / max(1, len(y))


def optical_efficiency(intensity):
    h, w = len(intensity), len(intensity[0])
    y0, y1 = h // 4, 3 * h // 4
    x0, x1 = w // 4, 3 * w // 4
    total = sum(sum(r) for r in intensity) + 1e-8
    center = sum(sum(intensity[y][x0:x1]) for y in range(y0, y1))
    return center / total
