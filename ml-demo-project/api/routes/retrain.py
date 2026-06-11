"""
重训练路由

提供 API 接口触发模型重训练流程
"""

import asyncio
import json
import os
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException
from loguru import logger

from api.schemas import RetrainRequest, RetrainResponse

router = APIRouter()

# 重训练状态
retrain_status = {
    "running": False,
    "last_run": None,
    "last_result": None,
}


@router.post("/retrain", response_model=RetrainResponse, tags=["Retrain"])
async def trigger_retrain(
    request: RetrainRequest,
    background_tasks: BackgroundTasks,
):
    """
    触发模型重训练
    
    支持:
    - 强制重训练 (忽略晋升检查)
    - 超参数调优
    - 后台异步执行
    
    返回:
    - 任务状态
    - Pipeline ID (可用于查询进度)
    """
    if retrain_status["running"]:
        raise HTTPException(
            status_code=409,
            detail="重训练任务正在执行中，请稍后再试",
        )
    
    # 检查是否需要重训练 (漂移检测)
    if not request.force:
        drift_check = _check_drift_before_retrain()
        if not drift_check["should_retrain"]:
            return RetrainResponse(
                status="skipped",
                message=f"无需重训练: {drift_check['reason']}",
            )
    
    # 启动后台任务
    pipeline_id = f"retrain_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    background_tasks.add_task(
        _run_retrain_task,
        pipeline_id=pipeline_id,
        tune_hyperparameters=request.tune_hyperparameters,
    )
    
    return RetrainResponse(
        status="started",
        message="重训练任务已启动，后台执行中",
        pipeline_id=pipeline_id,
    )


@router.get("/retrain/status", tags=["Retrain"])
async def retrain_status_check():
    """
    查询重训练状态
    
    返回:
    - 是否正在运行
    - 上次运行时间
    - 上次运行结果
    """
    return {
        "running": retrain_status["running"],
        "last_run": retrain_status["last_run"],
        "last_result": retrain_status["last_result"],
    }


@router.post("/retrain/compare", tags=["Retrain"])
async def compare_with_current():
    """
    对比最新训练的模型与当前生产模型
    
    返回:
    - 指标对比
    - 是否应该晋升
    """
    model_dir = "models"
    
    # 加载训练摘要
    summary_path = os.path.join(model_dir, "training_summary.json")
    if not os.path.exists(summary_path):
        raise HTTPException(status_code=404, detail="未找到训练结果")
    
    with open(summary_path) as f:
        summary = json.load(f)
    
    # 加载生产版本
    prod_path = os.path.join(model_dir, "production_version.json")
    if not os.path.exists(prod_path):
        return {
            "message": "当前无生产模型，最新训练的模型可直接部署",
            "latest_training": summary,
        }
    
    with open(prod_path) as f:
        prod_version = json.load(f)
    
    # 对比
    latest_model = summary.get("best_model")
    latest_metrics = None
    for result in summary.get("results", []):
        if result["model"] == latest_model:
            latest_metrics = result["metrics"]
            break
    
    prod_metrics = prod_version.get("metrics", {})
    
    comparison = {
        "latest_model": latest_model,
        "production_model": prod_version.get("model_name"),
        "latest_metrics": latest_metrics,
        "production_metrics": prod_metrics,
    }
    
    if latest_metrics and prod_metrics:
        rmse_improvement = (prod_metrics.get("rmse", 0) - latest_metrics.get("rmse", 0)) / prod_metrics.get("rmse", 1)
        comparison["rmse_improvement_pct"] = round(rmse_improvement * 100, 2)
        comparison["should_promote"] = rmse_improvement > 0.01  # 至少改善 1%
    
    return comparison


def _check_drift_before_retrain() -> dict:
    """检查是否需要重训练"""
    try:
        from src.monitoring.drift_detector import check_drift_and_alert
        
        result = check_drift_and_alert()
        
        if result["severity"] == "critical":
            return {"should_retrain": True, "reason": "检测到严重数据漂移"}
        elif result["severity"] == "warning":
            return {"should_retrain": True, "reason": "检测到数据漂移警告"}
        else:
            return {"should_retrain": False, "reason": "数据分布稳定，无需重训练"}
    
    except Exception as e:
        logger.warning(f"漂移检测失败: {e}")
        return {"should_retrain": False, "reason": f"漂移检测失败: {str(e)}"}


def _run_retrain_task(pipeline_id: str, tune_hyperparameters: bool = False):
    """后台执行重训练任务"""
    retrain_status["running"] = True
    retrain_status["last_run"] = datetime.now().isoformat()
    
    logger.info(f"开始重训练任务: {pipeline_id}")
    
    try:
        if tune_hyperparameters:
            # 超参数调优模式
            from src.models.train import tune_hyperparameters as tune_func
            from src.data.preprocess import prepare_data, load_config
            from src.models.train import train_model
            
            config = load_config()
            data = prepare_data(config)
            
            tuning_config = config.get("training", {}).get("hyperparameter_tuning", {})
            best_params = tune_func(
                "LGBMRegressor",
                data["X_train"],
                data["y_train"],
                n_trials=tuning_config.get("n_trials", 50),
                timeout=tuning_config.get("timeout", 300),
            )
            
            result = train_model(
                model_name="lightgbm_tuned",
                model_type="LGBMRegressor",
                params=best_params,
                X_train=data["X_train"],
                y_train=data["y_train"],
                X_test=data["X_test"],
                y_test=data["y_test"],
                config=config,
            )
            
            retrain_status["last_result"] = {
                "pipeline_id": pipeline_id,
                "status": "success",
                "model_name": result["model_name"],
                "metrics": result["metrics"],
                "tuned": True,
            }
        
        else:
            # 标准训练流程
            from src.pipeline.pipeline import run_full_pipeline
            
            report = run_full_pipeline()
            
            retrain_status["last_result"] = {
                "pipeline_id": pipeline_id,
                "status": report["status"],
                "best_model": report.get("steps", {}).get("evaluation", {}).get("best_model"),
                "metrics": report.get("steps", {}).get("evaluation", {}).get("metrics"),
                "tuned": False,
            }
        
        logger.info(f"重训练任务完成: {pipeline_id}")
    
    except Exception as e:
        logger.error(f"重训练任务失败: {e}")
        retrain_status["last_result"] = {
            "pipeline_id": pipeline_id,
            "status": "failed",
            "error": str(e),
        }
    
    finally:
        retrain_status["running"] = False
