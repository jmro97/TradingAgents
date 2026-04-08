from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("{"):
        return json.loads(text)

    match = _JSON_BLOCK.search(text)
    if not match:
        raise ValueError("No se encontró JSON en la respuesta del modelo.")
    return json.loads(match.group(0))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
