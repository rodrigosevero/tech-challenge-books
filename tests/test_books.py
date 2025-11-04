# tests/test_books.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    payload = r.json()
    assert payload["status"] == "ok"
    assert payload["dataset_size"] > 0

def test_list_books_ok():
    r = client.get("/api/v1/books?limit=3")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data and len(data["items"]) <= 3
    assert data["total"] >= len(data["items"])

def test_get_book_404():
    r = client.get("/api/v1/books/999999")
    assert r.status_code == 404

def test_search_by_title():
    r = client.get("/api/v1/books/search?title=the")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data

def test_categories():
    r = client.get("/api/v1/categories")
    assert r.status_code == 200
    cats = r.json()
    assert cats["total"] >= 1
