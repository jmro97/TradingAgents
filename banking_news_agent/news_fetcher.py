from __future__ import annotations

import logging
from datetime import date

from openai import OpenAI

from .config import Settings
from .models import RawNewsItem
from .prompts import NEWS_FETCH_SYSTEM_PROMPT, NEWS_FETCH_USER_TEMPLATE
from .utils import extract_json

logger = logging.getLogger(__name__)


class NewsFetcher:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def fetch(self, target_date: date, max_candidates: int | None = None) -> list[RawNewsItem]:
        limit = max_candidates or self.settings.max_candidates
        user_prompt = NEWS_FETCH_USER_TEMPLATE.format(
            target_date=target_date.isoformat(),
            max_candidates=limit,
        )
        logger.info("Buscando noticias para %s (máximo=%s)", target_date, limit)

        response = self.client.responses.create(
            model=self.settings.openai_model,
            tools=[{"type": "web_search"}],
            input=[
                {"role": "system", "content": NEWS_FETCH_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        payload = extract_json(response.output_text)
        items = payload.get("news", [])
        validated: list[RawNewsItem] = []
        for item in items:
            try:
                validated.append(RawNewsItem.model_validate(item))
            except Exception as exc:  # noqa: BLE001
                logger.warning("Noticia descartada por validación: %s", exc)

        logger.info("Noticias válidas recuperadas: %s", len(validated))
        return validated
