"""
模型评估模块

功能:
- 详细评估报告生成
- 模型对比
- 残差分析
- 特征重要性分析
- 模型晋升判断
"""

import json
import os

import joblib
import numpy as np
import yaml
from loguru import logger

from src.data.preprocess import load_config, prepare_data
from src.models.train import MODEL_DIR, train_all_models


def load_metrics(model_name: str) -> dict:
    """加载已保存的模型指标"""
    metrics_path = os.path.join(MODEL_DIR, f"{model_name}_metrics.json")
    if not os.path.exists(metrics_path):
        return {}
    with open(metrics_path, "r") as f:
        return json.load(f)


def load_training_summary() -> dict:
    """加载训练摘要"""
    summary_path = os.path.join(MODEL_DIR, "training_summary.json")
    if not os.path.exists(summary_path):
        return {}
    with open(summary_path, "r") as f:
        return json.load(f)


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    """
    详细评估模型
    
    Returns:
        dict: 包含各项评估指标和图表数据
    """
    y_pred = model.predict(X_test)
    
    # 基础指标
    residuals = y_test - y_pred
    abs_residuals = np.abs(residuals)
    
    metrics = {
        "mae": round(float(np.mean(abs_residuals)), 4),
        "rmse": round(float(np.sqrt(np.mean(residuals ** 2))), 4),
        "r2": round(float(1 - np.sum(residuals ** 2) / np.sum((y_test - np.mean(y_test)) ** 2)), 4),
        "max_error": round(float(np.max(abs_residuals)), 4),
        "median_ae": round(float(np.median(abs_residuals)), 4),
    }
    
    # 残差分析
    residual_analysis = {
        "mean_residual": round(float(np.mean(residuals)), 4),
        "std_residual": round(float(np.std(residuals)), 4),
        "skewness": round(float(_skewness(residuals)), 4),
        "within_05": round(float(np.mean(abs_residuals < 0.5) * 100), 2),
        "within_10": round(float(np.mean(abs_residuals < 1.0) * 100), 2),
    }
    
    return {
        "metrics": metrics,
        "residual_analysis": residual_analysis,
        "predictions": y_pred.tolist()[:100],  # 保存前100个预测
        "actuals": y_test.tolist()[:100],
    }


def compare_models(results: list[dict]) -> dict:
    """
    对比多个模型
    
    Returns:
        dict: 对比报告
    """
    comparison = []
    for r in results:
        comparison.append({
            "model": r["model_name"],
            "mae": r["metrics"]["mae"],
            "rmse": r["metrics"]["rmse"],
            "r2": r["metrics"]["r2"],
            "mape": r["metrics"]["mape"],
        })
    
    # 排序 (按 RMSE 升序)
    comparison.sort(key=lambda x: x["rmse"])
    
    # 找最佳
    best = comparison[0]
    
    report = {
        "ranking": comparison,
        "best_model": best["model"],
        "best_rmse": best["rmse"],
        "best_r2": best["r2"],
    }
    
    # 打印对比表
    logger.info("\n" + "=" * 60)
    logger.info("模型对比报告")
    logger.info("=" * 60)
    logger.info(f"{'排名':<4} {'模型':<20} {'MAE':<8} {'RMSE':<8} {'R²':<8} {'MAPE%':<8}")
    logger.info("-" * 60)
    for i, m in enumerate(comparison, 1):
        logger.info(f"{i:<4} {m['model']:<20} {m['mae']:<8.4f} {m['rmse']:<8.4f} {m['r2']:<8.4f} {m['mape']:<8.2f}")
    logger.info("=" * 60)
    logger.info(f"🏆 最佳模型: {best['model']} (RMSE={best['rmse']:.4f})")
    
    return report


def should_promote_model(
    new_metrics: dict,
    config: dict = None,
) -> dict:
    """
    判断新模型是否应该替代当前生产模型
    
    基于配置中的 promotion_thresholds
    
    Returns:
        dict: {should_promote: bool, reason: str}
    """
    if config is None:
        config = load_config()
    
    thresholds = config.get("evaluation", {}).get("promotion_thresholds", {})
    rmse_improvement = thresholds.get("rmse_improvement", 0.01)
    r2_minimum = thresholds.get("r2_minimum", 0.75)
    
    # 加载当前生产模型的指标
    current_summary = load_training_summary()
    current_best = current_summary.get("best_model", "")
    current_metrics = load_metrics(current_best) if current_best else {}
    
    # 判断逻辑
    reasons = []
    
    # 检查 R² 最低要求
    if new_metrics.get("r2", 0) < r2_minimum:
        return {
            "should_promote": False,
            "reason": f"R² ({new_metrics.get('r2', 0):.4f}) 低于最低要求 ({r2_minimum})",
        }
    
    # 如果没有旧模型，直接晋升
    if not current_metrics:
        return {
            "should_promote": True,
            "reason": "无现有生产模型，直接晋升",
        }
    
    # 检查 RMSE 改善
    old_rmse = current_metrics.get("rmse", float("inf"))
    new_rmse = new_metrics.get("rmse", float("inf"))
    improvement = (old_rmse - new_rmse) / old_rmse
    
    if improvement >= rmse_improvement:
        reasons.append(f"RMSE 改善 {improvement:.2%} (阈值: {rmse_improvement:.2%})")
    
    # 检查 R² 改善
    old_r2 = current_metrics.get("r2", 0)
    new_r2 = new_metrics.get("r2", 0)
    if new_r2 > old_r2:
        reasons.append(f"R² 从 {old_r2:.4f} 提升到 {new_r2:.4f}")
    
    should_promote = len(reasons) > 0
    
    return {
        "should_promote": should_promote,
        "reason": "; ".join(reasons) if reasons else "新模型未优于当前模型",
        "old_rmse": old_rmse,
        "new_rmse": new_rmse,
        "improvement": round(improvement, 4),
    }


def get_feature_importance(model, feature_names: list[str]) -> list[dict]:
    """提取特征重要性"""
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        logger.warning("模型不支持特征重要性")
        return []
    
    importance_list = [
        {"feature": name, "importance": round(float(imp), 4)}
        for name, imp in zip(feature_names, importances)
    ]
    importance_list.sort(key=lambda x: x["importance"], reverse=True)
    
    logger.info("\n特征重要性 Top 10:")
    for i, item in enumerate(importance_list[:10], 1):
        bar = "█" * int(item["importance"] * 50)
        logger.info(f"  {i:>2}. {item['feature']:<25} {item['importance']:.4f} {bar}")
    
    return importance_list


def _skewness(data: np.ndarray) -> float:
    """计算偏度"""
    n = len(data)
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:
        return 0.0
    return (n / ((n - 1) * (n - 2) + 1e-8)) * np.sum(((data - mean) / std) ** 3)


def run_evaluation(config: dict = None) -> dict:
    """
    运行完整评估流程
    
    Returns:
        dict: 评估报告
    """
    if config is None:
        config = load_config()
    
    # 加载训练摘要
    summary = load_training_summary()
    if not summary:
        logger.warning("未找到训练结果，先执行训练...")
        results = train_all_models(config)
        summary = load_training_summary()
    
    # 准备数据
    data = prepare_data(config)
    
    # 加载最佳模型
    best_model_name = summary.get("best_model", "")
    model_path = os.path.join(MODEL_DIR, f"{best_model_name}.joblib")
    model = joblib.load(model_path)
    
    # 详细评估
    eval_result = evaluate_model(model, data["X_test"], data["y_test"])
    
    # 特征重要性
    feature_importance = get_feature_importance(model, data["feature_names"])
    
    # 模型晋升判断
    promotion = should_promote_model(eval_result["metrics"], config)
    
    report = {
        "best_model": best_model_name,
        "evaluation": eval_result,
        "feature_importance": feature_importance,
        "promotion": promotion,
    }
    
    # 保存报告
    report_path = os.path.join(MODEL_DIR, "evaluation_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n评估报告已保存: {report_path}")
    logger.info(f"模型晋升: {'✅ 是' if promotion['should_promote'] else '❌ 否'} - {promotion['reason']}")
    
    return report


if __name__ == "__main__":
    config = load_config()
    run_evaluation(config)
