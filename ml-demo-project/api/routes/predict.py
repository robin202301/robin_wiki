"""
预测路由
"""

import time
from fastapi import APIRouter, HTTPException
from loguru import logger

from api.schemas import (
    BatchPredictRequest,
    BatchPredictResponse,
    PredictRequest,
    PredictResponse,
)
from src.models.predict import get_predictor

router = APIRouter()


@router.post("/predict", response_model=PredictResponse, tags=["Predict"])
async def predict(request: PredictRequest):
    """
    单条预测
    
    输入 8 个特征，返回房价预测值。
    
    特征说明:
    - MedInc: 街区收入中位数 (万美元)
    - HouseAge: 房屋年龄中位数 (年)
    - AveRooms: 平均房间数
    - AveBedrms: 平均卧室数
    - Population: 街区人口
    - AveOccup: 平均入住人数
    - Latitude: 纬度
    - Longitude: 经度
    
    示例:
    ```json
    {
        "features": [8.32, 41, 6.98, 1.02, 322, 2.56, 37.88, -122.23]
    }
    ```
    """
    try:
        predictor = get_predictor()
        result = predictor.predict(request.features)
        
        logger.info(f"预测请求: {request.features} → {result['prediction_label']}")
        
        return PredictResponse(**result)
    
    except FileNotFoundError as e:
        logger.error(f"模型未加载: {e}")
        raise HTTPException(status_code=503, detail="模型未加载，请先训练模型")
    
    except ValueError as e:
        logger.error(f"输入验证失败: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"预测失败: {e}")
        raise HTTPException(status_code=500, detail=f"预测失败: {str(e)}")


@router.post("/predict/batch", response_model=BatchPredictResponse, tags=["Predict"])
async def predict_batch(request: BatchPredictRequest):
    """
    批量预测
    
    输入多条样本 (最多 1000 条)，返回批量预测结果。
    
    示例:
    ```json
    {
        "samples": [
            [8.32, 41, 6.98, 1.02, 322, 2.56, 37.88, -122.23],
            [7.25, 30, 5.0, 1.0, 200, 2.0, 35.0, -121.5]
        ]
    }
    ```
    """
    try:
        predictor = get_predictor()
        result = predictor.predict_batch(request.samples)
        
        logger.info(f"批量预测: {result['count']} 条样本, 延迟 {result['latency_ms']:.2f}ms")
        
        return BatchPredictResponse(**result)
    
    except FileNotFoundError as e:
        logger.error(f"模型未加载: {e}")
        raise HTTPException(status_code=503, detail="模型未加载，请先训练模型")
    
    except ValueError as e:
        logger.error(f"输入验证失败: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"批量预测失败: {e}")
        raise HTTPException(status_code=500, detail=f"预测失败: {str(e)}")


@router.get("/model/info", tags=["Model"])
async def model_info():
    """
    获取当前模型信息
    
    返回:
    - 模型名称
    - 训练指标
    - 特征列表
    """
    import json
    import os
    
    model_dir = "models"
    
    info = {}
    
    # 训练摘要
    summary_path = os.path.join(model_dir, "training_summary.json")
    if os.path.exists(summary_path):
        with open(summary_path) as f:
            info["training_summary"] = json.load(f)
    
    # 生产版本
    prod_path = os.path.join(model_dir, "production_version.json")
    if os.path.exists(prod_path):
        with open(prod_path) as f:
            info["production_version"] = json.load(f)
    
    # 当前加载的模型
    try:
        predictor = get_predictor()
        info["current_model"] = predictor.model_name
    except:
        info["current_model"] = None
    
    # 特征名
    import joblib
    features_path = os.path.join(model_dir, "feature_names.joblib")
    if os.path.exists(features_path):
        info["feature_names"] = joblib.load(features_path)
    
    return info


@router.post("/model/reload", tags=["Model"])
async def reload_model(model_name: str = None):
    """
    热重载模型
    
    可选指定模型名，不指定则加载最佳模型。
    """
    try:
        from src.models.predict import reload_predictor
        
        predictor = reload_predictor(model_name)
        
        return {
            "status": "success",
            "message": f"模型已重载: {predictor.model_name}",
            "model_name": predictor.model_name,
        }
    
    except Exception as e:
        logger.error(f"模型重载失败: {e}")
        raise HTTPException(status_code=500, detail=f"模型重载失败: {str(e)}")
