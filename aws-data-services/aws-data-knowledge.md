# AWS 数据服务知识体系

## 一、整体架构概览

### 1.1 AWS数据服务分类

```
数据存储层
├── 对象存储: S3
├── 关系数据库: RDS, Aurora
├── NoSQL: DynamoDB, DocumentDB
├── 数据仓库: Redshift
└── 缓存: ElastiCache, MemoryDB

数据处理层
├── ETL: Glue, Data Pipeline
├── 大数据: EMR, EMR Serverless
├── 流处理: Kinesis, Managed Streaming for Kafka (MSK)
├── 无服务器计算: Lambda, Fargate
└── 工作流: Step Functions, Airflow (MWAA)

数据分析层
├── 交互式查询: Athena
├── 可视化: QuickSight
├── 搜索: OpenSearch Service
├── 数据湖分析: Lake Formation
└── 日志分析: CloudWatch Logs Insights

数据集成层
├── 数据迁移: DMS (Database Migration Service)
├── 数据传输: Snowball, DataSync
├── 应用集成: AppFlow, EventBridge
└── API管理: API Gateway

机器学习层
├── ML平台: SageMaker
├── 预训练服务: Comprehend, Rekognition, Transcribe
└── AI服务: Bedrock, Lex, Polly
```

---

## 二、核心数据存储服务

### 2.1 Amazon S3 (Simple Storage Service)

#### 基础概念
- **Bucket**: 存储容器，全局唯一命名
- **Object**: 数据对象，最大5TB
- **Key**: 对象键（路径）
- **Region**: 存储区域

#### 存储类别
| 类别 | 适用场景 | 成本 | 访问频率 |
|------|---------|------|---------|
| S3 Standard | 频繁访问 | 高 | 高 |
| S3 Intelligent-Tiering | 访问模式未知 | 中 | 自动 |
| S3 Standard-IA | 偶尔访问 | 中低 | 低 |
| S3 One Zone-IA | 不重要数据 | 低 | 低 |
| S3 Glacier Instant | 归档即时访问 | 很低 | 极低 |
| S3 Glacier Flexible | 归档 | 很低 | 极低（分钟-小时） |
| S3 Glacier Deep Archive | 长期归档 | 最低 | 极少（12小时） |

#### 生命周期策略
```json
{
  "Rules": [
    {
      "ID": "Move to IA after 30 days",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

#### 性能优化
- **分区策略**: 使用日期前缀 `s3://bucket/year=2024/month=01/day=15/`
- **请求速率**: 3,500 PUT/5,500 GET每秒每前缀
- **Multipart Upload**: >100MB文件分片上传
- **Transfer Acceleration**: 使用CloudFront边缘节点加速

#### 安全
- **Bucket Policy**: JSON策略文档
- **IAM Policy**: 用户/组/角色权限
- **Block Public Access**: 阻止公开访问
- **Encryption**: 
  - SSE-S3 (AWS管理密钥)
  - SSE-KMS (KMS密钥)
  - SSE-C (客户密钥)
- **VPC Endpoint**: 私有访问

#### S3 Select & Glacier Select
```sql
SELECT s.name, s.age
FROM S3Object s
WHERE s.age > 30
```

---

### 2.2 Amazon RDS (Relational Database Service)

#### 支持的引擎
- **Aurora** (MySQL/PostgreSQL兼容) - AWS原生
- **MySQL**
- **PostgreSQL**
- **Oracle**
- **SQL Server**
- **MariaDB**

#### Aurora特性
- **性能**: 比MySQL快5倍，比PostgreSQL快3倍
- **存储**: 自动扩展至128TB
- **高可用**: 6副本跨3AZ
- **读副本**: 最多15个
- **Aurora Serverless v2**: 自动扩缩容

#### Multi-AZ部署
- **主实例**: 可用区A
- **备用实例**: 可用区B/C（同步复制）
- **故障转移**: 自动切换，通常60-120秒

#### 读副本
- 异步复制
- 最多5个直接读副本
- 可级联（但增加延迟）
- 跨Region复制支持

#### 备份策略
- **自动备份**: 保留1-35天
- **快照**: 手动创建，长期保留
- **时间点恢复**: 恢复到5分钟精度

#### 最佳实践
```yaml
# CloudFormation示例
MyDB:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceClass: db.r5.large
    Engine: aurora-postgresql
    MultiAZ: true
    StorageEncrypted: true
    BackupRetentionPeriod: 7
    EnablePerformanceInsights: true
    MonitoringInterval: 60
```

---

### 2.3 Amazon DynamoDB

#### 核心概念
- **表**: 数据集合
- **项目**: 一行记录
- **属性**: 一列数据
- **分区键**: 数据分布
- **排序键**: 排序和范围查询

#### 容量模式
| 模式 | 特点 | 适用场景 |
|------|------|---------|
| On-Demand | 自动扩缩 | 不可预测负载 |
| Provisioned | 预置RCU/WCU | 可预测负载 |

#### 性能单位
- **RCU (Read Capacity Unit)**: 1次强一致读/秒（4KB）或2次最终一致读/秒
- **WCU (Write Capacity Unit)**: 1次写入/秒（1KB）

#### 索引类型
- **主索引**: 分区键 + 可选排序键
- **GSI (Global Secondary Index)**: 不同分区键，跨表
- **LSI (Local Secondary Index)**: 相同分区键，不同排序键，创建时定义

#### DAX (DynamoDB Accelerator)
- 内存缓存
- 微秒级延迟
- 兼容DynamoDB API

#### 最佳实践
- **分区设计**: 避免热点分区
- **单表设计**: 相关数据放一起
- **稀疏索引**: 减少无用数据
- **TTL**: 自动过期数据

---

### 2.4 Amazon Redshift

#### 架构
- **集群**: 计算+存储资源
- **节点类型**:
  - Leader Node: 协调查询
  - Compute Node: 存储和执行

#### 存储架构
- **列式存储**: 优化分析查询
- **数据分布**:
  - KEY: 按分布键哈希
  - EVEN: 轮询分布
  - ALL: 复制到所有节点
- **排序键**:
  - Compound: 多列组合
  - Interleaved: 多列独立

#### Redshift Spectrum
- 直接查询S3数据
- 无需加载到Redshift
- 支持多种格式（Parquet/ORC/CSV/JSON）
- 按扫描数据量计费

#### 性能优化
```sql
-- 表设计
CREATE TABLE sales (
    sale_id INTEGER,
    product_id INTEGER,
    sale_date DATE,
    amount DECIMAL(10,2)
)
DISTKEY(product_id)
SORTKEY(sale_date);

-- 压缩
ANALYZE COMPRESSION sales;

--  Vacuum (回收空间)
VACUUM FULL sales;

-- 统计信息更新
ANALYZE sales;
```

#### 工作负载管理(WLM)
- 最多50个队列
- 基于查询优先级分配资源
- 自动WLM（推荐）

#### Serverless
- 无需管理集群
- 自动扩缩容
- 按RPU（Redshift Processing Units）计费

---

## 三、数据处理服务

### 3.1 AWS Glue

#### 核心组件

##### Glue Data Catalog
- **数据库**: 表的逻辑分组
- **表**: Schema定义
- **Crawler**: 自动发现Schema
- **Connection**: 数据源连接信息

##### Glue ETL Jobs
```python
# PySpark示例
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

glueContext = GlueContext(SparkContext.getOrCreate())
job = Job(glueContext)

# 从Data Catalog读取
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="my_database",
    table_name="my_table"
)

# 转换
transformed = datasource.apply_mapping([
    ("id", "int", "user_id", "int"),
    ("name", "string", "full_name", "string")
])

# 过滤
filtered = transformed.filter(lambda x: x["age"] > 18)

# 写入S3
glueContext.write_dynamic_frame.from_options(
    frame=filtered,
    connection_type="s3",
    connection_options={"path": "s3://bucket/output/"},
    format="parquet"
)
```

##### Glue Crawler
```python
# 自动发现Schema
crawler = boto3.client('glue')
crawler.start_crawler(
    Name='my-crawler',
    DatabaseName='target_db',
    Role='GlueServiceRole',
    Targets={
        'S3Targets': [
            {'Path': 's3://bucket/data/'}
        ]
    },
    SchemaChangePolicy={
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'LOG'
    }
)
```

##### Glue Studio
- 可视化ETL编辑器
- 拖拽组件构建作业
- 代码生成

##### Glue DataBrew
- 数据清洗和准备
- 90+预置转换
- 无代码/低代码

#### Glue版本
| 版本 | 特点 |
|------|------|
| Glue 3.0 | Spark 3.1, Python 3 |
| Glue 4.0 | Spark 3.3, Python 3.10, Ray支持 |

#### 性能优化
- **Worker类型**: G.1X, G.2X（内存/CPU）
- **自动扩展**: 动态分配worker
- **作业书签**: 增量处理
- **分区**: 减少扫描数据量

#### 成本优化
- DPU（Data Processing Units）计费
- 开发端点按需启动/停止
- 使用Glue Studio监控

---

### 3.2 Amazon EMR (Elastic MapReduce)

#### 支持的框架
- **Apache Spark**
- **Apache Hadoop**
- **Apache Hive**
- **Apache HBase**
- **Apache Flink**
- **Presto/Trino**
- **Apache Kafka**

#### 集群架构
- **Master Node**: 管理集群
- **Core Node**: 存储HDFS + 计算
- **Task Node**: 仅计算（可伸缩）

#### 实例类型
- **按需实例**: 稳定负载
- **竞价实例**: 容错工作负载，节省90%
- **预留实例**: 长期承诺

#### EMR Serverless
- 无需管理集群
- 自动扩缩容
- 按实际使用计费
- 支持Spark和Hive

#### 最佳实践
```yaml
# EMR集群配置
{
  "Name": "MyCluster",
  "ReleaseLabel": "emr-6.10.0",
  "Applications": [
    {"Name": "Spark"},
    {"Name": "Hive"}
  ],
  "Instances": {
    "MasterInstanceGroup": {
      "InstanceCount": 1,
      "InstanceType": "m5.xlarge",
      "Market": "ON_DEMAND"
    },
    "CoreInstanceGroup": {
      "InstanceCount": 4,
      "InstanceType": "m5.2xlarge",
      "Market": "SPOT",
      "BidPrice": "0.50"
    }
  },
  "Configurations": [
    {
      "Classification": "spark-defaults",
      "Properties": {
        "spark.executor.memory": "8g",
        "spark.executor.cores": "4"
      }
    }
  ]
}
```

#### 性能调优
- **内存**: `spark.executor.memory`, `spark.driver.memory`
- **并行度**: `spark.executor.instances`, `spark.sql.shuffle.partitions`
- **序列化**: Kryo序列化
- **压缩**: Snappy/LZO压缩中间数据

---

### 3.3 AWS Lambda

#### 基本概念
- **函数**: 代码单元
- **触发器**: 事件源
- **执行角色**: IAM权限
- **层**: 共享代码/依赖

#### 限制
- **内存**: 128MB - 10GB
- **超时**: 最长15分钟
- **部署包**: 50MB压缩，250MB解压
- **并发**: 默认1000，可申请提升

#### 数据处理场景
```python
import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # S3事件触发
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # 读取文件
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        
        # 处理数据
        # ...
        
        # 写入结果
        s3.put_object(
            Bucket='output-bucket',
            Key=f"processed/{key}",
            Body=json.dumps(result)
        )
    
    return {'statusCode': 200}
```

#### 最佳实践
- **无状态**: 函数应无状态
- **幂等性**: 处理重复事件
- **连接池**: 复用数据库连接
- **环境变量**: 配置外部化

---

## 四、数据分析服务

### 4.1 Amazon Athena

#### 核心特性
- **无服务器**: 无需管理基础设施
- **交互式查询**: 标准SQL
- **直接查询S3**: 无需ETL
- **按查询付费**: 按扫描数据量

#### 支持的数据格式
- CSV, JSON, Avro, Parquet, ORC
- 压缩: Snappy, Gzip, LZ4

#### 性能优化
```sql
-- 分区表
CREATE EXTERNAL TABLE sales (
    product_id INT,
    amount DECIMAL(10,2)
)
PARTITIONED BY (year INT, month INT, day INT)
STORED AS PARQUET
LOCATION 's3://bucket/sales/';

-- 添加分区
MSCK REPAIR TABLE sales;
-- 或
ALTER TABLE sales ADD PARTITION (year=2024, month=1, day=15)
LOCATION 's3://bucket/sales/2024/01/15/';

-- 查询时指定分区（减少扫描）
SELECT * FROM sales
WHERE year = 2024 AND month = 1;

-- 使用CTAS优化
CREATE TABLE sales_summary
WITH (format = 'PARQUET')
AS SELECT product_id, SUM(amount) as total
FROM sales
GROUP BY product_id;
```

#### 成本优化
- **列式格式**: Parquet/ORC减少扫描
- **压缩**: 减少数据传输
- **分区**: 限制扫描范围
- **CTAS**: 预聚合常用查询

#### Federated Query
```sql
-- 查询RDS
SELECT * FROM lambda_mysql.mydb.users
WHERE created_at > '2024-01-01';

-- 查询DynamoDB
SELECT * FROM lambda_dynamodb.mytable
WHERE user_id = '123';
```

---

### 4.2 Amazon Kinesis

#### 数据流类型

##### Kinesis Data Streams
- **实时流处理**
- **分片**: 并行处理单元
- **容量**: 每分片1MB/s写入，2MB/s读取
- **保留期**: 1-365天

```python
# 写入数据
kinesis = boto3.client('kinesis')
kinesis.put_record(
    StreamName='my-stream',
    Data=json.dumps({'user_id': 123, 'action': 'click'}),
    PartitionKey='user_123'
)

# 批量写入
kinesis.put_records(
    StreamName='my-stream',
    Records=[
        {'Data': b'data1', 'PartitionKey': 'key1'},
        {'Data': b'data2', 'PartitionKey': 'key2'}
    ]
)
```

##### Kinesis Data Firehose
- **自动加载**到S3/Redshift/Elasticsearch
- **无需管理代码**
- **近实时**（60秒延迟）
- **自动扩展**

##### Kinesis Data Analytics
- **流SQL处理**
- **Apache Flink**
- **实时聚合/过滤/转换**

##### Kinesis Video Streams
- **视频流存储**
- **实时处理**
- **机器学习集成**

#### 应用场景
- 日志聚合
- 实时分析
- IoT数据处理
- 点击流分析

---

### 4.3 Amazon QuickSight

#### 核心功能
- **数据可视化**: 图表、仪表板
- **数据源**: S3, RDS, Redshift, Athena等
- **SPICE**: 内存计算引擎
- **ML洞察**: 自动异常检测、预测

#### 数据源连接
```python
# 通过API创建数据源
quicksight = boto3.client('quicksight')
quicksight.create_data_source(
    AwsAccountId='123456789012',
    DataSourceId='my-athena',
    Name='Athena Data Source',
    Type='ATHENA',
    AthenaParameters={
        'WorkGroup': 'primary'
    }
)
```

#### 计费模式
- **Standard**: $9/用户/月
- **Enterprise**: $18/用户/月（ML功能）

---

## 五、数据集成服务

### 5.1 AWS DMS (Database Migration Service)

#### 迁移类型
- **Homogeneous**: 相同数据库类型（MySQL→MySQL）
- **Heterogeneous**: 不同数据库类型（Oracle→Aurora）
- **Schema Conversion**: SCT工具转换Schema

#### 复制任务
```json
{
  "SourceEndpointArn": "arn:aws:dms:us-east-1:123456789:endpoint:source",
  "TargetEndpointArn": "arn:aws:dms:us-east-1:123456789:endpoint:target",
  "ReplicationInstanceArn": "arn:aws:dms:us-east-1:123456789:rep:instance",
  "MigrationType": "full-load-and-cdc",
  "TableMappings": "{...}",
  "ReplicationTaskSettings": "{...}"
}
```

#### CDC (Change Data Capture)
- 实时捕获变更
- 基于日志（MySQL binlog, Oracle redo log）
- 持续复制

#### 最佳实践
- **预迁移评估**: 使用Schema Conversion Tool
- **测试迁移**: 先在测试环境验证
- **监控**: CloudWatch指标
- **切换窗口**: 计划停机时间

---

### 5.2 Amazon AppFlow

#### 集成应用
- **SaaS**: Salesforce, Slack, ServiceNow, Zendesk
- **AWS服务**: S3, Redshift, EventBridge

#### 流程配置
```python
appflow = boto3.client('appflow')
appflow.create_flow(
    flowName='salesforce-to-s3',
    destinationFlowConfigList=[{
        'connectorType': 'S3',
        'destinationConnectorProperties': {
            'S3': {
                'bucketName': 'my-bucket',
                'object': {'key': 'salesforce/'}
            }
        }
    }],
    sourceFlowConfig={
        'connectorType': 'Salesforce',
        'sourceConnectorProperties': {
            'Salesforce': {'object': 'Account'}
        }
    },
    tasks=[
        {
            'sourceFields': ['Name', 'Industry'],
            'taskType': 'Map',
            'connectorOperator': {'Salesforce': 'NO_OP'}
        }
    ],
    triggerConfig={
        'triggerType': 'Scheduled',
        'triggerProperties': {
            'Scheduled': {
                'scheduleExpression': 'rate(1hour)',
                'dataPullMode': 'Incremental'
            }
        }
    }
)
```

---

## 六、数据治理服务

### 6.1 AWS Lake Formation

#### 核心功能
- **数据湖管理**: 集中管理S3数据湖
- **权限控制**: 细粒度访问控制
- **数据目录**: 统一元数据管理
- **数据共享**: 跨账户安全共享

#### 注册数据湖位置
```python
lakeformation = boto3.client('lakeformation')
lakeformation.register_resource(
    ResourceArn='arn:aws:s3:::my-data-lake'
)
```

#### 授予权限
```python
lakeformation.grant_permissions(
    Principal={
        'DataLakePrincipal': {
            'DataLakePrincipalIdentifier': 'arn:aws:iam::123456789:role/AnalystRole'
        }
    },
    Resource={
        'Table': {
            'DatabaseName': 'mydb',
            'TableWildcard': {}
        }
    },
    Permissions=['SELECT', 'DESCRIBE']
)
```

#### 与Glue集成
- Lake Formation管理Glue Data Catalog
- 统一权限模型
- 行/列级安全

---

## 七、机器学习服务

### 7.1 Amazon SageMaker

#### 核心功能
- **Notebook**: Jupyter环境
- **训练**: 分布式训练
- **推理**: 模型部署
- **管道**: ML工作流

#### 训练作业
```python
import sagemaker
from sagemaker.pytorch import PyTorch

estimator = PyTorch(
    entry_point='train.py',
    role='SageMakerRole',
    instance_count=2,
    instance_type='ml.p3.2xlarge',
    framework_version='1.12',
    py_version='py38',
    hyperparameters={
        'epochs': 10,
        'batch-size': 64
    }
)

estimator.fit({'training': 's3://bucket/train/'})
```

#### 部署端点
```python
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.xlarge'
)

result = predictor.predict(data)
```

#### SageMaker Studio
- 集成IDE
- 可视化管道
- 模型注册表
- 实验跟踪

#### 预构建算法
- Linear Learner
- XGBoost
- DeepAR
- Object2Vec
- BlazingText

---

## 八、成本优化

### 8.1 存储优化
- **S3生命周期**: 自动转移存储类别
- **S3 Intelligent-Tiering**: 自动优化
- **Glacier**: 长期归档
- **压缩**: Parquet/ORC减少存储

### 8.2 计算优化
- **竞价实例**: EMR/EC2节省90%
- **Reserved Instances**: 长期承诺折扣
- **Serverless**: Lambda/Athena按需付费
- **自动扩展**: 根据负载调整

### 8.3 数据传输优化
- **分区裁剪**: 减少扫描
- **列式存储**: 只读需要的列
- **缓存**: CloudFront/ElastiCache
- **压缩**: 减少传输量

---

## 九、安全最佳实践

### 9.1 身份与访问
- **IAM角色**: 最小权限原则
- **临时凭证**: STS AssumeRole
- **MFA**: 多因素认证
- **SSO**: 单点登录

### 9.2 数据加密
- **传输中**: TLS/SSL
- **静态**: S3 SSE, RDS加密, EBS加密
- **KMS**: 密钥管理服务

### 9.3 网络安全
- **VPC**: 私有网络隔离
- **安全组**: 实例级防火墙
- **NACL**: 子网级防火墙
- **PrivateLink**: 私有访问AWS服务

### 9.4 监控与审计
- **CloudTrail**: API调用日志
- **CloudWatch**: 指标和告警
- **Config**: 资源合规性
- **GuardDuty**: 威胁检测

---

## 十、架构模式

### 10.1 数据湖架构
```
S3 (原始数据)
  ↓
Glue Crawler (发现Schema)
  ↓
Glue Data Catalog (元数据)
  ↓
Athena / Redshift Spectrum (查询)
  ↓
QuickSight (可视化)
```

### 10.2 实时分析架构
```
Kinesis Data Streams (数据流)
  ↓
Kinesis Data Analytics (流处理)
  ↓
  ├→ S3 (存储)
  ├→ Redshift (分析)
  └→ Kinesis Data Firehose → Elasticsearch (搜索)
```

### 10.3 ETL架构
```
数据源 (RDS/S3/API)
  ↓
Glue Crawler (发现)
  ↓
Glue ETL Job (转换)
  ↓
S3 (数据湖)
  ↓
Redshift (数据仓库)
  ↓
QuickSight (报表)
```

---

## 十一、实战案例

### 案例1: 电商数据分析平台

**需求**:
- 存储订单、用户、商品数据
- 实时销售监控
- 用户行为分析
- 推荐系统

**架构**:
```yaml
存储层:
  - S3: 原始日志，数据湖
  - RDS/Aurora: 订单数据库
  - DynamoDB: 用户会话，购物车
  - Redshift: 分析数据仓库

处理层:
  - Kinesis: 实时事件流
  - Lambda: 实时处理
  - Glue: 批处理ETL
  - EMR: 推荐算法训练

分析层:
  - Athena: 即席查询
  - QuickSight: 仪表板
  - SageMaker: 推荐模型

治理:
  - Lake Formation: 权限管理
  - Glue Data Catalog: 元数据
```

### 案例2: IoT数据处理

**需求**:
- 百万设备数据上报
- 实时监控告警
- 历史数据分析

**架构**:
```
IoT设备
  ↓
IoT Core (MQTT)
  ↓
Kinesis Data Streams
  ↓
  ├→ Lambda (实时告警)
  ├→ Kinesis Analytics (聚合)
  └→ Timestream (时序存储)
  ↓
QuickSight (监控仪表板)
```

---

## 十二、学习路径

### 入门级
1. **AWS Cloud Practitioner**: 基础概念
2. **S3基础**: 存储桶、对象、权限
3. **RDS基础**: 创建、连接、备份
4. **Lambda入门**: 简单函数

### 中级
1. **Solutions Architect Associate**: 架构设计
2. **Glue ETL**: 数据转换作业
3. **Athena查询**: SQL分析
4. **Redshift**: 数据仓库

### 高级
1. **Data Analytics Specialty**: 数据分析认证
2. **Lake Formation**: 数据湖治理
3. **Kinesis**: 流处理
4. **SageMaker**: ML工程

---

## 十三、参考资源

### 官方文档
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/)

### 认证考试
- AWS Certified Cloud Practitioner
- AWS Certified Solutions Architect - Associate
- AWS Certified Data Analytics - Specialty
- AWS Certified Database - Specialty

### 工具
- **AWS CLI**: 命令行工具
- **AWS CDK**: 基础设施即代码
- **CloudFormation**: 资源编排
- **Terraform**: 多云IaC

---

**文档版本**: v1.0  
**最后更新**: 2026-06-10  
**维护者**: Data Engineering Team
