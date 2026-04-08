from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

from .briefing import BriefingSynthesizer
from .config import load_settings
from .news_fetcher import NewsFetcher
from .processor import build_scored_items, deduplicate_news
from .utils import ensure_dir, setup_logging

logger = logging.getLogger(__name__)


def render_markdown(briefing) -> str:
    lines = [
        f"# Briefing diario banca - {briefing.generated_for.isoformat()}",
        "",
        "## Resumen ejecutivo (<=200 palabras)",
        briefing.executive_summary_200w,
        "",
        "## Top 5 noticias",
    ]

    for idx, item in enumerate(briefing.top_5_news, start=1):
        lines.extend(
            [
                f"### {idx}. {item.title}",
                f"- Fuente: {item.source}",
                f"- Fecha: {item.published_at.isoformat()}",
                f"- URL: {item.url}",
                f"- Resumen ejecutivo: {item.executive_summary}",
                f"- Por qué importa: {item.why_it_matters}",
                f"- Impacto esperado en banca: {item.expected_impact_on_banking}",
                f"- Urgencia: **{item.urgency.upper()}**",
                f"- Score de relevancia: **{item.relevance_score}/100**",
                "",
            ]
        )

    lines.append("## 3 temas clave a vigilar")
    for topic in briefing.watch_topics:
        lines.append(f"- {topic}")

    return "\n".join(lines)


def run_daily_briefing(target_date: date, output_dir: Path) -> tuple[Path, Path]:
    setup_logging()
    settings = load_settings()
    ensure_dir(output_dir)

    fetcher = NewsFetcher(settings)
    synthesizer = BriefingSynthesizer(settings)

    raw = fetcher.fetch(target_date=target_date, max_candidates=settings.max_candidates)
    deduped = deduplicate_news(raw)
    ranked = build_scored_items(deduped, target_date=target_date)[: settings.max_final_news]
    briefing = synthesizer.synthesize(generated_for=target_date, ranked_news=ranked)

    json_path = output_dir / f"briefing_{target_date.isoformat()}.json"
    md_path = output_dir / f"briefing_{target_date.isoformat()}.md"

    json_path.write_text(briefing.model_dump_json(indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(briefing), encoding="utf-8")

    logger.info("Briefing generado: %s y %s", json_path, md_path)
    return json_path, md_path
