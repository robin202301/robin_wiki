"""
健康检查路由
"""

from datetime import datetime
from fastapi import APIRouter

from api.schemas import HealthResponse
from src.models.predict import get_predictor

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    健康检查端点
    
    返回:
    - 服务状态
    - 模型加载状态
    - 版本信息
    """
    try:
        predictor = get_predictor()
        return HealthResponse(
            status="healthy",
            model_loaded=True,
            model_name=predictor.model_name,
            version="1.0.0",
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            model_name=None,
            version="1.0.0",
            timestamp=datetime.now().isoformat(),
        )


@router.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """详细健康检查"""
    import os
    import json
    from pathlib import Path
    
    model_dir = Path("models")
    
    health_info = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model": {},
        "files": {},
    }
    
    # 检查模型文件
    if model_dir.exists():
        health_info["files"]["models_dir"] = str(model_dir)
        
        # 训练摘要
        summary_path = model_dir / "training_summary.json"
        if summary_path.exists():
            with open(summary_path) as f:
                health_info["model"]["training_summary"] = json.load(f)
        
        # 生产版本
        prod_path = model_dir / "production_version.json"
        if prod_path.exists():
            with open(prod_path) as f:
                health_info["model"]["production_version"] = json.load(f)
        
        # 列出所有模型文件
        model_files = [f.name for f in model_dir.glob("*.joblib")]
        health_info["files"]["model_files"] = model_files
    
    # 模型加载状态
    try:
        predictor = get_predictor()
        health_info["model"]["loaded"] = True
        health_info["model"]["name"] = predictor.model_name
    except Exception as e:
        health_info["model"]["loaded"] = False
        health_info["model"]["error"] = str(e)
    
    return health_info
