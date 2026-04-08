from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


Urgency = Literal["alta", "media", "baja"]


class RawNewsItem(BaseModel):
    title: str = Field(..., min_length=10)
    source: str = Field(..., min_length=2)
    published_at: date
    url: HttpUrl
    summary: str = Field(..., min_length=20)


class ScoredNewsItem(BaseModel):
    title: str
    source: str
    published_at: date
    url: HttpUrl
    executive_summary: str
    why_it_matters: str
    expected_impact_on_banking: str
    urgency: Urgency
    relevance_score: int = Field(..., ge=0, le=100)


class DailyBriefing(BaseModel):
    generated_for: date
    generated_at: str
    top_5_news: list[ScoredNewsItem]
    all_ranked_news: list[ScoredNewsItem]
    executive_summary_200w: str = Field(..., max_length=1500)
    watch_topics: list[str] = Field(..., min_length=3, max_length=3)
