"""
预测封装模块

功能:
- 加载生产模型
- 统一预测接口
- 输入验证和预处理
"""

import os
import time

import joblib
import numpy as np
from loguru import logger

from src.data.preprocess import feature_engineering

MODEL_DIR = "models"


class ModelPredictor:
    """模型预测器 - 封装模型加载和预测逻辑"""
    
    def __init__(self, model_name: str = None):
        """
        初始化预测器
        
        Args:
            model_name: 指定模型名，不指定则自动加载最佳模型
        """
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_name = model_name
        
        self._load_model()
    
    def _load_model(self):
        """加载模型和相关文件"""
        # 确定模型名
        if self.model_name is None:
            import json
            summary_path = os.path.join(MODEL_DIR, "training_summary.json")
            if os.path.exists(summary_path):
                with open(summary_path, "r") as f:
                    summary = json.load(f)
                self.model_name = summary.get("best_model", "lightgbm")
            else:
                self.model_name = "lightgbm"
        
        # 加载模型
        model_path = os.path.join(MODEL_DIR, f"{self.model_name}.joblib")
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"模型文件不存在: {model_path}\n"
                f"请先运行训练: python -m src.models.train"
            )
        
        self.model = joblib.load(model_path)
        logger.info(f"模型已加载: {self.model_name}")
        
        # 加载 scaler
        scaler_path = os.path.join(MODEL_DIR, "scaler.joblib")
        if os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)
        
        # 加载特征名
        features_path = os.path.join(MODEL_DIR, "feature_names.joblib")
        if os.path.exists(features_path):
            self.feature_names = joblib.load(features_path)
    
    def predict(self, features: list | np.ndarray) -> dict:
        """
        单条预测
        
        Args:
            features: 8个原始特征值
                [MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]
                
        Returns:
            dict: {prediction, model, latency_ms}
        """
        start = time.time()
        
        # 输入验证
        features = self._validate_input(features)
        
        # 转为 DataFrame 以进行特征工程
        import pandas as pd
        original_features = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", 
                           "Population", "AveOccup", "Latitude", "Longitude"]
        df = pd.DataFrame([features], columns=original_features)
        
        # 特征工程
        df = feature_engineering(df)
        
        # 确保列对齐
        if self.feature_names:
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0
            df = df[self.feature_names]
        
        # 标准化
        if self.scaler:
            X = self.scaler.transform(df)
        else:
            X = df.values
        
        # 预测
        prediction = float(self.model.predict(X)[0])
        
        latency = (time.time() - start) * 1000
        
        return {
            "prediction": round(prediction, 4),
            "prediction_label": f"${prediction * 100000:,.0f}",
            "model": self.model_name,
            "latency_ms": round(latency, 2),
        }
    
    def predict_batch(self, samples: list[list] | np.ndarray) -> dict:
        """
        批量预测
        
        Args:
            samples: 多条特征数据
            
        Returns:
            dict: {predictions, model, latency_ms, count}
        """
        start = time.time()
        
        import pandas as pd
        original_features = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", 
                           "Population", "AveOccup", "Latitude", "Longitude"]
        
        # 转为 DataFrame
        samples = np.array(samples)
        if samples.shape[1] != 8:
            raise ValueError(f"需要 8 个特征, 收到 {samples.shape[1]} 个")
        
        df = pd.DataFrame(samples, columns=original_features)
        
        # 特征工程
        df = feature_engineering(df)
        
        # 确保列对齐
        if self.feature_names:
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0
            df = df[self.feature_names]
        
        # 标准化
        if self.scaler:
            X = self.scaler.transform(df)
        else:
            X = df.values
        
        # 预测
        predictions = self.model.predict(X).tolist()
        
        latency = (time.time() - start) * 1000
        
        return {
            "predictions": [round(p, 4) for p in predictions],
            "prediction_labels": [f"${p * 100000:,.0f}" for p in predictions],
            "model": self.model_name,
            "latency_ms": round(latency, 2),
            "count": len(predictions),
        }
    
    def _validate_input(self, features: list | np.ndarray) -> np.ndarray:
        """验证输入特征"""
        features = np.array(features, dtype=float)
        if features.shape != (8,):
            raise ValueError(
                f"需要 8 个特征 [MedInc, HouseAge, AveRooms, AveBedrms, "
                f"Population, AveOccup, Latitude, Longitude], 收到 {features.shape}"
            )
        return features
    
    def reload(self, model_name: str = None):
        """热重载模型"""
        self.model_name = model_name
        self._load_model()
        logger.info("模型已热重载")


# 全局单例
_predictor: ModelPredictor = None


def get_predictor() -> ModelPredictor:
    """获取全局预测器实例"""
    global _predictor
    if _predictor is None:
        _predictor = ModelPredictor()
    return _predictor


def reload_predictor(model_name: str = None):
    """重载全局预测器"""
    global _predictor
    _predictor = ModelPredictor(model_name)
    return _predictor
