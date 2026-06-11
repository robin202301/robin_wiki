"""
Pydantic 数据模型 - 请求/响应 Schema
"""

from typing import Optional
from pydantic import BaseModel, Field


# ===== 健康检查 =====
class HealthResponse(BaseModel):
    status: str = "healthy"
    model_loaded: bool
    model_name: Optional[str] = None
    version: str = "1.0.0"
    timestamp: str


# ===== 预测请求 =====
class PredictRequest(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=8,
        max_length=8,
        description="8个特征: [MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]"
    )


class BatchPredictRequest(BaseModel):
    samples: list[list[float]] = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="多条样本，每条 8 个特征"
    )


# ===== 预测响应 =====
class PredictResponse(BaseModel):
    prediction: float = Field(..., description="预测值 (房价中位数，单位: 十万美元)")
    prediction_label: str = Field(..., description="格式化预测值 (美元)")
    model: str = Field(..., description="使用的模型名称")
    latency_ms: float = Field(..., description="预测延迟 (毫秒)")


class BatchPredictResponse(BaseModel):
    predictions: list[float] = Field(..., description="预测值列表")
    prediction_labels: list[str] = Field(..., description="格式化预测值列表")
    model: str = Field(..., description="使用的模型名称")
    latency_ms: float = Field(..., description="预测延迟 (毫秒)")
    count: int = Field(..., description="预测样本数")


# ===== 重训练 =====
class RetrainRequest(BaseModel):
    force: bool = Field(False, description="强制执行重训练")
    tune_hyperparameters: bool = Field(False, description="是否进行超参数调优")


class RetrainResponse(BaseModel):
    status: str
    message: str
    pipeline_id: Optional[str] = None
    duration_seconds: Optional[float] = None
    best_model: Optional[str] = None
    metrics: Optional[dict] = None


# ===== 模型信息 =====
class ModelInfo(BaseModel):
    name: str
    version: str
    metrics: dict
    trained_at: str
    feature_count: int
    feature_names: list[str]


# ===== 漂移检测 =====
class DriftCheckResponse(BaseModel):
    overall_status: str
    alert: bool
    severity: str
    message: str
    feature_drift: list[dict]
    recommendation: str
