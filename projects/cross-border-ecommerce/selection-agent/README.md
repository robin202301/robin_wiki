# 选品Agent - 跨境电商AI选品系统

> 精品配饰 × 美妆工具 | 东南亚 × 俄罗斯 | AI视频引流

## 功能

- 📦 **选品管理** - 产品录入 + 多维度自动评分
- 📊 **利润计算** - 各平台/市场利润分析
- 🌐 **Listing生成** - LLM多语言商品文案
- 🎬 **视频脚本** - AI生成多语言短视频脚本
- 📱 **移动端UI** - PWA适配手机操作

## 选品漏斗

```
L1 数据海选 → L2 数据筛选 → L3 AI评估 → L4 小批量测品 → L5 爆品放大
```

## 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 视频适配 | 25% | 是否适合AI视频展示 |
| 利润潜力 | 30% | 基于成本/重量/品类毛利 |
| 竞争优势 | 20% | 竞争程度（越高=竞争越小） |
| 趋势匹配 | 15% | 市场趋势对齐度 |
| 供应链 | 10% | 供应稳定性评估 |

## 快速部署

### Docker (推荐)

```bash
# 1. 复制环境变量
cp .env.example .env

# 2. 编辑 .env，填入你的 LLM API Key
vi .env

# 3. 启动
docker compose up -d

# 4. 访问
open http://localhost:8000
```

### 本地运行

```bash
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入 LLM API Key
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 手机访问

服务启动后，手机和电脑在同一WiFi下，手机浏览器访问：
```
http://<电脑IP>:8000
```

或添加到主屏幕作为PWA应用。

## LLM 配置

支持任何 OpenAI 兼容接口：

```bash
# OpenAI
LLM_API_BASE=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

# DeepSeek
LLM_API_BASE=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# 通义千问
LLM_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus

# 本地 Ollama
LLM_API_BASE=http://host.docker.internal:11434/v1
LLM_MODEL=qwen2.5
```

## API 文档

启动后访问 `http://localhost:8000/docs` 查看完整 API 文档 (Swagger UI)。

### 主要接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/products/` | 添加产品（自动评分） |
| GET | `/products/` | 产品列表（支持筛选） |
| POST | `/analysis/profit` | 利润计算 |
| GET | `/analysis/price-suggestion/{id}` | 定价建议 |
| POST | `/listings/generate` | 生成多语言Listing |
| POST | `/listings/video-script/{id}` | 生成视频脚本 |
| POST | `/listings/analyze/{id}` | AI分析产品 |

## 项目结构

```
selection-agent/
├── app/
│   ├── main.py           # FastAPI 入口
│   ├── config.py          # 配置管理
│   ├── database.py        # 数据库
│   ├── models.py          # 数据模型
│   ├── schemas.py         # Pydantic Schema
│   ├── routers/
│   │   ├── products.py    # 产品管理
│   │   ├── analysis.py    # 利润分析
│   │   └── listing.py     # Listing/脚本生成
│   ├── services/
│   │   ├── scorer.py      # 评分引擎
│   │   ├── profit.py      # 利润计算
│   │   └── llm.py         # LLM 服务
│   └── static/
│       └── index.html     # 移动端 UI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## TODO

- [ ] 1688商品链接自动解析
- [ ] 竞品监控爬虫
- [ ] TikTok/Shopee趋势数据接入
- [ ] 批量选品导入
- [ ] 数据导出 (Excel)
- [ ] Agent协同决策
- [ ] 视频效果追踪反馈闭环
