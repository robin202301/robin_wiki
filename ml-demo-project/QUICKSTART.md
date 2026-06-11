# 🚀 快速开始指南

## 1️⃣ 环境准备

```bash
# 进入项目目录
cd ml-demo-project

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

## 2️⃣ 训练模型

```bash
# 标准训练（推荐首次使用）
python -m src.models.train

# 或运行完整 Pipeline
python -m src.pipeline.pipeline

# 超参数调优模式
python -m src.models.train --tune
```

## 3️⃣ 启动 API 服务

```bash
# 开发模式
uvicorn api.main:app --reload --port 8000

# 或
make serve
```

访问 http://localhost:8000/docs 查看 API 文档

## 4️⃣ 测试 API

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

# 模型信息
curl http://localhost:8000/model/info

# 触发重训练
curl -X POST http://localhost:8000/retrain \
  -H "Content-Type: application/json" \
  -d '{"force": false}'
```

## 5️⃣ Docker 部署

```bash
# 一键启动全部服务（API + MLflow + Prometheus + Grafana）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

服务访问：
- API: http://localhost:8000
- MLflow: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## 6️⃣ 运行测试

```bash
# 全部测试
pytest tests/ -v

# 带覆盖率
pytest tests/ -v --cov=src --cov=api

# 或使用 Makefile
make test
```

## 7️⃣ 持续训练

```bash
# 手动触发重训练
./scripts/retrain.sh

# 带超参数调优
./scripts/retrain.sh --tune

# 强制重训练（跳过漂移检查）
./scripts/retrain.sh --force

# 检查数据漂移
python scripts/check_drift.py

# 对比模型性能
python scripts/compare_models.py
```

## 📊 项目结构

```
ml-demo-project/
├── src/                    # 核心源码
│   ├── data/              # 数据处理
│   ├── models/            # 模型训练/评估/预测
│   ├── pipeline/          # 完整 Pipeline
│   ├── monitoring/        # 漂移检测
│   └── utils/             # 工具函数
├── api/                   # FastAPI 服务
├── tests/                 # 测试
├── scripts/               # 脚本
├── config/                # 配置
├── models/                # 模型输出
├── monitoring/            # 监控配置
└── .github/workflows/     # CI/CD
```

## 🎯 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 训练 | `python -m src.models.train` | 训练 3 个模型并选最佳 |
| 评估 | `python -m src.models.evaluate` | 生成评估报告 |
| Pipeline | `python -m src.pipeline.pipeline` | 完整流程 |
| 漂移检测 | `python scripts/check_drift.py` | 检查数据漂移 |
| API 服务 | `uvicorn api.main:app` | 启动预测服务 |
| Docker | `docker-compose up` | 容器化部署 |

## 📝 下一步

1. **探索代码**: 阅读 `src/` 下的模块，理解数据流
2. **调整配置**: 修改 `config/config.yaml` 调整超参数
3. **添加新模型**: 在 `src/models/train.py` 的 `MODEL_REGISTRY` 添加
4. **自定义特征**: 修改 `src/data/preprocess.py` 的 `feature_engineering`
5. **监控集成**: 配置 Grafana 仪表盘展示指标

## 🔧 常见问题

**Q: 模型训练失败？**
```bash
# 检查依赖
pip install -r requirements.txt

# 清除缓存
make clean
```

**Q: API 启动失败？**
```bash
# 确保已训练模型
python -m src.models.train

# 检查端口占用
lsof -i :8000
```

**Q: Docker 构建失败？**
```bash
# 清理旧镜像
docker-compose down -v

# 重新构建
docker-compose build --no-cache
```

## 📚 扩展学习

- 添加更多模型（XGBoost、神经网络）
- 实现增量学习
- 集成 A/B 测试框架
- 添加模型解释性（SHAP）
- 实现实时特征存储

---

**祝你学习愉快！** 🎉
