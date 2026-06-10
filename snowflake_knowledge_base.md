# Snowflake 完整知识体系

> 基于 Snowflake 2026 最新官方文档 | 更新时间：2026-06-10
> 官方文档：https://docs.snowflake.com

---

## 📚 目录

- [第一部分：架构与核心概念](#第一部分架构与核心概念)
  - [1.1 什么是 Snowflake](#11-什么是-snowflake)
  - [1.2 三层架构](#12-三层架构)
  - [1.3 存储层](#13-存储层)
  - [1.4 计算层](#14-计算层)
  - [1.5 云服务层](#15-云服务层)
  - [1.6 数据类型](#16-数据类型)
- [第二部分：数据库对象](#第二部分数据库对象)
  - [2.1 表类型](#21-表类型)
  - [2.2 视图](#22-视图)
  - [2.3 Schema 与 Database](#23-schema-与-database)
  - [2.4 Stage（数据暂存区）](#24-stage数据暂存区)
- [第三部分：SQL 基础](#第三部分sql-基础)
  - [3.1 DDL 语句](#31-ddl-语句)
  - [3.2 DML 语句](#32-dml-语句)
  - [3.3 查询语句](#33-查询语句)
  - [3.4 窗口函数](#34-窗口函数)
  - [3.5 CTE 与子查询](#35-cte-与子查询)
- [第四部分：数据加载与集成](#第四部分数据加载与集成)
  - [4.1 数据加载概述](#41-数据加载概述)
  - [4.2 COPY INTO 命令](#42-copy-into-命令)
  - [4.3 Snowpipe](#43-snowpipe)
  - [4.4 Snowpipe Streaming](#44-snowpipe-streaming)
  - [4.5 外部表](#45-外部表)
  - [4.6 数据共享](#46-数据共享)
- [第五部分：虚拟仓库与性能优化](#第五部分虚拟仓库与性能优化)
  - [5.1 虚拟仓库概述](#51-虚拟仓库概述)
  - [5.2 仓库大小与计费](#52-仓库大小与计费)
  - [5.3 多集群仓库](#53-多集群仓库)
  - [5.4 自动挂起与自动恢复](#54-自动挂起与自动恢复)
  - [5.5 查询优化](#55-查询优化)
  - [5.6 缓存与物化视图](#56-缓存与物化视图)
  - [5.7 聚簇键](#57-聚簇键)
- [第六部分：安全与访问控制](#第六部分安全与访问控制)
  - [6.1 访问控制模型](#61-访问控制模型)
  - [6.2 角色类型](#62-角色类型)
  - [6.3 系统角色](#63-系统角色)
  - [6.4 权限授予](#64-权限授予)
  - [6.5 数据安全](#65-数据安全)
- [第七部分：高级功能](#第七部分高级功能)
  - [7.1 Streams 与 Tasks](#71-streams-与-tasks)
  - [7.2 动态表](#72-动态表)
  - [7.3 Snowpark](#73-snowpark)
  - [7.4 Cortex AI](#74-cortex-ai)
  - [7.5 机器学习功能](#75-机器学习功能)
  - [7.6 Time Travel](#76-time-travel)
  - [7.7 Fail-safe](#77-fail-safe)
- [第八部分：开发流程](#第八部分开发流程)
  - [8.1 环境搭建](#81-环境搭建)
  - [8.2 连接方式](#82-连接方式)
  - [8.3 数据建模最佳实践](#83-数据建模最佳实践)
  - [8.4 性能调优最佳实践](#84-性能调优最佳实践)
  - [8.5 成本优化最佳实践](#85-成本优化最佳实践)
- [第九部分：实战代码示例](#第九部分实战代码示例)
  - [Demo 1: 创建表并加载数据](#demo-1-创建表并加载数据)
  - [Demo 2: 数据转换与 ETL](#demo-2-数据转换与-etl)
  - [Demo 3: 半结构化数据处理](#demo-3-半结构化数据处理)
  - [Demo 4: 增量加载与 CDC](#demo-4-增量加载与-cdc)
  - [Demo 5: 多表关联查询优化](#demo-5-多表关联查询优化)
- [附录：常用资源](#附录常用资源)

---

# 第一部分：架构与核心概念

## 1.1 什么是 Snowflake

Snowflake 是一个**云原生数据平台**，采用独特的**存算分离架构**，将数据存储、计算和云服务分离，实现真正的弹性扩展和按需付费。

**核心优势：**
- ✅ **无需管理基础设施**：无硬件、无虚拟机、无软件安装配置
- ✅ **弹性扩展**：计算和存储独立扩展，互不影响
- ✅ **多集群架构**：支持同时运行多个独立计算集群
- ✅ **多平台支持**：AWS、Azure、GCP 三大云平台
- ✅ **零管理**：自动维护、升级、调优
- ✅ **秒级计费**：按实际使用量计费，精确到秒

**支持的数据类型：**
- **结构化数据**：行列表格，严格 Schema
- **半结构化数据**：JSON、XML、Avro、Parquet 等，灵活 Schema
- **非结构化数据**：文档、图片、音频、视频

## 1.2 三层架构

Snowflake 采用独特的三层架构设计：

```
┌─────────────────────────────────────────────────────────┐
│                    云服务层 (Cloud Services)              │
│  认证、授权、查询优化、元数据管理、基础设施管理            │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                    计算层 (Compute)                      │
│              虚拟仓库 (Virtual Warehouses)                │
│         独立计算集群，MPP 并行处理，弹性扩展              │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                    存储层 (Storage)                      │
│              列式存储，微分区，自动压缩                   │
│         数据持久化在云存储，所有计算节点共享访问          │
└─────────────────────────────────────────────────────────┘
```

**架构特点：**
- **存储与计算分离**：存储和计算独立计费，互不影响
- **共享存储**：所有计算节点共享同一份数据，无需数据复制
- **MPP 计算**：每个虚拟仓库是独立的 MPP 集群，查询高度并行化
- **无锁设计**：读写不冲突，支持高并发

## 1.3 存储层

### 核心特性

Snowflake 自动将数据组织成优化的**列式存储格式**：

- **自动压缩**：根据数据类型自动选择最佳压缩算法
- **微分区**：数据自动分割成 50-500MB 的微分区单元
- **元数据管理**：自动维护列统计信息、min/max 值、空值计数等
- **不可变存储**：微分区一旦创建就不会被修改，只会被替换

### 存储计费

- 按压缩后的实际存储量计费
- 典型压缩率：10:1 到 20:1
- 包括 Time Travel 和 Fail-safe 的存储

### 微分区

微分区是 Snowflake 的核心优化：

- **大小**：50-500MB 未压缩数据
- **自动维护**：无需手动分区
- **列式存储**：每个微分区按列组织
- **元数据缓存**：每个微分区的列统计信息会被缓存
- **分区裁剪**：查询时自动跳过不相关的微分区

## 1.4 计算层

### 虚拟仓库

虚拟仓库是 Snowflake 的计算资源集群：

- **独立集群**：每个仓库是独立的计算资源，不共享
- **弹性扩展**：可在运行时动态调整大小
- **多集群支持**：一个仓库可包含多个集群，处理并发
- **自动挂起/恢复**：闲置时自动挂起，需要时自动恢复
- **秒级计费**：按实际使用时长计费，最小 1 分钟

### 仓库类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **Standard** | 标准仓库，通用计算 | 大多数场景 |
| **Snowpark-optimized** | 针对 Snowpark 优化 | Python/Java/Scala 工作负载 |

### 仓库大小

| 大小 | Credits/小时 | 适用场景 |
|------|-------------|----------|
| X-Small | 1 | 开发测试、小查询 |
| Small | 2 | 轻量级 ETL |
| Medium | 4 | 中等复杂度查询 |
| Large | 8 | 复杂查询、大数据量 |
| X-Large | 16 | 高并发、复杂分析 |
| 2X-Large | 32 | 大型企业级工作负载 |
| 3X-Large | 64 | 超大规模数据处理 |
| 4X-Large | 128 | 极端性能需求 |
| 5X-Large | 256 | 最大规模（AWS/Azure） |
| 6X-Large | 512 | 最大规模（AWS/Azure） |

**重要说明：**
- 每增加一个级别，计算资源翻倍
- 更大的仓库不总是更快，取决于查询特性
- 数据加载性能主要取决于文件数量，而非仓库大小
- 查询性能通常随仓库大小线性扩展

## 1.5 云服务层

云服务层是 Snowflake 的"大脑"，协调所有活动：

### 核心服务

- **认证与授权**：用户认证、访问控制、权限管理
- **查询解析与优化**：SQL 解析、查询计划生成、成本优化
- **元数据管理**：表统计信息、列信息、数据血缘
- **基础设施管理**：仓库调度、资源分配、负载均衡
- **合规与安全**：加密、审计、合规性检查
- **数据共享**：安全数据共享、市场数据访问

### 查询处理流程

```
SQL 语句 → 解析 → 优化 → 计划生成 → 分发到仓库 → 执行 → 返回结果
   ↓         ↓       ↓         ↓           ↓          ↓
  检查语法  检查权限  成本估算  生成执行计划  分配到节点  并行处理
```

## 1.6 数据类型

### 数值类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `NUMBER` / `DECIMAL` / `NUMERIC` | 定点数，精度最高 38 位 | `NUMBER(10,2)` |
| `INT` / `INTEGER` | 整数 | `INT` |
| `BIGINT` | 大整数 | `BIGINT` |
| `SMALLINT` | 小整数 | `SMALLINT` |
| `TINYINT` | 微整数 | `TINYINT` |
| `BYTEINT` | 字节整数 | `BYTEINT` |
| `FLOAT` / `FLOAT4` / `FLOAT8` | 浮点数 | `FLOAT` |
| `DOUBLE` / `DOUBLE PRECISION` | 双精度浮点 | `DOUBLE` |
| `REAL` | 单精度浮点 | `REAL` |

### 字符串类型

| 类型 | 说明 | 最大长度 |
|------|------|----------|
| `VARCHAR` / `STRING` / `TEXT` | 可变长度字符串 | 16MB |
| `CHAR` / `CHARACTER` | 固定长度字符串 | 16MB |

### 布尔类型

| 类型 | 说明 | 值 |
|------|------|-----|
| `BOOLEAN` | 布尔值 | `TRUE` / `FALSE` / `NULL` |

### 日期时间类型

| 类型 | 说明 | 精度 |
|------|------|------|
| `DATE` | 日期 | 年-月-日 |
| `DATETIME` | 日期时间 | 等同于 TIMESTAMP |
| `TIME` | 时间 | 时:分:秒.毫秒 |
| `TIMESTAMP` | 时间戳 | 默认包含时区 |
| `TIMESTAMP_LTZ` | 本地时区时间戳 | 带本地时区 |
| `TIMESTAMP_NTZ` | 无时区时间戳 | 不带时区 |
| `TIMESTAMP_TZ` | 带时区时间戳 | 带时区偏移 |

### 半结构化数据类型

| 类型 | 说明 | 用途 |
|------|------|------|
| `VARIANT` | 多态类型 | 存储 JSON、XML 等任意结构 |
| `OBJECT` | JSON 对象 | 键值对集合 |
| `ARRAY` | JSON 数组 | 有序元素集合 |

### 二进制类型

| 类型 | 说明 | 最大长度 |
|------|------|----------|
| `BINARY` | 固定长度二进制 | 8MB |
| `VARBINARY` | 可变长度二进制 | 8MB |

---

# 第二部分：数据库对象

## 2.1 表类型

### Snowflake 表（标准表）

最常用的表类型，数据存储在 Snowflake 管理的云存储中：

```sql
-- 创建标准表
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    hire_date DATE,
    salary NUMBER(10,2),
    department_id INT,
    is_active BOOLEAN DEFAULT TRUE
);

-- 创建临时表
CREATE TEMPORARY TABLE temp_data (
    id INT,
    value VARCHAR(100)
);

-- 创建瞬态表（无 Fail-safe）
CREATE TRANSIENT TABLE transient_data (
    id INT,
    data VARIANT
);

-- 创建易失表（会话结束后消失）
CREATE VOLATILE TABLE volatile_data (
    id INT,
    value VARCHAR(100)
);
```

**表类型对比：**

| 类型 | 持久性 | Time Travel | Fail-safe | 计费 |
|------|--------|-------------|-----------|------|
| Permanent | 永久 | ✅ | ✅ | 标准 |
| Transient | 永久 | ⚠️ 最多 1 天 | ❌ | 较低 |
| Temporary | 会话结束 | ⚠️ 最多 1 天 | ❌ | 较低 |
| Volatile | 会话结束 | ❌ | ❌ | 最低 |

### Iceberg 表

将数据存储在外部云存储（S3/GCS/Azure），同时保持 Snowflake 的查询性能：

```sql
-- 创建 Iceberg 表
CREATE ICEBERG TABLE my_iceberg_table (
    id INT,
    name VARCHAR,
    created_at TIMESTAMP
)
CATALOG_SYNC = 'my_catalog'
EXTERNAL_VOLUME = 'my_volume'
BASE_LOCATION = 'iceberg/my_table';
```

**适用场景：**
- 现有数据湖需要 Snowflake 查询能力
- 需要跨多个系统共享数据
- 不想迁移数据到 Snowflake 内部存储

### Hybrid 表

针对低延迟、高吞吐的事务性工作负载优化：

```sql
-- 创建 Hybrid 表
CREATE HYBRID TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**特性：**
- 支持行级锁
- 支持唯一约束和外键约束
- 低延迟的点查和更新
- 适合 OLTP 和 Unistore 工作负载

## 2.2 视图

### 标准视图

```sql
-- 创建视图
CREATE VIEW active_employees AS
SELECT employee_id, first_name, last_name, department_id
FROM employees
WHERE is_active = TRUE;
```

### 物化视图

```sql
-- 创建物化视图
CREATE MATERIALIZED VIEW department_stats AS
SELECT 
    department_id,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employees
WHERE is_active = TRUE
GROUP BY department_id;
```

**物化视图优势：**
- 预计算并缓存结果
- 查询性能显著提升
- 自动刷新

### 安全视图

```sql
-- 创建安全视图（隐藏底层权限）
CREATE SECURE VIEW public_employees AS
SELECT employee_id, first_name, last_name
FROM employees
WHERE department_id IN (1, 2, 3)
WITH GRANT OPTION;
```

## 2.3 Schema 与 Database

### 层级结构

```
Account
  └── Database
        ├── Schema (默认: PUBLIC)
        │     ├── Tables
        │     ├── Views
        │     ├── Stages
        │     └── ...
        └── Schema
              └── ...
```

### 创建与管理

```sql
-- 创建数据库
CREATE DATABASE analytics_db
    DATA_RETENTION_TIME_IN_DAYS = 7
    COMMENT = 'Analytics data warehouse';

-- 创建 Schema
CREATE SCHEMA analytics_db.raw_data
    COMMENT = 'Raw data layer';

-- 使用数据库和 Schema
USE DATABASE analytics_db;
USE SCHEMA raw_data;
```

## 2.4 Stage（数据暂存区）

Stage 是存储数据文件的位置，用于数据加载。

### Stage 类型

| 类型 | 位置 | 用途 |
|------|------|------|
| **用户 Stage** | `@~` | 每个用户的私有暂存区 |
| **表 Stage** | `@%table_name` | 特定表的暂存区 |
| **命名内部 Stage** | `@stage_name` | 账号内的命名暂存区 |
| **命名外部 Stage** | `@external_stage` | 指向外部云存储 |

### 创建外部 Stage

```sql
-- 创建 S3 外部 Stage
CREATE STAGE my_s3_stage
    URL = 's3://my-bucket/data/'
    STORAGE_INTEGRATION = my_s3_integration
    FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1);

-- 创建 Azure Blob Stage
CREATE STAGE my_azure_stage
    URL = 'azure://myaccount.blob.core.windows.net/mycontainer/path/'
    STORAGE_INTEGRATION = my_azure_integration
    FILE_FORMAT = (TYPE = 'PARQUET');

-- 创建 GCS Stage
CREATE STAGE my_gcs_stage
    URL = 'gcs://my-bucket/data/'
    STORAGE_INTEGRATION = my_gcs_integration
    FILE_FORMAT = (TYPE = 'JSON');
```

### 文件操作

```sql
-- 列出 Stage 中的文件
LIST @my_s3_stage;

-- 上传文件到内部 Stage
PUT file:///local/path/data.csv @my_stage;

-- 下载文件
GET @my_s3_stage/data.csv file:///local/path/;

-- 删除 Stage 中的文件
REMOVE @my_s3_stage/old_data/;
```

---

# 第三部分：SQL 基础

## 3.1 DDL 语句

### CREATE TABLE

```sql
-- 基础创建
CREATE TABLE products (
    product_id INT AUTOINCREMENT PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP
);

-- 带约束的创建
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) CHECK (total_amount >= 0),
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 创建表同时定义聚簇键
CREATE TABLE sales_data (
    sale_date DATE,
    product_id INT,
    quantity INT,
    amount DECIMAL(10,2)
)
CLUSTER BY (sale_date, product_id);

-- CTAS (Create Table As Select)
CREATE TABLE high_value_customers AS
SELECT customer_id, first_name, last_name, total_spent
FROM customers
WHERE total_spent > 10000;

-- CREATE TABLE LIKE (复制结构)
CREATE TABLE customers_backup LIKE customers;

-- CREATE TABLE CLONE (克隆表，包括数据)
CREATE TABLE customers_clone CLONE customers;

-- CREATE OR ALTER TABLE (不存在则创建，存在则修改)
CREATE OR ALTER TABLE new_table (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);
```

### ALTER TABLE

```sql
-- 添加列
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

-- 删除列
ALTER TABLE employees DROP COLUMN phone;

-- 修改列
ALTER TABLE employees 
    ALTER COLUMN salary SET DATA TYPE DECIMAL(12,2);

-- 重命名列
ALTER TABLE employees RENAME COLUMN first_name TO fname;

-- 添加约束
ALTER TABLE employees 
    ADD CONSTRAINT unique_email UNIQUE (email);

-- 修改表属性
ALTER TABLE employees 
    SET DATA_RETENTION_TIME_IN_DAYS = 30
    SET COMMENT = 'Employee master data';

-- 启用变更跟踪
ALTER TABLE employees 
    SET CHANGE_TRACKING = TRUE;
```

### DROP TABLE

```sql
-- 删除表
DROP TABLE temp_data;

-- 如果存在则删除
DROP TABLE IF EXISTS temp_data;

-- 删除并跳过回收站（立即删除）
DROP TABLE temp_data CASCADE;
```

## 3.2 DML 语句

### INSERT

```sql
-- 插入单行
INSERT INTO employees (first_name, last_name, email, hire_date, salary)
VALUES ('John', 'Doe', 'john.doe@example.com', '2024-01-15', 75000.00);

-- 插入多行
INSERT INTO employees (first_name, last_name, email, hire_date, salary)
VALUES 
    ('Jane', 'Smith', 'jane.smith@example.com', '2024-02-01', 80000.00),
    ('Bob', 'Johnson', 'bob.johnson@example.com', '2024-02-15', 70000.00);

-- 从查询插入
INSERT INTO high_performers
SELECT employee_id, first_name, last_name, performance_score
FROM employees
WHERE performance_score > 90;
```

### UPDATE

```sql
-- 基础更新
UPDATE employees
SET salary = salary * 1.05,
    updated_at = CURRENT_TIMESTAMP()
WHERE department_id = 10;

-- 条件更新
UPDATE employees
SET is_active = FALSE,
    termination_date = '2024-12-31'
WHERE employee_id = 123;
```

### DELETE

```sql
-- 删除特定行
DELETE FROM employees
WHERE employee_id = 456;

-- 条件删除
DELETE FROM employees
WHERE hire_date < '2020-01-01' AND is_active = FALSE;
```

### MERGE (UPSERT)

```sql
-- 合并操作：存在则更新，不存在则插入
MERGE INTO target_table AS t
USING source_table AS s
ON t.id = s.id
WHEN MATCHED AND s.is_active = TRUE THEN
    UPDATE SET 
        t.name = s.name,
        t.value = s.value,
        t.updated_at = CURRENT_TIMESTAMP()
WHEN MATCHED AND s.is_active = FALSE THEN
    DELETE
WHEN NOT MATCHED THEN
    INSERT (id, name, value, created_at)
    VALUES (s.id, s.name, s.value, CURRENT_TIMESTAMP());
```

## 3.3 查询语句

### 基础查询

```sql
-- 选择列
SELECT employee_id, first_name, last_name, salary
FROM employees;

-- 使用别名
SELECT 
    employee_id AS id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    salary * 12 AS annual_salary
FROM employees;

-- DISTINCT 去重
SELECT DISTINCT department_id FROM employees;

-- WHERE 过滤
SELECT employee_id, first_name, salary
FROM employees
WHERE department_id = 10 
  AND salary > 50000
  AND is_active = TRUE;

-- ORDER BY 排序
SELECT employee_id, first_name, salary
FROM employees
ORDER BY salary DESC, first_name ASC;

-- LIMIT 限制结果数
SELECT employee_id, first_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 10;
```

### 聚合查询

```sql
-- 基础聚合
SELECT 
    department_id,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    SUM(salary) AS total_salary
FROM employees
WHERE is_active = TRUE
GROUP BY department_id
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;
```

### 常用聚合函数

| 函数 | 说明 |
|------|------|
| `COUNT()` | 计数 |
| `SUM()` | 求和 |
| `AVG()` | 平均值 |
| `MIN()` | 最小值 |
| `MAX()` | 最大值 |
| `MEDIAN()` | 中位数 |
| `PERCENTILE_CONT()` | 连续百分位 |
| `STDDEV()` | 标准差 |
| `VARIANCE()` | 方差 |
| `LISTAGG()` | 字符串聚合 |

### JOIN 操作

```sql
-- INNER JOIN
SELECT 
    e.employee_id,
    e.first_name,
    d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;

-- LEFT JOIN
SELECT 
    d.department_name,
    COUNT(e.employee_id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name;

-- RIGHT JOIN
SELECT 
    e.employee_id,
    p.project_name
FROM employees e
RIGHT JOIN project_assignments p ON e.employee_id = p.employee_id;

-- FULL OUTER JOIN
SELECT 
    e.employee_id,
    e.first_name,
    o.order_id
FROM employees e
FULL OUTER JOIN orders o ON e.employee_id = o.sales_rep_id;

-- CROSS JOIN (笛卡尔积)
SELECT 
    d.department_name,
    r.role_name
FROM departments d
CROSS JOIN roles r;

-- SELF JOIN
SELECT 
    e.employee_id,
    e.first_name AS employee_name,
    m.first_name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

## 3.4 窗口函数

窗口函数在不折叠行的情况下对行集执行计算。

### 基础语法

```sql
function_name(args) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY sort_expression]
    [frame_clause]
)
```

### 常用窗口函数

```sql
-- ROW_NUMBER: 行号
SELECT 
    employee_id,
    department_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as rank_in_dept
FROM employees;

-- RANK: 排名（有并列）
SELECT 
    employee_id,
    salary,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;

-- DENSE_RANK: 密集排名（无间隔）
SELECT 
    employee_id,
    salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;

-- NTILE: 分桶
SELECT 
    employee_id,
    salary,
    NTILE(4) OVER (ORDER BY salary DESC) as quartile
FROM employees;

-- LAG/LEAD: 前后行
SELECT 
    employee_id,
    hire_date,
    salary,
    LAG(salary) OVER (ORDER BY hire_date) as prev_salary,
    LEAD(salary) OVER (ORDER BY hire_date) as next_salary
FROM employees;

-- 运行总计
SELECT 
    employee_id,
    hire_date,
    salary,
    SUM(salary) OVER (ORDER BY hire_date) as running_total
FROM employees;

-- 移动平均
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7days
FROM daily_sales;

-- 分区聚合
SELECT 
    employee_id,
    department_id,
    salary,
    AVG(salary) OVER (PARTITION BY department_id) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department_id) as diff_from_avg
FROM employees;
```

## 3.5 CTE 与子查询

### CTE (Common Table Expression)

```sql
-- 基础 CTE
WITH department_stats AS (
    SELECT 
        department_id,
        COUNT(*) as emp_count,
        AVG(salary) as avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT 
    d.department_name,
    s.emp_count,
    s.avg_salary
FROM department_stats s
JOIN departments d ON s.department_id = d.department_id;

-- 多个 CTE
WITH 
high_earners AS (
    SELECT employee_id, first_name, salary
    FROM employees
    WHERE salary > 100000
),
managers AS (
    SELECT DISTINCT manager_id
    FROM employees
    WHERE manager_id IS NOT NULL
)
SELECT 
    h.first_name,
    h.salary
FROM high_earners h
JOIN managers m ON h.employee_id = m.manager_id;

-- 递归 CTE
WITH RECURSIVE org_chart AS (
    -- 锚点：顶级管理者
    SELECT 
        employee_id,
        first_name,
        manager_id,
        1 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- 递归：下属
    SELECT 
        e.employee_id,
        e.first_name,
        e.manager_id,
        o.level + 1
    FROM employees e
    JOIN org_chart o ON e.manager_id = o.employee_id
)
SELECT * FROM org_chart
ORDER BY level, first_name;
```

### 子查询

```sql
-- 标量子查询
SELECT 
    employee_id,
    first_name,
    salary,
    (SELECT AVG(salary) FROM employees) as company_avg
FROM employees;

-- 列子查询
SELECT 
    employee_id,
    first_name,
    salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 行子查询
SELECT *
FROM employees
WHERE (department_id, salary) IN (
    SELECT department_id, MAX(salary)
    FROM employees
    GROUP BY department_id
);

-- 表子查询
SELECT *
FROM (
    SELECT 
        employee_id,
        first_name,
        salary,
        RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank <= 10;

-- EXISTS 子查询
SELECT employee_id, first_name
FROM employees e
WHERE EXISTS (
    SELECT 1 
    FROM projects p 
    WHERE p.lead_id = e.employee_id
);
```

---

# 第四部分：数据加载与集成

## 4.1 数据加载概述

Snowflake 提供多种数据加载方式，适应不同场景：

| 方式 | 适用场景 | 延迟 | 复杂度 |
|------|----------|------|--------|
| **COPY INTO** | 批量加载大文件 | 分钟级 | 低 |
| **Snowpipe** | 持续加载小批量 | 分钟级 | 中 |
| **Snowpipe Streaming** | 实时流式加载 | 秒级 | 中 |
| **外部表** | 直接查询外部数据 | 实时 | 低 |
| **Kafka Connector** | Kafka 主题加载 | 近实时 | 中 |
| **Connectors** | 第三方系统集成 | 近实时 | 中 |

### Stage 类型

```sql
-- 用户 Stage
PUT file:///tmp/data.csv @~/data/;

-- 表 Stage
PUT file:///tmp/data.csv @%my_table/;

-- 命名内部 Stage
CREATE STAGE my_internal_stage;
PUT file:///tmp/data.csv @my_internal_stage/;

-- 命名外部 Stage
CREATE STAGE my_s3_stage
    URL = 's3://my-bucket/data/'
    STORAGE_INTEGRATION = my_s3_integration;
```

## 4.2 COPY INTO 命令

COPY INTO 是最常用的批量加载方式。

### 基础用法

```sql
-- 从外部 Stage 加载 CSV
COPY INTO my_table
FROM @my_s3_stage/data/
FILE_FORMAT = (
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE
)
ON_ERROR = 'CONTINUE';

-- 从表 Stage 加载
COPY INTO my_table
FROM @%my_table/
FILE_FORMAT = (TYPE = 'PARQUET');

-- 从用户 Stage 加载
COPY INTO my_table
FROM @~/data/
PATTERN = '.*data.*\\.csv'
FILE_FORMAT = my_csv_format;
```

### 文件格式对象

```sql
-- 创建 CSV 文件格式
CREATE FILE FORMAT my_csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    ENCODING = 'UTF8';

-- 创建 JSON 文件格式
CREATE FILE FORMAT my_json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE
    STRIP_NULL_VALUES = TRUE;

-- 创建 Parquet 文件格式
CREATE FILE FORMAT my_parquet_format
    TYPE = 'PARQUET'
    USE_VECTORIZED_SCANNER = TRUE;

-- 使用文件格式
COPY INTO my_table
FROM @my_stage/
FILE_FORMAT = (FORMAT_NAME = my_csv_format);
```

### 转换加载

```sql
-- 列重映射
COPY INTO target_table (col1, col2, col3)
FROM (
    SELECT 
        $1 AS col1,
        $2::INT AS col2,
        UPPER($3) AS col3
    FROM @my_stage/data.csv
)
FILE_FORMAT = (TYPE = 'CSV');

-- 添加计算列
COPY INTO target_table
FROM (
    SELECT 
        $1,
        $2,
        $3,
        CURRENT_TIMESTAMP() AS loaded_at,
        'batch_001' AS batch_id
    FROM @my_stage/data.csv
)
FILE_FORMAT = (TYPE = 'CSV');
```

### 错误处理

```sql
-- 继续加载，跳过错误行
COPY INTO my_table
FROM @my_stage/
FILE_FORMAT = (TYPE = 'CSV')
ON_ERROR = 'CONTINUE';

-- 限制错误数量
COPY INTO my_table
FROM @my_stage/
FILE_FORMAT = (TYPE = 'CSV')
ON_ERROR = 'CONTINUE'
SIZE_LIMIT = 100;  -- 最多 100 个错误

-- 启用错误日志
ALTER TABLE my_table SET ERROR_LOGGING = TRUE;

-- 查询错误表
SELECT * FROM ERROR_TABLE(my_table);
```

### 验证加载

```sql
-- 验证而不实际加载
COPY INTO my_table
FROM @my_stage/
FILE_FORMAT = (TYPE = 'CSV')
VALIDATE_ONLY;

-- 查看将加载的文件
LIST @my_stage/data/;

-- 查看已加载的文件
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

## 4.3 Snowpipe

Snowpipe 实现持续、自动的数据加载。

### 创建 Pipe

```sql
-- 创建 Snowpipe
CREATE PIPE my_pipe
    AUTO_INGEST = TRUE
    COMMENT = 'Auto-ingest from S3'
AS
COPY INTO my_table
FROM @my_s3_stage
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1);

-- 查看 Pipe 状态
SHOW PIPES;
SELECT * FROM TABLE(INFORMATION_SCHEMA.PIPE_USAGE_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_DATE())
));

-- 暂停/恢复 Pipe
ALTER PIPE my_pipe SET PIPE_EXECUTION_PAUSED = TRUE;
ALTER PIPE my_pipe SET PIPE_EXECUTION_PAUSED = FALSE;

-- 删除 Pipe
DROP PIPE my_pipe;
```

### 配置自动通知

需要在云存储中配置事件通知：

- **S3**: 配置 SQS 队列和 S3 事件通知
- **Azure**: 配置 Event Grid
- **GCS**: 配置 Pub/Sub

## 4.4 Snowpipe Streaming

Snowpipe Streaming 提供最低延迟的数据加载。

```python
# Python SDK 示例
from snowflake.ingest import SnowflakeIngestion, IngestResponse
from snowflake.ingest.utils.uris import DEFAULT_SCHEME

# 创建 Streaming 客户端
ingestion_client = SnowflakeIngestion(
    account_name='my_account',
    host='my_account.snowflakecomputing.com',
    user='my_user',
    private_key=private_key,
    role='my_role',
    scheme=DEFAULT_SCHEME,
    port=443
)

# 流式插入数据
response = ingestion_client.ingest_files(
    staging='my_stage',
    files=['data/file1.csv', 'data/file2.csv']
)

print(f"Insert response: {response}")
```

## 4.5 外部表

外部表允许直接查询外部存储的数据，无需加载。

```sql
-- 创建外部表
CREATE EXTERNAL TABLE ext_s3_data (
    id INT AS (VALUE:c1::INT),
    name VARCHAR AS (VALUE:c2::VARCHAR),
    value FLOAT AS (VALUE:c3::FLOAT)
)
LOCATION = @my_s3_stage/external/
FILE_FORMAT = my_csv_format
AUTO_REFRESH = TRUE;

-- 查询外部表
SELECT * FROM ext_s3_data WHERE id > 100;

-- 物化外部表结果
CREATE MATERIALIZED VIEW ext_data_mv AS
SELECT * FROM ext_s3_data;
```

## 4.6 数据共享

### 直接共享

```sql
-- 创建共享
CREATE SHARE my_share;

-- 添加对象到共享
GRANT USAGE ON DATABASE my_db TO SHARE my_share;
GRANT USAGE ON SCHEMA my_db.my_schema TO SHARE my_share;
GRANT SELECT ON TABLE my_db.my_schema.my_table TO SHARE my_share;

-- 添加消费者账号
ALTER SHARE my_share ADD ACCOUNT = consumer_account;
```

### 市场数据

```sql
-- 查看市场列表
SHOW LISTINGS;

-- 获取市场数据
CREATE DATABASE market_data FROM LISTING marketplace_listing;
```

---

# 第五部分：虚拟仓库与性能优化

## 5.1 虚拟仓库概述

虚拟仓库是 Snowflake 的计算资源集群，负责执行所有查询和 DML 操作。

### 仓库特性

- **独立资源**：每个仓库拥有独立的计算资源
- **不影响性能**：一个仓库的活动不影响其他仓库
- **弹性扩展**：可在运行时调整大小
- **多集群支持**：可配置多个集群处理并发
- **自动管理**：自动挂起和恢复

### 创建仓库

```sql
-- 创建基础仓库
CREATE WAREHOUSE my_warehouse
    WAREHOUSE_SIZE = 'X-Small'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    COMMENT = 'Development warehouse';

-- 创建多集群仓库
CREATE WAREHOUSE analytics_wh
    WAREHOUSE_SIZE = 'Large'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 5
    SCALING_POLICY = 'STANDARD'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- 创建 Snowpark 优化仓库
CREATE WAREHOUSE snowpark_wh
    WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
    WAREHOUSE_SIZE = 'Medium';
```

## 5.2 仓库大小与计费

### 计费模型

- **秒级计费**：最小计费 60 秒
- **按仓库大小计费**：每增加一个级别，费用翻倍
- **多集群额外计费**：每个集群独立计费

### 大小选择建议

| 场景 | 推荐大小 | 说明 |
|------|----------|------|
| 开发测试 | X-Small | 成本低，足够使用 |
| 小查询 | Small/Medium | 快速响应 |
| 复杂分析 | Large/X-Large | 需要更多计算资源 |
| 高并发 | 多集群 Small/Medium | 扩展并发能力 |
| 大数据加载 | Small/Large | 取决于文件数量 |
| 实时查询 | Medium/Large | 平衡性能和成本 |

### 调整仓库大小

```sql
-- 调整仓库大小（可在运行时执行）
ALTER WAREHOUSE my_warehouse SET WAREHOUSE_SIZE = 'Large';

-- 查看仓库状态
SHOW WAREHOUSES;
SELECT * FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_LOAD_HISTORY(
    DATE_RANGE_START => DATEADD('day', -1, CURRENT_DATE())
));
```

## 5.3 多集群仓库

多集群仓库自动扩展计算资源以处理并发查询。

```sql
-- 创建多集群仓库
CREATE WAREHOUSE multi_cluster_wh
    WAREHOUSE_SIZE = 'Medium'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 10
    SCALING_POLICY = 'ECONOMY'  -- 或 'STANDARD'
    AUTO_SUSPEND = 600
    AUTO_RESUME = TRUE;

-- 调整多集群设置
ALTER WAREHOUSE multi_cluster_wh
    SET MAX_CLUSTER_COUNT = 15
    SET SCALING_POLICY = 'STANDARD';
```

**扩缩策略：**

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **STANDARD** | 积极扩展，快速响应 | 高并发、延迟敏感 |
| **ECONOMY** | 保守扩展，节省成本 | 成本敏感、可接受排队 |

## 5.4 自动挂起与自动恢复

### 配置

```sql
-- 启用自动挂起和恢复
ALTER WAREHOUSE my_warehouse
    SET AUTO_SUSPEND = 300      -- 300 秒无活动后挂起
    SET AUTO_RESUME = TRUE;     -- 有查询时自动恢复

-- 禁用自动挂起
ALTER WAREHOUSE my_warehouse
    SET AUTO_SUSPEND = NULL;

-- 禁用自动恢复
ALTER WAREHOUSE my_warehouse
    SET AUTO_RESUME = FALSE;
```

### 最佳实践

- **开发环境**：AUTO_SUSPEND = 60（快速挂起节省成本）
- **生产环境**：AUTO_SUSPEND = 300-600（平衡响应和成本）
- **高并发环境**：禁用自动挂起或使用多集群

## 5.5 查询优化

### 查询分析

```sql
-- 查看查询执行计划
EXPLAIN SELECT * FROM my_table WHERE date_col = '2024-01-01';

-- 查看查询历史
SELECT 
    query_id,
    query_text,
    execution_time,
    bytes_scanned,
    partitions_scanned,
    partitions_total
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    DATE_RANGE_START => DATEADD('hour', -24, CURRENT_TIMESTAMP())
))
WHERE execution_time > 10000  -- 超过 10 秒的查询
ORDER BY execution_time DESC;

-- 查看查询 Profile
SHOW PROFILES;
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

### 优化技巧

#### 1. 分区裁剪

```sql
-- ✅ 利用分区裁剪（微分区）
SELECT * FROM sales
WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31';

-- ❌ 避免函数导致分区裁剪失效
SELECT * FROM sales
WHERE YEAR(sale_date) = 2024 AND MONTH(sale_date) = 1;
```

#### 2. 避免 SELECT *

```sql
-- ✅ 只选择需要的列
SELECT customer_id, order_date, total_amount
FROM orders;

-- ❌ 避免 SELECT *
SELECT * FROM orders;
```

#### 3. 使用适当的 JOIN

```sql
-- ✅ 使用 INNER JOIN 而不是 LEFT JOIN（当确定有匹配时）
SELECT c.customer_id, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- ✅ 先过滤再 JOIN
SELECT c.customer_id, o.order_id
FROM (
    SELECT customer_id 
    FROM customers 
    WHERE region = 'US'
) c
JOIN orders o ON c.customer_id = o.customer_id;
```

#### 4. 使用 CTE 提高可读性

```sql
-- ✅ 使用 CTE
WITH high_value_customers AS (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total_amount) > 10000
)
SELECT c.*
FROM customers c
WHERE c.customer_id IN (SELECT customer_id FROM high_value_customers);
```

#### 5. 利用缓存

```sql
-- ✅ 重复查询利用结果缓存
SELECT * FROM my_table WHERE date_col = '2024-01-01';
-- 第二次执行会使用缓存
```

## 5.6 缓存与物化视图

### 结果缓存

Snowflake 自动缓存查询结果：

- **缓存有效期**：24 小时
- **缓存失效**：底层数据变更时
- **自动利用**：相同查询自动使用缓存

### 元数据缓存

- **微分区元数据**：自动缓存
- **列统计信息**：min/max、空值计数等
- **自动优化**：无需手动管理

### 物化视图

```sql
-- 创建物化视图
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT 
    DATE_TRUNC('day', sale_date) AS sale_day,
    product_id,
    SUM(quantity) AS total_quantity,
    SUM(amount) AS total_amount
FROM sales
GROUP BY 1, 2;

-- 查询物化视图（自动刷新）
SELECT * FROM mv_daily_sales
WHERE sale_day = '2024-01-01';

-- 手动刷新
ALTER MATERIALIZED VIEW mv_daily_sales REFRESH;
```

## 5.7 聚簇键

聚簇键优化大表的查询性能。

```sql
-- 创建带聚簇键的表
CREATE TABLE large_sales (
    sale_date DATE,
    customer_id INT,
    product_id INT,
    amount DECIMAL(10,2)
)
CLUSTER BY (sale_date, customer_id);

-- 修改聚簇键
ALTER TABLE large_sales CLUSTER BY (sale_date, product_id);

-- 移除聚簇键
ALTER TABLE large_sales DROP CLUSTERING KEY;

-- 查看聚簇信息
SELECT SYSTEM$CLUSTERING_INFORMATION('large_sales');
```

**何时使用聚簇键：**
- 表大小超过数百 GB
- 查询有明确的过滤模式
- 数据按时间序列增长

---

# 第六部分：安全与访问控制

## 6.1 访问控制模型

Snowflake 采用混合访问控制模型：

### DAC (Discretionary Access Control)

- 对象所有者可以授予或撤销访问权限
- 默认情况下，创建对象的角色拥有所有权

### RBAC (Role-Based Access Control)

- 权限授予角色
- 角色分配给用户
- 用户通过角色获得权限

### UBAC (User-Based Access Control)

- 直接授予用户权限（较少使用）
- 仅在特定场景下使用

## 6.2 角色类型

| 角色类型 | 范围 | 用途 |
|----------|------|------|
| **Account Role** | 整个账号 | 管理账号级对象 |
| **Database Role** | 单个数据库 | 限制在数据库内 |
| **Application Role** | 原生应用 | 应用内访问控制 |
| **Service Role** | 服务端点 | 服务访问控制 |

## 6.3 系统角色

Snowflake 预定义的系统角色：

| 角色 | 权限 | 用途 |
|------|------|------|
| **ACCOUNTADMIN** | 最高权限 | 账号管理，谨慎使用 |
| **SECURITYADMIN** | 安全管理 | 用户和角色管理 |
| **USERADMIN** | 用户管理 | 专门管理用户和角色 |
| **SYSADMIN** | 系统管理 | 创建和管理数据库对象 |
| **PUBLIC** | 基础权限 | 所有用户自动拥有 |

### 角色层次

```
ACCOUNTADMIN
    ├── SECURITYADMIN
    │       └── USERADMIN
    └── SYSADMIN
```

## 6.4 权限授予

### 创建角色

```sql
-- 创建自定义角色
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;
CREATE ROLE data_scientist;

-- 角色层次
GRANT ROLE data_analyst TO ROLE data_engineer;
GRANT ROLE data_engineer TO ROLE SYSADMIN;
```

### 授予权限

```sql
-- 授予数据库权限
GRANT USAGE ON DATABASE analytics_db TO ROLE data_analyst;

-- 授予 Schema 权限
GRANT USAGE ON SCHEMA analytics_db.public TO ROLE data_analyst;

-- 授予表权限
GRANT SELECT ON TABLE analytics_db.public.sales TO ROLE data_analyst;

-- 授予多个表权限
GRANT SELECT ON ALL TABLES IN SCHEMA analytics_db.public TO ROLE data_analyst;
GRANT SELECT ON FUTURE TABLES IN SCHEMA analytics_db.public TO ROLE data_analyst;

-- 授予仓库使用权
GRANT USAGE ON WAREHOUSE analytics_wh TO ROLE data_analyst;

-- 授予多个权限
GRANT SELECT, INSERT, UPDATE ON TABLE my_table TO ROLE data_engineer;
```

### 分配角色给用户

```sql
-- 分配角色
GRANT ROLE data_analyst TO USER john_doe;
GRANT ROLE data_engineer TO USER jane_smith;

-- 设置默认角色
ALTER USER john_doe SET DEFAULT_ROLE = 'data_analyst';

-- 查看用户角色
SHOW GRANTS TO USER john_doe;
```

### 撤销权限

```sql
-- 撤销权限
REVOKE SELECT ON TABLE my_table FROM ROLE data_analyst;

-- 撤销角色
REVOKE ROLE data_analyst FROM USER john_doe;
```

### 查看权限

```sql
-- 查看角色权限
SHOW GRANTS TO ROLE data_analyst;

-- 查看对象权限
SHOW GRANTS ON TABLE my_table;

-- 查看用户权限
SHOW GRANTS TO USER john_doe;
```

## 6.5 数据安全

### 列级安全

```sql
-- 创建脱敏策略
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('HR_ADMIN') THEN val
        ELSE '***@***.***'
    END;

-- 应用脱敏策略
ALTER TABLE employees
    ALTER COLUMN email SET MASKING POLICY email_mask;
```

### 行级安全

```sql
-- 创建行访问策略
CREATE ROW ACCESS POLICY region_access AS (region STRING) RETURNS BOOLEAN ->
    CURRENT_ROLE() IN ('ADMIN', 'MANAGER')
    OR region IN (SELECT allowed_region FROM user_regions WHERE user_name = CURRENT_USER());

-- 应用行访问策略
ALTER TABLE sales
    ADD ROW ACCESS POLICY region_access ON (region);
```

### 数据加密

- **传输加密**：TLS 1.2+
- **存储加密**：自动加密所有数据
- **密钥管理**：Snowflake 管理或客户管理

### 审计

```sql
-- 查看登录历史
SELECT * FROM TABLE(INFORMATION_SCHEMA.LOGIN_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_DATE())
));

-- 查看查询历史
SELECT * FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    DATE_RANGE_START => DATEADD('day', -1, CURRENT_TIMESTAMP())
));

-- 查看复制历史
SELECT * FROM TABLE(INFORMATION_SCHEMA.REPLICATION_USAGE_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_DATE())
));
```

---

# 第七部分：高级功能

## 7.1 Streams 与 Tasks

### Streams（变更数据捕获）

```sql
-- 创建 Stream
CREATE STREAM my_stream ON TABLE my_table;

-- 查询变更数据
SELECT * FROM my_stream
WHERE metadata$action = 'INSERT';

-- 消费 Stream 后更新
CREATE TASK my_task
    WAREHOUSE = my_warehouse
    SCHEDULE = '5 MINUTE'
AS
MERGE INTO target_table t
USING (
    SELECT id, name, metadata$action
    FROM my_stream
) s
ON t.id = s.id
WHEN MATCHED AND s.metadata$action = 'DELETE' THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET t.name = s.name
WHEN NOT MATCHED AND s.metadata$action = 'INSERT' THEN
    INSERT (id, name) VALUES (s.id, s.name);
```

### Tasks（定时任务）

```sql
-- 创建 Task
CREATE TASK my_task
    WAREHOUSE = my_warehouse
    SCHEDULE = 'USING CRON 0 * * * * UTC'  -- 每小时
    COMMENT = 'Hourly data refresh'
AS
INSERT INTO target_table
SELECT * FROM source_table
WHERE updated_at > DATEADD('hour', -1, CURRENT_TIMESTAMP());

-- 创建 Task 依赖
CREATE TASK task2
    WAREHOUSE = my_warehouse
    AFTER task1
AS
UPDATE stats_table SET last_updated = CURRENT_TIMESTAMP();

-- 管理 Task
ALTER TASK my_task RESUME;  -- 启用
ALTER TASK my_task SUSPEND; -- 暂停

-- 查看 Task 历史
SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_DATE())
));
```

## 7.2 动态表

动态表自动刷新，基于查询定义。

```sql
-- 创建动态表
CREATE DYNAMIC TABLE mv_hourly_sales
    TARGET_LAG = '1 HOUR'
    WAREHOUSE = my_warehouse
AS
SELECT 
    DATE_TRUNC('hour', sale_time) AS sale_hour,
    product_id,
    SUM(quantity) AS total_quantity,
    SUM(amount) AS total_amount
FROM sales
GROUP BY 1, 2;

-- 查询动态表
SELECT * FROM mv_hourly_sales
WHERE sale_hour >= DATEADD('day', -1, CURRENT_TIMESTAMP());

-- 查看动态表状态
SHOW DYNAMIC TABLES;
```

## 7.3 Snowpark

Snowpark 允许使用 Python、Java、Scala 编写 Snowflake 逻辑。

```python
# Python Snowpark 示例
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum

# 创建会话
session = Session.builder.configs({
    "account": "my_account",
    "user": "my_user",
    "password": "my_password",
    "role": "my_role",
    "warehouse": "my_warehouse",
    "database": "my_db",
    "schema": "my_schema"
}).create()

# 读取表
df = session.table("sales")

# 转换
result = df.filter(col("amount") > 100) \
           .group_by("product_id") \
           .agg(sum("amount").alias("total_amount")) \
           .sort("total_amount", ascending=False)

# 显示结果
result.show()

# 写入表
result.write.mode("overwrite").save_as_table("high_value_sales")
```

## 7.4 Cortex AI

Cortex AI 提供 LLM 能力。

```sql
-- 文本摘要
SELECT SNOWFLAKE.CORTEX.SUMMARIZE(text_column) AS summary
FROM articles;

-- 情感分析
SELECT 
    review_text,
    SNOWFLAKE.CORTEX.SENTIMENT(review_text) AS sentiment_score
FROM product_reviews;

-- 文本分类
SELECT 
    text,
    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
        text, 
        ['positive', 'negative', 'neutral']
    ) AS classification
FROM feedback;

-- 翻译
SELECT 
    original_text,
    SNOWFLAKE.CORTEX.TRANSLATE(
        original_text, 
        'en', 
        'zh'
    ) AS translated_text
FROM documents;

-- 完成（文本生成）
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large',
    'Write a product description for a wireless headphone'
) AS description;
```

## 7.5 机器学习功能

```sql
-- 创建预测函数
CREATE SNOWFLAKE.ML.FORECAST sales_forecast(
    INPUT_DATA => TABLE(sales_data),
    TIMESTAMP_COLNAME => 'sale_date',
    TARGET_COLNAME => 'sales_amount',
    CONFIG => {'holiday_key': 'US'}
);

-- 使用预测
SELECT * FROM TABLE(sales_forecast(
    FORECASTING_PERIODS => 30
));

-- 异常检测
SELECT 
    *,
    SNOWFLAKE.ML.ANOMALY_DETECTION(
        OBJECT_CONSTRUCT('algorithm', 'IFOREST', 'contamination', 0.1)
    ) OVER (ORDER BY timestamp) AS anomaly_score
FROM metrics_data;
```

## 7.6 Time Travel

Time Travel 允许查询历史数据。

```sql
-- 查询 1 小时前的数据
SELECT * FROM my_table
AT(OFFSET => -60*60);

-- 查询特定时间点
SELECT * FROM my_table
AT(TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP);

-- 查询特定语句之前
SELECT * FROM my_table
BEFORE(STATEMENT => '01c2fc06-000e-6668-0000-76b90170a28e');

-- 恢复表
CREATE TABLE my_table_restored CLONE my_table
AT(TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP);

-- 恢复删除的行
INSERT INTO my_table
SELECT * FROM my_table
AT(OFFSET => -60*60)
WHERE id NOT IN (SELECT id FROM my_table);
```

**Time Travel 保留期：**
- 标准版：0-1 天
- 企业版：0-90 天
- 默认：1 天

## 7.7 Fail-safe

Fail-safe 提供数据恢复的最后保障：

- **保留期**：7 天（不可配置）
- **仅 Snowflake 可访问**：用户无法直接查询
- **需要联系支持**：数据恢复需要 Snowflake 支持团队
- **额外计费**：Fail-safe 存储单独计费

---

# 第八部分：开发流程

## 8.1 环境搭建

### Snowflake 账号

1. 访问 https://signup.snowflake.com 注册
2. 选择云平台和区域
3. 选择版本（Standard/Enterprise/Business Critical）
4. 设置管理员账号

### 连接工具

#### Snowsight (Web UI)

- 访问 https://app.snowflake.com
- 输入账号 URL 和凭证
- 直接在浏览器中编写和运行 SQL

#### SnowSQL (CLI)

```bash
# 安装 SnowSQL
# macOS
brew install snowflake

# 连接
snowsql -a my_account -u my_user -w my_warehouse -d my_db -s my_schema

# 执行 SQL 文件
snowsql -a my_account -u my_user -f script.sql
```

#### 驱动程序

```python
# Python Connector
pip install snowflake-connector-python
pip install snowflake-sqlalchemy

# JDBC
# 下载 snowflake-jdbc-x.x.x.jar

# ODBC
# 下载 Snowflake ODBC Driver
```

## 8.2 连接方式

### Python

```python
import snowflake.connector

# 基础连接
conn = snowflake.connector.connect(
    user='my_user',
    password='my_password',
    account='my_account',
    warehouse='my_warehouse',
    database='my_db',
    schema='my_schema',
    role='my_role'
)

# 使用连接参数
conn = snowflake.connector.connect(
    **{
        'user': 'my_user',
        'password': 'my_password',
        'account': 'my_account',
    }
)

# 执行查询
cursor = conn.cursor()
cursor.execute("SELECT * FROM my_table LIMIT 10")
results = cursor.fetchall()

# 使用 DataFrame
import pandas as pd
df = cursor.fetch_pandas_all()
```

### SQLAlchemy

```python
from sqlalchemy import create_engine

# 连接字符串
engine = create_engine(
    'snowflake://my_user:my_password@my_account/my_db/my_schema?warehouse=my_warehouse&role=my_role'
)

# 使用 pandas
import pandas as pd
df = pd.read_sql("SELECT * FROM my_table", engine)
```

### Snowpark

```python
from snowflake.snowpark import Session

# 创建会话
session = Session.builder.configs({
    "account": "my_account",
    "user": "my_user",
    "password": "my_password",
    "role": "my_role",
    "warehouse": "my_warehouse",
    "database": "my_db",
    "schema": "my_schema"
}).create()

# 使用 DataFrame API
df = session.table("my_table")
result = df.filter(df["amount"] > 100).collect()
```

## 8.3 数据建模最佳实践

### 分层架构

```
Raw Layer (原始层)
    ├── 原始数据，不做转换
    ├── 保留完整历史
    └── 用于审计和回溯

Staging Layer (暂存层)
    ├── 数据清洗和标准化
    ├── 数据类型转换
    └── 基础验证

Core Layer (核心层)
    ├── 业务规则应用
    ├── 主数据管理
    └── 一致性保证

Presentation Layer (展示层)
    ├── 聚合和汇总
    ├── 业务指标计算
    └── 面向最终用户
```

### 命名规范

```sql
-- 数据库命名
analytics_db      -- 小写，下划线分隔
raw_data_db
core_db

-- Schema 命名
raw               -- 原始数据
staging           -- 暂存数据
core              -- 核心数据
presentation      -- 展示数据

-- 表命名
fact_sales        -- 事实表，fact_ 前缀
dim_customer      -- 维度表，dim_ 前缀
agg_daily_sales   -- 聚合表，agg_ 前缀

-- 列命名
customer_id       -- ID 列，_id 后缀
created_at        -- 时间戳，_at 后缀
is_active         -- 布尔值，is_ 前缀
total_amount      -- 度量值
```

### 表设计原则

```sql
-- 事实表设计
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_id INT REFERENCES dim_date(date_id),
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY (date_id, customer_id);

-- 维度表设计
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),
    address VARCHAR(500),
    segment VARCHAR(50),
    effective_from DATE,
    effective_to DATE,
    is_current BOOLEAN DEFAULT TRUE
);
```

## 8.4 性能调优最佳实践

### 查询优化

```sql
-- 1. 使用 EXPLAIN 分析查询计划
EXPLAIN SELECT * FROM sales WHERE date_col = '2024-01-01';

-- 2. 避免全表扫描
-- ✅ 使用分区裁剪
SELECT * FROM sales WHERE sale_date = '2024-01-01';

-- ❌ 避免函数包裹分区列
SELECT * FROM sales WHERE DATE(sale_date) = '2024-01-01';

-- 3. 使用适当的 JOIN 类型
-- ✅ 使用 INNER JOIN 当确定有匹配
SELECT * FROM a INNER JOIN b ON a.id = b.id;

-- 4. 预过滤数据
SELECT * FROM (
    SELECT * FROM sales WHERE date_col > '2024-01-01'
) s
JOIN customers c ON s.customer_id = c.customer_id;

-- 5. 使用物化视图
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT 
    DATE_TRUNC('month', sale_date) AS month,
    SUM(amount) AS total_amount
FROM sales
GROUP BY 1;
```

### 加载优化

```sql
-- 1. 使用适当的文件大小
-- 推荐：10-250 MB（压缩后）

-- 2. 使用适当的文件数量
-- 文件数量应该与仓库集群数匹配或成倍数

-- 3. 使用 COPY 转换功能
COPY INTO target_table
FROM (
    SELECT $1, $2, $3, CURRENT_TIMESTAMP()
    FROM @stage/data.csv
)
FILE_FORMAT = (TYPE = 'CSV');

-- 4. 并行加载
-- Snowflake 自动并行化，确保文件数量足够

-- 5. 使用适当的仓库大小
-- 数据加载通常 Small-Medium 足够
```

### 仓库优化

```sql
-- 1. 为不同工作负载创建独立仓库
CREATE WAREHOUSE etl_wh WAREHOUSE_SIZE = 'Medium';
CREATE WAREHOUSE analytics_wh WAREHOUSE_SIZE = 'Large';
CREATE WAREHOUSE reporting_wh WAREHOUSE_SIZE = 'Small';

-- 2. 配置自动挂起
ALTER WAREHOUSE analytics_wh 
    SET AUTO_SUSPEND = 300
    SET AUTO_RESUME = TRUE;

-- 3. 使用多集群处理并发
CREATE WAREHOUSE concurrent_wh
    WAREHOUSE_SIZE = 'Medium'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 5;

-- 4. 监控仓库使用
SELECT * FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_LOAD_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_DATE())
));
```

## 8.5 成本优化最佳实践

### 存储成本

```sql
-- 1. 使用适当的表类型
CREATE TRANSIENT TABLE temp_data (
    id INT,
    data VARCHAR
)
DATA_RETENTION_TIME_IN_DAYS = 1;  -- 最短保留期

-- 2. 清理不需要的数据
DELETE FROM old_data WHERE created_at < DATEADD('year', -2, CURRENT_DATE());

-- 3. 使用压缩
-- Snowflake 自动压缩，但良好的数据类型选择有帮助

-- 4. 监控存储使用
SELECT * FROM TABLE(INFORMATION_SCHEMA.TABLE_STORAGE_METRICS(
    TABLE_CATALOG => 'MY_DB',
    TABLE_SCHEMA => 'PUBLIC'
));
```

### 计算成本

```sql
-- 1. 使用适当的仓库大小
-- 不要过度配置

-- 2. 配置自动挂起
ALTER WAREHOUSE my_wh SET AUTO_SUSPEND = 60;

-- 3. 使用资源监控器
CREATE RESOURCE MONITOR my_monitor
    WITH CREDIT_QUOTA = 100
    TRIGGERS
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO SUSPEND
        ON 100 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE my_wh SET RESOURCE_MONITOR = my_monitor;

-- 4. 监控查询成本
SELECT 
    query_id,
    query_text,
    credits_used,
    execution_time
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    DATE_RANGE_START => DATEADD('day', -1, CURRENT_TIMESTAMP())
))
WHERE credits_used > 1
ORDER BY credits_used DESC;
```

### 数据传输成本

```sql
-- 1. 同区域部署
-- 确保仓库和数据在同一区域

-- 2. 避免跨区域查询
-- 使用复制而非跨区域查询

-- 3. 监控数据传输
SELECT * FROM TABLE(INFORMATION_SCHEMA.DATA_TRANSFER_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_DATE())
));
```

---

# 第九部分：实战代码示例

## Demo 1: 创建表并加载数据

```sql
-- 创建数据库和 Schema
CREATE DATABASE ecommerce_db;
USE DATABASE ecommerce_db;
CREATE SCHEMA raw;

-- 创建维度表
CREATE TABLE raw.dim_customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(200),
    phone VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE raw.dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE
);

-- 创建事实表
CREATE TABLE raw.fact_orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES raw.dim_customers(customer_id),
    order_date DATE,
    ship_date DATE,
    status VARCHAR(50),
    total_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    shipping_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE raw.fact_order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT REFERENCES raw.fact_orders(order_id),
    product_id INT REFERENCES raw.dim_products(product_id),
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(10,2),
    line_total DECIMAL(10,2)
);

-- 创建 Stage
CREATE STAGE raw.ecommerce_stage
    URL = 's3://my-ecommerce-bucket/data/'
    STORAGE_INTEGRATION = my_s3_integration;

-- 创建文件格式
CREATE FILE FORMAT raw.csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL');

-- 加载数据
COPY INTO raw.dim_customers
FROM @raw.ecommerce_stage/customers/
FILE_FORMAT = (FORMAT_NAME = raw.csv_format)
ON_ERROR = 'CONTINUE';

COPY INTO raw.dim_products
FROM @raw.ecommerce_stage/products/
FILE_FORMAT = (FORMAT_NAME = raw.csv_format);

COPY INTO raw.fact_orders
FROM @raw.ecommerce_stage/orders/
FILE_FORMAT = (FORMAT_NAME = raw.csv_format);

COPY INTO raw.fact_order_items
FROM @raw.ecommerce_stage/order_items/
FILE_FORMAT = (FORMAT_NAME = raw.csv_format);

-- 验证加载
SELECT COUNT(*) FROM raw.dim_customers;
SELECT COUNT(*) FROM raw.fact_orders;
SELECT COUNT(*) FROM raw.fact_order_items;
```

## Demo 2: 数据转换与 ETL

```sql
-- 创建核心层 Schema
CREATE SCHEMA core;

-- 创建转换视图
CREATE OR REPLACE VIEW core.vw_customer_orders AS
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.city,
    c.state,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date
FROM raw.dim_customers c
LEFT JOIN raw.fact_orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2, 3, 4, 5;

-- 创建聚合表
CREATE TABLE core.agg_daily_sales (
    sale_date DATE PRIMARY KEY,
    order_count INT,
    customer_count INT,
    total_revenue DECIMAL(12,2),
    avg_order_value DECIMAL(10,2),
    top_product_id INT,
    top_product_sales DECIMAL(10,2)
);

-- 填充聚合表
INSERT INTO core.agg_daily_sales
WITH daily_stats AS (
    SELECT 
        o.order_date AS sale_date,
        COUNT(DISTINCT o.order_id) AS order_count,
        COUNT(DISTINCT o.customer_id) AS customer_count,
        SUM(o.total_amount) AS total_revenue,
        AVG(o.total_amount) AS avg_order_value
    FROM raw.fact_orders o
    GROUP BY 1
),
product_ranking AS (
    SELECT 
        DATE(o.order_date) AS sale_date,
        oi.product_id AS top_product_id,
        SUM(oi.line_total) AS product_sales,
        ROW_NUMBER() OVER (PARTITION BY DATE(o.order_date) ORDER BY SUM(oi.line_total) DESC) AS rn
    FROM raw.fact_orders o
    JOIN raw.fact_order_items oi ON o.order_id = oi.order_id
    GROUP BY 1, 2
)
SELECT 
    d.sale_date,
    d.order_count,
    d.customer_count,
    d.total_revenue,
    d.avg_order_value,
    p.top_product_id,
    p.product_sales AS top_product_sales
FROM daily_stats d
LEFT JOIN product_ranking p ON d.sale_date = p.sale_date AND p.rn = 1;

-- 创建 Task 自动刷新
CREATE TASK core.task_refresh_daily_sales
    WAREHOUSE = etl_wh
    SCHEDULE = 'USING CRON 0 2 * * * UTC'  -- 每天 UTC 2:00
AS
INSERT OVERWRITE INTO core.agg_daily_sales
SELECT * FROM (
    -- 上面的 INSERT 逻辑
);

ALTER TASK core.task_refresh_daily_sales RESUME;
```

## Demo 3: 半结构化数据处理

```sql
-- 创建存储 JSON 数据的表
CREATE TABLE raw.json_events (
    event_id INT AUTOINCREMENT PRIMARY KEY,
    event_data VARIANT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- 加载 JSON 数据
COPY INTO raw.json_events (event_data)
FROM @raw.ecommerce_stage/events/
FILE_FORMAT = (TYPE = 'JSON' STRIP_OUTER_ARRAY = TRUE);

-- 查询 JSON 数据
SELECT 
    event_data:id::INT AS event_id,
    event_data:type::VARCHAR AS event_type,
    event_data:timestamp::TIMESTAMP AS event_time,
    event_data:user.id::INT AS user_id,
    event_data:user.email::VARCHAR AS user_email,
    event_data:properties.product_id::INT AS product_id,
    event_data:properties.amount::DECIMAL(10,2) AS amount
FROM raw.json_events
WHERE event_data:type::VARCHAR = 'purchase';

-- 展平嵌套数组
SELECT 
    e.event_data:id::INT AS event_id,
    e.event_data:type::VARCHAR AS event_type,
    f.value:item_id::INT AS item_id,
    f.value:quantity::INT AS quantity,
    f.value:price::DECIMAL(10,2) AS price
FROM raw.json_events e,
LATERAL FLATTEN(input => e.event_data:items) f;

-- 创建结构化视图
CREATE TABLE core.fact_events (
    event_id INT,
    event_type VARCHAR,
    event_time TIMESTAMP,
    user_id INT,
    product_id INT,
    amount DECIMAL(10,2),
    properties VARIANT
);

INSERT INTO core.fact_events
SELECT 
    event_data:id::INT,
    event_data:type::VARCHAR,
    event_data:timestamp::TIMESTAMP,
    event_data:user.id::INT,
    event_data:properties.product_id::INT,
    event_data:properties.amount::DECIMAL(10,2),
    event_data:properties
FROM raw.json_events;
```

## Demo 4: 增量加载与 CDC

```sql
-- 创建 Stream 捕获变更
CREATE STREAM raw.customer_stream ON TABLE raw.dim_customers;

-- 查看变更数据
SELECT 
    customer_id,
    first_name,
    last_name,
    metadata$action,
    metadata$isupdate,
    metadata$row_id
FROM raw.customer_stream;

-- 创建 SCD Type 2 表
CREATE TABLE core.dim_customer_scd2 (
    customer_key INT AUTOINCREMENT PRIMARY KEY,
    customer_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(200),
    effective_from TIMESTAMP,
    effective_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);

-- 初始加载
INSERT INTO core.dim_customer_scd2 (
    customer_id, first_name, last_name, email, effective_from, effective_to, is_current
)
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    created_at,
    '9999-12-31'::TIMESTAMP,
    TRUE
FROM raw.dim_customers;

-- 增量处理 Task
CREATE TASK core.task_process_customer_changes
    WAREHOUSE = etl_wh
    SCHEDULE = '15 MINUTE'
AS
BEGIN
    -- 关闭当前记录
    UPDATE core.dim_customer_scd2
    SET 
        effective_to = CURRENT_TIMESTAMP(),
        is_current = FALSE
    WHERE customer_id IN (
        SELECT DISTINCT customer_id 
        FROM raw.customer_stream 
        WHERE metadata$action = 'INSERT' AND metadata$isupdate = TRUE
    )
    AND is_current = TRUE;
    
    -- 插入新记录
    INSERT INTO core.dim_customer_scd2 (
        customer_id, first_name, last_name, email, effective_from, effective_to, is_current
    )
    SELECT 
        customer_id,
        first_name,
        last_name,
        email,
        CURRENT_TIMESTAMP(),
        '9999-12-31'::TIMESTAMP,
        TRUE
    FROM raw.customer_stream
    WHERE metadata$action = 'INSERT' AND metadata$isupdate = TRUE;
END;

ALTER TASK core.task_process_customer_changes RESUME;
```

## Demo 5: 多表关联查询优化

```sql
-- 优化前：多个子查询
SELECT 
    c.customer_id,
    c.first_name,
    (SELECT COUNT(*) FROM raw.fact_orders o WHERE o.customer_id = c.customer_id) AS order_count,
    (SELECT SUM(total_amount) FROM raw.fact_orders o WHERE o.customer_id = c.customer_id) AS total_spent,
    (SELECT MAX(order_date) FROM raw.fact_orders o WHERE o.customer_id = c.customer_id) AS last_order
FROM raw.dim_customers c
WHERE c.is_active = TRUE;

-- 优化后：使用 JOIN 和 GROUP BY
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    MAX(o.order_date) AS last_order_date
FROM raw.dim_customers c
LEFT JOIN raw.fact_orders o ON c.customer_id = o.customer_id
WHERE c.is_active = TRUE
GROUP BY 1, 2, 3;

-- 进一步优化：使用 CTE
WITH customer_stats AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS order_count,
        SUM(total_amount) AS total_spent,
        MAX(order_date) AS last_order_date,
        AVG(total_amount) AS avg_order_value
    FROM raw.fact_orders
    GROUP BY 1
)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    COALESCE(s.order_count, 0) AS order_count,
    COALESCE(s.total_spent, 0) AS total_spent,
    s.last_order_date,
    s.avg_order_value,
    CASE 
        WHEN s.total_spent > 10000 THEN 'VIP'
        WHEN s.total_spent > 5000 THEN 'Gold'
        WHEN s.total_spent > 1000 THEN 'Silver'
        ELSE 'Bronze'
    END AS customer_tier
FROM raw.dim_customers c
LEFT JOIN customer_stats s ON c.customer_id = s.customer_id
WHERE c.is_active = TRUE
ORDER BY s.total_spent DESC NULLS LAST;

-- 使用窗口函数分析
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    o.order_date,
    o.total_amount,
    SUM(o.total_amount) OVER (
        PARTITION BY c.customer_id 
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    LAG(o.total_amount) OVER (
        PARTITION BY c.customer_id 
        ORDER BY o.order_date
    ) AS prev_order_amount,
    RANK() OVER (
        PARTITION BY DATE_TRUNC('month', o.order_date)
        ORDER BY o.total_amount DESC
    ) AS monthly_rank
FROM raw.dim_customers c
JOIN raw.fact_orders o ON c.customer_id = o.customer_id
WHERE c.is_active = TRUE
QUALIFY monthly_rank <= 10;  -- Snowflake 特有的 QUALIFY 子句
```

---

## 附录：常用资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.snowflake.com |
| Snowsight | https://app.snowflake.com |
| 社区论坛 | https://community.snowflake.com |
| 知识库 | https://community.snowflake.com/s/article/Snowflake-Help-Support |
| 培训 | https://www.snowflake.com/en/training/ |
| 认证 | https://www.snowflake.com/en/certifications/ |
| 市场 | https://www.snowflake.com/en/data-cloud/marketplace/ |
| GitHub | https://github.com/Snowflake-Labs |
| Python Connector | https://docs.snowflake.com/en/developer-guide/python-connector/python-connector |
| Snowpark | https://docs.snowflake.com/en/developer-guide/snowpark/python/index |

---

> 📝 本文档基于 Snowflake 2026 年最新官方文档整理
> 作者：Robin 的 AI 助手
> 最后更新：2026-06-10
