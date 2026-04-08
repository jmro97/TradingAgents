from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlparse

from .models import RawNewsItem, ScoredNewsItem

BANKING_KEYWORDS = {
    "capital", "liquidity", "credit", "loan", "deposit", "bank", "banking", "fintech",
    "payment", "basel", "supervision", "ecb", "fed", "interest rate", "inflation",
    "risk", "npl", "compliance", "regulation", "stress test", "margin",
}

HIGH_PRIORITY_HINTS = {
    "central bank", "fed", "ecb", "boe", "supervisor", "regulator", "capital requirement",
    "interest rate", "inflation", "liquidity", "bank failure", "stress test", "basel",
}

NOISE_HINTS = {"opinion", "editorial", "rumor", "gossip", "exclusive:"}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def deduplicate_news(items: list[RawNewsItem]) -> list[RawNewsItem]:
    seen: set[tuple[str, str]] = set()
    deduped: list[RawNewsItem] = []

    for item in items:
        title_key = _normalize(item.title)
        domain = urlparse(str(item.url)).netloc.replace("www.", "")
        key = (title_key, domain)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    return deduped


def score_news(item: RawNewsItem, target_date: date) -> int:
    text = f"{item.title} {item.summary}".lower()
    score = 35

    keyword_hits = sum(1 for kw in BANKING_KEYWORDS if kw in text)
    score += min(keyword_hits * 7, 35)

    high_hits = sum(1 for kw in HIGH_PRIORITY_HINTS if kw in text)
    score += min(high_hits * 8, 24)

    if any(noise in text for noise in NOISE_HINTS):
        score -= 20

    days_old = max((target_date - item.published_at).days, 0)
    score -= min(days_old * 4, 20)

    return max(0, min(score, 100))


def urgency_from_score(score: int) -> str:
    if score >= 78:
        return "alta"
    if score >= 55:
        return "media"
    return "baja"


def build_scored_items(items: list[RawNewsItem], target_date: date) -> list[ScoredNewsItem]:
    ranked: list[ScoredNewsItem] = []

    for item in items:
        score = score_news(item, target_date)
        ranked.append(
            ScoredNewsItem(
                title=item.title,
                source=item.source,
                published_at=item.published_at,
                url=item.url,
                executive_summary=item.summary,
                why_it_matters=(
                    "Afecta variables clave del negocio bancario (margen, riesgo, volumen de crédito o costes regulatorios)."
                ),
                expected_impact_on_banking=(
                    "Se espera impacto en pricing, apetito de riesgo y/o asignación de capital en entidades financieras."
                ),
                urgency=urgency_from_score(score),
                relevance_score=score,
            )
        )

    ranked.sort(key=lambda x: x.relevance_score, reverse=True)
    return ranked
