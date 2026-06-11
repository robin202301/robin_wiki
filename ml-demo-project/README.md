# 🤖 ML Demo: 加州房价预测 - 全流程实战

**从训练到部署到持续训练优化的完整机器学习项目**

## 📋 项目概述

使用 California Housing 数据集构建房价预测模型，涵盖完整 MLOps 流程：

```
数据处理 → 特征工程 → 模型训练 → 模型评估 → 模型服务化 → Docker部署 → 监控 → 持续训练
```

## 🏗️ 项目架构

```
┌─────────────────────────────────────────────────────────────┐
│                      CI/CD Pipeline                         │
│  GitHub Actions: 自动训练 → 测试 → 构建 → 部署              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Docker Compose 部署                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │  FastAPI  │  │  MLflow  │  │ Prometheus│  │  Grafana   │ │
│  │  :8000    │  │  :5000   │  │  :9090    │  │  :3000     │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    ML Pipeline                               │
│  数据加载 → 预处理 → 特征工程 → 训练 → 评估 → 注册模型      │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 1. 本地开发

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行训练
python -m src.models.train

# 启动 API
uvicorn api.main:app --reload --port 8000
```

### 2. Docker 部署

```bash
# 一键启动全部服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f api
```

### 3. 使用 API

```bash
# 健康检查
curl http://localhost:8000/health

# 预测
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.32, 41, 6.98, 1.02, 322, 2.56, 37.88, -122.23]}'

# 批量预测
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"samples": [[8.32, 41, 6.98, 1.02, 322, 2.56, 37.88, -122.23], [7.25, 30, 5.0, 1.0, 200, 2.0, 35.0, -121.5]]}'

# 触发重训练
curl -X POST http://localhost:8000/retrain
```

## 📁 项目结构

```
ml-demo-project/
├── README.md                       # 项目说明
├── requirements.txt                # Python 依赖
├── Dockerfile                      # API 生产镜像
├── Dockerfile.training             # 训练镜像
├── docker-compose.yml              # 服务编排
├── .dockerignore                   # Docker 忽略文件
├── Makefile                        # 常用命令快捷方式
├── config/
│   └── config.yaml                 # 训练和服务配置
├── src/
│   ├── data/
│   │   └── preprocess.py           # 数据加载与预处理
│   ├── models/
│   │   ├── train.py                # 模型训练
│   │   ├── evaluate.py             # 模型评估
│   │   └── predict.py              # 预测封装
│   ├── pipeline/
│   │   └── pipeline.py             # 完整 ML Pipeline
│   ├── monitoring/
│   │   └── drift_detector.py       # 数据漂移检测
│   └── utils/
│       └── helpers.py              # 工具函数
├── api/
│   ├── main.py                     # FastAPI 入口
│   ├── schemas.py                  # 数据模型
│   └── routes/
│       ├── predict.py              # 预测 API
│       ├── health.py               # 健康检查
│       └── retrain.py              # 重训练触发
├── tests/
│   ├── test_data.py                # 数据测试
│   ├── test_model.py               # 模型测试
│   └── test_api.py                 # API 测试
├── scripts/
│   ├── retrain.sh                  # 重训练脚本
│   ├── check_drift.py              # 漂移检查
│   └── compare_models.py           # 模型对比
└── .github/
    └── workflows/
        ├── ci-train.yml            # 训练 CI
        └── cd-deploy.yml           # 部署 CD
```

## 📊 数据集

**California Housing** (sklearn 内置)
- 20,640 条记录
- 8 个特征 + 1 个目标值 (房价中位数)
- 特征：收入中位数、房屋年龄中位数、平均房间数等

| 特征 | 说明 |
|------|------|
| MedInc | 街区收入中位数 |
| HouseAge | 房屋年龄中位数 |
| AveRooms | 平均房间数 |
| AveBedrms | 平均卧室数 |
| Population | 街区人口 |
| AveOccup | 平均入住人数 |
| Latitude | 纬度 |
| Longitude | 经度 |

## 🔄 MLOps 流程

### 持续训练触发条件
1. **定时触发**: 每天/每周自动运行
2. **数据漂移**: 检测到输入数据分布变化
3. **性能退化**: 生产模型指标低于阈值
4. **手动触发**: 通过 API 或 CI 手动触发

### 模型优化策略
- 超参数调优 (Optuna)
- 特征工程迭代
- 模型集成
- 在线学习 (增量训练)

## 📈 监控指标

| 指标 | 说明 | 阈值 |
|------|------|------|
| MAE | 平均绝对误差 | < 0.5 |
| RMSE | 均方根误差 | < 0.7 |
| R² | 决定系数 | > 0.75 |
| PSI | 种群稳定指数 | < 0.2 |
| Latency P99 | 预测延迟 | < 100ms |

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| ML 框架 | scikit-learn, LightGBM, XGBoost |
| 超参调优 | Optuna |
| 实验追踪 | MLflow |
| API 服务 | FastAPI |
| 容器化 | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| 监控 | Prometheus, Grafana |
| 测试 | pytest |
