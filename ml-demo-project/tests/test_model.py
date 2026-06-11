"""
模型训练测试
"""

import pytest
import numpy as np
from src.data.preprocess import prepare_data
from src.models.train import train_model, _calculate_metrics


class TestModelTraining:
    @pytest.fixture
    def sample_data(self):
        """准备测试数据"""
        data = prepare_data()
        return {
            "X_train": data["X_train"][:100],  # 使用小样本加速测试
            "y_train": data["y_train"][:100],
            "X_test": data["X_test"][:50],
            "y_test": data["y_test"][:50],
        }

    def test_train_random_forest(self, sample_data):
        """测试随机森林训练"""
        result = train_model(
            model_name="test_rf",
            model_type="RandomForestRegressor",
            params={"n_estimators": 10, "random_state": 42, "n_jobs": -1},
            X_train=sample_data["X_train"],
            y_train=sample_data["y_train"],
            X_test=sample_data["X_test"],
            y_test=sample_data["y_test"],
            config=None,
        )
        assert result["model"] is not None
        assert "metrics" in result
        assert "rmse" in result["metrics"]

    def test_train_lightgbm(self, sample_data):
        """测试 LightGBM 训练"""
        result = train_model(
            model_name="test_lgbm",
            model_type="LGBMRegressor",
            params={"n_estimators": 10, "verbose": -1},
            X_train=sample_data["X_train"],
            y_train=sample_data["y_train"],
            X_test=sample_data["X_test"],
            y_test=sample_data["y_test"],
            config=None,
        )
        assert result["model"] is not None
        assert result["metrics"]["r2"] > 0, "R² 应为正"


class TestMetrics:
    def test_calculate_metrics(self):
        """测试指标计算"""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 2.2, 2.9, 4.1, 4.8])
        
        metrics = _calculate_metrics(y_true, y_pred)
        
        assert "mae" in metrics
        assert "rmse" in metrics
        assert "r2" in metrics
        assert 0 < metrics["r2"] <= 1.0, "R² 应在 (0, 1]"

    def test_perfect_prediction(self):
        """测试完美预测"""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        
        metrics = _calculate_metrics(y_true, y_pred)
        
        assert metrics["mae"] == 0.0
        assert metrics["rmse"] == 0.0
        assert metrics["r2"] == 1.0
