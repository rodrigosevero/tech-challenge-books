# api/routers/books.py
from typing import List, Dict, Optional, Tuple
from fastapi import APIRouter, Depends, HTTPException, Query
from api.schemas import Book, PaginatedBooks
from api.deps import get_dataset

router = APIRouter(prefix="/api/v1", tags=["books"])

SORTABLE = {"id", "price", "rating", "title"}

def _parse_sort(sort: Optional[str]) -> Tuple[str, bool]:
    # "price|asc" ou "rating|desc"
    if not sort:
        return ("id", True)
    parts = sort.split("|", 1)
    field = parts[0].strip()
    order = parts[1].strip().lower() if len(parts) > 1 else "asc"
    if field not in SORTABLE:
        field = "id"
    asc = order != "desc"
    return (field, asc)

def _paginate(items: List[Dict], page: int, limit: int) -> Tuple[List[Dict], int]:
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    return items[start:end], total

@router.get("/books", response_model=PaginatedBooks)
def list_books(
    dataset = Depends(get_dataset),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    sort: Optional[str] = Query(None, description="Ex.: id|asc, price|desc, rating|asc, title|asc"),
):
    field, asc = _parse_sort(sort)
    ordered = sorted(dataset, key=lambda x: x.get(field), reverse=not asc)
    page_items, total = _paginate(ordered, page, limit)
    return {"items": page_items, "page": page, "limit": limit, "total": total}

@router.get("/books/search", response_model=PaginatedBooks)
def search_books(
    dataset = Depends(get_dataset),
    title: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    sort: Optional[str] = Query(None),
):
    items = dataset

    if title:
        t = title.lower().strip()
        items = [b for b in items if t in b["title"].lower()]

    if category:
        c = category.lower().strip()
        items = [b for b in items if b["category"].lower() == c]

    if min_price is not None:
        items = [b for b in items if b["price"] >= float(min_price)]
    if max_price is not None:
        items = [b for b in items if b["price"] <= float(max_price)]

    field, asc = _parse_sort(sort)
    items = sorted(items, key=lambda x: x.get(field), reverse=not asc)

    page_items, total = _paginate(items, page, limit)
    return {"items": page_items, "page": page, "limit": limit, "total": total}

@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, dataset = Depends(get_dataset)):
    for row in dataset:
        if row["id"] == book_id:
            return row
    raise HTTPException(status_code=404, detail="Book not found")
