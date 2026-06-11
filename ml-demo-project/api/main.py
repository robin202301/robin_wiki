"""
FastAPI 主入口

功能:
- 应用初始化
- 路由注册
- 中间件配置
- 启动/关闭事件
"""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from api.routes import health, predict, retrain


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("🚀 ML API 服务启动")
    logger.info(f"启动时间: {datetime.now().isoformat()}")
    
    # 预加载模型
    try:
        from src.models.predict import get_predictor
        predictor = get_predictor()
        logger.info(f"✅ 模型已预加载: {predictor.model_name}")
    except Exception as e:
        logger.warning(f"⚠️ 模型预加载失败: {e}")
        logger.warning("请确保已训练模型: python -m src.models.train")
    
    yield
    
    # 关闭时
    logger.info("🛑 ML API 服务关闭")


# 创建应用
app = FastAPI(
    title="California Housing ML API",
    description="""
    ## 加州房价预测 API
    
    基于 California Housing 数据集的机器学习模型服务。
    
    ### 功能
    - 单条/批量预测
    - 模型信息管理
    - 热重载模型
    - 触发重训练
    - 健康检查
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus 指标
Instrumentator().instrument(app).expose(app)

# 注册路由
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(retrain.router)


@app.get("/", tags=["Root"])
async def root():
    """
    API 根路径
    
    返回 API 信息和文档链接。
    """
    return {
        "name": "California Housing ML API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "status": "running",
    }


@app.get("/metrics", tags=["Metrics"])
async def metrics():
    """
    Prometheus 指标端点
    
    用于监控和告警。
    """
    from prometheus_client import generate_latest
    
    return generate_latest()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
