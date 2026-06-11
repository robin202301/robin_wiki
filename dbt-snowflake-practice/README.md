# dbt + Snowflake 实战项目

这是一个完整的 dbt + Snowflake 实战练习项目，使用电商数据集进行数据建模和转换。

## 📋 项目概述

本项目模拟真实电商数据分析场景，包含：
- 订单数据
- 客户数据
- 产品数据
- 数据仓库分层建模（Staging → Intermediate → Mart）

## 🎯 学习目标

1. 掌握 dbt 项目结构和配置
2. 学习 Snowflake 数据仓库连接和配置
3. 实践数据仓库分层建模（Raw → Staging → Intermediate → Mart）
4. 掌握 dbt 测试、文档、宏等核心功能
5. 熟悉 Git 工作流管理 dbt 项目

## 📦 数据集说明

使用模拟电商数据（包含在 `seeds/` 目录）：
- `raw_customers.csv` - 客户基础信息
- `raw_orders.csv` - 订单数据
- `raw_products.csv` - 产品信息
- `raw_order_items.csv` - 订单明细

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd dbt-snowflake-practice

# 创建虚拟环境
python -m venv dbt-env
source dbt-env/bin/activate  # Linux/Mac
# 或 dbt-env\Scripts\activate  # Windows

# 安装 dbt-snowflake
pip install dbt-snowflake
```

### 2. 配置 Snowflake

编辑 `~/.dbt/profiles.yml`（或项目根目录的 `profiles.yml`）：

```yaml
dbt_snowflake_practice:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <your-account-id>  # 例如: xy12345.us-east-1
      user: <your-username>
      password: <your-password>
      role: <your-role>
      database: <your-database>
      warehouse: <your-warehouse>
      schema: <your-schema>
      threads: 4
```

### 3. 测试连接

```bash
dbt debug
```

### 4. 加载种子数据

```bash
dbt seed
```

### 5. 运行模型

```bash
# 运行所有模型
dbt run

# 运行特定模型
dbt run --models staging

# 增量运行
dbt run --select state:modified
```

### 6. 运行测试

```bash
dbt test
```

### 7. 生成文档

```bash
dbt docs generate
dbt docs serve
```

## 📁 项目结构

```
dbt-snowflake-practice/
├── README.md
├── dbt_project.yml          # dbt 项目配置
├── profiles.yml              # 数据库连接配置（模板）
├── packages.yml              # 依赖包配置
├── .gitignore               # Git 忽略文件
├── models/
│   ├── staging/             # Staging 层：原始数据清洗
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   └── stg_products.sql
│   ├── intermediate/        # Intermediate 层：业务逻辑转换
│   │   └── int_orders_enriched.sql
│   └── marts/               # Mart 层：业务报表
│       ├── customers.sql
│       ├── orders_daily.sql
│       └── products_performance.sql
├── seeds/                   # 种子数据
│   ├── raw_customers.csv
│   ├── raw_orders.csv
│   ├── raw_products.csv
│   └── raw_order_items.csv
├── tests/                   # 自定义测试
│   └── test_order_amounts.sql
├── macros/                  # 可复用 SQL 宏
│   └── cents_to_dollars.sql
└── analyses/                # 临时分析查询
    └── customer_ltv.sql
```

## 🏗️ 数据模型分层

### Staging 层
- 从原始表（seeds）读取
- 基础数据清洗和类型转换
- 字段重命名和标准化
- 1:1 映射，保持原始粒度

### Intermediate 层
- 数据关联和聚合
- 业务逻辑转换
- 为 Mart 层准备数据

### Mart 层
- 业务指标计算
- 面向分析的宽表
- 直接用于 BI 报表

## 🔧 常用命令

```bash
# 调试配置
dbt debug

# 加载种子数据
dbt seed

# 运行模型
dbt run
dbt run --models +orders_daily  # 运行依赖链

# 测试
dbt test
dbt test --models customers

# 文档
dbt docs generate
dbt docs serve --port 8081

# 增量运行
dbt run --select state:modified

# 编译（查看生成的 SQL）
dbt compile --models stg_customers
```

## 📚 学习资源

- [dbt 官方文档](https://docs.getdbt.com/)
- [Snowflake 文档](https://docs.snowflake.com/)
- [dbt 最佳实践](https://docs.getdbt.com/guides/best-practices)

## 🎓 练习任务

完成基础设置后，尝试以下练习：

1. **添加新模型**：创建一个 `monthly_sales` 模型
2. **编写测试**：为 `customers` 模型添加自定义测试
3. **使用宏**：创建一个计算客户 LTV 的宏
4. **增量模型**：将 `orders_daily` 改为增量模型
5. **快照**：为 `customers` 表创建 SCD Type 2 快照

## ❓ 常见问题

**Q: 如何获取 Snowflake 账户？**
A: 注册 [Snowflake 免费试用](https://signup.snowflake.com/)，可获得 30 天免费额度。

**Q: 连接失败怎么办？**
A: 运行 `dbt debug` 查看详细信息，检查账户 ID、用户名、密码是否正确。

**Q: 种子数据加载失败？**
A: 确保 CSV 文件格式正确，字段类型与 `dbt_project.yml` 中的配置匹配。

## 📝 License

MIT License - 仅供学习和练习使用
