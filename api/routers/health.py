# api/routers/health.py
from fastapi import APIRouter, Depends
from api.schemas import HealthResponse
from api.deps import get_dataset

router = APIRouter(prefix="/api/v1", tags=["health"])

@router.get("/health", response_model=HealthResponse)
def health(dataset = Depends(get_dataset)):
    return HealthResponse(status="ok", dataset_size=len(dataset))
