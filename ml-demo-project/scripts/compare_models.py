#!/usr/bin/env python
"""
模型对比脚本

对比所有已训练模型的性能，输出对比报告。
"""

import json
import os
from loguru import logger

MODEL_DIR = "models"


def compare_models():
    """对比所有已训练模型"""
    
    # 加载训练摘要
    summary_path = os.path.join(MODEL_DIR, "training_summary.json")
    if not os.path.exists(summary_path):
        logger.error("未找到训练摘要，请先运行训练")
        return
    
    with open(summary_path) as f:
        summary = json.load(f)
    
    results = summary.get("results", [])
    
    if not results:
        logger.error("训练结果为空")
        return
    
    # 打印对比表
    logger.info("\n" + "=" * 70)
    logger.info("📊 模型性能对比")
    logger.info("=" * 70)
    logger.info(f"{'排名':<4} {'模型':<20} {'MAE':<10} {'RMSE':<10} {'R²':<10} {'MAPE%':<10}")
    logger.info("-" * 70)
    
    # 按 RMSE 排序
    sorted_results = sorted(results, key=lambda r: r["metrics"]["rmse"])
    
    for i, result in enumerate(sorted_results, 1):
        name = result["model"]
        metrics = result["metrics"]
        logger.info(
            f"{i:<4} {name:<20} "
            f"{metrics['mae']:<10.4f} "
            f"{metrics['rmse']:<10.4f} "
            f"{metrics['r2']:<10.4f} "
            f"{metrics['mape']:<10.2f}"
        )
    
    logger.info("=" * 70)
    
    # 最佳模型
    best = sorted_results[0]
    logger.info(f"\n🏆 最佳模型: {best['model']}")
    logger.info(f"   RMSE: {best['metrics']['rmse']:.4f}")
    logger.info(f"   R²: {best['metrics']['r2']:.4f}")
    
    # 与生产版本对比
    prod_path = os.path.join(MODEL_DIR, "production_version.json")
    if os.path.exists(prod_path):
        with open(prod_path) as f:
            prod_version = json.load(f)
        
        prod_metrics = prod_version.get("metrics", {})
        if prod_metrics:
            logger.info(f"\n📊 与生产版本对比:")
            logger.info(f"   生产模型: {prod_version.get('model_name')}")
            logger.info(f"   生产 RMSE: {prod_metrics.get('rmse', 'N/A')}")
            logger.info(f"   最新 RMSE: {best['metrics']['rmse']:.4f}")
            
            improvement = (prod_metrics.get("rmse", 0) - best["metrics"]["rmse"]) / prod_metrics.get("rmse", 1) * 100
            logger.info(f"   改善: {improvement:.2f}%")
    
    # 特征重要性
    logger.info("\n📊 特征重要性 (最佳模型):")
    importance_path = os.path.join(MODEL_DIR, "evaluation_report.json")
    if os.path.exists(importance_path):
        with open(importance_path) as f:
            report = json.load(f)
        
        feature_importance = report.get("feature_importance", [])
        for i, item in enumerate(feature_importance[:10], 1):
            logger.info(f"   {i:>2}. {item['feature']:<25} {item['importance']:.4f}")


if __name__ == "__main__":
    compare_models()
