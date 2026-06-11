"""
数据漂移检测测试
"""

import pytest
import numpy as np
from src.monitoring.drift_detector import DriftDetector


class TestDriftDetector:
    @pytest.fixture
    def detector(self):
        """创建检测器"""
        return DriftDetector()

    def test_psi_calculation(self, detector):
        """测试 PSI 计算"""
        expected = np.random.normal(0, 1, 1000)
        actual = np.random.normal(0, 1, 1000)
        
        psi = detector._calculate_psi(expected, actual)
        assert psi >= 0, "PSI 应为非负"
        assert psi < 0.5, "PSI 不应过大"

    def test_detect_drift_stable(self, detector):
        """测试稳定数据无漂移"""
        X_ref = np.random.normal(0, 1, (100, 5))
        X_curr = np.random.normal(0, 1, (100, 5))
        
        # 模拟参考数据
        detector.reference_data = {
            "X": X_ref,
            "feature_names": [f"feature_{i}" for i in range(5)],
        }
        
        results = detector.detect_drift(X_curr)
        assert results["overall_status"] in ["stable", "warning"]

    def test_detect_drift_significant(self, detector):
        """测试显著漂移"""
        X_ref = np.random.normal(0, 1, (100, 5))
        X_curr = np.random.normal(5, 1, (100, 5))  # 均值偏移
        
        detector.reference_data = {
            "X": X_ref,
            "feature_names": [f"feature_{i}" for i in range(5)],
        }
        
        results = detector.detect_drift(X_curr)
        assert results["overall_status"] == "critical"
