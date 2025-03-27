from fastapi import APIRouter, Request  # 添加Request导入
from fastapi import Depends
import torch

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

@router.get("/ready")
async def readiness_check(request: Request):
    return {
        "model_ready": hasattr(request.app.state, "qa_engine"),
        "gpu_memory": f"{torch.cuda.memory_allocated()/1e9:.2f}GB used"
    }