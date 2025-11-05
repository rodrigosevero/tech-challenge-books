# 📚 Books API — Tech Challenge Fase 1

API pública para consulta de livros, construída com **FastAPI**, **Python** e **Render**, integrando um pipeline completo de dados extraídos do site [Books to Scrape](https://books.toscrape.com/).

---

## 🎯 Problema que Resolve
A aplicação foi desenvolvida para atender à necessidade de **disponibilizar dados estruturados de livros** de forma aberta e escalável, permitindo que cientistas de dados e aplicações web possam:

- Criar sistemas de recomendação de livros.
- Analisar preços e tendências de categorias literárias.
- Treinar modelos de machine learning com dados limpos e padronizados.

> Em resumo: transforma dados não estruturados (HTML) em uma **API RESTful pública**, pronta para ser consumida em experimentos, dashboards e modelos de IA.

---

## ⚙️ Stack Utilizada
- **Linguagem:** Python 3.11
- **Framework:** FastAPI + Uvicorn
- **Bibliotecas:**
  - `httpx` e `beautifulsoup4` — scraping e parsing de HTML
  - `pandas` — manipulação de dados e geração do CSV
  - `pydantic` — validação e tipagem de dados na API
  - `pytest` — testes automatizados
- **Infraestrutura:** Render (deploy público)
- **Versionamento:** Git + GitHub
- **Documentação automática:** Swagger (/docs)

---

## 🧱 Arquitetura (Macro)

```text
books.toscrape.com
       │
       ▼
Web Scraper (Python)
 → Gera CSV em /data
       │
       ▼
FastAPI Backend (Rotas REST)
       │
       ▼
Render (Deploy)
 → API pública acessível
       │
       ▼
Usuários / Dashboards / ML
 → Consumo e análise dos dados
```

📎 Diagrama completo: [diagrama_arquitetural_conceitual.md](./diagrama_arquitetural_conceitual.md)

---

## 💻 Como Rodar Localmente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/rodrigosevero/tech-challenge-books
cd tech-challenge-books
```

### 2️⃣ Criar ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Gerar o dataset CSV (opcional)
```bash
python scripts/scrape_books.py
```

### 5️⃣ Rodar o servidor local
```bash
uvicorn api.main:app --reload
```

📍 Acesse em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🌍 Deploy em Produção
A API está disponível publicamente no Render:

🔗 **Link público:** https://tech-challenge-books-pikw.onrender.com
🩺 **Health check:** https://tech-challenge-books-pikw.onrender.com/api/v1/health

---

## 📹 Demonstração em Vídeo
🎥 [Assista à apresentação no YouTube](https://www.youtube.com/watch?v=YaP3vbroCmc)

O vídeo mostra:
- Pipeline de scraping e geração do CSV.
- Estrutura e rotas da API.
- Testes de endpoints em ambiente de produção.

---

## 📄 Entregáveis Oficiais
- ✅ API pública funcional (Render)
- ✅ Repositório GitHub organizado
- ✅ Diagrama de arquitetura
- ✅ Documentação Swagger (/docs)
- ✅ README completo (este arquivo)

---

**Autor:** Rodrigo Severo Ribeiro — *MestreDev 🧠*  
**Data:** Novembro/2025
