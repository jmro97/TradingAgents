# MVP: Agente diario de noticias económicas con foco en banca

## 1) Arquitectura del proyecto
Arquitectura modular en 4 capas:

1. **Ingesta (`news_fetcher.py`)**
   - Usa OpenAI Responses API + `web_search` para recuperar noticias del día.
2. **Procesamiento (`processor.py`)**
   - Deduplicación de noticias.
   - Scoring heurístico 0-100 orientado a impacto bancario.
   - Priorización y urgencia (alta/media/baja).
3. **Síntesis (`briefing.py`)**
   - Genera resumen ejecutivo diario (máx. 200 palabras) y 3 temas clave.
4. **Orquestación (`runner.py`, `cli.py`)**
   - Ejecuta pipeline diaria por CLI.
   - Exporta salida en JSON + Markdown.

## 2) Plan de implementación
1. Configuración por `.env`.
2. Definir esquemas Pydantic (`RawNewsItem`, `ScoredNewsItem`, `DailyBriefing`).
3. Implementar búsqueda diaria con Responses API y `web_search`.
4. Implementar filtrado de ruido y deduplicación.
5. Implementar scoring y priorización.
6. Generar briefing diario para comité ejecutivo.
7. Persistir JSON/Markdown.
8. Añadir tests mínimos con `pytest`.

## 3) Estructura de carpetas

```text
banking_news_agent/
├── __init__.py
├── briefing.py
├── cli.py
├── config.py
├── models.py
├── news_fetcher.py
├── processor.py
├── prompts.py
├── runner.py
├── utils.py
└── README.md

outputs/examples/
├── briefing_example.json
└── briefing_example.md

tests/banking_news_agent/
├── test_processor.py
└── test_runner_markdown.py
```

## 4) Prompt interno del agente
Ver `prompts.py`:
- `NEWS_FETCH_SYSTEM_PROMPT`
- `NEWS_FETCH_USER_TEMPLATE`
- `BRIEFING_SYNTHESIS_PROMPT`

Diseñado para:
- priorizar banca/regulación/tipos/riesgo/liquidez,
- penalizar ruido/opinión,
- forzar salida JSON estructurada.

## 5) Esquema de salida
### Por noticia
- `title`
- `source`
- `published_at`
- `url`
- `executive_summary`
- `why_it_matters`
- `expected_impact_on_banking`
- `urgency` (`alta|media|baja`)
- `relevance_score` (`0-100`)

### Salida final diaria
- `top_5_news`
- `all_ranked_news`
- `executive_summary_200w`
- `watch_topics` (3 elementos)

## 6) Uso por CLI

```bash
python -m banking_news_agent.cli --date 2026-04-08 --output-dir outputs
```

## 7) Variables `.env`
Usa `.env.example` como plantilla.

Variables clave:
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `NEWS_SEARCH_REGION`
- `MAX_CANDIDATE_NEWS`
- `MAX_FINAL_NEWS`

## 8) Ejemplo de salida
Hay ejemplos listos en `outputs/examples/`.

## 9) Tests mínimos

```bash
pytest tests/banking_news_agent -q
```
