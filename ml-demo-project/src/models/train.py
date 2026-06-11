"""
模型训练模块

功能:
- 多模型训练 (RandomForest, LightGBM, XGBoost)
- 超参数调优 (Optuna)
- 交叉验证
- MLflow 实验追踪
- 模型持久化
"""

import json
import os
import pickle
from datetime import datetime

import joblib
import mlflow
import numpy as np
import optuna
import yaml
from lightgbm import LGBMRegressor
from loguru import logger
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor

from src.data.preprocess import load_config, prepare_data

# 模型注册表
MODEL_REGISTRY = {
    "RandomForestRegressor": RandomForestRegressor,
    "LGBMRegressor": LGBMRegressor,
    "XGBRegressor": XGBRegressor,
}

# 模型保存目录
MODEL_DIR = "models"


def get_model(model_type: str, params: dict):
    """根据类型和参数创建模型实例"""
    if model_type not in MODEL_REGISTRY:
        raise ValueError(f"未知模型类型: {model_type}. 可选: {list(MODEL_REGISTRY.keys())}")
    return MODEL_REGISTRY[model_type](**params)


def train_model(
    model_name: str,
    model_type: str,
    params: dict,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    config: dict = None,
) -> dict:
    """
    训练单个模型
    
    Args:
        model_name: 模型名称
        model_type: 模型类型 (对应 MODEL_REGISTRY)
        params: 模型参数
        X_train, y_train: 训练数据
        X_test, y_test: 测试数据
        config: 配置
        
    Returns:
        dict: 训练结果 {model, metrics, model_name}
    """
    logger.info(f"训练模型: {model_name} ({model_type})")
    
    # 创建模型
    model = get_model(model_type, params)
    
    # 训练
    model.fit(X_train, y_train)
    
    # 预测
    y_pred = model.predict(X_test)
    
    # 计算指标
    metrics = _calculate_metrics(y_test, y_pred)
    
    # MLflow 追踪
    if config:
        mlflow_config = config.get("mlflow", {})
        tracking_uri = mlflow_config.get("tracking_uri", "http://localhost:5000")
        experiment_name = mlflow_config.get("experiment_name", "california-housing")
        
        try:
            mlflow.set_tracking_uri(tracking_uri)
            mlflow.set_experiment(experiment_name)
            
            with mlflow.start_run(run_name=model_name):
                # 记录参数
                mlflow.log_params(params)
                mlflow.log_param("model_type", model_type)
                
                # 记录指标
                mlflow.log_metrics(metrics)
                
                # 记录模型
                mlflow.sklearn.log_model(model, "model")
                
                logger.info(f"MLflow 记录完成: {model_name}")
        except Exception as e:
            logger.warning(f"MLflow 记录失败 (非关键): {e}")
    
    # 保存模型
    _save_model(model, model_name, metrics)
    
    logger.info(f"模型 {model_name} 训练完成 - RMSE: {metrics['rmse']:.4f}, R²: {metrics['r2']:.4f}")
    
    return {
        "model": model,
        "metrics": metrics,
        "model_name": model_name,
    }


def train_all_models(config: dict = None) -> list[dict]:
    """
    训练配置中的所有模型
    
    Returns:
        list[dict]: 所有模型的训练结果
    """
    if config is None:
        config = load_config()
    
    # 准备数据
    data = prepare_data(config)
    
    results = []
    models_config = config.get("training", {}).get("models", [])
    
    for model_conf in models_config:
        name = model_conf["name"]
        model_type = model_conf["type"]
        params = model_conf["params"]
        
        result = train_model(
            model_name=name,
            model_type=model_type,
            params=params,
            X_train=data["X_train"],
            y_train=data["y_train"],
            X_test=data["X_test"],
            y_test=data["y_test"],
            config=config,
        )
        results.append(result)
    
    # 找出最佳模型
    best = max(results, key=lambda r: r["metrics"]["r2"])
    logger.info(f"\n最佳模型: {best['model_name']} (R²={best['metrics']['r2']:.4f})")
    
    # 保存所有结果
    _save_training_results(results, best["model_name"])
    
    # 保存最佳模型的 scaler
    joblib.dump(data["scaler"], os.path.join(MODEL_DIR, "scaler.joblib"))
    joblib.dump(data["feature_names"], os.path.join(MODEL_DIR, "feature_names.joblib"))
    logger.info("Scaler 和特征名已保存")
    
    return results


def tune_hyperparameters(
    model_type: str,
    X_train: np.ndarray,
    y_train: np.ndarray,
    n_trials: int = 50,
    timeout: int = 300,
) -> dict:
    """
    使用 Optuna 进行超参数调优
    
    Args:
        model_type: 模型类型
        X_train, y_train: 训练数据
        n_trials: 试验次数
        timeout: 超时时间 (秒)
        
    Returns:
        dict: 最佳超参数
    """
    logger.info(f"开始超参数调优: {model_type}, {n_trials} 次试验")
    
    def objective(trial):
        if model_type == "LGBMRegressor":
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 500),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
                "max_depth": trial.suggest_int("max_depth", 3, 12),
                "num_leaves": trial.suggest_int("num_leaves", 15, 63),
                "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
                "min_child_samples": trial.suggest_int("min_child_samples", 5, 50),
                "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
                "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
                "random_state": 42,
                "verbose": -1,
            }
        elif model_type == "XGBRegressor":
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 500),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
                "max_depth": trial.suggest_int("max_depth", 3, 12),
                "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
                "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
                "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
                "random_state": 42,
                "verbosity": 0,
            }
        else:  # RandomForest
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 50, 300),
                "max_depth": trial.suggest_int("max_depth", 5, 30),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
                "random_state": 42,
                "n_jobs": -1,
            }
        
        model = get_model(model_type, params)
        scores = cross_val_score(model, X_train, y_train, cv=5, scoring="neg_root_mean_squared_error")
        return -scores.mean()
    
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials, timeout=timeout)
    
    best_params = study.best_params
    logger.info(f"最佳参数: {best_params}")
    logger.info(f"最佳 RMSE: {study.best_value:.4f}")
    
    return best_params


def _calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """计算评估指标"""
    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
    
    return {
        "mae": round(float(mae), 4),
        "rmse": round(float(rmse), 4),
        "r2": round(float(r2), 4),
        "mape": round(float(mape), 2),
    }


def _save_model(model, model_name: str, metrics: dict):
    """保存模型到磁盘"""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # 保存模型
    model_path = os.path.join(MODEL_DIR, f"{model_name}.joblib")
    joblib.dump(model, model_path)
    
    # 保存指标
    metrics_path = os.path.join(MODEL_DIR, f"{model_name}_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump({
            **metrics,
            "model_name": model_name,
            "trained_at": datetime.now().isoformat(),
        }, f, indent=2)
    
    logger.debug(f"模型已保存: {model_path}")


def _save_training_results(results: list[dict], best_model_name: str):
    """保存训练结果摘要"""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    summary = []
    for r in results:
        summary.append({
            "model_name": r["model_name"],
            "metrics": r["metrics"],
        })
    
    output = {
        "best_model": best_model_name,
        "trained_at": datetime.now().isoformat(),
        "results": summary,
    }
    
    with open(os.path.join(MODEL_DIR, "training_summary.json"), "w") as f:
        json.dump(output, f, indent=2)
    
    logger.info(f"训练摘要已保存: models/training_summary.json")


# ===== CLI 入口 =====
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="模型训练")
    parser.add_argument("--tune", action="store_true", help="启用超参数调优")
    parser.add_argument("--config", default="config/config.yaml", help="配置文件路径")
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    if args.tune:
        logger.info("=== 超参数调优模式 ===")
        data = prepare_data(config)
        
        tuning_config = config.get("training", {}).get("hyperparameter_tuning", {})
        n_trials = tuning_config.get("n_trials", 50)
        timeout = tuning_config.get("timeout", 300)
        
        # 对 LightGBM 调优
        best_params = tune_hyperparameters(
            "LGBMRegressor",
            data["X_train"],
            data["y_train"],
            n_trials=n_trials,
            timeout=timeout,
        )
        
        # 用最佳参数训练
        train_model(
            model_name="lightgbm_tuned",
            model_type="LGBMRegressor",
            params=best_params,
            X_train=data["X_train"],
            y_train=data["y_train"],
            X_test=data["X_test"],
            y_test=data["y_test"],
            config=config,
        )
    else:
        logger.info("=== 标准训练模式 ===")
        train_all_models(config)
