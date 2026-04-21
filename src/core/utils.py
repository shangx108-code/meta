import json
import os
import random
from pathlib import Path
from typing import Any, Dict


def set_seed(seed: int) -> None:
    random.seed(seed)


def load_yaml(path: str) -> Dict[str, Any]:
    # Lightweight YAML subset via JSON-compatible files.
    txt = Path(path).read_text(encoding="utf-8")
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        data = {}
        for line in txt.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            k, v = line.split(":", 1)
            data[k.strip()] = _parse_scalar(v.strip())
        return data


def _parse_scalar(v: str):
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(x.strip()) for x in inner.split(",")]
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


def dump_json(path: str, data: Dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
