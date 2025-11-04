# api/schemas.py
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    dataset_size: int
