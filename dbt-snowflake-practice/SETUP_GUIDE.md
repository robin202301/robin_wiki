# Snowflake 实战项目搭建指南

## 第一步：创建 Snowflake 免费试用账户

1. 访问 https://signup.snowflake.com/
2. 填写信息注册（需要邮箱，无需信用卡）
3. 选择 **Enterprise** 版本
4. 选择最近的 AWS 区域（例如 US East / US West）

## 第二步：在 Snowflake 中创建资源

登录 Snowsight（Snowflake Web UI），依次执行以下 SQL：

```sql
-- 1. 创建虚拟仓库（计算资源）
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH_PRACTICE
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- 2. 创建数据库
CREATE DATABASE IF NOT EXISTS ANALYTICS_DEV;

-- 3. 创建角色
CREATE ROLE IF NOT EXISTS DBT_PRACTICE_ROLE;

-- 4. 授权
GRANT ALL ON WAREHOUSE COMPUTE_WH_PRACTICE TO ROLE DBT_PRACTICE_ROLE;
GRANT ALL ON DATABASE ANALYTICS_DEV TO ROLE DBT_PRACTICE_ROLE;
GRANT ALL ON ALL SCHEMAS IN DATABASE ANALYTICS_DEV TO ROLE DBT_PRACTICE_ROLE;

-- 5. 创建用户并关联角色
CREATE USER IF NOT EXISTS dbt_practice
  PASSWORD = 'YourStrongPassword123!'
  DEFAULT_ROLE = DBT_PRACTICE_ROLE
  DEFAULT_WAREHOUSE = COMPUTE_WH_PRACTICE;

GRANT ROLE DBT_PRACTICE_ROLE TO USER dbt_practice;
```

## 第三步：获取 Account ID

1. 登录 Snowsight
2. 查看浏览器 URL，格式如：`https://xy12345.us-east-1.snowflakecomputing.com`
3. 其中 `xy12345.us-east-1` 就是你的 Account ID

## 第四步：配置 dbt profiles

编辑 `~/.dbt/profiles.yml`：

```yaml
dbt_snowflake_practice:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "xy12345.us-east-1"   # ← 替换为你的 Account ID
      user: "dbt_practice"
      password: "YourStrongPassword123!"
      role: "DBT_PRACTICE_ROLE"
      database: "ANALYTICS_DEV"
      warehouse: "COMPUTE_WH_PRACTICE"
      schema: "dbt_practice"
      threads: 4
```

## 第五步：验证连接

```bash
dbt debug --profiles-dir ~/.dbt
```

看到 `✓ Connection test: OK` 即配置成功！

## 第六步：运行项目

```bash
cd dbt-snowflake-practice

# 安装依赖包
dbt deps

# 加载种子数据
dbt seed

# 运行模型
dbt run

# 运行测试
dbt test

# 查看数据血缘
dbt docs generate
dbt docs serve
```

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| `250001: Could not connect` | 检查 Account ID 是否正确 |
| `JWT token is invalid` | 检查用户名和密码 |
| `Object does not exist` | 确认 warehouse/database/schema 已创建 |
| 免费版额度用完 | Snowflake 试用期 30 天，$400 额度 |
