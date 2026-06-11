"""
完整 ML Pipeline

功能:
- 端到端执行完整流程
- 数据准备 → 训练 → 评估 → 注册 → 部署检查
- 生成执行报告
"""

import json
import os
from datetime import datetime

import joblib
from loguru import logger

from src.data.preprocess import load_config, prepare_data
from src.models.evaluate import evaluate_model, get_feature_importance, should_promote_model
from src.models.train import train_all_models

MODEL_DIR = "models"


def run_full_pipeline(config_path: str = "config/config.yaml") -> dict:
    """
    运行完整 ML Pipeline
    
    Steps:
    1. 加载配置
    2. 数据准备
    3. 模型训练
    4. 模型评估
    5. 晋升决策
    6. 生成报告
    
    Returns:
        dict: 执行报告
    """
    start_time = datetime.now()
    logger.info("=" * 70)
    logger.info("🚀 开始执行完整 ML Pipeline")
    logger.info("=" * 70)
    
    report = {
        "pipeline_id": f"pipeline_{start_time.strftime('%Y%m%d_%H%M%S')}",
        "started_at": start_time.isoformat(),
        "status": "running",
        "steps": {},
    }
    
    try:
        # Step 1: 加载配置
        logger.info("\n📋 Step 1: 加载配置")
        config = load_config(config_path)
        report["steps"]["config"] = {
            "status": "success",
            "config_path": config_path,
        }
        
        # Step 2: 数据准备
        logger.info("\n📊 Step 2: 数据准备")
        data = prepare_data(config)
        report["steps"]["data"] = {
            "status": "success",
            "train_samples": len(data["y_train"]),
            "test_samples": len(data["y_test"]),
            "features": len(data["feature_names"]),
            "feature_names": data["feature_names"],
        }
        
        # Step 3: 模型训练
        logger.info("\n🏋️ Step 3: 模型训练")
        results = train_all_models(config)
        report["steps"]["training"] = {
            "status": "success",
            "models_trained": len(results),
            "results": [
                {
                    "model": r["model_name"],
                    "metrics": r["metrics"],
                }
                for r in results
            ],
        }
        
        # Step 4: 模型评估
        logger.info("\n📈 Step 4: 模型评估")
        best_result = max(results, key=lambda r: r["metrics"]["r2"])
        eval_result = evaluate_model(best_result["model"], data["X_test"], data["y_test"])
        feature_importance = get_feature_importance(best_result["model"], data["feature_names"])
        
        report["steps"]["evaluation"] = {
            "status": "success",
            "best_model": best_result["model_name"],
            "metrics": eval_result["metrics"],
            "residual_analysis": eval_result["residual_analysis"],
            "feature_importance": feature_importance[:10],
        }
        
        # Step 5: 晋升决策
        logger.info("\n🎯 Step 5: 晋升决策")
        promotion = should_promote_model(eval_result["metrics"], config)
        report["steps"]["promotion"] = {
            "status": "success",
            "should_promote": promotion["should_promote"],
            "reason": promotion["reason"],
        }
        
        # Step 6: 保存模型版本
        if promotion["should_promote"]:
            logger.info("\n💾 Step 6: 保存生产模型版本")
            _save_production_version(best_result["model_name"], eval_result["metrics"])
            report["steps"]["production_save"] = {
                "status": "success",
                "model_name": best_result["model_name"],
            }
        else:
            logger.info("\n⏸️ Step 6: 跳过 (模型未改进)")
            report["steps"]["production_save"] = {
                "status": "skipped",
                "reason": promotion["reason"],
            }
        
        report["status"] = "success"
        
    except Exception as e:
        logger.error(f"Pipeline 执行失败: {e}")
        report["status"] = "failed"
        report["error"] = str(e)
    
    # 完成
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    report["finished_at"] = end_time.isoformat()
    report["duration_seconds"] = round(duration, 2)
    
    # 保存报告
    _save_pipeline_report(report)
    
    # 打印摘要
    logger.info("\n" + "=" * 70)
    logger.info("✅ Pipeline 执行完成")
    logger.info("=" * 70)
    logger.info(f"Pipeline ID: {report['pipeline_id']}")
    logger.info(f"状态: {report['status']}")
    logger.info(f"耗时: {duration:.2f}s")
    if report["status"] == "success":
        logger.info(f"最佳模型: {report['steps']['evaluation']['best_model']}")
        logger.info(f"RMSE: {report['steps']['evaluation']['metrics']['rmse']:.4f}")
        logger.info(f"R²: {report['steps']['evaluation']['metrics']['r2']:.4f}")
        logger.info(f"晋升决策: {'✅ 是' if report['steps']['promotion']['should_promote'] else '❌ 否'}")
    logger.info("=" * 70)
    
    return report


def _save_production_version(model_name: str, metrics: dict):
    """保存生产版本标记"""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    version_info = {
        "model_name": model_name,
        "metrics": metrics,
        "promoted_at": datetime.now().isoformat(),
        "version": datetime.now().strftime("%Y%m%d_%H%M%S"),
    }
    
    with open(os.path.join(MODEL_DIR, "production_version.json"), "w") as f:
        json.dump(version_info, f, indent=2)
    
    logger.info(f"生产版本已更新: {model_name} v{version_info['version']}")


def _save_pipeline_report(report: dict):
    """保存 Pipeline 报告"""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    report_path = os.path.join(MODEL_DIR, f"pipeline_report_{report['pipeline_id']}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 同时保存最新的
    with open(os.path.join(MODEL_DIR, "latest_pipeline_report.json"), "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Pipeline 报告已保存: {report_path}")


def compare_pipeline_reports(report_id_1: str, report_id_2: str) -> dict:
    """
    对比两次 Pipeline 执行结果
    
    Args:
        report_id_1: 第一次 Pipeline ID
        report_id_2: 第二次 Pipeline ID
        
    Returns:
        dict: 对比结果
    """
    path1 = os.path.join(MODEL_DIR, f"pipeline_report_{report_id_1}.json")
    path2 = os.path.join(MODEL_DIR, f"pipeline_report_{report_id_2}.json")
    
    if not os.path.exists(path1) or not os.path.exists(path2):
        raise FileNotFoundError("报告文件不存在")
    
    with open(path1) as f:
        report1 = json.load(f)
    with open(path2) as f:
        report2 = json.load(f)
    
    metrics1 = report1["steps"]["evaluation"]["metrics"]
    metrics2 = report2["steps"]["evaluation"]["metrics"]
    
    comparison = {
        "report_1": report_id_1,
        "report_2": report_id_2,
        "metrics_comparison": {
            metric: {
                "value_1": metrics1.get(metric),
                "value_2": metrics2.get(metric),
                "improvement": round(
                    (metrics1.get(metric, 0) - metrics2.get(metric, 0)) / metrics1.get(metric, 1) * 100,
                    2
                ),
            }
            for metric in ["mae", "rmse", "r2"]
        },
    }
    
    logger.info("\nPipeline 对比:")
    logger.info(f"{'指标':<10} {'Pipeline 1':<15} {'Pipeline 2':<15} {'改善':<10}")
    logger.info("-" * 50)
    for metric, values in comparison["metrics_comparison"].items():
        logger.info(f"{metric:<10} {values['value_1']:<15.4f} {values['value_2']:<15.4f} {values['improvement']:.2f}%")
    
    return comparison


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="运行 ML Pipeline")
    parser.add_argument("--config", default="config/config.yaml", help="配置文件路径")
    args = parser.parse_args()
    
    run_full_pipeline(args.config)
