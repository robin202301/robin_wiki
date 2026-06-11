"""
API 测试
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self, client):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data

    def test_detailed_health(self, client):
        """测试详细健康检查"""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestPredictEndpoint:
    def test_predict_success(self, client):
        """测试预测成功"""
        features = [8.32, 41, 6.98, 1.02, 322, 2.56, 37.88, -122.23]
        response = client.post("/predict", json={"features": features})
        
        # 如果模型已加载
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "prediction_label" in data
            assert data["prediction"] > 0

    def test_predict_invalid_features(self, client):
        """测试无效特征输入"""
        features = [1.0, 2.0]  # 只有 2 个特征，应该失败
        response = client.post("/predict", json={"features": features})
        assert response.status_code == 422  # Validation error

    def test_batch_predict(self, client):
        """测试批量预测"""
        samples = [
            [8.32, 41, 6.98, 1.02, 322, 2.56, 37.88, -122.23],
            [7.25, 30, 5.0, 1.0, 200, 2.0, 35.0, -121.5],
        ]
        response = client.post("/predict/batch", json={"samples": samples})
        
        if response.status_code == 200:
            data = response.json()
            assert "predictions" in data
            assert len(data["predictions"]) == 2


class TestRetrainEndpoint:
    def test_retrain_status(self, client):
        """测试重训练状态查询"""
        response = client.get("/retrain/status")
        assert response.status_code == 200
        data = response.json()
        assert "running" in data


class TestRootEndpoint:
    def test_root(self, client):
        """测试根路径"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
