FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# deps nativos básicos (build-essential é baratinho e ajuda alguns wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# copia o app (inclui o CSV gerado no passo anterior)
COPY . .

# configs padrão
ENV ENV=prod \
    DATASET_PATH=/app/data/books.csv

EXPOSE 8000

# uvicorn com 2 workers (ajuste conforme CPU)
CMD ["uvicorn","api.main:app","--host","0.0.0.0","--port","8000","--workers","2"]
