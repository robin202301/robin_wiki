# dbt 完整知识体系

> Data Build Tool - 数据转换的最佳实践
> 更新时间：2026-06-10

---

## 📚 目录

1. [dbt 概述](#1-dbt-概述)
2. [核心概念](#2-核心概念)
3. [项目结构](#3-项目结构)
4. [Models](#4-models)
5. [Tests](#5-tests)
6. [Documentation](#6-documentation)
7. [Jinja 模板](#7-jinja-模板)
8. [Sources](#8-sources)
9. [Snapshots](#9-snapshots)
10. [Seeds](#10-seeds)
11. [Macros](#11-macros)
12. [Packages](#12-packages)
13. [环境变量](#13-环境变量)
14. [部署与 CI/CD](#14-部署与-cicd)
15. [最佳实践](#15-最佳实践)

---

## 1. dbt 概述

### 什么是 dbt

dbt (Data Build Tool) 是一个**数据转换工具**，让数据分析师和工程师可以使用 **SQL + Jinja** 来构建数据仓库的转换逻辑。

**核心理念：**
- ✅ **SQL 优先**：使用熟悉的 SQL 编写转换逻辑
- ✅ **版本控制**：所有代码纳入 Git 管理
- ✅ **测试驱动**：内置数据测试框架
- ✅ **文档自动生成**：自动从代码生成文档
- ✅ **依赖管理**：自动处理模型间依赖关系
- ✅ **软件工程最佳实践**：代码复用、模块化、CI/CD

### dbt 工作原理

```
Raw Data (原始数据)
    ↓
dbt Models (转换逻辑)
    ↓
Transformed Data (转换后的数据)
    ↓
BI Tools / Analytics (分析和报表)
```

**dbt 不做的事：**
- ❌ 不提取数据 (Extract)
- ❌ 不加载数据 (Load)
- ✅ 只做转换 (Transform)

### dbt 版本

| 版本 | 说明 | 适用场景 |
|------|------|----------|
| **dbt Core** | 开源版本 | 本地开发、小型团队 |
| **dbt Cloud** | 商业版本 | 企业级、团队协作、调度 |

---

## 2. 核心概念

### Models

Models 是 dbt 的核心，每个 model 是一个 SQL 文件，定义了一个数据转换：

```sql
-- models/customers.sql
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    created_at
FROM {{ source('raw', 'customers') }}
WHERE is_active = true
```

**Materializations（物化方式）：**

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `view` | 创建视图（默认） | 数据量小、频繁更新 |
| `table` | 创建物理表 | 数据量大、查询频繁 |
| `incremental` | 增量更新 | 大数据量、时间序列 |
| `ephemeral` | 不物化，CTE 方式引用 | 中间转换逻辑 |

### Sources

Sources 定义原始数据的位置：

```yaml
# models/sources.yml
version: 2

sources:
  - name: raw
    database: raw_data
    schema: public
    tables:
      - name: customers
      - name: orders
      - name: products
```

### Tests

Tests 验证数据质量：

```yaml
# models/schema.yml
version: 2

models:
  - name: customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - not_null
```

### Documentation

dbt 自动生成项目文档：

```yaml
# models/schema.yml
version: 2

models:
  - name: customers
    description: "Customer master data"
    columns:
      - name: customer_id
        description: "Primary key"
      - name: email
        description: "Customer email address"
```

---

## 3. 项目结构

### 标准项目结构

```
my_dbt_project/
├── dbt_project.yml          # 项目配置
├── packages.yml             # 依赖包
├── profiles.yml             # 数据库连接（通常在家目录）
│
├── models/                  # 模型定义
│   ├── staging/             # 暂存层
│   │   ├── stg_customers.sql
│   │   └── stg_orders.sql
│   ├── intermediate/        # 中间层
│   │   └── int_order_items.sql
│   └── marts/               # 业务层
│       ├── customers.sql
│       └── orders.sql
│
├── tests/                   # 自定义测试
│   └── assert_positive_amount.sql
│
├── macros/                  # Jinja 宏
│   └── cents_to_dollars.sql
│
├── seeds/                   # CSV 数据
│   └── country_codes.csv
│
├── snapshots/               # 快照（SCD Type 2）
│   └── orders_snapshot.sql
│
└── analyses/                # 临时查询
    └── ad_hoc_analysis.sql
```

### dbt_project.yml

```yaml
name: 'my_project'
version: '1.0.0'
config-version: 2

profile: 'my_profile'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  my_project:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      +schema: analytics
```

---

## 4. Models

### 基础 Model

```sql
-- models/staging/stg_customers.sql
{{
    config(
        materialized='view',
        tags=['staging', 'customers']
    )
}}

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    created_at,
    updated_at
FROM {{ source('raw', 'customers') }}
```

### Incremental Model

```sql
-- models/marts/daily_orders.sql
{{
    config(
        materialized='incremental',
        unique_key='order_date'
    )
}}

SELECT
    DATE(order_timestamp) AS order_date,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM {{ source('raw', 'orders') }}

{% if is_incremental() %}
    WHERE order_timestamp >= (
        SELECT MAX(order_date) FROM {{ this }}
    )
{% endif %}

GROUP BY 1
```

### Incremental with Merge

```sql
{{
    config(
        materialized='incremental',
        unique_key='customer_id',
        incremental_strategy='merge'
    )
}}

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    updated_at
FROM {{ source('raw', 'customers') }}

{% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

### Model Configuration

```sql
{{
    config(
        materialized='table',
        schema='analytics',
        tags=['daily', 'customers'],
        cluster_by=['customer_id'],
        partition_by={'field': 'created_at', 'data_type': 'date'},
        post_hook='GRANT SELECT ON {{ this }} TO ROLE analyst'
    )
}}
```

---

## 5. Tests

### 内置 Tests

```yaml
# models/schema.yml
version: 2

models:
  - name: customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      
      - name: email
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_match_regex:
              regex: '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
      
      - name: age
        tests:
          - dbt_utils.expression_is_true:
              expression: ">= 18"
      
      - name: status
        tests:
          - accepted_values:
              values: ['active', 'inactive', 'pending']
```

### Generic Tests

```sql
-- tests/generic/test_positive_values.sql
{% test positive_values(model, column_name) %}

SELECT *
FROM {{ model }}
WHERE {{ column_name }} < 0

{% endtest %}
```

使用：

```yaml
models:
  - name: orders
    columns:
      - name: amount
        tests:
          - positive_values
```

### Singular Tests

```sql
-- tests/assert_no_duplicate_orders.sql
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM {{ ref('orders') }}
GROUP BY 1
HAVING COUNT(*) > 1
```

### Custom Data Tests

```sql
-- tests/verify_order_totals.sql
SELECT
    order_id,
    SUM(line_total) AS calculated_total,
    order_total AS recorded_total
FROM {{ ref('order_items') }}
GROUP BY 1, 3
HAVING calculated_total != recorded_total
```

---

## 6. Documentation

### Schema Documentation

```yaml
# models/schema.yml
version: 2

models:
  - name: customers
    description: |
      Customer master data table. Contains all active and inactive customers.
      
      ## Key Business Rules
      - customer_id is the primary key
      - email must be unique and valid
      - created_at is automatically set
      
    columns:
      - name: customer_id
        description: "Unique identifier for each customer"
        tests:
          - unique
          - not_null
      
      - name: first_name
        description: "Customer's first name"
      
      - name: email
        description: |
          Customer's email address. Must be valid format.
          Used for communication and login.
      
      - name: lifetime_value
        description: |
          Total amount spent by the customer across all orders.
          Calculated as: SUM(order_total) WHERE status = 'completed'
```

### Documentation Blocks

```markdown
{% docs customers_model %}
### Customer Master Data

This model contains all customer information including:
- Personal details (name, email, phone)
- Account status (active/inactive)
- Lifetime metrics (total orders, total spent)

**Update Frequency:** Daily  
**Source:** `raw.customers`  
**Owner:** Data Engineering Team
{% enddocs %}

{% docs order_status %}
Order status can be:
- `pending`: Order placed, not yet processed
- `processing`: Order being prepared
- `shipped`: Order shipped to customer
- `delivered`: Order delivered successfully
- `cancelled`: Order cancelled
{% enddocs %}
```

使用：

```yaml
models:
  - name: customers
    description: "{{ doc('customers_model') }}"
    columns:
      - name: status
        description: "{{ doc('order_status') }}"
```

---

## 7. Jinja 模板

### 变量和控制流

```sql
SELECT
    customer_id,
    first_name,
    last_name,
    
    {% if var('include_phone', false) %}
    phone,
    {% endif %}
    
    {% if target.name == 'prod' %}
    email_hash AS email,
    {% else %}
    email,
    {% endif %}
    
    created_at
FROM {{ source('raw', 'customers') }}
```

### 循环

```sql
SELECT
    order_id,
    {% for payment_method in ['credit_card', 'paypal', 'bank_transfer'] %}
    SUM(CASE WHEN payment_method = '{{ payment_method }}' THEN amount ELSE 0 END) 
        AS {{ payment_method }}_amount{% if not loop.last %},{% endif %}
    {% endfor %}
FROM {{ source('raw', 'payments') }}
GROUP BY 1
```

### Macros

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    ({{ column_name }} / 100)::numeric(16, {{ precision }})
{% endmacro %}

-- 使用
SELECT
    order_id,
    {{ cents_to_dollars('amount_in_cents') }} AS amount_in_dollars
FROM {{ ref('orders') }}
```

### 常用 Macros

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ default_schema }}_{{ custom_schema_name }}
    {%- endif -%}
{%- endmacro %}

-- macros/date_spine.sql
{% macro date_spine(datepart, start_date, end_date) %}
WITH rawdata AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY 1) - 1 AS n,
        DATEADD({{datepart}}, n, '{{ start_date }}') AS date_{{datepart}}
    FROM {{ ref('numbers') }}
    WHERE n <= DATEDIFF({{datepart}}, '{{ start_date }}', '{{ end_date }}')
)
SELECT date_{{datepart}}
FROM rawdata
{% endmacro %}
```

---

## 8. Sources

### 定义 Sources

```yaml
# models/sources.yml
version: 2

sources:
  - name: raw
    description: "Raw data from production database"
    database: raw_db
    schema: public
    
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
      filter: |
        loaded_at >= dateadd('hour', -24, current_timestamp())
    
    loaded_at_field: loaded_at
    
    tables:
      - name: customers
        identifier: customer_master
        description: "Customer master data"
        columns:
          - name: customer_id
            description: "Primary key"
          - name: email
            description: "Customer email"
      
      - name: orders
        description: "Order transactions"
        freshness:
          warn_after: {count: 6, period: hour}
```

### Testing Sources

```sql
-- 测试 source freshness
-- 运行: dbt source freshness

SELECT
    source_name,
    table_name,
    max_loaded_at,
    snapshotted_at,
    CASE 
        WHEN max_loaded_at < dateadd('hour', -24, current_timestamp())
        THEN 'error'
        WHEN max_loaded_at < dateadd('hour', -12, current_timestamp())
        THEN 'warn'
        ELSE 'pass'
    END AS freshness_status
FROM {{ ref('sources_freshness') }}
```

---

## 9. Snapshots

### SCD Type 2

```sql
-- snapshots/orders_snapshot.sql
{% snapshot orders_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='order_id',
      strategy='timestamp',
      updated_at='updated_at',
    )
}}

SELECT * FROM {{ source('raw', 'orders') }}

{% endsnapshot %}
```

### Check Strategy

```sql
{% snapshot products_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='product_id',
      strategy='check',
      check_cols=['price', 'status', 'inventory_count']
    )
}}

SELECT * FROM {{ source('raw', 'products') }}

{% endsnapshot %}
```

### 查询快照

```sql
-- 查询当前有效记录
SELECT * FROM orders_snapshot
WHERE dbt_valid_to IS NULL;

-- 查询特定时间点的数据
SELECT * FROM orders_snapshot
WHERE '2024-01-01' BETWEEN dbt_valid_from AND COALESCE(dbt_valid_to, '9999-12-31');
```

---

## 10. Seeds

### CSV Seeds

```csv
# seeds/country_codes.csv
country_code,country_name,currency
US,United States,USD
GB,United Kingdom,GBP
CN,China,CNY
JP,Japan,JPY
```

### 加载 Seeds

```bash
dbt seed
```

### 引用 Seeds

```sql
SELECT
    o.order_id,
    o.country_code,
    s.country_name,
    s.currency
FROM {{ ref('orders') }} o
LEFT JOIN {{ ref('country_codes') }} s
    ON o.country_code = s.country_code
```

### Seed Configuration

```yaml
# dbt_project.yml
seeds:
  my_project:
    country_codes:
      +column_types:
        country_code: varchar(2)
        country_name: varchar(100)
        currency: varchar(3)
```

---

## 11. Macros

### 创建 Macros

```sql
-- macros/calculate_age.sql
{% macro calculate_age(birth_date_column) %}
    DATEDIFF(year, {{ birth_date_column }}, CURRENT_DATE)
    - CASE 
        WHEN DATEADD(year, 
              DATEDIFF(year, {{ birth_date_column }}, CURRENT_DATE),
              {{ birth_date_column }}) > CURRENT_DATE
        THEN 1
        ELSE 0
      END
{% endmacro %}

-- 使用
SELECT
    customer_id,
    birth_date,
    {{ calculate_age('birth_date') }} AS age
FROM {{ ref('customers') }}
```

### 动态生成 SQL

```sql
-- macros/pivot_values.sql
{% macro pivot_values(column_name, values) %}
    {% for value in values %}
    SUM(CASE WHEN {{ column_name }} = '{{ value }}' THEN 1 ELSE 0 END) 
        AS {{ column_name }}_{{ value | lower | replace(' ', '_') }}
    {% if not loop.last %},{% endif %}
    {% endfor %}
{% endmacro %}

-- 使用
SELECT
    customer_id,
    {{ pivot_values('status', ['active', 'inactive', 'pending']) }}
FROM {{ ref('customers') }}
GROUP BY 1
```

### Adapter Macros

```sql
-- macros/current_timestamp.sql
{% macro current_timestamp() %}
    {{ return(adapter.dispatch('current_timestamp')()) }}
{% endmacro %}

{% macro default__current_timestamp() %}
    CURRENT_TIMESTAMP()
{% endmacro %}

{% macro snowflake__current_timestamp() %}
    CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())
{% endmacro %}

{% macro bigquery__current_timestamp() %}
    CURRENT_TIMESTAMP()
{% endmacro %}
```

---

## 12. Packages

### 安装 Packages

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  
  - package: calogica/dbt_expectations
    version: 0.10.1
  
  - package: dbt-labs/codegen
    version: 0.12.1
  
  - git: "https://github.com/my-org/my-dbt-macros.git"
    revision: 0.1.0
```

### 安装命令

```bash
dbt deps
```

### 常用 Packages

| Package | 用途 |
|---------|------|
| `dbt_utils` | 通用工具和 macros |
| `dbt_expectations` | 数据质量测试 |
| `codegen` | 自动生成 model 代码 |
| `audit_helper` | 审计和数据对比 |
| `dbt_external_tables` | 外部表管理 |

### 使用 dbt_utils

```sql
-- Surrogate key
SELECT
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'order_date']) }} AS order_key,
    *
FROM {{ ref('orders') }}

-- Star 列出生成
SELECT
    {{ dbt_utils.star(from=ref('customers'), except=['password_hash']) }}
FROM {{ ref('customers') }}

-- Pivot
SELECT
    customer_id,
    {{ dbt_utils.pivot('status', dbt_utils.get_column_values(ref('customers'), 'status')) }}
FROM {{ ref('customers') }}
GROUP BY 1
```

---

## 13. 环境变量

### 使用环境变量

```sql
-- 在 model 中使用
SELECT *
FROM {{ env_var('DBT_RAW_SCHEMA', 'raw') }}.customers
```

### profiles.yml 中使用

```yaml
# ~/.dbt/profiles.yml
my_profile:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('DBT_ACCOUNT') }}"
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: "{{ env_var('DBT_ROLE', 'ANALYST') }}"
      database: "{{ env_var('DBT_DATABASE', 'ANALYTICS') }}"
      warehouse: "{{ env_var('DBT_WAREHOUSE', 'DEV_WH') }}"
      schema: "{{ env_var('DBT_SCHEMA', 'dev') }}"
```

### 变量

```bash
# 传递变量
dbt run --vars '{run_date: "2024-01-01", environment: "prod"}'
```

```sql
-- 在 model 中使用
SELECT *
FROM {{ ref('orders') }}
WHERE order_date = '{{ var("run_date") }}'

{% if var('environment') == 'prod' %}
    AND is_test = FALSE
{% endif %}
```

---

## 14. 部署与 CI/CD

### dbt Cloud

1. 连接 Git 仓库
2. 配置数据库连接
3. 设置调度任务
4. 配置环境

### CI/CD Pipeline

```yaml
# .github/workflows/dbt-ci.yml
name: dbt CI

on:
  pull_request:
    branches: [main]

jobs:
  dbt-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dbt
        run: |
          pip install dbt-snowflake
      
      - name: dbt deps
        run: dbt deps
        env:
          DBT_PROFILES_DIR: .
      
      - name: dbt build
        run: |
          dbt build --target ci
        env:
          DBT_PROFILES_DIR: .
          DBT_ACCOUNT: ${{ secrets.DBT_ACCOUNT }}
          DBT_USER: ${{ secrets.DBT_USER }}
          DBT_PASSWORD: ${{ secrets.DBT_PASSWORD }}
```

### 部署流程

```bash
# 开发环境
dbt run --target dev
dbt test --target dev

# 预发布环境
dbt run --target staging
dbt test --target staging

# 生产环境
dbt run --target prod
dbt test --target prod
dbt docs generate --target prod
```

---

## 15. 最佳实践

### 项目结构

```
models/
├── staging/              # 源数据清洗
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   └── _stg_models.yml
│
├── intermediate/         # 中间转换
│   ├── int_order_items.sql
│   └── _int_models.yml
│
└── marts/               # 业务模型
    ├── customers/
    │   ├── dim_customers.sql
    │   └── fct_customer_orders.sql
    ├── orders/
    │   └── fct_orders.sql
    └── _marts_models.yml
```

### 命名规范

| 类型 | 前缀 | 示例 |
|------|------|------|
| Staging | `stg_` | `stg_customers` |
| Intermediate | `int_` | `int_order_items` |
| Dimension | `dim_` | `dim_customers` |
| Fact | `fct_` | `fct_orders` |
| Aggregate | `agg_` | `agg_daily_sales` |

### SQL 风格

```sql
-- ✅ 好的 SQL 风格
WITH customers AS (
    SELECT
        customer_id,
        first_name,
        last_name,
        email
    FROM {{ ref('stg_customers') }}
    WHERE is_active = TRUE
),

orders AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount
    FROM {{ ref('stg_orders') }}
    WHERE order_date >= '2024-01-01'
)

SELECT
    c.customer_id,
    c.first_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2
```

### 增量模型最佳实践

```sql
{{
    config(
        materialized='incremental',
        unique_key='event_id',
        on_schema_change='sync_all_columns'
    )
}}

WITH events AS (
    SELECT *
    FROM {{ source('raw', 'events') }}
    
    {% if is_incremental() %}
    WHERE loaded_at > (
        SELECT MAX(loaded_at) FROM {{ this }}
    )
    {% endif %}
)

SELECT
    event_id,
    event_type,
    event_timestamp,
    user_id,
    properties,
    CURRENT_TIMESTAMP() AS dbt_loaded_at
FROM events
```

### 测试策略

```yaml
models:
  - name: fct_orders
    columns:
      # 主键测试
      - name: order_id
        tests:
          - unique
          - not_null
      
      # 业务规则测试
      - name: total_amount
        tests:
          - dbt_utils.expression_is_true:
              expression: ">= 0"
      
      # 关系测试
      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      
      # 数据质量测试
      - name: order_date
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: "'2020-01-01'"
              max_value: "current_date"
```

---

## 附录：常用命令

```bash
# 项目初始化
dbt init my_project

# 安装依赖
dbt deps

# 运行模型
dbt run
dbt run --models +customers
dbt run --select tag:daily

# 测试
dbt test
dbt test --models customers

# 构建（运行 + 测试）
dbt build

# 生成文档
dbt docs generate
dbt docs serve

# 调试
dbt debug
dbt compile

# Seed
dbt seed

# Snapshot
dbt snapshot

# 清理
dbt clean
```

---

> 📝 本文档基于 dbt 最新官方文档整理
> 官方文档：https://docs.getdbt.com
> 更新时间：2026-06-10
