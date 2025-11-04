# api/config.py
from pydantic import BaseModel
from functools import lru_cache
import os

class Settings(BaseModel):
    ENV: str = os.getenv("ENV", "dev")
    DATASET_PATH: str = os.getenv("DATASET_PATH", "data/books.csv")

@lru_cache
def get_settings() -> Settings:
    return Settings()
