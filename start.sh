#!/bin/bash
set -e

echo "🔍 Verificando dataset em data/books.csv..."
if [ ! -f "data/books.csv" ]; then
  echo "📚 CSV ausente — gerando via scripts/scrape_books.py"
  python scripts/scrape_books.py
else
  echo "✅ CSV encontrado — seguindo"
fi

echo "🚀 Subindo API..."
exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2
