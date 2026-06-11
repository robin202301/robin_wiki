"""
数据加载与预处理模块

功能:
- 加载 California Housing 数据集
- 特征工程 (交互特征、多项式特征)
- 数据标准化
- 数据集划分
"""

import numpy as np
import pandas as pd
import yaml
from loguru import logger
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_config(config_path: str = "config/config.yaml") -> dict:
    """加载配置文件"""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    """
    加载 California Housing 数据集
    
    Returns:
        X: 特征 DataFrame
        y: 目标 Series
    """
    logger.info("加载 California Housing 数据集...")
    data = fetch_california_housing(as_frame=True)
    X = data.data
    y = data.target
    
    logger.info(f"数据加载完成: {X.shape[0]} 样本, {X.shape[1]} 特征")
    return X, y


def feature_engineering(X: pd.DataFrame) -> pd.DataFrame:
    """
    特征工程: 创建新特征
    
    Args:
        X: 原始特征 DataFrame
        
    Returns:
        增强后的特征 DataFrame
    """
    logger.info("执行特征工程...")
    X_new = X.copy()
    
    # 1. 交互特征: 收入 × 房间数
    X_new["income_rooms"] = X["MedInc"] * X["AveRooms"]
    
    # 2. 卧室比例
    X_new["bedroom_ratio"] = X["AveBedrms"] / (X["AveRooms"] + 1e-8)
    
    # 3. 人口密度
    X_new["pop_per_room"] = X["Population"] / (X["AveRooms"] + 1e-8)
    
    # 4. 位置特征 (距离洛杉矶的近似距离)
    # 洛杉矶大致坐标: 34.05, -118.25
    X_new["dist_la"] = np.sqrt(
        (X["Latitude"] - 34.05) ** 2 + (X["Longitude"] + 118.25) ** 2
    )
    
    # 5. 位置特征 (距离旧金山的近似距离)
    # 旧金山大致坐标: 37.77, -122.42
    X_new["dist_sf"] = np.sqrt(
        (X["Latitude"] - 37.77) ** 2 + (X["Longitude"] + 122.42) ** 2
    )
    
    # 6. 收入分箱
    X_new["income_category"] = pd.cut(
        X["MedInc"],
        bins=[0, 2, 4, 6, 8, float("inf")],
        labels=["very_low", "low", "medium", "high", "very_high"]
    )
    X_new = pd.get_dummies(X_new, columns=["income_category"], drop_first=True)
    
    logger.info(f"特征工程完成: {X.shape[1]} → {X_new.shape[1]} 特征")
    return X_new


def prepare_data(
    config: dict = None,
    test_size: float = None,
    random_state: int = None,
) -> dict:
    """
    完整的数据准备流程
    
    Args:
        config: 配置字典
        test_size: 测试集比例
        random_state: 随机种子
        
    Returns:
        dict with keys: X_train, X_test, y_train, y_test, scaler, feature_names
    """
    if config is None:
        config = load_config()
    
    data_config = config.get("data", {})
    test_size = test_size or data_config.get("test_size", 0.2)
    random_state = random_state or data_config.get("random_state", 42)
    
    # 加载数据
    X, y = load_data()
    
    # 特征工程
    X = feature_engineering(X)
    
    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=True
    )
    
    # 标准化 (只 fit 训练集)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    feature_names = list(X.columns)
    
    logger.info(f"训练集: {X_train_scaled.shape}, 测试集: {X_test_scaled.shape}")
    logger.info(f"特征列表: {feature_names}")
    
    return {
        "X_train": X_train_scaled,
        "X_test": X_test_scaled,
        "y_train": y_train.values,
        "y_test": y_test.values,
        "scaler": scaler,
        "feature_names": feature_names,
        "X_train_raw": X_train,
        "X_test_raw": X_test,
    }


if __name__ == "__main__":
    data = prepare_data()
    print(f"\n数据集信息:")
    print(f"  训练集: {data['X_train'].shape}")
    print(f"  测试集: {data['X_test'].shape}")
    print(f"  特征: {data['feature_names']}")
    print(f"  目标值范围: [{data['y_train'].min():.2f}, {data['y_train'].max():.2f}]")
