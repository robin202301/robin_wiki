# MLOps 详尽知识库

> **最后更新：2026-06-10**

---

## 目录

1. [MLOps 概述](#1-mlops-概述)
2. [核心原则](#2-核心原则)
3. [ML 生命周期](#3-ml-生命周期)
4. [特征工程](#4-特征工程)
5. [实验跟踪（MLflow / Weights & Biases）](#5-实验跟踪)
6. [模型注册与管理](#6-模型注册与管理)
7. [模型训练与调优](#7-模型训练与调优)
8. [模型评估](#8-模型评估)
9. [模型部署](#9-模型部署)
10. [模型监控与漂移检测](#10-模型监控与漂移检测)
11. [CI/CD for ML](#11-cicd-for-ml)
12. [数据版本控制（DVC）](#12-数据版本控制dvc)
13. [特征存储（Feature Store）](#13-特征存储feature-store)
14. [AutoML](#14-automl)
15. [ML 平台](#15-ml-平台)
16. [最佳实践](#16-最佳实践)
17. [完整代码示例](#17-完整代码示例)
18. [参考资料与推荐阅读](#18-参考资料与推荐阅读)

---

## 1. MLOps 概述

### 1.1 什么是 MLOps

MLOps（Machine Learning Operations）是将 DevOps 的理念和实践应用于机器学习系统的工程学科。它涵盖从数据准备、模型训练、模型评估到模型部署和持续监控的完整生命周期，旨在实现 ML 系统的自动化、可复现性和可靠交付。

### 1.2 为什么需要 MLOps

| 挑战 | 传统软件 | ML 系统 |
|------|-----------|---------|
| 代码变更 | 代码逻辑变化 | 代码 + 数据 + 模型参数 |
| 测试 | 单元测试 + 集成测试 | + 模型评估 + 数据质量 |
| 部署 | 二进制/容器 | 模型 + 特征管道 + 推理服务 |
| 监控 | 性能/可用性 | + 数据漂移 + 模型退化 |
| 回滚 | 代码版本 | 模型版本 + 数据版本 |

### 1.3 MLOps 成熟度模型

```
Level 0: 手动流程 — 训练、部署、监控全手动
Level 1: ML 实验自动化 — 自动训练管道、实验跟踪
Level 2: ML 管道自动化 — CI/CD for ML、自动触发训练/部署
```

### 1.4 MLOps 技术栈概览

```
┌─────────────────────────────────────────────────────┐
│                    应用层 / 消费端                      │
├─────────────────────────────────────────────────────┤
│  模型服务  │  监控  │  A/B 测试  │  告警               │
├─────────────────────────────────────────────────────┤
│  部署层: Docker / Kubernetes / SageMaker / Vertex AI  │
├─────────────────────────────────────────────────────┤
│  编排层: Airflow / Kubeflow / Argo Workflows         │
├─────────────────────────────────────────────────────┤
│  实验跟踪: MLflow / W&B / Neptune / ClearML          │
├─────────────────────────────────────────────────────┤
│  数据层: DVC / Feature Store / Data Lake              │
├─────────────────────────────────────────────────────┤
│  基础设施: Cloud / On-Prem / Hybrid                   │
└─────────────────────────────────────────────────────┘
```

### 1.5 MLOps 与传统 DevOps 的区别

```python
# 传统 DevOps 的 CI/CD 只关注代码
# MLOps 的 CI/CD/CT (Continuous Training) 需要关注三个维度:

class MLOpsDimensions:
    """MLOps 的三个持续维度"""

    # 持续集成 (CI)
    CI = {
        "代码测试": "单元测试 + 集成测试",
        "数据验证": "Schema 检查 + 质量检查 + 分布检查",
        "模型验证": "评估指标 + 公平性 + 鲁棒性",
    }

    # 持续交付 (CD)
    CD = {
        "模型部署": "容器化 + 编排 + 推理服务",
        "管道部署": "训练管道 + 特征管道 + 预处理",
        "基础设施": "IaC + 配置管理 + 资源监控",
    }

    # 持续训练 (CT)
    CT = {
        "自动重训练": "数据漂移触发 + 定时触发 + 性能触发",
        "实验管理": "超参搜索 + 模型对比 + 可复现性",
        "模型注册": "版本管理 + 阶段管理 + 审批流",
    }
```

---

## 2. 核心原则

### 2.1 可复现性 (Reproducibility)

确保在任何时间、任何环境都能重现相同的模型结果。

```python
import random
import numpy as np
import torch

def set_seed(seed: int = 42):
    """设置全局随机种子以确保可复现性"""
    random.seed(seed)
    np.random.seed(seed)
    # Python hash seed
    import os
    os.environ["PYTHONHASHSEED"] = str(seed)
    # PyTorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # TensorFlow
    import tensorflow as tf
    tf.random.set_seed(seed)

# 环境锁定
"""
# requirements.txt 或 Pipfile.lock
scikit-learn==1.4.0
torch==2.2.0
transformers==4.38.0
numpy==1.26.4
pandas==2.2.0
mlflow==2.10.0
"""
```

### 2.2 自动化 (Automation)

```yaml
# .github/workflows/ml-pipeline.yml
# 自动化 ML 管道的 CI/CD 示例
name: ML Pipeline CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * 0'  # 每周日凌晨2点自动重训练

env:
  PYTHON_VERSION: '3.11'
  MODEL_REGISTRY: ghcr.io/${{ github.repository }}

jobs:
  validate-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Data Schema
        run: |
          pip install great_expectations
          python scripts/validate_data.py --config config/data_validation.yaml

  train-model:
    needs: validate-data
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Train Model
        run: |
          python src/train.py --config config/train_config.yaml
      - name: Evaluate Model
        run: |
          python src/evaluate.py --model-path models/latest
      - name: Register Model
        run: |
          python src/register_model.py --model-path models/latest

  deploy-staging:
    needs: train-model
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        run: |
          kubectl apply -f k8s/staging/
          kubectl rollout status deployment/ml-model -n staging

  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Production
        run: |
          kubectl apply -f k8s/production/
```

### 2.3 可复现性与版本控制

```python
"""
完整的版本控制策略
"""
from dataclasses import dataclass
from typing import Dict, Optional
import hashlib
import json

@dataclass
class MLVersion:
    """ML 项目的版本管理"""
    code_version: str          # Git commit SHA
    data_version: str          # DVC commit / 数据哈希
    config_version: str        # 配置哈希
    model_version: str         # 模型注册表版本号
    environment: Dict          # 依赖锁定信息
    seed: int                  # 随机种子

    def to_hash(self) -> str:
        """生成唯一版本指纹"""
        fingerprint = f"{self.code_version}:{self.data_version}:{self.config_version}:{self.seed}"
        return hashlib.sha256(fingerprint.encode()).hexdigest()[:12]

    def to_json(self) -> str:
        return json.dumps({
            "code": self.code_version,
            "data": self.data_version,
            "config": self.config_version,
            "model": self.model_version,
            "seed": self.seed,
            "fingerprint": self.to_hash()
        }, indent=2)


# 使用示例
version = MLVersion(
    code_version="abc1234",
    data_version="dvc_sha256:xyz789",
    config_version="config_v2.1",
    model_version="3.1.0",
    environment={"python": "3.11.7", "torch": "2.2.0"},
    seed=42
)
print(version.to_json())
```

### 2.4 可观测性 (Observability)

```python
import logging
import structlog

def setup_structured_logging():
    """配置结构化日志用于 ML 系统"""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()

# 结构化日志输出
logger.info(
    "model_prediction",
    model_name="fraud_detector",
    model_version="2.1.0",
    prediction_latency_ms=15.3,
    input_features_hash="a1b2c3",
    batch_size=32
)
# 输出: {"event": "model_prediction", "model_name": "fraud_detector", 
#         "model_version": "2.1.0", "prediction_latency_ms": 15.3, ...}
```

---

## 3. ML 生命周期

### 3.1 完整生命周期阶段

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 问题定义  │───▶│ 数据收集  │───▶│ 数据预处理│───▶│ 特征工程  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                       │
┌──────────┐    ┌──────────┐    ┌──────────┐          ▼
│ 监控维护  │◀───│ 模型部署  │◀───│ 模型评估  │◀─── ┌──────────┐
└──────────┘    └──────────┘    └──────────┘     │ 模型训练  │
      │                                           └──────────┘
      │                                                 ▲
      ▼                                                 │
┌──────────┐    ┌──────────┐                           │
│ 模型退役  │◀───│ 漂移检测  │───────────────────────────┘
└──────────┘    └──────────┘
```

### 3.2 各阶段详细说明

```python
"""
ML 生命周期管理框架
"""
from enum import Enum
from typing import List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

class LifecycleStage(Enum):
    PROBLEM_DEFINITION = "problem_definition"
    DATA_COLLECTION = "data_collection"
    DATA_PREPROCESSING = "data_preprocessing"
    FEATURE_ENGINEERING = "feature_engineering"
    MODEL_TRAINING = "model_training"
    MODEL_EVALUATION = "model_evaluation"
    MODEL_DEPLOYMENT = "model_deployment"
    MONITORING = "monitoring"
    RETIREMENT = "retirement"

class ModelStage(Enum):
    """模型注册阶段"""
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"

@dataclass
class PipelineStage:
    """管道阶段定义"""
    name: str
    stage: LifecycleStage
    handler: Callable
    retries: int = 3
    timeout_seconds: int = 3600
    depends_on: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)

class MLPipelineManager:
    """ML 管道管理器"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.stages: List[PipelineStage] = []
        self.stage_results = {}

    def add_stage(self, stage: PipelineStage):
        self.stages.append(stage)

    def run(self, context: dict) -> dict:
        """执行管道"""
        for stage in self.stages:
            # 检查依赖
            for dep in stage.depends_on:
                if dep not in self.stage_results:
                    raise RuntimeError(f"依赖 {dep} 未完成")

            # 执行阶段
            try:
                result = stage.handler(context)
                self.stage_results[stage.name] = result
                context[f"{stage.name}_result"] = result
            except Exception as e:
                # 重试逻辑
                for attempt in range(stage.retries):
                    try:
                        result = stage.handler(context)
                        self.stage_results[stage.name] = result
                        break
                    except Exception:
                        if attempt == stage.retries - 1:
                            raise
        return self.stage_results
```

### 3.3 使用 Kubeflow Pipelines 编排

```python
# kubeflow_pipeline.py
from kfp import dsl, compiler
from kfp.dsl import Dataset, Model, HTML, Metrics

@dsl.component(base_image="python:3.11-slim")
def preprocess_data(input_data: Dataset, output_data: Dataset):
    """数据预处理组件"""
    import pandas as pd
    
    df = pd.read_csv(input_data.path)
    
    # 清洗数据
    df = df.dropna(subset=["target"])
    df = df.fillna(df.median(numeric_only=True))
    
    # 特征编码
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        df[col] = df[col].astype("category").cat.codes
    
    df.to_csv(output_data.path, index=False)

@dsl.component(base_image="python:3.11-slim", packages_to_install=["scikit-learn", "mlflow"])
def train_model(training_data: Dataset, output_model: Model, metrics: Metrics):
    """模型训练组件"""
    import pandas as pd
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, f1_score
    import mlflow
    
    df = pd.read_csv(training_data.path)
    X = df.drop("target", axis=1)
    y = df["target"]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingClassifier(n_estimators=200, max_depth=5, learning_rate=0.1)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred)
    
    # 记录指标
    metrics.log_metric("accuracy", accuracy)
    metrics.log_metric("f1_score", f1)
    
    # 保存模型
    import joblib
    joblib.dump(model, output_model.path)

@dsl.component
def evaluate_model(model: Model, test_data: Dataset, metrics_html: HTML):
    """模型评估组件"""
    import pandas as pd
    import joblib
    from sklearn.metrics import classification_report
    
    df = pd.read_csv(test_data.path)
    X = df.drop("target", axis=1)
    y = df["target"]
    
    model_obj = joblib.load(model.path)
    y_pred = model_obj.predict(X)
    report = classification_report(y, y_pred, output_dict=True)
    
    # 生成 HTML 报告
    html = f"<h2>Classification Report</h2><pre>{classification_report(y, y_pred)}</pre>"
    with open(metrics_html.path, "w") as f:
        f.write(html)

@dsl.pipeline(name="ml-training-pipeline", description="End-to-end ML Pipeline")
def ml_pipeline(data_path: str = "gs://bucket/data.csv"):
    """完整的 ML 管道"""
    preprocess_task = preprocess_data(
        input_data=Dataset.from_uri(data_path)
    )
    
    train_task = train_model(
        training_data=preprocess_task.outputs["output_data"]
    )
    
    evaluate_task = evaluate_model(
        model=train_task.outputs["output_model"],
        test_data=preprocess_task.outputs["output_data"]
    )


# 编译管道
if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path="ml_pipeline.yaml"
    )
```

---

## 4. 特征工程

### 4.1 特征工程概述

特征工程是 ML 管道中最关键也最耗时的环节，直接影响模型性能。

### 4.2 特征处理管道

```python
"""
完整的特征工程管道
"""
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import SelectKBest, mutual_info_classif, RFE
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

# ============= 自定义 Transformer =============

class DateTimeFeatureExtractor(BaseEstimator, TransformerMixin):
    """从日期时间列提取特征"""
    
    def __init__(self, datetime_cols=None):
        self.datetime_cols = datetime_cols or []
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        for col in self.datetime_cols:
            dt = pd.to_datetime(X[col])
            X[f"{col}_year"] = dt.dt.year
            X[f"{col}_month"] = dt.dt.month
            X[f"{col}_day"] = dt.dt.day
            X[f"{col}_hour"] = dt.dt.hour
            X[f"{col}_dayofweek"] = dt.dt.dayofweek
            X[f"{col}_is_weekend"] = dt.dt.dayofweek >= 5
            X[f"{col}_quarter"] = dt.dt.quarter
            # 周期性编码
            X[f"{col}_month_sin"] = np.sin(2 * np.pi * dt.dt.month / 12)
            X[f"{col}_month_cos"] = np.cos(2 * np.pi * dt.dt.month / 12)
            X[f"{col}_hour_sin"] = np.sin(2 * np.pi * dt.dt.hour / 24)
            X[f"{col}_hour_cos"] = np.cos(2 * np.pi * dt.dt.hour / 24)
        return X.drop(columns=self.datetime_cols)


class OutlierClipper(BaseEstimator, TransformerMixin):
    """基于 IQR 的异常值裁剪"""
    
    def __init__(self, cols=None, factor=1.5):
        self.cols = cols
        self.factor = factor
        self.lower_bounds_ = {}
        self.upper_bounds_ = {}
    
    def fit(self, X, y=None):
        cols = self.cols or X.select_dtypes(include=[np.number]).columns
        for col in cols:
            Q1 = X[col].quantile(0.25)
            Q3 = X[col].quantile(0.75)
            IQR = Q3 - Q1
            self.lower_bounds_[col] = Q1 - self.factor * IQR
            self.upper_bounds_[col] = Q3 + self.factor * IQR
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        for col in self.lower_bounds_:
            X[col] = X[col].clip(self.lower_bounds_[col], self.upper_bounds_[col])
        return X


class TargetEncoder(BaseEstimator, TransformerMixin):
    """目标编码（带交叉验证防止泄漏）"""
    
    def __init__(self, cols=None, smoothing=10):
        self.cols = cols
        self.smoothing = smoothing
        self.encodings_ = {}
        self.global_mean_ = None
    
    def fit(self, X, y=None):
        self.global_mean_ = y.mean()
        cols = self.cols or X.select_dtypes(include=["object", "category"]).columns
        for col in cols:
            stats = X.groupby(col).agg({col: "count"})
            stats.columns = ["count"]
            stats["mean"] = X.groupby(col).apply(lambda g: y.loc[g.index].mean())
            # 平滑
            stats["smoothed"] = (
                (stats["count"] * stats["mean"] + self.smoothing * self.global_mean_)
                / (stats["count"] + self.smoothing)
            )
            self.encodings_[col] = stats["smoothed"].to_dict()
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        for col, encoding in self.encodings_.items():
            X[f"{col}_target_enc"] = X[col].map(encoding).fillna(self.global_mean_)
        return X


class FeatureInteractionGenerator(BaseEstimator, TransformerMixin):
    """特征交互生成器"""
    
    def __init__(self, cols=None, interactions="auto"):
        """
        interactions: 'auto' (全部组合), 'multiply', 'divide', 'diff'
        """
        self.cols = cols
        self.interactions = interactions
    
    def fit(self, X, y=None):
        self.feature_cols_ = self.cols or X.select_dtypes(include=[np.number]).columns.tolist()
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        for i, col1 in enumerate(self.feature_cols_):
            for col2 in self.feature_cols_[i+1:]:
                if self.interactions in ("auto", "multiply"):
                    X[f"{col1}_x_{col2}"] = X[col1] * X[col2]
                if self.interactions in ("auto", "divide"):
                    X[f"{col1}_div_{col2}"] = X[col1] / (X[col2] + 1e-8)
                if self.interactions in ("auto", "diff"):
                    X[f"{col1}_minus_{col2}"] = X[col1] - X[col2]
        return X
```

### 4.3 特征选择策略

```python
"""
多种特征选择方法
"""
import pandas as pd
import numpy as np
from sklearn.feature_selection import (
    SelectKBest, f_classif, mutual_info_classif,
    RFE, RFECV, SelectFromModel, SequentialFeatureSelector
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LassoCV
from sklearn.model_selection import cross_val_score

def comprehensive_feature_selection(X, y, method="all"):
    """综合特征选择"""
    results = {}
    
    # 1. 统计检验
    selector_stat = SelectKBest(score_func=f_classif, k=10)
    selector_stat.fit(X, y)
    results["f_classif"] = pd.DataFrame({
        "feature": X.columns,
        "score": selector_stat.scores_,
        "p_value": selector_stat.pvalues_
    }).sort_values("score", ascending=False)
    
    # 2. 互信息
    mi_scores = mutual_info_classif(X, y, random_state=42)
    results["mutual_info"] = pd.DataFrame({
        "feature": X.columns,
        "mi_score": mi_scores
    }).sort_values("mi_score", ascending=False)
    
    # 3. 基于模型的特征重要性
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    results["rf_importance"] = pd.DataFrame({
        "feature": X.columns,
        "importance": rf.feature_importances_
    }).sort_values("importance", ascending=False)
    
    # 4. L1 正则化 (Lasso)
    lasso = LassoCV(cv=5, random_state=42)
    lasso.fit(X, y)
    results["lasso"] = pd.DataFrame({
        "feature": X.columns,
        "coefficient": lasso.coef_
    }).sort_values("coefficient", ascending=False, key=abs)
    
    # 5. RFE (递归特征消除)
    rfe = RFECV(rf, step=1, cv=5, scoring="accuracy", n_jobs=-1)
    rfe.fit(X, y)
    results["rfe_selected"] = X.columns[rfe.support_].tolist()
    
    # 6. 逐步选择
    sfs = SequentialFeatureSelector(rf, n_features_to_select=10, cv=5, n_jobs=-1)
    sfs.fit(X, y)
    results["sfs_selected"] = X.columns[sfs.get_support()].tolist()
    
    return results


# 特征选择结果可视化
def plot_feature_selection_results(results, top_k=20):
    """可视化特征选择结果"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # F-test
    ax = axes[0, 0]
    sns.barplot(data=results["f_classif"].head(top_k), x="score", y="feature", ax=ax)
    ax.set_title("F-test (ANOVA)")
    
    # Mutual Information
    ax = axes[0, 1]
    sns.barplot(data=results["mutual_info"].head(top_k), x="mi_score", y="feature", ax=ax)
    ax.set_title("Mutual Information")
    
    # RF Importance
    ax = axes[0, 2]
    sns.barplot(data=results["rf_importance"].head(top_k), x="importance", y="feature", ax=ax)
    ax.set_title("Random Forest Importance")
    
    plt.tight_layout()
    plt.savefig("feature_selection_results.png", dpi=150, bbox_inches="tight")
```

### 4.4 文本特征工程

```python
"""
文本特征工程示例
"""
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
import re

class TextFeaturePipeline:
    """文本特征处理管道"""
    
    def __init__(self):
        self.tfidf = TfidfVectorizer(
            max_features=5000,
            min_df=5,
            max_df=0.95,
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english"
        )
        self.lda = LatentDirichletAllocation(n_components=10, random_state=42)
    
    @staticmethod
    def clean_text(text: str) -> str:
        """文本清洗"""
        # 转小写
        text = text.lower()
        # 去除 HTML 标签
        text = re.sub(r'<[^>]+>', '', text)
        # 去除特殊字符
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # 去除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def fit_transform(self, texts):
        """拟合并转换文本"""
        cleaned = [self.clean_text(t) for t in texts]
        tfidf_matrix = self.tfidf.fit_transform(cleaned)
        topics = self.lda.fit_transform(tfidf_matrix)
        return tfidf_matrix, topics
    
    def get_top_topics(self, feature_names=None, n_words=10):
        """获取每个主题的前N个词"""
        if feature_names is None:
            feature_names = self.tfidf.get_feature_names_out()
        
        for idx, topic in enumerate(self.lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-n_words - 1:-1]]
            print(f"Topic {idx}: {', '.join(top_words)}")
```

---

## 5. 实验跟踪

### 5.1 MLflow 实验跟踪

```python
"""
MLflow 完整使用示例
"""
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
import pandas as pd
import numpy as np

# ============= 基础设置 =============
mlflow.set_tracking_uri("http://localhost:5000")  # 或使用 databricks
mlflow.set_experiment("fraud-detection-experiment")


def train_with_mlflow(X_train, y_train, X_val, y_val, params: dict):
    """带 MLflow 跟踪的模型训练"""
    
    with mlflow.start_run(run_name=f"rf_{params.get('n_estimators', 100)}"):
        # 记录参数
        mlflow.log_params(params)
        
        # 记录数据集信息
        mlflow.log_input(
            mlflow.data.from_pandas(
                pd.DataFrame(X_train),
                targets=pd.Series(y_train),
                name="training_data"
            )
        )
        
        # 训练模型
        model = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        
        # 评估
        train_score = model.score(X_train, y_train)
        val_score = model.score(X_val, y_val)
        cross_val_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        # 记录指标
        mlflow.log_metric("train_accuracy", train_score)
        mlflow.log_metric("val_accuracy", val_score)
        mlflow.log_metric("cv_mean", cross_val_scores.mean())
        mlflow.log_metric("cv_std", cross_val_scores.std())
        
        # 记录模型
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="fraud_detector_rf",
            signature=mlflow.models.infer_signature(X_train, model.predict(X_train))
        )
        
        # 记录特征重要性图
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 6))
        importances = pd.Series(
            model.feature_importances_,
            index=X_train.columns if hasattr(X_train, 'columns') else range(len(model.feature_importances_))
        ).nlargest(20)
        importances.plot(kind="barh", ax=ax)
        ax.set_title("Top 20 Feature Importances")
        mlflow.log_figure(fig, "feature_importances.png")
        
        return model, val_score


# ============= 超参搜索 =============
def hyperparam_search_with_mlflow(X_train, y_train):
    """使用 MLflow 进行超参搜索跟踪"""
    
    param_grid = {
        "n_estimators": [100, 200, 500],
        "max_depth": [5, 10, 15, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    }
    
    with mlflow.start_run(run_name="grid_search"):
        rf = RandomForestClassifier(random_state=42)
        grid = GridSearchCV(
            rf, param_grid, cv=5, scoring="accuracy", 
            n_jobs=-1, return_train_score=True
        )
        
        mlflow.log_params({f"search_{k}": str(v) for k, v in param_grid.items()})
        
        grid.fit(X_train, y_train)
        
        # 记录最佳结果
        mlflow.log_params(grid.best_params_)
        mlflow.log_metric("best_cv_score", grid.best_score_)
        
        # 记录所有参数组合结果
        results_df = pd.DataFrame(grid.cv_results_)
        results_df.to_csv("grid_search_results.csv", index=False)
        mlflow.log_artifact("grid_search_results.csv")
        
        return grid.best_estimator_


# ============= 模型对比 =============
def compare_models(experiment_name: str):
    """对比同一实验中的所有运行"""
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.val_accuracy DESC"],
        max_results=10
    )
    
    comparison = []
    for run in runs:
        comparison.append({
            "run_id": run.info.run_id[:8],
            "run_name": run.info.run_name,
            "val_accuracy": run.data.metrics.get("val_accuracy"),
            "cv_mean": run.data.metrics.get("cv_mean"),
            "params": run.data.params,
            "status": run.info.status,
            "created": run.info.start_time,
        })
    
    return pd.DataFrame(comparison)


# ============= 模型注册与阶段管理 =============
def promote_model(model_name: str, current_stage: str, new_stage: str):
    """提升模型阶段: Staging -> Production"""
    client = MlflowClient()
    
    # 获取当前阶段的最佳版本
    versions = client.get_latest_versions(model_name, stages=[current_stage])
    if not versions:
        raise ValueError(f"没有 {current_stage} 阶段的模型版本")
    
    latest_version = versions[0].version
    
    # 验证新版本是否优于当前生产版本
    if new_stage == "Production":
        current_prod = client.get_latest_versions(model_name, stages=["Production"])
        if current_prod:
            new_run = client.get_run(versions[0].run_id)
            prod_run = client.get_run(current_prod[0].run_id)
            
            new_metric = new_run.data.metrics.get("val_accuracy", 0)
            prod_metric = prod_run.data.metrics.get("val_accuracy", 0)
            
            if new_metric < prod_metric:
                print(f"警告: 新模型 ({new_metric}) 不如生产模型 ({prod_metric})")
                return False
    
    # 执行阶段转换
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version,
        stage=new_stage,
        archive_existing_versions=True
    )
    
    print(f"模型 {model_name} v{latest_version}: {current_stage} → {new_stage}")
    return True
```

### 5.2 Weights & Biases (W&B)

```python
"""
Weights & Biases 完整使用示例
"""
import wandb
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# ============= 初始化 =============
wandb.init(
    project="image-classification",
    name="resnet50-baseline",
    group="resnet-family",
    job_type="training",
    config={
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 50,
        "optimizer": "AdamW",
        "scheduler": "cosine",
        "weight_decay": 1e-4,
        "model_architecture": "resnet50",
        "pretrained": True,
    },
    tags=["baseline", "v1"],
    notes="Initial baseline model with ResNet50"
)


# ============= 深度学习训练循环 =============
class Trainer:
    """W&B 集成的训练器"""
    
    def __init__(self, model, train_loader, val_loader, config):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=config["learning_rate"],
            weight_decay=config["weight_decay"]
        )
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=config["epochs"]
        )
        self.criterion = nn.CrossEntropyLoss()
    
    def train_epoch(self, epoch):
        """训练一个 epoch"""
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(self.train_loader):
            data, target = data.to(self.device), target.to(self.device)
            
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            
            # 梯度裁剪
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            
            total_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            # 每 10 个 batch 记录一次
            if batch_idx % 10 == 0:
                wandb.log({
                    "train/batch_loss": loss.item(),
                    "train/batch_accuracy": 100. * correct / total,
                    "train/learning_rate": self.optimizer.param_groups[0]["lr"],
                    "epoch": epoch,
                    "step": epoch * len(self.train_loader) + batch_idx
                })
        
        return total_loss / len(self.train_loader), 100. * correct / total
    
    @torch.no_grad()
    def validate(self, epoch):
        """验证"""
        self.model.eval()
        val_loss = 0
        correct = 0
        total = 0
        all_preds = []
        all_targets = []
        
        for data, target in self.val_loader:
            data, target = data.to(self.device), target.to(self.device)
            output = self.model(data)
            loss = self.criterion(output, target)
            
            val_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            all_preds.extend(predicted.cpu().numpy())
            all_targets.extend(target.cpu().numpy())
        
        val_loss /= len(self.val_loader)
        val_acc = 100. * correct / total
        
        # 记录验证指标
        wandb.log({
            "val/loss": val_loss,
            "val/accuracy": val_acc,
            "epoch": epoch
        })
        
        # 记录混淆矩阵
        class_names = ["class_0", "class_1", "class_2"]  # 替换为实际类名
        wandb.log({
            "val/confusion_matrix": wandb.plot.confusion_matrix(
                preds=np.array(all_preds),
                y_true=np.array(all_targets),
                class_names=class_names
            )
        })
        
        return val_loss, val_acc
    
    def log_sample_predictions(self, num_samples=16):
        """记录样本预测可视化"""
        self.model.eval()
        images, targets = next(iter(self.val_loader))
        images = images[:num_samples].to(self.device)
        
        with torch.no_grad():
            outputs = self.model(images)
            _, preds = outputs.max(1)
        
        # W&B 图像记录
        wandb.log({
            "predictions": [
                wandb.Image(
                    img.permute(1, 2, 0).cpu().numpy(),
                    caption=f"True: {tgt.item()} | Pred: {pred.item()}"
                )
                for img, tgt, pred in zip(images, targets[:num_samples], preds)
            ]
        })
    
    def train(self):
        """完整训练流程"""
        best_val_acc = 0
        
        for epoch in range(self.config["epochs"]):
            train_loss, train_acc = self.train_epoch(epoch)
            val_loss, val_acc = self.validate(epoch)
            self.scheduler.step()
            
            print(f"Epoch {epoch}: train_loss={train_loss:.4f}, val_acc={val_acc:.2f}%")
            
            # 保存最佳模型
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(self.model.state_dict(), "best_model.pt")
                wandb.log({"best_val_accuracy": best_val_acc, "epoch": epoch})
                
                # 作为 artifact 保存
                artifact = wandb.Artifact(
                    name="best-model",
                    type="model",
                    metadata={"val_accuracy": best_val_acc, "epoch": epoch}
                )
                artifact.add_file("best_model.pt")
                wandb.log_artifact(artifact)
            
            # 每 5 个 epoch 记录一次样本预测
            if epoch % 5 == 0:
                self.log_sample_predictions()


# ============= Artifact 管理 =============
def use_dataset_artifact():
    """使用 W&B Artifact 数据集"""
    
    # 创建数据集 artifact
    artifact = wandb.Artifact(name="cifar10-processed", type="dataset")
    artifact.add_dir("data/processed/")
    artifact.add_file("data/info.json")
    
    # 记录 artifact
    run = wandb.init(project="my-project")
    run.log_artifact(artifact)
    
    # 在其他运行中使用 artifact
    artifact = run.use_artifact("my-project/cifar10-processed:latest")
    data_dir = artifact.download()
    return data_dir


# ============= Sweep 超参搜索 =============
def create_sweep():
    """创建 W&B Sweep"""
    
    sweep_config = {
        "method": "bayes",
        "metric": {
            "name": "val_accuracy",
            "goal": "maximize"
        },
        "parameters": {
            "learning_rate": {
                "distribution": "log_uniform_values",
                "min": 1e-5,
                "max": 1e-2
            },
            "batch_size": {
                "values": [16, 32, 64, 128]
            },
            "dropout": {
                "distribution": "uniform",
                "min": 0.1,
                "max": 0.5
            },
            "hidden_size": {
                "values": [128, 256, 512]
            },
            "num_layers": {
                "values": [2, 3, 4]
            },
            "optimizer": {
                "values": ["AdamW", "SGD", "Adam"]
            }
        }
    }
    
    sweep_id = wandb.sweep(sweep_config, project="image-classification")
    return sweep_id


def sweep_train():
    """Sweep 训练函数"""
    
    with wandb.init() as run:
        config = wandb.config
        
        # 使用 config 中的超参进行训练
        model = build_model(config)
        trainer = Trainer(model, train_loader, val_loader, config)
        trainer.train()
        
        # 记录最终结果
        wandb.log({"final_best_accuracy": trainer.best_val_acc})
```

### 5.3 MLflow vs W&B 对比

| 功能 | MLflow | Weights & Biases |
|------|--------|-------------------|
| 实验跟踪 | ✅ 开源 | ✅ 商业 (有免费层) |
| 模型注册 | ✅ 内置 | ✅ 内置 |
| 模型服务 | ✅ 内置 REST | ❌ 需外部工具 |
| 超参搜索 | 有限 | ✅ 强大的 Sweep |
| 可视化 | 基础 | ✅ 强大的仪表盘 |
| Artifact 管理 | ✅ | ✅ |
| 自托管 | ✅ 免费 | 商业许可 |
| 团队协作 | 基础 | ✅ 优秀 |
| 深度学习可视化 | 有限 | ✅ TensorBoard 集成 |
| 报告 | 有限 | ✅ 内置报告 |

---

## 6. 模型注册与管理

### 6.1 模型注册表架构

```python
"""
模型注册表管理
"""
import mlflow
from mlflow.tracking import MlflowClient
from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum

class ModelLifecycle(Enum):
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"
    DEPRECATED = "Deprecated"

@dataclass
class ModelCard:
    """模型卡片 - 模型文档"""
    name: str
    version: str
    description: str
    owner: str
    task: str
    metrics: Dict[str, float]
    training_data: str
    evaluation_data: str
    limitations: str
    ethical_considerations: str
    created_at: datetime = None
    last_updated: datetime = None


class ModelRegistryManager:
    """模型注册表管理器"""
    
    def __init__(self, tracking_uri: str = "http://localhost:5000"):
        self.client = MlflowClient(tracking_uri)
    
    def register_model(self, run_id: str, model_path: str, 
                       name: str, tags: Dict[str, str] = None) -> str:
        """注册新模型版本"""
        model_uri = f"runs:/{run_id}/{model_path}"
        
        result = mlflow.register_model(model_uri, name)
        
        # 添加元数据标签
        if tags:
            self.client.set_model_version_tag(name, result.version, "task", tags.get("task", ""))
            self.client.set_model_version_tag(name, result.version, "owner", tags.get("owner", ""))
        
        return result.version
    
    def get_production_model(self, model_name: str):
        """获取当前生产模型"""
        versions = self.client.get_latest_versions(model_name, stages=["Production"])
        if not versions:
            return None
        return versions[0]
    
    def promote_model(self, model_name: str, version: str, 
                      target_stage: str, require_approval: bool = True):
        """提升模型到目标阶段"""
        # 检查目标阶段是否有现有模型
        current = self.client.get_latest_versions(model_name, stages=[target_stage])
        
        if current and require_approval:
            # 记录审批日志
            current_version = current[0].version
            print(f"即将替换 {model_name} {target_stage} 阶段的 v{current_version}")
        
        # 执行转换
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=target_stage,
            archive_existing_versions=True
        )
        
        # 添加转换备注
        self.client.set_model_version_tag(
            model_name, version, "promoted_at", datetime.now().isoformat()
        )
    
    def validate_before_promotion(self, model_name: str, version: str,
                                   min_metrics: Dict[str, float]) -> bool:
        """提升前的验证检查"""
        version_info = self.client.get_model_version(model_name, version)
        run = self.client.get_run(version_info.run_id)
        
        for metric_name, min_value in min_metrics.items():
            actual_value = run.data.metrics.get(metric_name, 0)
            if actual_value < min_value:
                print(f"❌ 指标 {metric_name}: {actual_value} < {min_value}")
                return False
            print(f"✅ 指标 {metric_name}: {actual_value} >= {min_value}")
        
        return True
    
    def get_model_lineage(self, model_name: str, version: str):
        """获取模型血缘"""
        version_info = self.client.get_model_version(model_name, version)
        run = self.client.get_run(version_info.run_id)
        
        lineage = {
            "model": model_name,
            "version": version,
            "run_id": run.info.run_id,
            "params": run.data.params,
            "metrics": run.data.metrics,
            "tags": run.data.tags,
            "artifacts": self.client.list_artifacts(run.info.run_id),
        }
        return lineage
    
    def compare_model_versions(self, model_name: str, version_a: str, version_b: str):
        """对比两个模型版本"""
        va = self.client.get_model_version(model_name, version_a)
        vb = self.client.get_model_version(model_name, version_b)
        
        run_a = self.client.get_run(va.run_id)
        run_b = self.client.get_run(vb.run_id)
        
        comparison = {
            "metrics": {},
            "params_diff": {},
        }
        
        # 对比指标
        all_metrics = set(run_a.data.metrics.keys()) | set(run_b.data.metrics.keys())
        for metric in all_metrics:
            val_a = run_a.data.metrics.get(metric)
            val_b = run_b.data.metrics.get(metric)
            comparison["metrics"][metric] = {
                f"v{version_a}": val_a,
                f"v{version_b}": val_b,
                "diff": (val_b or 0) - (val_a or 0)
            }
        
        return comparison
```

### 6.2 模型版本管理 YAML 配置

```yaml
# model_registry_config.yaml
model_registry:
  name: fraud-detector
  description: "信用卡欺诈检测模型"
  owner: ml-team
  
  stages:
    development:
      auto_promote: false
      min_metrics:
        precision: 0.85
        recall: 0.80
        f1: 0.82
    
    staging:
      auto_promote: false
      requires_approval: true
      approvers:
        - ml-lead
        - security-officer
      min_metrics:
        precision: 0.90
        recall: 0.85
        f1: 0.87
        fairness_score: 0.95
    
    production:
      monitoring:
        enabled: true
        drift_threshold: 0.1
        retrain_trigger: 
          metric_drop: 0.05
          time_days: 30
      rollback:
        enabled: true
        auto_rollback_metric: "precision"
        auto_rollback_threshold: 0.80
  
  retention:
    max_versions_per_stage: 5
    archive_after_days: 90
    delete_after_days: 365
  
  notifications:
    on_register: true
    on_promotion: true
    on_degradation: true
    channels:
      - type: slack
        webhook: "${SLACK_WEBHOOK}"
      - type: email
        recipients: ["ml-team@company.com"]
```

---

## 7. 模型训练与调优

### 7.1 分布式训练

```python
"""
PyTorch 分布式训练 (DDP) 示例
"""
import os
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler
from torch.utils.data.distributed import DistributedSampler
import torch.nn as nn
import torch.optim as optim

def setup_distributed(rank: int, world_size: int, backend: str = "nccl"):
    """初始化分布式环境"""
    os.environ["MASTER_ADDR"] = os.environ.get("MASTER_ADDR", "localhost")
    os.environ["MASTER_PORT"] = os.environ.get("MASTER_PORT", "12355")
    dist.init_process_group(backend=backend, rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def cleanup():
    """清理分布式环境"""
    dist.destroy_process_group()


class ResNetTrainer:
    """分布式训练器"""
    
    def __init__(self, rank, world_size):
        self.rank = rank
        self.world_size = world_size
        self.device = torch.device(f"cuda:{rank}")
    
    def setup_model(self):
        """设置模型"""
        from torchvision.models import resnet50, ResNet50_Weights
        
        model = resnet50(weights=ResNet50_Weights.DEFAULT)
        model = model.to(self.device)
        model = DDP(model, device_ids=[self.rank])
        return model
    
    def setup_data(self, data_dir: str, batch_size: int = 64):
        """设置分布式数据加载器"""
        from torchvision import datasets, transforms
        
        transform = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225]),
        ])
        
        dataset = datasets.ImageFolder(data_dir, transform=transform)
        sampler = DistributedSampler(
            dataset, 
            num_replicas=self.world_size, 
            rank=self.rank,
            shuffle=True
        )
        
        loader = DataLoader(
            dataset,
            batch_size=batch_size,
            sampler=sampler,
            num_workers=4,
            pin_memory=True,
            drop_last=True
        )
        return loader, sampler
    
    def train(self, data_dir: str, epochs: int = 30, batch_size: int = 64):
        """执行分布式训练"""
        setup_distributed(self.rank, self.world_size)
        
        model = self.setup_model()
        train_loader, train_sampler = self.setup_data(data_dir, batch_size)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
        
        # 混合精度训练
        scaler = torch.amp.GradScaler()
        
        best_acc = 0
        for epoch in range(epochs):
            train_sampler.set_epoch(epoch)  # 确保每个 epoch 数据打乱不同
            model.train()
            
            total_loss = 0
            correct = 0
            total = 0
            
            for batch_idx, (inputs, targets) in enumerate(train_loader):
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                
                optimizer.zero_grad()
                
                # 混合精度前向传播
                with torch.amp.autocast(device_type='cuda'):
                    outputs = model(inputs)
                    loss = criterion(outputs, targets)
                
                # 混合精度反向传播
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
                
                total_loss += loss.item()
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()
            
            # 仅 rank 0 打印
            if self.rank == 0:
                train_acc = 100. * correct / total
                avg_loss = total_loss / len(train_loader)
                print(f"Epoch {epoch}: Loss={avg_loss:.4f}, Acc={train_acc:.2f}%")
                
                # 保存 checkpoint
                if train_acc > best_acc:
                    best_acc = train_acc
                    torch.save({
                        "epoch": epoch,
                        "model_state_dict": model.module.state_dict(),
                        "optimizer_state_dict": optimizer.state_dict(),
                        "accuracy": best_acc,
                    }, f"checkpoint_best.pt")
            
            scheduler.step()
        
        cleanup()


def main():
    """入口函数"""
    world_size = torch.cuda.device_count()
    mp.spawn(
        lambda rank: ResNetTrainer(rank, world_size).train("/data/imagenet"),
        args=(),
        nprocs=world_size,
        join=True
    )

if __name__ == "__main__":
    main()
```

### 7.2 超参数调优

```python
"""
多种超参数调优方法
"""
import optuna
from optuna.samplers import TPESampler, CmaEsSampler
from optuna.pruners import MedianPruner, HyperbandPruner
import torch
import torch.nn as nn
import torch.optim as optim


# ============= Optuna 超参搜索 =============
def objective(trial):
    """Optuna 优化目标"""
    
    # 定义超参搜索空间
    params = {
        "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-1, log=True),
        "batch_size": trial.suggest_categorical("batch_size", [16, 32, 64, 128]),
        "num_layers": trial.suggest_int("num_layers", 2, 6),
        "hidden_size": trial.suggest_categorical("hidden_size", [64, 128, 256, 512]),
        "dropout": trial.suggest_float("dropout", 0.1, 0.5),
        "optimizer": trial.suggest_categorical("optimizer", ["Adam", "AdamW", "SGD"]),
        "weight_decay": trial.suggest_float("weight_decay", 1e-6, 1e-2, log=True),
        "scheduler": trial.suggest_categorical("scheduler", ["cosine", "step", "plateau", "none"]),
        "warmup_steps": trial.suggest_int("warmup_steps", 0, 1000),
    }
    
    # 条件搜索空间
    if params["optimizer"] == "SGD":
        params["momentum"] = trial.suggest_float("momentum", 0.5, 0.99)
        params["nesterov"] = trial.suggest_categorical("nesterov", [True, False])
    
    # 构建模型
    model = build_classifier(params)
    
    # 训练
    val_acc = train_and_evaluate(model, params)
    
    return val_acc


def run_optuna_study():
    """运行 Optuna 研究"""
    
    study = optuna.create_study(
        direction="maximize",
        study_name="classifier-optimization",
        storage="sqlite:///optuna_study.db",
        load_if_exists=True,
        sampler=TPESampler(seed=42, n_startup_trials=10),
        pruner=HyperbandPruner(min_resource=1, max_resource=50, reduction_factor=3),
    )
    
    # 添加先验知识作为初始试验
    study.enqueue_trial({
        "learning_rate": 0.001,
        "batch_size": 32,
        "num_layers": 3,
        "hidden_size": 256,
        "dropout": 0.3,
        "optimizer": "AdamW",
        "weight_decay": 1e-4,
        "scheduler": "cosine",
        "warmup_steps": 100,
    })
    
    # 运行优化
    study.optimize(
        objective,
        n_trials=100,
        timeout=3600 * 4,  # 4小时超时
        n_jobs=1,
        show_progress_bar=True,
        callbacks=[optuna_logging_callback]
    )
    
    # 结果分析
    print(f"最佳试验: Trial {study.best_trial.number}")
    print(f"最佳值: {study.best_value:.4f}")
    print(f"最佳参数: {study.best_params}")
    
    # 参数重要性分析
    importance = optuna.importance.get_param_importances(study)
    for param, imp in importance.items():
        print(f"  {param}: {imp:.3f}")
    
    # 可视化
    fig = optuna.visualization.plot_optimization_history(study)
    fig.write_html("optimization_history.html")
    
    fig = optuna.visualization.plot_param_importances(study)
    fig.write_html("param_importances.html")
    
    fig = optuna.visualization.plot_parallel_coordinate(study)
    fig.write_html("parallel_coordinate.html")
    
    return study


# ============= Ray Tune 分布式调参 =============
"""
使用 Ray Tune 进行分布式超参搜索
"""
# pip install "ray[tune]"
from ray import tune
from ray.tune.schedulers import ASHAScheduler, PopulationBasedTraining
from ray.tune.search.optuna import OptunaSearch

def ray_tune_example():
    """Ray Tune 超参搜索"""
    
    # ASHA 调度器 (早期停止)
    scheduler = ASHAScheduler(
        metric="val_accuracy",
        mode="max",
        max_t=50,
        grace_period=5,
        reduction_factor=2,
    )
    
    # 搜索算法
    search_algo = OptunaSearch(
        metric="val_accuracy",
        mode="max",
        seed=42
    )
    
    # 搜索空间
    search_space = {
        "learning_rate": tune.loguniform(1e-5, 1e-1),
        "batch_size": tune.choice([16, 32, 64, 128]),
        "num_layers": tune.randint(2, 6),
        "hidden_size": tune.choice([64, 128, 256, 512]),
        "dropout": tune.uniform(0.1, 0.5),
    }
    
    # 运行
    analysis = tune.run(
        train_function,
        config=search_space,
        num_samples=100,
        scheduler=scheduler,
        search_alg=search_algo,
        resources_per_trial={"cpu": 2, "gpu": 0.5},
        metric="val_accuracy",
        mode="max",
        name="ray_tune_experiment",
        local_dir="./ray_results",
        verbose=1,
    )
    
    # 最佳配置
    best_config = analysis.get_best_config(metric="val_accuracy", mode="max")
    print(f"最佳配置: {best_config}")
    
    # 结果 DataFrame
    results_df = analysis.results_df
    results_df.to_csv("tune_results.csv")
    
    return analysis


# ============= Population Based Training =============
def pbt_example():
    """Population Based Training"""
    
    pbt_scheduler = PopulationBasedTraining(
        time_attr="training_iteration",
        metric="val_accuracy",
        mode="max",
        perturbation_interval=5,
        hyperparam_mutations={
            "learning_rate": tune.loguniform(1e-5, 1e-1),
            "batch_size": tune.choice([16, 32, 64, 128]),
            "dropout": tune.uniform(0.1, 0.5),
        },
    )
    
    analysis = tune.run(
        train_function,
        config={
            "learning_rate": tune.loguniform(1e-5, 1e-1),
            "batch_size": tune.choice([16, 32, 64, 128]),
            "dropout": tune.uniform(0.1, 0.5),
        },
        scheduler=pbt_scheduler,
        num_samples=8,
        resources_per_trial={"cpu": 2, "gpu": 1},
        metric="val_accuracy",
        mode="max",
    )
    
    return analysis
```

### 7.3 训练优化技巧

```python
"""
训练性能优化最佳实践
"""
import torch
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LambdaLR


class TrainingOptimizer:
    """训练优化器集合"""
    
    @staticmethod
    def get_warmup_scheduler(optimizer: Optimizer, warmup_steps: int, 
                              total_steps: int) -> LambdaLR:
        """线性预热 + 余弦退火"""
        def lr_lambda(current_step):
            if current_step < warmup_steps:
                return float(current_step) / float(max(1, warmup_steps))
            progress = float(current_step - warmup_steps) / float(
                max(1, total_steps - warmup_steps)
            )
            return max(0.0, 0.5 * (1.0 + torch.cos(torch.tensor(3.14159 * progress))))
        
        return LambdaLR(optimizer, lr_lambda)
    
    @staticmethod
    def label_smoothing_loss(logits, targets, num_classes, smoothing=0.1):
        """标签平滑损失"""
        confidence = 1.0 - smoothing
        log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
        
        with torch.no_grad():
            true_dist = torch.zeros_like(log_probs)
            true_dist.fill_(smoothing / (num_classes - 1))
            true_dist.scatter_(1, targets.unsqueeze(1), confidence)
        
        return torch.mean(torch.sum(-true_dist * log_probs, dim=-1))
    
    @staticmethod
    def mixup_data(x, y, alpha=0.2):
        """Mixup 数据增强"""
        if alpha > 0:
            lam = torch.distributions.Beta(alpha, alpha).sample()
        else:
            lam = 1.0
        
        batch_size = x.size(0)
        index = torch.randperm(batch_size, device=x.device)
        
        mixed_x = lam * x + (1 - lam) * x[index]
        return mixed_x, y, y[index], lam
    
    @staticmethod
    def mixup_criterion(criterion, pred, y_a, y_b, lam):
        """Mixup 损失计算"""
        return lam * criterion(pred, y_a) + (1 - lam) * criterion(pred, y_b)
    
    @staticmethod
    def gradient_accumulation_step(model, inputs, targets, criterion, 
                                    accumulation_steps=4):
        """梯度累积"""
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss = loss / accumulation_steps
        loss.backward()
        return loss.item() * accumulation_steps
    
    @staticmethod
    def exponential_moving_average(model, decay=0.999):
        """模型指数移动平均 (EMA)"""
        class EMA:
            def __init__(self, model, decay):
                self.decay = decay
                self.shadow = {}
                self.backup = {}
                for name, param in model.named_parameters():
                    if param.requires_grad:
                        self.shadow[name] = param.data.clone()
            
            def update(self, model):
                for name, param in model.named_parameters():
                    if param.requires_grad:
                        new_average = self.decay * self.shadow[name] + (1 - self.decay) * param.data
                        self.shadow[name] = new_average.clone()
            
            def apply_shadow(self, model):
                for name, param in model.named_parameters():
                    if param.requires_grad:
                        self.backup[name] = param.data.clone()
                        param.data = self.shadow[name]
            
            def restore(self, model):
                for name, param in model.named_parameters():
                    if param.requires_grad:
                        if name in self.backup:
                            param.data = self.backup[name]
                self.backup = {}
        
        return EMA(model, decay)


# ============= 数据加载优化 =============
class OptimizedDataLoader:
    """优化的数据加载"""
    
    @staticmethod
    def create_loader(dataset, batch_size, num_workers=None, pin_memory=True):
        """创建优化的数据加载器"""
        import multiprocessing
        if num_workers is None:
            num_workers = min(multiprocessing.cpu_count() // 2, 8)
        
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=pin_memory,
            prefetch_factor=2 if num_workers > 0 else None,
            persistent_workers=True if num_workers > 0 else False,
            drop_last=True,
        )
```

---

## 8. 模型评估

### 8.1 综合评估框架

```python
"""
全面的模型评估框架
"""
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, roc_curve,
    confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error, r2_score,
    mean_absolute_percentage_error
)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple


class ModelEvaluator:
    """综合模型评估器"""
    
    def __init__(self, y_true, y_pred, y_prob=None):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.y_prob = np.array(y_prob) if y_prob is not None else None
    
    def classification_metrics(self) -> Dict[str, float]:
        """分类指标"""
        metrics = {
            "accuracy": accuracy_score(self.y_true, self.y_pred),
            "precision_macro": precision_score(self.y_true, self.y_pred, average="macro", zero_division=0),
            "recall_macro": recall_score(self.y_true, self.y_pred, average="macro", zero_division=0),
            "f1_macro": f1_score(self.y_true, self.y_pred, average="macro", zero_division=0),
            "precision_weighted": precision_score(self.y_true, self.y_pred, average="weighted", zero_division=0),
            "f1_weighted": f1_score(self.y_true, self.y_pred, average="weighted", zero_division=0),
        }
        
        if self.y_prob is not None:
            if self.y_prob.ndim == 1:
                metrics["roc_auc"] = roc_auc_score(self.y_true, self.y_prob)
            else:
                metrics["roc_auc_ovr"] = roc_auc_score(
                    self.y_true, self.y_prob, multi_class="ovr"
                )
        
        return metrics
    
    def regression_metrics(self) -> Dict[str, float]:
        """回归指标"""
        return {
            "mae": mean_absolute_error(self.y_true, self.y_pred),
            "rmse": np.sqrt(mean_squared_error(self.y_true, self.y_pred)),
            "mape": mean_absolute_percentage_error(self.y_true, self.y_pred),
            "r2": r2_score(self.y_true, self.y_pred),
            "adj_r2": self._adjusted_r2(),
        }
    
    def _adjusted_r2(self) -> float:
        n = len(self.y_true)
        p = 1  # 特征数（需要根据实际调整）
        r2 = r2_score(self.y_true, self.y_pred)
        return 1 - (1 - r2) * (n - 1) / (n - p - 1)
    
    def plot_confusion_matrix(self, labels=None, save_path=None):
        """绘制混淆矩阵"""
        cm = confusion_matrix(self.y_true, self.y_pred)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=labels, yticklabels=labels, ax=ax
        )
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
        ax.set_title("Confusion Matrix")
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        
        return fig
    
    def plot_roc_curve(self, save_path=None):
        """绘制 ROC 曲线"""
        if self.y_prob is None:
            raise ValueError("需要概率值才能绘制 ROC 曲线")
        
        fpr, tpr, thresholds = roc_curve(self.y_true, self.y_prob)
        auc = roc_auc_score(self.y_true, self.y_prob)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(fpr, tpr, label=f"AUC = {auc:.3f}", linewidth=2)
        ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
        ax.fill_between(fpr, tpr, alpha=0.1)
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve")
        ax.legend(loc="lower right")
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        
        return fig
    
    def plot_precision_recall_curve(self, save_path=None):
        """绘制 Precision-Recall 曲线"""
        if self.y_prob is None:
            raise ValueError("需要概率值")
        
        precision, recall, thresholds = precision_recall_curve(self.y_true, self.y_prob)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(recall, precision, linewidth=2)
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_title("Precision-Recall Curve")
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        
        return fig
    
    def plot_residuals(self, save_path=None):
        """绘制残差图 (回归任务)"""
        residuals = self.y_true - self.y_pred
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # 残差 vs 预测值
        axes[0].scatter(self.y_pred, residuals, alpha=0.3)
        axes[0].axhline(y=0, color='r', linestyle='--')
        axes[0].set_xlabel("Predicted Values")
        axes[0].set_ylabel("Residuals")
        axes[0].set_title("Residuals vs Predicted")
        
        # 残差分布
        axes[1].hist(residuals, bins=50, edgecolor='black', alpha=0.7)
        axes[1].axvline(x=0, color='r', linestyle='--')
        axes[1].set_xlabel("Residuals")
        axes[1].set_ylabel("Frequency")
        axes[1].set_title("Residual Distribution")
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
        
        return fig


class FairnessEvaluator:
    """模型公平性评估"""
    
    def __init__(self, y_true, y_pred, sensitive_attribute):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.sensitive_attribute = np.array(sensitive_attribute)
        self.groups = np.unique(sensitive_attribute)
    
    def demographic_parity(self) -> Dict:
        """人口统计均等性"""
        results = {}
        for group in self.groups:
            mask = self.sensitive_attribute == group
            results[group] = self.y_pred[mask].mean()
        
        # 差异
        values = list(results.values())
        results["max_difference"] = max(values) - min(values)
        results["ratio"] = min(values) / max(values) if max(values) > 0 else 0
        return results
    
    def equalized_odds(self) -> Dict:
        """均等机会"""
        results = {}
        for group in self.groups:
            mask = self.sensitive_attribute == group
            results[group] = {
                "tpr": recall_score(self.y_true[mask], self.y_pred[mask]),
                "fpr": self._false_positive_rate(mask),
            }
        return results
    
    def _false_positive_rate(self, mask) -> float:
        tn = np.sum((self.y_true[mask] == 0) & (self.y_pred[mask] == 0))
        fp = np.sum((self.y_true[mask] == 0) & (self.y_pred[mask] == 1))
        return fp / (fp + tn) if (fp + tn) > 0 else 0


class RobustnessEvaluator:
    """模型鲁棒性评估"""
    
    def __init__(self, model, X_test, y_test):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
    
    def adversarial_noise_test(self, noise_levels=None) -> Dict:
        """对抗噪声测试"""
        if noise_levels is None:
            noise_levels = [0.01, 0.05, 0.1, 0.2, 0.5]
        
        results = {}
        for level in noise_levels:
            noise = np.random.normal(0, level, self.X_test.shape)
            X_noisy = self.X_test + noise
            
            y_pred = self.model.predict(X_noisy)
            acc = accuracy_score(self.y_test, y_pred)
            results[f"noise_{level}"] = acc
        
        return results
    
    def feature_dropout_test(self, drop_rates=None) -> Dict:
        """特征丢弃测试"""
        if drop_rates is None:
            drop_rates = [0.1, 0.2, 0.3, 0.5]
        
        results = {}
        n_features = self.X_test.shape[1]
        
        for rate in drop_rates:
            n_drop = int(n_features * rate)
            # 多次随机丢弃取平均
            accuracies = []
            for _ in range(10):
                drop_cols = np.random.choice(n_features, n_drop, replace=False)
                X_masked = self.X_test.copy()
                X_masked[:, drop_cols] = 0
                
                y_pred = self.model.predict(X_masked)
                accuracies.append(accuracy_score(self.y_test, y_pred))
            
            results[f"drop_{rate}"] = np.mean(accuracies)
        
        return results
```

### 8.3 评估报告生成

```python
"""
自动生成评估报告
"""
from jinja2 import Template
import json
from datetime import datetime

EVALUATION_REPORT_TEMPLATE = """
# 模型评估报告

## 基本信息
- **模型名称**: {{ model_name }}
- **版本**: {{ version }}
- **评估日期**: {{ eval_date }}
- **数据集**: {{ dataset_name }} (样本数: {{ n_samples }})

## 性能指标

{% for metric, value in metrics.items() %}
- {{ metric }}: {{ "%.4f"|format(value) }}
{% endfor %}

## 指标阈值检查
{% for metric, check in threshold_checks.items() %}
- {{ metric }}: {{ "✅ 通过" if check["passed"] else "❌ 未通过" }}
  (实际: {{ "%.4f"|format(check["actual"]) }}, 要求: ≥ {{ "%.4f"|format(check["threshold"]) }})
{% endfor %}

## 对比上一版本
| 指标 | 当前版本 | 上一版本 | 变化 |
|------|----------|----------|------|
{% for metric, values in comparison.items() %}
| {{ metric }} | {{ "%.4f"|format(values["current"]) }} | {{ "%.4f"|format(values["previous"]) }} | {{ "%+.4f"|format(values["diff"]) }} |
{% endfor %}

## 公平性分析
{% for group, value in fairness.items() %}
- {{ group }}: {{ "%.4f"|format(value) }}
{% endfor %}

## 结论与建议
{{ recommendations }}

---
*报告自动生成于 {{ generated_at }}*
"""

def generate_evaluation_report(
    model_name: str,
    version: str,
    metrics: dict,
    thresholds: dict,
    comparison: dict = None,
    fairness: dict = None,
    dataset_name: str = "",
    n_samples: int = 0,
    recommendations: str = ""
) -> str:
    """生成 Markdown 格式的评估报告"""
    
    template = Template(EVALUATION_REPORT_TEMPLATE)
    
    # 阈值检查
    threshold_checks = {}
    for metric, threshold in thresholds.items():
        actual = metrics.get(metric, 0)
        threshold_checks[metric] = {
            "actual": actual,
            "threshold": threshold,
            "passed": actual >= threshold,
        }
    
    report = template.render(
        model_name=model_name,
        version=version,
        eval_date=datetime.now().strftime("%Y-%m-%d"),
        dataset_name=dataset_name,
        n_samples=n_samples,
        metrics=metrics,
        threshold_checks=threshold_checks,
        comparison=comparison or {},
        fairness=fairness or {},
        recommendations=recommendations,
        generated_at=datetime.now().isoformat(),
    )
    
    return report
```

---

## 9. 模型部署

### 9.1 Docker 容器化部署

#### Dockerfile 最佳实践

```dockerfile
# ============= 多阶段构建 =============

# Stage 1: 构建阶段
FROM python:3.11-slim AS builder

WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件 (利用 Docker 缓存)
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: 运行阶段
FROM python:3.11-slim AS runtime

# 安全: 创建非 root 用户
RUN groupadd -r mlops && useradd -r -g mlops -s /sbin/nologin mlops

WORKDIR /app

# 从构建阶段复制安装的包
COPY --from=builder /install /usr/local

# 复制模型和代码
COPY src/ ./src/
COPY models/ ./models/
COPY config/ ./config/

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_PATH=/app/models \
    CONFIG_PATH=/app/config \
    PORT=8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# 切换到非 root 用户
USER mlops

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "-m", "uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

#### FastAPI 推理服务

```python
# src/serve.py
"""
高性能模型推理服务
"""
import os
import time
import logging
import json
from typing import List, Dict, Optional, Any
from contextlib import asynccontextmanager

import numpy as np
import joblib
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import asyncio

# ============= 配置 =============
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models")
MODEL_NAME = os.getenv("MODEL_NAME", "fraud_detector_v2")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


# ============= 模型加载 =============
class ModelManager:
    """模型管理器 - 支持热加载"""
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.model_metadata = {}
        self.loaded_at = None
        self._lock = asyncio.Lock()
    
    async def load_model(self, model_name: str = None):
        """加载模型"""
        async with self._lock:
            name = model_name or MODEL_NAME
            model_file = os.path.join(MODEL_PATH, name, "model.pkl")
            preprocessor_file = os.path.join(MODEL_PATH, name, "preprocessor.pkl")
            metadata_file = os.path.join(MODEL_PATH, name, "metadata.json")
            
            logger.info(f"Loading model from {model_file}")
            
            self.model = joblib.load(model_file)
            self.preprocessor = joblib.load(preprocessor_file)
            
            if os.path.exists(metadata_file):
                with open(metadata_file) as f:
                    self.model_metadata = json.load(f)
            
            self.loaded_at = time.time()
            logger.info(f"Model loaded: {self.model_metadata}")
    
    async def predict(self, features: np.ndarray) -> np.ndarray:
        """预测"""
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        if self.preprocessor is not None:
            features = self.preprocessor.transform(features)
        
        return self.model.predict_proba(features)
    
    async def reload(self, model_name: str = None):
        """热加载模型"""
        await self.load_model(model_name)


# 全局模型管理器
model_manager = ModelManager()


# ============= FastAPI 应用 =============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    await model_manager.load_model()
    logger.info("Model loaded on startup")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="ML Model Inference API",
    description="高性能模型推理服务",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= 请求/响应模型 =============
class PredictionRequest(BaseModel):
    instances: List[Dict[str, Any]] = Field(..., description="预测请求列表")
    parameters: Optional[Dict[str, Any]] = Field(None, description="额外参数")

class PredictionResponse(BaseModel):
    predictions: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    inference_time_ms: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    model_version: str
    uptime_seconds: float


# ============= API 路由 =============
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    uptime = time.time() - model_manager.loaded_at if model_manager.loaded_at else 0
    return HealthResponse(
        status="healthy" if model_manager.model is not None else "unhealthy",
        model_loaded=model_manager.model is not None,
        model_name=model_manager.model_metadata.get("name", MODEL_NAME),
        model_version=model_manager.model_metadata.get("version", "unknown"),
        uptime_seconds=uptime,
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """模型推理"""
    start_time = time.time()
    
    try:
        # 转换为特征数组
        features = np.array([list(inst.values()) for inst in request.instances])
        
        # 预测
        probabilities = await model_manager.predict(features)
        
        # 构建响应
        predictions = []
        for i, prob in enumerate(probabilities):
            pred = {
                "index": i,
                "prediction": int(np.argmax(prob)),
                "probabilities": prob.tolist(),
                "confidence": float(np.max(prob)),
            }
            predictions.append(pred)
        
        inference_time = (time.time() - start_time) * 1000
        
        return PredictionResponse(
            predictions=predictions,
            metadata={
                "model": model_manager.model_metadata.get("name"),
                "version": model_manager.model_metadata.get("version"),
            },
            inference_time_ms=round(inference_time, 2),
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/admin/reload")
async def reload_model(model_name: Optional[str] = None, 
                        background_tasks: BackgroundTasks = None):
    """热加载模型"""
    background_tasks.add_task(model_manager.reload, model_name)
    return {"status": "reload_initiated", "model_name": model_name or MODEL_NAME}


@app.get("/metrics")
async def metrics():
    """Prometheus 指标端点"""
    from prometheus_client import generate_latest
    return Response(content=generate_latest(), media_type="text/plain")


# ============= 中间件: 请求日志 =============
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration*1000:.2f}ms"
    )
    return response
```

### 9.2 Kubernetes 部署

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-serving
  namespace: ml-production
  labels:
    app: ml-model
    version: v2.1.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
        version: v2.1.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: ml-service-account
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: model-server
          image: registry.example.com/ml-model:v2.1.0
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              name: http
              protocol: TCP
          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "2000m"
              memory: "4Gi"
              nvidia.com/gpu: "0"    # 如需 GPU 设置为 "1"
          env:
            - name: MODEL_NAME
              value: "fraud_detector_v2"
            - name: LOG_LEVEL
              value: "INFO"
            - name: PORT
              value: "8080"
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          volumeMounts:
            - name: model-storage
              mountPath: /app/models
              readOnly: true
            - name: config
              mountPath: /app/config
              readOnly: true
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: model-pvc
        - name: config
          configMap:
            name: ml-model-config
      nodeSelector:
        node-type: ml-serving
      tolerations:
        - key: "ml-workload"
          operator: "Equal"
          value: "true"
          effect: "NoSchedule"
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
  namespace: ml-production
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
      name: http
  selector:
    app: ml-model
---
# HPA 自动扩缩
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
  namespace: ml-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model-serving
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: request_latency_p99
        target:
          type: AverageValue
          averageValue: "200m"    # 200ms
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Pods
          value: 1
          periodSeconds: 120
---
# Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ml-model-ingress
  namespace: ml-production
  annotations:
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - ml-api.example.com
      secretName: ml-api-tls
  rules:
    - host: ml-api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ml-model-service
                port:
                  number: 80
```

#### Kustomize 多环境管理

```yaml
# k8s/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ml-production

resources:
  - ../../base

patches:
  - target:
      kind: Deployment
      name: ml-model-serving
    patch: |
      - op: replace
        path: /spec/replicas
        value: 5
      - op: replace
        path: /spec/template/spec/containers/0/resources/requests/cpu
        value: "1000m"
      - op: replace
        path: /spec/template/spec/containers/0/resources/requests/memory
        value: "2Gi"
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/cpu
        value: "4000m"
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/memory
        value: "8Gi"

configMapGenerator:
  - name: ml-model-config
    literals:
      - MODEL_NAME=fraud_detector_v2
      - LOG_LEVEL=WARNING
      - BATCH_SIZE=64
      - MAX_CONCURRENT_REQUESTS=100
```

### 9.3 AWS SageMaker 部署

```python
"""
AWS SageMaker 部署完整流程
"""
import boto3
import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.model import Model
from sagemaker.predictor import Predictor
from sagemaker.serializers import CSVSerializer, JSONSerializer
from sagemaker.deserializers import JSONDeserializer
from sagemaker.transformer import Transformer

sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()
bucket = "sagemaker-ml-models"
prefix = "fraud-detection"


# ============= 训练 =============
sklearn_estimator = SKLearn(
    entry_point="train.py",
    source_dir="src",
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    framework_version="1.2-1",
    py_version="py39",
    hyperparameters={
        "n_estimators": 500,
        "max_depth": 10,
        "learning_rate": 0.1,
    },
    output_path=f"s3://{bucket}/{prefix}/output",
    base_job_name="fraud-detector-train",
)

sklearn_estimator.fit({"train": f"s3://{bucket}/{prefix}/data/train/"})


# ============= 部署为端点 =============
model = sklearn_estimator.create_model()

predictor = model.deploy(
    initial_instance_count=2,
    instance_type="ml.m5.large",
    endpoint_name="fraud-detector-endpoint",
    serializer=JSONSerializer(),
    deserializer=JSONDeserializer(),
)


# ============= Serverless 推理 =============
from sagemaker.serverless import ServerlessInferenceConfig

serverless_config = ServerlessInferenceConfig(
    memory_size_in_mb=2048,
    max_concurrency=10,
)

predictor_serverless = model.deploy(
    serverless_inference_config=serverless_config,
    endpoint_name="fraud-detector-serverless",
)


# ============= 批量转换 =============
transformer = Transformer(
    model=sklearn_estimator.create_model(),
    instance_count=2,
    instance_type="ml.m5.xlarge",
    output_path=f"s3://{bucket}/{prefix}/batch-output/",
    strategy="SingleRecord",
    assemble_with="Line",
)

transformer.transform(
    data=f"s3://{bucket}/{prefix}/batch-input/",
    content_type="text/csv",
    split_type="Line",
)


# ============= 端点自动扩缩 =============
def setup_auto_scaling(endpoint_name: str):
    """配置端点自动扩缩"""
    app_auto_scaling = boto3.client("application-autoscaling")
    
    # 注册可扩缩目标
    app_auto_scaling.register_scalable_target(
        ServiceNamespace="sagemaker",
        ResourceId=f"endpoint/{endpoint_name}/variant/AllTraffic",
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        MinCapacity=1,
        MaxCapacity=10,
    )
    
    # 基于 CPU 利用率的扩缩策略
    app_auto_scaling.put_scaling_policy(
        PolicyName="cpu-utilization-policy",
        ServiceNamespace="sagemaker",
        ResourceId=f"endpoint/{endpoint_name}/variant/AllTraffic",
        ScalableDimension="sagemaker:variant:DesiredInstanceCount",
        PolicyType="TargetTrackingScaling",
        TargetTrackingScalingPolicyConfiguration={
            "TargetValue": 70.0,
            "PredefinedMetricSpecification": {
                "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance",
            },
            "ScaleInCooldown": 300,
            "ScaleOutCooldown": 60,
        },
    )


# ============= A/B 测试部署 =============
def create_ab_test_endpoint(primary_model, shadow_model, endpoint_name):
    """创建 A/B 测试端点"""
    from sagemaker.session import production_variant
    
    primary_variant = production_variant(
        model_name=primary_model.name,
        instance_type="ml.m5.large",
        initial_instance_count=3,
        variant_name="Primary",
        initial_weight=70,  # 70% 流量
    )
    
    shadow_variant = production_variant(
        model_name=shadow_model.name,
        instance_type="ml.m5.large",
        initial_instance_count=1,
        variant_name="Shadow",
        initial_weight=30,  # 30% 流量
    )
    
    sagemaker_session.create_endpoint_config(
        name=f"{endpoint_name}-config",
        production_variants=[primary_variant, shadow_variant],
        data_capture_config=sagemaker.model_monitor.DataCaptureConfig(
            enable_capture=True,
            sampling_percentage=100,
            destination_s3_uri=f"s3://{bucket}/{prefix}/data-capture/",
            capture_options=[
                {"captureMode": "Input"},
                {"captureMode": "Output"},
            ],
        ),
    )
```

### 9.4 Google Vertex AI 部署

```python
"""
Google Vertex AI 部署
"""
from google.cloud import aiplatform
from google.cloud.aiplatform import Model, Endpoint
import vertexai
from vertexai.preview.model_monitoring import (
    ModelMonitoringObjectiveConfig,
    SamplingStrategy,
    ThresholdConfig,
)


# 初始化
PROJECT_ID = "my-project"
REGION = "us-central1"
BUCKET_URI = f"gs://{PROJECT_ID}-ml-models"

vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)


# ============= 上传模型 =============
def upload_model():
    """上传模型到 Vertex AI Model Registry"""
    
    model = Model.upload(
        display_name="fraud-detector-v2",
        artifact_uri=f"{BUCKET_URI}/models/fraud_detector/v2/",
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-2:latest",
        serving_container_predict_route="/predict",
        serving_container_health_route="/health",
        serving_container_ports=[8080],
        description="Credit card fraud detection model v2",
        labels={
            "task": "fraud-detection",
            "team": "ml-platform",
        },
    )
    
    model.wait()
    print(f"Model uploaded: {model.resource_name}")
    return model


# ============= 创建端点 =============
def deploy_model(model: Model):
    """部署模型到端点"""
    
    endpoint = Endpoint.create(
        display_name="fraud-detector-endpoint",
        description="Production fraud detection endpoint",
        labels={"environment": "production"},
    )
    
    # 部署
    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name="fraud-detector-v2",
        machine_type="n1-standard-4",
        min_replica_count=2,
        max_replica_count=10,
        traffic_percentage=100,
        # 自动扩缩
        accelerator_type=None,  # 或 "NVIDIA_TESLA_T4"
        accelerator_count=0,
        # 流量分割
        disable_container_logging=False,
        sync=True,
    )
    
    return endpoint


# ============= 在线预测 =============
def online_predict(endpoint: Endpoint, instances: list):
    """在线预测"""
    
    response = endpoint.predict(instances=instances)
    
    for prediction in response.predictions:
        print(f"Prediction: {prediction}")
    
    return response.predictions


# ============= 批量预测 =============
def batch_predict(model: Model, input_uri: str, output_uri: str):
    """批量预测"""
    
    batch_prediction_job = model.batch_predict(
        job_display_name="fraud-batch-prediction",
        instances_format="jsonl",
        predictions_format="jsonl",
        instance_uri=input_uri,
        prediction_uri=output_uri,
        machine_type="n1-standard-8",
        starting_replica_count=2,
        max_replica_count=10,
        sync=True,
    )
    
    print(f"Batch prediction completed: {batch_prediction_job.state}")
    return batch_prediction_job


# ============= 模型监控 =============
def setup_model_monitoring(endpoint: Endpoint):
    """配置模型监控"""
    
    # 数据漂移检测
    monitoring_config = ModelMonitoringObjectiveConfig(
        drift_detection_config={
            "drift_thresholds": {
                "default": ThresholdConfig(value=0.001),
            }
        },
        feature_thresholds={
            "amount": ThresholdConfig(value=0.01),
            "transaction_count_7d": ThresholdConfig(value=0.02),
        },
        sampling_strategy=SamplingStrategy(random_sample_rate=0.8),
    )
    
    # 创建监控作业
    model_monitoring_job = aiplatform.ModelDeploymentMonitoringJob.create(
        display_name="fraud-detector-monitoring",
        endpoint=endpoint,
        model_monitoring_objective_configs=[
            {
                "objective_config": monitoring_config,
                "deployed_model_index": 0,
            }
        ],
        logging_sampling_strategy=SamplingStrategy(random_sample_rate=0.5),
        schedule_config={"monitor_interval": 1},  # 每小时
        alert_email_addresses=["ml-team@company.com"],
    )
    
    return model_monitoring_job
```

### 9.5 gRPC 高性能推理服务

```python
"""
gRPC 推理服务
"""
# proto file: inference.proto
"""
syntax = "proto3";

package inference;

service InferenceService {
    rpc Predict(PredictRequest) returns (PredictResponse);
    rpc PredictStream(stream PredictRequest) returns (stream PredictResponse);
    rpc GetModelInfo(GetModelInfoRequest) returns (GetModelInfoResponse);
}

message PredictRequest {
    repeated FeatureInstance instances = 1;
    map<string, string> parameters = 2;
}

message FeatureInstance {
    map<string, FeatureValue> features = 1;
}

message FeatureValue {
    oneof value {
        double float_val = 1;
        int64 int_val = 2;
        string str_val = 3;
        bool bool_val = 4;
    }
}

message PredictResponse {
    repeated PredictionResult predictions = 1;
    string model_name = 2;
    string model_version = 3;
    double inference_time_ms = 4;
}

message PredictionResult {
    int32 prediction = 1;
    repeated double probabilities = 2;
    double confidence = 3;
}

message GetModelInfoRequest {}
message GetModelInfoResponse {
    string model_name = 1;
    string model_version = 2;
    int64 load_time = 3;
    map<string, string> metadata = 4;
}
"""

# server implementation
import grpc
from concurrent import futures
import time
import asyncio

class InferenceServicer:
    """gRPC 推理服务实现"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.predict_count = 0
        self.total_latency = 0
    
    def Predict(self, request, context):
        """同步预测 RPC"""
        start_time = time.perf_counter()
        
        try:
            # 解析请求
            instances = []
            for inst in request.instances:
                features = {}
                for key, value in inst.features.items():
                    if value.HasField("float_val"):
                        features[key] = value.float_val
                    elif value.HasField("int_val"):
                        features[key] = value.int_val
                    elif value.HasField("str_val"):
                        features[key] = value.str_val
                    elif value.HasField("bool_val"):
                        features[key] = value.bool_val
                instances.append(features)
            
            # 预测
            import numpy as np
            features_array = np.array([list(inst.values()) for inst in instances])
            probabilities = self.model_manager.model.predict_proba(features_array)
            
            # 构建响应
            predictions = []
            for prob in probabilities:
                pred_idx = int(np.argmax(prob))
                predictions.append(
                    PredictResponse.PredictionResult(
                        prediction=pred_idx,
                        probabilities=prob.tolist(),
                        confidence=float(np.max(prob)),
                    )
                )
            
            latency_ms = (time.perf_counter() - start_time) * 1000
            self.predict_count += 1
            self.total_latency += latency_ms
            
            return PredictResponse(
                predictions=predictions,
                model_name=self.model_manager.model_metadata.get("name", ""),
                model_version=self.model_manager.model_metadata.get("version", ""),
                inference_time_ms=latency_ms,
            )
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return PredictResponse()


def serve(port: int = 50051):
    """启动 gRPC 服务"""
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 100 * 1024 * 1024),
            ("grpc.max_receive_message_length", 100 * 1024 * 1024),
        ]
    )
    
    model_manager = ModelManager()
    # 同步加载模型
    import joblib
    model_manager.model = joblib.load("/app/models/model.pkl")
    
    servicer = InferenceServicer(model_manager)
    # add_InferenceServiceServicer_to_server(servicer, server)  # 从生成的代码导入
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC server started on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
```

---

## 10. 模型监控与漂移检测

### 10.1 监控架构

```
┌─────────────────────────────────────────────────┐
│                   监控仪表盘                       │
│          (Grafana / Kibana / W&B)                │
├─────────────────────────────────────────────────┤
│  告警系统: PagerDuty / Slack / Email / Webhook    │
├─────────────────────────────────────────────────┤
│  指标聚合: Prometheus + AlertManager              │
├─────────────────────────────────────────────────┤
│  漂移检测: Evidently AI / Alibi / SageMaker      │
├─────────────────────────────────────────────────┤
│  数据收集: 推理日志 + 特征快照 + 预测结果          │
├─────────────────────────────────────────────────┤
│  模型服务 (K8s / Cloud)                           │
└─────────────────────────────────────────────────┘
```

### 10.2 数据漂移检测

```python
"""
数据漂移检测完整实现
"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json

class DriftType(Enum):
    NO_DRIFT = "no_drift"
    FEATURE_DRIFT = "feature_drift"
    CONCEPT_DRIFT = "concept_drift"
    LABEL_DRIFT = "label_drift"
    DATA_QUALITY = "data_quality"


@dataclass
class DriftResult:
    """漂移检测结果"""
    drift_type: DriftType
    feature_name: str
    statistic: float
    p_value: float
    threshold: float
    is_drifted: bool
    details: Dict = None
    
    def to_dict(self) -> dict:
        return {
            "drift_type": self.drift_type.value,
            "feature_name": self.feature_name,
            "statistic": self.statistic,
            "p_value": self.p_value,
            "threshold": self.threshold,
            "is_drifted": self.is_drifted,
            "details": self.details or {},
        }


class DriftDetector:
    """多方法漂移检测器"""
    
    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level
        self.reference_data = None
        self.feature_types = {}
    
    def set_reference(self, reference_df: pd.DataFrame):
        """设置参考数据（训练数据分布）"""
        self.reference_data = reference_df
        self.feature_types = {
            col: "numeric" if reference_df[col].dtype in [np.float64, np.int64, np.float32]
            else "categorical"
            for col in reference_df.columns
        }
    
    def detect_feature_drift(self, current_df: pd.DataFrame) -> List[DriftResult]:
        """检测特征漂移"""
        results = []
        
        for col in self.reference_data.columns:
            if col not in current_df.columns:
                continue
            
            ref_data = self.reference_data[col].dropna()
            cur_data = current_df[col].dropna()
            
            if self.feature_types[col] == "numeric":
                result = self._ks_test(col, ref_data, cur_data)
            else:
                result = self._chi_square_test(col, ref_data, cur_data)
            
            results.append(result)
        
        return results
    
    def _ks_test(self, feature_name: str, ref: pd.Series, cur: pd.Series) -> DriftResult:
        """Kolmogorov-Smirnov 检验（数值特征）"""
        statistic, p_value = stats.ks_2samp(ref, cur)
        
        return DriftResult(
            drift_type=DriftType.FEATURE_DRIFT,
            feature_name=feature_name,
            statistic=statistic,
            p_value=p_value,
            threshold=self.significance_level,
            is_drifted=p_value < self.significance_level,
            details={
                "test": "KS",
                "ref_mean": ref.mean(),
                "cur_mean": cur.mean(),
                "ref_std": ref.std(),
                "cur_std": cur.std(),
            }
        )
    
    def _chi_square_test(self, feature_name: str, ref: pd.Series, cur: pd.Series) -> DriftResult:
        """卡方检验（分类特征）"""
        # 获取共同的类别
        categories = set(ref.unique()) & set(cur.unique())
        
        if not categories:
            return DriftResult(
                drift_type=DriftType.FEATURE_DRIFT,
                feature_name=feature_name,
                statistic=1.0,
                p_value=0.0,
                threshold=self.significance_level,
                is_drifted=True,
                details={"test": "Chi2", "error": "No common categories"}
            )
        
        ref_counts = ref[ref.isin(categories)].value_counts(normalize=True)
        cur_counts = cur[cur.isin(categories)].value_counts(normalize=True)
        
        # 对齐
        ref_freq = [ref_counts.get(cat, 0) for cat in categories]
        cur_freq = [cur_counts.get(cat, 0) for cat in categories]
        
        # 缩放
        scale_factor = len(cur) / len(ref)
        ref_freq_scaled = [f * scale_factor * len(ref) for f in ref_freq]
        cur_freq_scaled = [f * len(cur) for f in cur_freq]
        
        statistic, p_value = stats.chisquare(cur_freq_scaled, f_exp=ref_freq_scaled)
        
        return DriftResult(
            drift_type=DriftType.FEATURE_DRIFT,
            feature_name=feature_name,
            statistic=statistic,
            p_value=p_value,
            threshold=self.significance_level,
            is_drifted=p_value < self.significance_level,
            details={"test": "Chi2"}
        )
    
    def detect_concept_drift(self, y_ref: np.ndarray, y_cur: np.ndarray,
                              predictions_ref: np.ndarray, predictions_cur: np.ndarray
                              ) -> DriftResult:
        """检测概念漂移（模型性能下降）"""
        from sklearn.metrics import accuracy_score
        
        acc_ref = accuracy_score(y_ref, predictions_ref)
        acc_cur = accuracy_score(y_cur, predictions_cur)
        
        # 使用 bootstrap 测试性能差异
        n_bootstrap = 1000
        diffs = []
        for _ in range(n_bootstrap):
            idx = np.random.choice(len(y_cur), len(y_cur), replace=True)
            acc_boot = accuracy_score(y_cur[idx], predictions_cur[idx])
            diffs.append(acc_ref - acc_boot)
        
        p_value = np.mean(np.array(diffs) < 0)
        
        return DriftResult(
            drift_type=DriftType.CONCEPT_DRIFT,
            feature_name="model_performance",
            statistic=acc_ref - acc_cur,
            p_value=p_value,
            threshold=self.significance_level,
            is_drifted=(acc_ref - acc_cur) > 0.05,
            details={
                "accuracy_reference": acc_ref,
                "accuracy_current": acc_cur,
                "performance_drop": acc_ref - acc_cur,
            }
        )
    
    def detect_population_stability_index(self, feature_name: str,
                                           ref: pd.Series, cur: pd.Series,
                                           n_bins: int = 10) -> DriftResult:
        """PSI (Population Stability Index) 检测"""
        # 创建分箱
        bins = np.linspace(ref.min(), ref.max(), n_bins + 1)
        
        ref_hist, _ = np.histogram(ref, bins=bins)
        cur_hist, _ = np.histogram(cur, bins=bins)
        
        # 转换为比例，避免除零
        ref_pct = ref_hist / ref_hist.sum() + 1e-6
        cur_pct = cur_hist / cur_hist.sum() + 1e-6
        
        # 计算 PSI
        psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
        
        # PSI 解释: < 0.1 无漂移, 0.1-0.25 轻微漂移, > 0.25 显著漂移
        is_drifted = psi > 0.25
        
        return DriftResult(
            drift_type=DriftType.FEATURE_DRIFT,
            feature_name=feature_name,
            statistic=psi,
            p_value=1 - psi if psi < 1 else 0,  # 近似
            threshold=0.25,
            is_drifted=is_drifted,
            details={
                "test": "PSI",
                "psi_value": psi,
                "interpretation": (
                    "No significant shift" if psi < 0.1 
                    else "Moderate shift" if psi < 0.25 
                    else "Significant shift"
                )
            }
        )


class EvidentlyAIDriftReport:
    """使用 Evidently AI 生成漂移报告"""
    
    @staticmethod
    def generate_report(reference_df: pd.DataFrame, current_df: pd.DataFrame,
                         output_path: str = "drift_report.html"):
        """生成完整的漂移报告"""
        try:
            from evidently.report import Report
            from evidently.metric_preset import DataDriftPreset, DataQualityPreset
            from evidently.metrics import DatasetDriftMetric
            
            report = Report(metrics=[
                DataDriftPreset(),
                DataQualityPreset(),
                DatasetDriftMetric(),
            ])
            
            report.run(reference_data=reference_df, current_data=current_df)
            report.save_html(output_path)
            
            print(f"Drift report saved to {output_path}")
            return output_path
        
        except ImportError:
            print("请安装 evidently: pip install evidently")
            return None


class DriftAlertManager:
    """漂移告警管理"""
    
    def __init__(self, alert_channels: List[str] = None):
        self.alert_channels = alert_channels or ["log"]
        self.alert_history = []
    
    def check_and_alert(self, drift_results: List[DriftResult]):
        """检查漂移结果并发送告警"""
        drifted_features = [r for r in drift_results if r.is_drifted]
        
        if not drifted_features:
            return
        
        alert = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "n_features_drifted": len(drifted_features),
            "total_features": len(drift_results),
            "drift_rate": len(drifted_features) / len(drift_results),
            "drifted_features": [
                {
                    "feature": r.feature_name,
                    "statistic": r.statistic,
                    "p_value": r.p_value,
                }
                for r in drifted_features
            ]
        }
        
        self.alert_history.append(alert)
        
        # 告警判断
        drift_rate = alert["drift_rate"]
        if drift_rate > 0.5:
            self._send_critical_alert(alert)
        elif drift_rate > 0.2:
            self._send_warning_alert(alert)
        else:
            self._send_info_alert(alert)
    
    def _send_critical_alert(self, alert: dict):
        """严重告警"""
        msg = (
            f"🚨 严重数据漂移告警\n"
            f"漂移率: {alert['drift_rate']:.1%}\n"
            f"漂移特征数: {alert['n_features_drifted']}/{alert['total_features']}\n"
            f"建议: 立即检查数据源并考虑重训练模型"
        )
        self._dispatch_alert(msg, level="critical")
    
    def _send_warning_alert(self, alert: dict):
        """警告告警"""
        msg = (
            f"⚠️ 数据漂移警告\n"
            f"漂移率: {alert['drift_rate']:.1%}\n"
            f"漂移特征: {[f['feature'] for f in alert['drifted_features']]}"
        )
        self._dispatch_alert(msg, level="warning")
    
    def _send_info_alert(self, alert: dict):
        """信息告警"""
        msg = f"ℹ️ 轻微漂移: {alert['n_features_drifted']} 个特征"
        self._dispatch_alert(msg, level="info")
    
    def _dispatch_alert(self, message: str, level: str):
        """分发告警到各渠道"""
        for channel in self.alert_channels:
            if channel == "log":
                print(f"[{level.upper()}] {message}")
            elif channel == "slack":
                self._send_slack(message, level)
            elif channel == "email":
                self._send_email(message, level)
    
    def _send_slack(self, message: str, level: str):
        """发送 Slack 告警"""
        import requests
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if webhook_url:
            color = {"critical": "#ff0000", "warning": "#ffaa00", "info": "#36a64f"}[level]
            payload = {
                "attachments": [{
                    "color": color,
                    "text": message,
                    "ts": int(pd.Timestamp.now().timestamp())
                }]
            }
            requests.post(webhook_url, json=payload)
    
    def _send_email(self, message: str, level: str):
        """发送邮件告警（简化实现）"""
        pass  # 实际实现使用 smtplib
```

### 10.3 Prometheus 监控指标

```python
"""
Prometheus 指标暴露
"""
from prometheus_client import Counter, Histogram, Gauge, Summary, CollectorRegistry
import time
import numpy as np

# 注册表
registry = CollectorRegistry()

# ============= 推理指标 =============
PREDICTION_COUNTER = Counter(
    "model_predictions_total",
    "Total number of predictions",
    ["model_name", "model_version", "prediction_class"],
    registry=registry
)

PREDICTION_LATENCY = Histogram(
    "model_prediction_latency_seconds",
    "Prediction latency in seconds",
    ["model_name", "endpoint"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
    registry=registry
)

PREDICTION_CONFIDENCE = Histogram(
    "model_prediction_confidence",
    "Distribution of prediction confidence scores",
    ["model_name"],
    buckets=np.arange(0, 1.05, 0.05).tolist(),
    registry=registry
)

BATCH_SIZE = Histogram(
    "model_batch_size",
    "Distribution of batch sizes",
    ["model_name"],
    buckets=[1, 2, 4, 8, 16, 32, 64, 128, 256],
    registry=registry
)

# ============= 数据质量指标 =============
FEATURE_NULL_RATE = Gauge(
    "model_feature_null_rate",
    "Rate of null values per feature",
    ["feature_name", "model_name"],
    registry=registry
)

DRIFT_SCORE = Gauge(
    "model_drift_score",
    "Data drift score per feature",
    ["feature_name", "model_name", "test_type"],
    registry=registry
)

# ============= 系统指标 =============
ACTIVE_CONNECTIONS = Gauge(
    "model_active_connections",
    "Number of active connections",
    registry=registry
)

MODEL_LOAD_TIME = Summary(
    "model_load_time_seconds",
    "Time taken to load model",
    ["model_name"],
    registry=registry
)

GPU_MEMORY_USAGE = Gauge(
    "model_gpu_memory_bytes",
    "GPU memory usage in bytes",
    ["gpu_id", "model_name"],
    registry=registry
)


class MetricsCollector:
    """指标收集装饰器"""
    
    @staticmethod
    def track_prediction(model_name: str, model_version: str):
        """追踪预测调用"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = await func(*args, **kwargs)
                    
                    # 记录指标
                    PREDICTION_COUNTER.labels(
                        model_name=model_name,
                        model_version=model_version,
                        prediction_class=str(result.get("class", "unknown"))
                    ).inc()
                    
                    if "confidence" in result:
                        PREDICTION_CONFIDENCE.labels(model_name=model_name).observe(
                            result["confidence"]
                        )
                    
                    return result
                finally:
                    latency = time.time() - start_time
                    PREDICTION_LATENCY.labels(
                        model_name=model_name,
                        endpoint="predict"
                    ).observe(latency)
            
            return wrapper
        return decorator
    
    @staticmethod
    def update_drift_metrics(drift_results: list, model_name: str):
        """更新漂移指标"""
        for result in drift_results:
            DRIFT_SCORE.labels(
                feature_name=result.feature_name,
                model_name=model_name,
                test_type=result.details.get("test", "unknown")
            ).set(result.statistic)
```

### 10.4 Grafana 仪表盘配置

```json
{
  "dashboard": {
    "title": "ML Model Monitoring",
    "panels": [
      {
        "title": "Prediction Rate (QPS)",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(model_predictions_total[5m])",
            "legendFormat": "{{model_name}} v{{model_version}}"
          }
        ]
      },
      {
        "title": "Prediction Latency (P99)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(model_prediction_latency_seconds_bucket[5m]))",
            "legendFormat": "P99 {{model_name}}"
          }
        ]
      },
      {
        "title": "Prediction Confidence Distribution",
        "type": "histogram",
        "targets": [
          {
            "expr": "model_prediction_confidence_bucket",
            "legendFormat": "{{model_name}}"
          }
        ]
      },
      {
        "title": "Data Drift Score",
        "type": "heatmap",
        "targets": [
          {
            "expr": "model_drift_score",
            "legendFormat": "{{feature_name}}"
          }
        ]
      },
      {
        "title": "Feature Null Rate",
        "type": "table",
        "targets": [
          {
            "expr": "model_feature_null_rate",
            "legendFormat": "{{feature_name}}"
          }
        ]
      }
    ]
  }
}
```

---

## 11. CI/CD for ML

### 11.1 GitHub Actions 完整流水线

```yaml
# .github/workflows/ml-cicd.yml
name: ML CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      force_retrain:
        description: 'Force model retraining'
        required: false
        default: 'false'

env:
  PYTHON_VERSION: '3.11'
  MODEL_REGISTRY: ${{ secrets.MODEL_REGISTRY }}
  AWS_REGION: us-east-1

jobs:
  # ============= 代码质量检查 =============
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      
      - name: Lint
        run: |
          ruff check src/ --output-format=github
          mypy src/ --ignore-missing-imports
      
      - name: Unit Tests
        run: |
          pytest tests/unit/ -v --cov=src --cov-report=xml --cov-report=html
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
      
      - name: Security Scan
        run: |
          bandit -r src/ -f json -o bandit_report.json || true
          safety check --json || true

  # ============= 数据验证 =============
  validate-data:
    runs-on: ubuntu-latest
    needs: lint-and-test
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate Data Schema
        run: |
          python scripts/validate_data.py \
            --input ${{ vars.DATA_PATH }} \
            --config config/data_validation.yaml \
            --output data_validation_report.json
      
      - name: Check Data Quality
        run: |
          python scripts/data_quality_check.py \
            --input ${{ vars.DATA_PATH }} \
            --thresholds config/quality_thresholds.yaml
      
      - name: Upload Validation Report
        uses: actions/upload-artifact@v4
        with:
          name: data-validation-report
          path: data_validation_report.json

  # ============= 模型训练 =============
  train-model:
    runs-on: ubuntu-latest
    needs: validate-data
    if: github.ref == 'refs/heads/main' || github.event.inputs.force_retrain == 'true'
    outputs:
      model_version: ${{ steps.train.outputs.model_version }}
      val_accuracy: ${{ steps.evaluate.outputs.val_accuracy }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Train Model
        id: train
        run: |
          python src/train.py \
            --config config/train_config.yaml \
            --experiment-name ${{ github.run_id }}
          echo "model_version=$(cat model_version.txt)" >> $GITHUB_OUTPUT
      
      - name: Evaluate Model
        id: evaluate
        run: |
          python src/evaluate.py \
            --model-path models/latest \
            --output evaluation_report.json
          ACCURACY=$(python -c "import json; print(json.load(open('evaluation_report.json'))['val_accuracy'])")
          echo "val_accuracy=$ACCURACY" >> $GITHUB_OUTPUT
      
      - name: Check Model Quality Gate
        run: |
          python scripts/check_quality_gate.py \
            --report evaluation_report.json \
            --thresholds config/quality_gate.yaml
      
      - name: Upload Model Artifact
        uses: actions/upload-artifact@v4
        with:
          name: trained-model
          path: models/latest/
      
      - name: Register in MLflow
        run: |
          python src/register_model.py \
            --model-path models/latest \
            --model-name fraud-detector \
            --version ${{ steps.train.outputs.model_version }}
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}

  # ============= 构建容器 =============
  build-container:
    runs-on: ubuntu-latest
    needs: train-model
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Download Model
        uses: actions/download-artifact@v4
        with:
          name: trained-model
          path: models/latest/
      
      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ needs.train-model.outputs.model_version }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ============= 部署到 Staging =============
  deploy-staging:
    runs-on: ubuntu-latest
    needs: [train-model, build-container]
    environment: staging
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure K8s
        uses: azure/k8s-set-context@v4
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}
      
      - name: Deploy to Staging
        run: |
          kubectl set image deployment/ml-model-serving \
            model-server=ghcr.io/${{ github.repository }}:${{ needs.train-model.outputs.model_version }} \
            -n ml-staging
          kubectl rollout status deployment/ml-model-serving -n ml-staging --timeout=300s
      
      - name: Run Integration Tests
        run: |
          python tests/integration/test_endpoint.py \
            --endpoint ${{ secrets.STAGING_ENDPOINT }} \
            --timeout 300

  # ============= 部署到 Production =============
  deploy-production:
    runs-on: ubuntu-latest
    needs: [train-model, deploy-staging]
    environment: production
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure K8s
        uses: azure/k8s-set-context@v4
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
      
      - name: Canary Deploy
        run: |
          # 部署 canary 版本 (10% 流量)
          kubectl apply -f k8s/canary/ -n ml-production
          kubectl set image deployment/ml-model-canary \
            model-server=ghcr.io/${{ github.repository }}:${{ needs.train-model.outputs.model_version }} \
            -n ml-production
      
      - name: Monitor Canary
        run: |
          python scripts/monitor_canary.py \
            --duration 300 \
            --error-threshold 0.01 \
            --latency-threshold 200
      
      - name: Promote to Full
        run: |
          kubectl set image deployment/ml-model-serving \
            model-server=ghcr.io/${{ github.repository }}:${{ needs.train-model.outputs.model_version }} \
            -n ml-production
          kubectl rollout status deployment/ml-model-serving -n ml-production --timeout=600s
      
      - name: Cleanup Canary
        if: always()
        run: kubectl delete -f k8s/canary/ -n ml-production || true

  # ============= 通知 =============
  notify:
    runs-on: ubuntu-latest
    needs: [train-model, deploy-production]
    if: always()
    steps:
      - name: Slack Notification
        uses: slackapi/slack-github-action@v1.24
        with:
          payload: |
            {
              "text": "ML Pipeline ${{ job.status }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*ML Pipeline Result: ${{ job.status }}*\nModel: ${{ needs.train-model.outputs.model_version }}\nAccuracy: ${{ needs.train-model.outputs.val_accuracy }}\nRun: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### 11.2 GitLab CI/CD 示例

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - test
  - build
  - deploy-staging
  - evaluate-staging
  - deploy-production

variables:
  PYTHON_VERSION: "3.11"
  DOCKER_REGISTRY: $CI_REGISTRY_IMAGE
  MODEL_NAME: "fraud-detector"

# ============= 模板 =============
.python_setup: &python_setup
  image: python:${PYTHON_VERSION}-slim
  before_script:
    - pip install -r requirements-dev.txt

# ============= 数据验证 =============