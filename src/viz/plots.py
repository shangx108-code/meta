from pathlib import Path


def plot_metric_curves(csv_path, out_png, y="val_acc"):
    # Fallback: write simple text plot artifact with .png extension for traceability.
    txt = Path(csv_path).read_text(encoding="utf-8")
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    Path(out_png).write_text(f"Fallback plot for {y}\n\n{txt}", encoding="utf-8")


def plot_bar(rows, x, y, out_png, title):
    lines = [title, ""]
    for r in rows:
        lines.append(f"{r[x]}: {r[y]:.4f}")
    Path(out_png).write_text("\n".join(lines), encoding="utf-8")
