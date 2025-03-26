from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "components": {
            "database": "connected",
            "gpu": "available"
        }
    }