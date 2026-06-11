"""
数据处理测试
"""

import pytest
import numpy as np
from src.data.preprocess import load_data, feature_engineering, prepare_data


class TestDataLoading:
    def test_load_data_returns_dataframe(self):
        """测试数据加载返回正确格式"""
        X, y = load_data()
        assert X.shape[0] > 0, "数据不应为空"
        assert X.shape[1] == 8, "应有 8 个特征"
        assert len(y) == X.shape[0], "目标变量长度应匹配"

    def test_load_data_no_missing_values(self):
        """测试数据无缺失值"""
        X, y = load_data()
        assert X.isnull().sum().sum() == 0, "特征不应有缺失值"
        assert y.isnull().sum() == 0, "目标变量不应有缺失值"


class TestFeatureEngineering:
    def test_feature_engineering_adds_columns(self):
        """测试特征工程增加新特征"""
        X, _ = load_data()
        X_new = feature_engineering(X)
        assert X_new.shape[1] > X.shape[1], "特征数应增加"

    def test_feature_engineering_no_errors(self):
        """测试特征工程无运行时错误"""
        X, _ = load_data()
        try:
            X_new = feature_engineering(X)
            assert True
        except Exception as e:
            pytest.fail(f"特征工程失败: {e}")


class TestDataPreparation:
    def test_prepare_data_returns_correct_keys(self):
        """测试数据准备返回正确键"""
        data = prepare_data()
        required_keys = ["X_train", "X_test", "y_train", "y_test", "scaler", "feature_names"]
        for key in required_keys:
            assert key in data, f"缺少键: {key}"

    def test_prepare_data_split_ratio(self):
        """测试数据划分比例"""
        data = prepare_data(test_size=0.2)
        total = len(data["y_train"]) + len(data["y_test"])
        test_ratio = len(data["y_test"]) / total
        assert 0.15 <= test_ratio <= 0.25, f"测试集比例应为 0.2，实际为 {test_ratio}"

    def test_prepare_data_scaled(self):
        """测试数据已标准化"""
        data = prepare_data()
        # 标准化后均值应接近 0
        mean = np.mean(data["X_train"], axis=0)
        assert np.allclose(mean, 0, atol=0.1), "训练数据应近似零均值"
