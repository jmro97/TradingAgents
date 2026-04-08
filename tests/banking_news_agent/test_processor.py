from datetime import date

from banking_news_agent.models import RawNewsItem
from banking_news_agent.processor import deduplicate_news, score_news


def test_deduplicate_news_removes_same_title_same_domain():
    items = [
        RawNewsItem(
            title="Fed keeps rates high amid inflation concerns",
            source="Reuters",
            published_at=date(2026, 4, 8),
            url="https://www.reuters.com/a",
            summary="Decision with implications for banking margins and credit risk.",
        ),
        RawNewsItem(
            title="Fed keeps rates high amid inflation concerns",
            source="Reuters",
            published_at=date(2026, 4, 8),
            url="https://www.reuters.com/b",
            summary="Same story duplicated.",
        ),
    ]

    deduped = deduplicate_news(items)
    assert len(deduped) == 1


def test_score_news_rewards_banking_relevance():
    item = RawNewsItem(
        title="ECB supervisor tightens capital requirement for euro banks",
        source="Bloomberg",
        published_at=date(2026, 4, 8),
        url="https://www.bloomberg.com/news/articles/test",
        summary="The move affects liquidity, risk-weighted assets and lending appetite.",
    )

    score = score_news(item, target_date=date(2026, 4, 8))
    assert score >= 80
