# Diagrama Arquitetural (conceitual)

| books.toscrape.com |
|--------------------|
| 🌐 Fonte de dados  |
        │
        ▼
| Web Scraper (Python) |
| → Gera CSV em /data |
        │
        ▼
| FastAPI Backend |
| → Rotas REST públicas (/api/v1/...) |
        │
        ▼
| Render (Deploy) |
| → Disponibiliza API pública |
        │
        ▼
| Usuários / Apps / ML |
| → Consumo dos dados para dashboards e modelos |
