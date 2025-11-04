# api/routers/categories.py
from typing import List
from fastapi import APIRouter, Depends
from api.schemas import CategoriesResponse
from api.deps import get_dataset

router = APIRouter(prefix="/api/v1", tags=["categories"])

@router.get("/categories", response_model=CategoriesResponse)
def list_categories(dataset = Depends(get_dataset)):
    cats = sorted({row["category"] for row in dataset})
    return {"items": cats, "total": len(cats)}
