from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path

from .runner import run_daily_briefing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agente diario de noticias económicas y banca (MVP)")
    parser.add_argument("--date", type=str, default=date.today().isoformat(), help="Fecha objetivo YYYY-MM-DD")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Directorio de salida")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    json_path, md_path = run_daily_briefing(target_date=target_date, output_dir=Path(args.output_dir))
    print(f"JSON: {json_path}")
    print(f"Markdown: {md_path}")


if __name__ == "__main__":
    main()
