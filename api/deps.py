# api/deps.py
from functools import lru_cache
from typing import List, Dict
import pandas as pd
from api.config import get_settings

REQUIRED_COLS = [
    "id","title","price","rating","availability","category","image_url","product_url"
]

@lru_cache
def _load_dataset() -> List[Dict]:
    settings = get_settings()
    df = pd.read_csv(settings.DATASET_PATH)
    # Tipos e limpeza mínimos
    df = df[REQUIRED_COLS].copy()
    df["id"] = df["id"].astype(int)
    df["title"] = df["title"].astype(str)
    df["price"] = df["price"].astype(float)
    df["rating"] = df["rating"].astype(int)
    df["availability"] = df["availability"].astype(str)
    df["category"] = df["category"].astype(str)
    df["image_url"] = df["image_url"].astype(str)
    df["product_url"] = df["product_url"].astype(str)
    # ordena por id
    df = df.sort_values("id").reset_index(drop=True)
    return df.to_dict(orient="records")

def get_dataset() -> List[Dict]:
    """Injetado nas rotas via Depends."""
    return _load_dataset()
