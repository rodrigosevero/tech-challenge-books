# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import health as health_router
from api.routers import books as books_router
from api.routers import categories as categories_router

app = FastAPI(
    title="Books API (Tech Challenge)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(health_router.router)
app.include_router(books_router.router)
app.include_router(categories_router.router)
