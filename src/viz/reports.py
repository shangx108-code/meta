from pathlib import Path


def write_markdown_report(path, title, metrics, notes=""):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    for k, v in metrics.items():
        lines.append(f"- **{k}**: {v}")
    if notes:
        lines += ["", "## Notes", notes]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
