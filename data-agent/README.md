# Data Agent - 数据领域智能助手

基于 RAG + Embedding + VectorDB + Text2SQL 的数据分析Agent

## 🌟 功能特性

- 🤖 **自然语言转SQL** - 将用户问题转换为SQL查询
- 📊 **数据分析** - 支持聚合、比较、趋势分析等
- 🔍 **RAG增强** - 基于向量检索的Schema理解和示例检索
- 💬 **多轮对话** - 支持上下文理解的连续查询
- 🛡️ **安全执行** - SQL验证、防注入、权限控制
- 📖 **结果解读** - 自动生成查询结果的自然语言解释
- 🎯 **Few-shot学习** - 动态检索相似示例提升准确率

## 📁 项目结构

```
data-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py          # 主Agent逻辑
│   ├── config.py         # 配置管理
│   ├── models.py         # 数据模型
│   ├── llm.py           # LLM服务
│   ├── embedding.py     # Embedding服务
│   ├── vector_store.py  # 向量数据库
│   ├── schema_loader.py # Schema加载器
│   ├── sql_generator.py # SQL生成器
│   ├── sql_executor.py  # SQL执行器
│   ├── prompts.py       # Prompt模板
│   └── utils.py         # 工具函数
├── tests/
│   └── test_agent.py    # 测试用例
├── docs/
│   └── text2sql-knowledge.md  # Text2SQL知识体系
├── main.py              # 主入口
├── requirements.txt     # 依赖
└── README.md           # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd data-agent
pip install -r requirements.txt
```

### 2. 配置API密钥

编辑 `src/config.py` 或设置环境变量：

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # 可选
export OPENAI_MODEL="gpt-4o-mini"  # 可选
```

### 3. 运行

```bash
python main.py
```

## 💡 使用示例

### 交互式模式

```bash
📝 你的问题: 上个月销售额是多少？

🤔 思考中...

💡 SQL:
SELECT SUM(total_amount) AS monthly_sales 
FROM orders 
WHERE order_date >= date('now', '-1 month') 
  AND status != 'cancelled'

📖 解释: 统计上个月非取消订单的总金额

⏱️ 执行时间: 2.34ms

📊 结果:
查询结果: 125,680.50
```

### 代码调用

```python
from src.agent import DataAgent

# 创建Agent
agent = DataAgent()

# 加载Schema
ddl = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
);
"""
agent.load_schema_from_ddl(ddl)

# 添加示例
agent.add_example(
    "有多少用户？",
    "SELECT COUNT(*) FROM users",
    "统计总用户数"
)

# 提问
result = agent.ask("20岁以上的用户有多少？")
print(result["sql"])
print(result["interpretation"])
```

## 🔧 配置说明

### LLM配置

```python
from src.config import LLMConfig

llm_config = LLMConfig(
    api_key="sk-...",
    base_url="https://api.openai.com/v1",  # 或其他兼容API
    model="gpt-4o-mini",  # 或 gpt-4, gpt-3.5-turbo
    temperature=0.1,
    max_tokens=2000
)
```

### 数据库配置

```python
from src.config import DatabaseConfig

# SQLite
db_config = DatabaseConfig(
    db_type="sqlite",
    connection_string="sqlite:///./data.db"
)

# PostgreSQL
db_config = DatabaseConfig(
    db_type="postgresql",
    connection_string="postgresql://user:pass@host:5432/dbname"
)
```

### 完整配置

```python
from src.config import AgentConfig, LLMConfig, EmbeddingConfig, DatabaseConfig

config = AgentConfig(
    llm=LLMConfig(api_key="sk-..."),
    embedding=EmbeddingConfig(api_key="sk-...", model="text-embedding-3-small"),
    database=DatabaseConfig(connection_string="sqlite:///./data.db"),
    max_retries=3,
    enable_sql_validation=True,
    enable_multi_turn=True
)

agent = DataAgent(config)
```

## 📊 支持的查询类型

- **统计查询**: "有多少..."、"总数"
- **聚合分析**: "平均值"、"总和"、"最大/最小"
- **排名查询**: "前N个"、"最高"、"最多"
- **分组统计**: "每个...有多少"
- **条件过滤**: "满足...条件的"
- **多表关联**: 自动JOIN相关表
- **时间分析**: "上个月"、"今年"、"趋势"
- **对比分析**: "对比"、"同比"、"环比"

## 🛠️ 高级功能

### 自定义Schema

```python
from src.models import SchemaInfo, TableInfo, ColumnInfo

schema = SchemaInfo()
table = TableInfo(
    name="custom_table",
    columns=[
        ColumnInfo(name="id", data_type="INTEGER", is_primary_key=True),
        ColumnInfo(name="value", data_type="DECIMAL(10,2)", comment="金额"),
    ],
    comment="自定义业务表"
)
schema.tables.append(table)

agent.current_schema = schema
agent._index_schema()
```

### 批量添加示例

```python
examples = [
    {
        "question": "问题1",
        "sql": "SELECT ...",
        "explanation": "解释1"
    },
    {
        "question": "问题2",
        "sql": "SELECT ...",
        "explanation": "解释2"
    }
]
agent.add_examples_batch(examples)
```

### 直接执行SQL

```python
result = agent.execute_sql("SELECT COUNT(*) FROM users")
print(result.to_markdown())
```

### 对话历史管理

```python
# 获取对话历史
history = agent.get_conversation_history(session_id)

# 清除对话
agent.clear_conversation(session_id)
```

## 🧪 测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_agent.py::test_agent_creation

# 详细输出
pytest tests/ -v
```

## 📚 参考项目

- [Vanna](https://github.com/vanna-ai/vanna) - RAG-based Text2SQL
- [DB-GPT](https://github.com/eosphoros-ai/DB-GPT) - 全栈数据智能平台
- [SQLCoder](https://github.com/defog/sqlcoder) - Text2SQL专用模型
- [DAIL-SQL](https://github.com/BeachWang/DAIL-SQL) - Few-shot优化

## 🔐 安全说明

- ✅ 默认禁止DELETE/UPDATE/DROP等修改操作
- ✅ SQL注入检测
- ✅ 多语句执行限制
- ⚠️ 生产环境建议启用数据库权限控制
- ⚠️ 敏感数据查询添加审计日志

## 📝 TODO

- [ ] 支持更多数据库方言
- [ ] 添加可视化图表生成
- [ ] 实现查询性能优化建议
- [ ] 添加用户反馈学习机制
- [ ] 支持更复杂的子查询和窗口函数
- [ ] 添加缓存机制提升性能

## 📄 License

MIT

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**版本**: 0.1.0  
**作者**: Data Agent Team  
**日期**: 2026-06-10
