from datetime import date

from banking_news_agent.models import DailyBriefing, ScoredNewsItem
from banking_news_agent.runner import render_markdown


def test_render_markdown_contains_sections():
    briefing = DailyBriefing(
        generated_for=date(2026, 4, 8),
        generated_at="2026-04-08T12:00:00+00:00",
        top_5_news=[
            ScoredNewsItem(
                title="Fed keeps rates unchanged",
                source="WSJ",
                published_at=date(2026, 4, 8),
                url="https://example.com/fed",
                executive_summary="No changes in rates; cautious guidance.",
                why_it_matters="Affects funding costs and loan demand.",
                expected_impact_on_banking="Margin stable; credit growth uncertain.",
                urgency="alta",
                relevance_score=88,
            )
        ],
        all_ranked_news=[],
        executive_summary_200w="Executive summary",
        watch_topics=["Topic 1", "Topic 2", "Topic 3"],
    )

    md = render_markdown(briefing)
    assert "## Top 5 noticias" in md
    assert "Score de relevancia" in md
    assert "## 3 temas clave a vigilar" in md
