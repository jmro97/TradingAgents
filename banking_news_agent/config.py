from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"
    search_region: str = "US"
    max_candidates: int = 40
    max_final_news: int = 12



def load_settings() -> Settings:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY no está definido en el entorno.")

    return Settings(
        openai_api_key=api_key,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        search_region=os.getenv("NEWS_SEARCH_REGION", "US"),
        max_candidates=int(os.getenv("MAX_CANDIDATE_NEWS", "40")),
        max_final_news=int(os.getenv("MAX_FINAL_NEWS", "12")),
    )
