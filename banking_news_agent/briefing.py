from __future__ import annotations

import json
import logging

from openai import OpenAI

from .config import Settings
from .models import DailyBriefing, ScoredNewsItem
from .prompts import BRIEFING_SYNTHESIS_PROMPT
from .utils import extract_json, utc_now_iso

logger = logging.getLogger(__name__)


class BriefingSynthesizer:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def synthesize(self, generated_for, ranked_news: list[ScoredNewsItem]) -> DailyBriefing:
        top_5 = ranked_news[:5]
        input_payload = [item.model_dump(mode="json") for item in top_5]

        response = self.client.responses.create(
            model=self.settings.openai_model,
            input=[
                {"role": "system", "content": BRIEFING_SYNTHESIS_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Genera síntesis para comité bancario con base en estas noticias:\n"
                        f"{json.dumps(input_payload, ensure_ascii=False, indent=2)}"
                    ),
                },
            ],
        )

        synthesis = extract_json(response.output_text)
        watch_topics = synthesis.get("watch_topics", [])[:3]
        if len(watch_topics) < 3:
            watch_topics += [
                "Evolución de tipos e impacto en margen financiero",
                "Cambios regulatorios y requerimientos de capital",
                "Calidad de crédito y coste de riesgo",
            ][: 3 - len(watch_topics)]

        return DailyBriefing(
            generated_for=generated_for,
            generated_at=utc_now_iso(),
            top_5_news=top_5,
            all_ranked_news=ranked_news,
            executive_summary_200w=synthesis.get("executive_summary_200w", ""),
            watch_topics=watch_topics,
        )
