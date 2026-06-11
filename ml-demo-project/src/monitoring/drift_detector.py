"""
数据漂移检测模块

功能:
- 检测特征分布变化 (PSI, KS 检验)
- 检测目标变量变化
- 生成漂移报告
- 触发重训练告警
"""

import json
import os
from datetime import datetime

import numpy as np
import yaml
from loguru import logger
from scipy import stats

from src.data.preprocess import load_config, prepare_data

MODEL_DIR = "models"


class DriftDetector:
    """数据漂移检测器"""
    
    def __init__(self, config: dict = None):
        if config is None:
            config = load_config()
        
        drift_config = config.get("monitoring", {}).get("drift_detection", {})
        self.psi_warning = drift_config.get("psi_warning", 0.1)
        self.psi_critical = drift_config.get("psi_critical", 0.2)
        self.ks_threshold = drift_config.get("ks_threshold", 0.05)
        
        self.reference_data = None
        self._load_reference_data()
    
    def _load_reference_data(self):
        """加载参考数据 (训练数据)"""
        ref_path = os.path.join(MODEL_DIR, "reference_data.joblib")
        if os.path.exists(ref_path):
            import joblib
            self.reference_data = joblib.load(ref_path)
            logger.info("参考数据已加载")
        else:
            logger.warning("参考数据不存在，将使用当前训练数据")
            self._create_reference_data()
    
    def _create_reference_data(self):
        """创建参考数据"""
        try:
            data = prepare_data()
            import joblib
            os.makedirs(MODEL_DIR, exist_ok=True)
            joblib.dump(
                {"X": data["X_train"], "y": data["y_train"], "feature_names": data["feature_names"]},
                os.path.join(MODEL_DIR, "reference_data.joblib")
            )
            self.reference_data = {
                "X": data["X_train"],
                "y": data["y_train"],
                "feature_names": data["feature_names"],
            }
            logger.info("参考数据已创建")
        except Exception as e:
            logger.error(f"创建参考数据失败: {e}")
    
    def detect_drift(
        self,
        X_current: np.ndarray,
        y_current: np.ndarray = None,
        feature_names: list[str] = None,
    ) -> dict:
        """
        检测数据漂移
        
        Args:
            X_current: 当前数据
            y_current: 当前目标 (可选)
            feature_names: 特征名
            
        Returns:
            dict: 漂移检测结果
        """
        if self.reference_data is None:
            raise ValueError("参考数据未加载")
        
        X_ref = self.reference_data["X"]
        if feature_names is None:
            feature_names = self.reference_data.get("feature_names", [f"feature_{i}" for i in range(X_ref.shape[1])])
        
        logger.info(f"开始漂移检测: {X_ref.shape[0]} 参考样本 vs {X_current.shape[0]} 当前样本")
        
        drift_results = {
            "detected_at": datetime.now().isoformat(),
            "overall_status": "stable",
            "feature_drift": [],
            "target_drift": None,
            "recommendation": "no_action",
        }
        
        # 特征级漂移检测
        n_features = min(X_ref.shape[1], X_current.shape[1])
        drift_count = 0
        
        for i in range(n_features):
            feature_name = feature_names[i] if i < len(feature_names) else f"feature_{i}"
            
            ref_feature = X_ref[:, i]
            curr_feature = X_current[:, i]
            
            # PSI 计算
            psi = self._calculate_psi(ref_feature, curr_feature)
            
            # KS 检验
            ks_stat, ks_pvalue = stats.ks_2samp(ref_feature, curr_feature)
            
            # 判断漂移
            if psi >= self.psi_critical or ks_pvalue < self.ks_threshold:
                status = "critical"
                drift_count += 1
            elif psi >= self.psi_warning:
                status = "warning"
            else:
                status = "stable"
            
            drift_results["feature_drift"].append({
                "feature": feature_name,
                "psi": round(float(psi), 4),
                "ks_statistic": round(float(ks_stat), 4),
                "ks_pvalue": round(float(ks_pvalue), 4),
                "status": status,
            })
        
        # 目标变量漂移 (如果有)
        if y_current is not None and "y" in self.reference_data:
            y_ref = self.reference_data["y"]
            ks_stat, ks_pvalue = stats.ks_2samp(y_ref, y_current)
            
            drift_results["target_drift"] = {
                "ks_statistic": round(float(ks_stat), 4),
                "ks_pvalue": round(float(ks_pvalue), 4),
                "status": "critical" if ks_pvalue < self.ks_threshold else "stable",
            }
        
        # 整体判断
        if drift_count > n_features * 0.3:
            drift_results["overall_status"] = "critical"
            drift_results["recommendation"] = "retrain_immediately"
        elif drift_count > 0:
            drift_results["overall_status"] = "warning"
            drift_results["recommendation"] = "monitor_closely"
        else:
            drift_results["overall_status"] = "stable"
            drift_results["recommendation"] = "no_action"
        
        # 打印结果
        self._print_drift_report(drift_results)
        
        return drift_results
    
    def _calculate_psi(self, expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
        """
        计算 PSI (Population Stability Index)
        
        PSI < 0.1: 无显著变化
        0.1 <= PSI < 0.2: 轻微变化
        PSI >= 0.2: 显著变化
        """
        # 创建分箱
        breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
        breakpoints = np.unique(breakpoints)
        
        if len(breakpoints) < 3:
            return 0.0
        
        expected_counts, _ = np.histogram(expected, bins=breakpoints)
        actual_counts, _ = np.histogram(actual, bins=breakpoints)
        
        # 转换为比例
        expected_pct = expected_counts / len(expected)
        actual_pct = actual_counts / len(actual)
        
        # 避免除零
        expected_pct = np.where(expected_pct == 0, 1e-6, expected_pct)
        actual_pct = np.where(actual_pct == 0, 1e-6, actual_pct)
        
        # 计算 PSI
        psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
        
        return float(psi)
    
    def _print_drift_report(self, results: dict):
        """打印漂移检测报告"""
        logger.info("\n" + "=" * 70)
        logger.info("🔍 数据漂移检测报告")
        logger.info("=" * 70)
        logger.info(f"检测时间: {results['detected_at']}")
        logger.info(f"整体状态: {results['overall_status']}")
        logger.info(f"建议: {results['recommendation']}")
        
        # 特征漂移
        logger.info("\n特征级漂移:")
        for fd in results["feature_drift"]:
            status_icon = {"stable": "✅", "warning": "⚠️", "critical": "❌"}[fd["status"]]
            logger.info(
                f"  {status_icon} {fd['feature']:<25} "
                f"PSI={fd['psi']:.4f}  KS={fd['ks_statistic']:.4f} (p={fd['ks_pvalue']:.4f})"
            )
        
        # 目标漂移
        if results["target_drift"]:
            td = results["target_drift"]
            status_icon = {"stable": "✅", "critical": "❌"}.get(td["status"], "⚠️")
            logger.info(f"\n目标变量漂移: {status_icon} KS={td['ks_statistic']:.4f} (p={td['ks_pvalue']:.4f})")
        
        logger.info("=" * 70)
    
    def save_drift_report(self, results: dict):
        """保存漂移报告"""
        os.makedirs(MODEL_DIR, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(MODEL_DIR, f"drift_report_{timestamp}.json")
        
        with open(report_path, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"漂移报告已保存: {report_path}")
        
        return report_path


def check_drift_and_alert(config: dict = None) -> dict:
    """
    检查漂移并生成告警
    
    Returns:
        dict: 检测结果和告警信息
    """
    if config is None:
        config = load_config()
    
    detector = DriftDetector(config)
    
    # 生成模拟的当前数据 (实际应从生产环境获取)
    # 这里演示用随机扰动模拟漂移
    data = prepare_data(config)
    X_current = data["X_test"]
    
    # 添加一些噪声模拟漂移
    noise = np.random.normal(0, 0.1, X_current.shape)
    X_noisy = X_current + noise
    
    results = detector.detect_drift(
        X_current=X_noisy,
        feature_names=data["feature_names"]
    )
    
    # 保存报告
    detector.save_drift_report(results)
    
    # 判断是否需要告警
    if results["overall_status"] == "critical":
        logger.warning("🚨 检测到严重数据漂移！建议立即重训练模型")
        return {
            "alert": True,
            "severity": "critical",
            "message": "数据漂移严重，需要重训练",
            "results": results,
        }
    elif results["overall_status"] == "warning":
        logger.warning("⚠️ 检测到数据漂移，建议密切关注")
        return {
            "alert": True,
            "severity": "warning",
            "message": "数据漂移警告",
            "results": results,
        }
    else:
        logger.info("✅ 数据分布稳定")
        return {
            "alert": False,
            "severity": "none",
            "message": "数据稳定",
            "results": results,
        }


if __name__ == "__main__":
    result = check_drift_and_alert()
    print(f"\n检测结果: {result['severity']}")
    print(f"告警: {result['alert']}")
    print(f"消息: {result['message']}")
