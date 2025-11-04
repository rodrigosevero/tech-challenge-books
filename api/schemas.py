# api/schemas.py
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class HealthResponse(BaseModel):
    status: str
    dataset_size: int

class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    availability: str
    category: str
    image_url: HttpUrl
    product_url: HttpUrl

class PaginatedBooks(BaseModel):
    items: List[Book]
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=200)
    total: int

class CategoriesResponse(BaseModel):
    items: List[str]
    total: int
