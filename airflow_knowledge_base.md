# Apache Airflow 完整知识体系

> 工作流编排平台 - DAG 调度与任务管理
> 更新时间：2026-06-10

---

## 📚 目录

1. [Airflow 概述](#1-airflow-概述)
2. [核心概念](#2-核心概念)
3. [DAG 编写](#3-dag-编写)
4. [Operators](#4-operators)
5. [Sensors](#5-sensors)
6. [Hooks](#6-hooks)
7. [Connections](#7-connections)
8. [Variables & XCom](#8-variables--xcom)
9. [调度与执行](#9-调度与执行)
10. [任务依赖](#10-任务依赖)
11. [动态 DAG](#11-动态-dag)
12. [错误处理与重试](#12-错误处理与重试)
13. [测试](#13-测试)
14. [部署与架构](#14-部署与架构)
15. [最佳实践](#15-最佳实践)

---

## 1. Airflow 概述

### 什么是 Airflow

Apache Airflow 是一个开源的**工作流编排平台**，用于编写、调度和监控批量应用程序的工作流。

**核心特性：**
- ✅ **代码定义工作流**：Python 代码定义 DAG
- ✅ **丰富的 UI**：可视化管理和监控
- ✅ **可扩展**：自定义 Operators、Hooks、Plugins
- ✅ **调度灵活**：支持 Cron、定时、依赖触发
- ✅ **可观测**：详细的日志和指标
- ✅ **活跃社区**：200+ 官方 provider 包

### Airflow vs 其他工具

| 工具 | 定位 | 优势 |
|------|------|------|
| **Airflow** | 工作流编排 | Python 代码、丰富生态 |
| **Prefect** | 工作流编排 | 现代设计、动态工作流 |
| **Luigi** | 批处理管道 | 简单、Spotify 开发 |
| **Azkaban** | 工作流调度 | LinkedIn 开发 |
| **Step Functions** | AWS 工作流 | AWS 原生、Serverless |

---

## 2. 核心概念

### DAG (Directed Acyclic Graph)

DAG 是有向无环图，定义了任务的执行顺序和依赖关系。

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='my_first_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    
    def print_hello():
        print('Hello from Airflow!')
    
    hello_task = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello,
    )
```

### Task

Task 是 DAG 中的工作单元，由 Operator 定义。

### Operator

Operator 定义了单个任务的执行逻辑：
- **BashOperator**：执行 shell 命令
- **PythonOperator**：执行 Python 函数
- **EmailOperator**：发送邮件
- **HttpOperator**：发送 HTTP 请求
- **MySqlOperator**：执行 SQL

### Task Instance

Task Instance 是 Task 的特定运行实例，包含状态和元数据。

### Executor

Executor 决定了任务的执行方式：
- **SequentialExecutor**：单进程顺序执行（开发用）
- **LocalExecutor**：多进程本地执行
- **CeleryExecutor**：分布式执行（生产推荐）
- **KubernetesExecutor**：K8s Pod 执行

---

## 3. DAG 编写

### 基础 DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'data_team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

with DAG(
    dag_id='etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline',
    schedule_interval='0 2 * * *',  # 每天凌晨 2 点
    catchup=False,
    tags=['etl', 'daily'],
) as dag:
    
    extract = BashOperator(
        task_id='extract_data',
        bash_command='python /opt/airflow/scripts/extract.py',
    )
    
    transform = BashOperator(
        task_id='transform_data',
        bash_command='python /opt/airflow/scripts/transform.py',
    )
    
    load = BashOperator(
        task_id='load_data',
        bash_command='python /opt/airflow/scripts/load.py',
    )
    
    extract >> transform >> load
```

### DAG 参数

```python
with DAG(
    dag_id='my_dag',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
        'retry_exponential_backoff': True,
        'max_retry_delay': timedelta(hours=1),
        'execution_timeout': timedelta(hours=2),
    },
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    catchup=False,
    max_active_runs=1,
    max_active_tasks=4,
    dagrun_timeout=timedelta(hours=3),
    description='My DAG description',
    tags=['production', 'daily'],
    params={
        'env': 'production',
        'batch_size': 1000,
    },
) as dag:
    pass
```

### 调度间隔

```python
# Cron 表达式
schedule_interval='0 2 * * *'      # 每天凌晨 2 点
schedule_interval='*/15 * * * *'   # 每 15 分钟
schedule_interval='0 0 * * 0'      # 每周日
schedule_interval='0 0 1 * *'      # 每月 1 号

# 预设值
schedule_interval='@once'          # 只运行一次
schedule_interval='@hourly'        # 每小时
schedule_interval='@daily'         # 每天
schedule_interval='@weekly'        # 每周
schedule_interval='@monthly'       # 每月
schedule_interval='@yearly'        # 每年

# None - 手动触发
schedule_interval=None

# timedelta
schedule_interval=timedelta(hours=6)
```

---

## 4. Operators

### BashOperator

```python
from airflow.operators.bash import BashOperator

bash_task = BashOperator(
    task_id='run_script',
    bash_command='echo "Hello {{ ds }}" && python /opt/airflow/scripts/process.py',
    env={'MY_VAR': 'value'},
    cwd='/opt/airflow/scripts',
)
```

### PythonOperator

```python
from airflow.operators.python import PythonOperator

def my_function(arg1, arg2, **kwargs):
    print(f"Arguments: {arg1}, {arg2}")
    
    # 获取上下文
    execution_date = kwargs['execution_date']
    dag_run = kwargs['dag_run']
    
    return {'result': 'success'}

python_task = PythonOperator(
    task_id='process_data',
    python_callable=my_function,
    op_args=['value1', 'value2'],
    op_kwargs={'key': 'value'},
    provide_context=True,
)
```

### BranchPythonOperator

```python
from airflow.operators.python import BranchPythonOperator

def branch_func(**kwargs):
    execution_date = kwargs['execution_date']
    
    if execution_date.day == 1:
        return 'monthly_task'
    else:
        return 'daily_task'

branch = BranchPythonOperator(
    task_id='branch_decision',
    python_callable=branch_func,
)

daily_task = BashOperator(
    task_id='daily_task',
    bash_command='echo "Daily task"',
)

monthly_task = BashOperator(
    task_id='monthly_task',
    bash_command='echo "Monthly task"',
)

branch >> [daily_task, monthly_task]
```

### ShortCircuitOperator

```python
from airflow.operators.python import ShortCircuitOperator

def check_condition(**kwargs):
    # 返回 False 会跳过下游任务
    return kwargs['execution_date'].day != 1

short_circuit = ShortCircuitOperator(
    task_id='check_condition',
    python_callable=check_condition,
)

downstream_task = BashOperator(
    task_id='downstream',
    bash_command='echo "This may be skipped"',
)

short_circuit >> downstream_task
```

### EmailOperator

```python
from airflow.operators.email import EmailOperator

email_task = EmailOperator(
    task_id='send_email',
    to='user@example.com',
    subject='Airflow Alert: {{ dag.dag_id }}',
    html_content="""
        <h3>DAG Run Report</h3>
        <p>DAG: {{ dag.dag_id }}</p>
        <p>Execution Date: {{ execution_date }}</p>
        <p>Status: {{ task_instance.state }}</p>
    """,
)
```

### HttpOperator

```python
from airflow.providers.http.operators.http import SimpleHttpOperator

http_task = SimpleHttpOperator(
    task_id='call_api',
    http_conn_id='my_api',
    endpoint='/api/v1/data',
    method='GET',
    data={'param': '{{ ds }}'},
    headers={'Content-Type': 'application/json'},
    response_filter=lambda response: response.json(),
)
```

### TriggerDagRunOperator

```python
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

trigger = TriggerDagRunOperator(
    task_id='trigger_downstream_dag',
    trigger_dag_id='downstream_dag',
    conf={'message': 'Triggered from upstream'},
    wait_for_completion=True,
    poke_interval=60,
)
```

---

## 5. Sensors

### BaseSensorOperator

```python
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class MySensor(BaseSensorOperator):
    
    @apply_defaults
    def __init__(self, my_param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_param = my_param
    
    def poke(self, context):
        # 返回 True 表示条件满足，任务继续
        # 返回 False 会继续等待
        self.log.info(f"Checking condition with param: {self.my_param}")
        return self.check_condition()
    
    def check_condition(self):
        # 实现你的检查逻辑
        return True
```

### FileSensor

```python
from airflow.sensors.filesystem import FileSensor

file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/input/{{ ds }}/data.csv',
    fs_conn_id='fs_default',
    poke_interval=60,
    timeout=3600,
    mode='poke',  # 'poke' 或 'reschedule'
)
```

### S3KeySensor

```python
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

s3_sensor = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_name='my-bucket',
    bucket_key='data/{{ ds }}/file.parquet',
    aws_conn_id='aws_default',
    poke_interval=300,
    timeout=7200,
)
```

### ExternalTaskSensor

```python
from airflow.sensors.external_task import ExternalTaskSensor

external_sensor = ExternalTaskSensor(
    task_id='wait_for_upstream',
    external_dag_id='upstream_dag',
    external_task_id='final_task',
    execution_delta=timedelta(hours=1),
    timeout=7200,
    poke_interval=300,
    mode='poke',
)
```

### SqlSensor

```python
from airflow.sensors.sql import SqlSensor

sql_sensor = SqlSensor(
    task_id='wait_for_data',
    conn_id='postgres_default',
    sql="""
        SELECT COUNT(*) > 0
        FROM raw_events
        WHERE date = '{{ ds }}'
    """,
    poke_interval=300,
    timeout=3600,
)
```

---

## 6. Hooks

### BaseHook

```python
from airflow.hooks.base import BaseHook

class MyHook(BaseHook):
    
    def __init__(self, my_conn_id='my_default'):
        super().__init__()
        self.conn_id = my_conn_id
        self.conn = None
    
    def get_conn(self):
        if self.conn is None:
            conn = self.get_connection(self.conn_id)
            # 使用连接信息建立连接
            self.conn = self.create_connection(conn)
        return self.conn
    
    def create_connection(self, conn):
        # 实现连接创建逻辑
        pass
```

### PostgresHook

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

def process_data(**kwargs):
    hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # 执行查询
    records = hook.get_records(
        "SELECT * FROM users WHERE created_at >= %s",
        parameters=[kwargs['ds']]
    )
    
    # 获取 Pandas DataFrame
    df = hook.get_pandas_df("SELECT * FROM events LIMIT 1000")
    
    # 插入数据
    hook.insert_rows(
        table='processed_events',
        rows=[(1, 'event1'), (2, 'event2')],
        target_fields=['id', 'name']
    )
    
    # 执行 SQL
    hook.run("UPDATE users SET processed = TRUE WHERE id IN %s", parameters=[(1, 2, 3)])
```

### S3Hook

```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def process_s3(**kwargs):
    hook = S3Hook(aws_conn_id='aws_default')
    
    # 检查文件是否存在
    exists = hook.check_for_key('data/file.parquet', 'my-bucket')
    
    # 下载文件
    local_path = hook.download_file(
        key='data/file.parquet',
        bucket_name='my-bucket',
        local_path='/tmp/file.parquet'
    )
    
    # 上传文件
    hook.load_file(
        filename='/tmp/result.parquet',
        key='output/result.parquet',
        bucket_name='my-bucket',
        replace=True
    )
    
    # 列出文件
    keys = hook.list_keys(
        bucket_name='my-bucket',
        prefix='data/{{ ds }}/'
    )
```

### HttpHook

```python
from airflow.providers.http.hooks.http import HttpHook

def fetch_api_data(**kwargs):
    hook = HttpHook(method='GET', http_conn_id='my_api')
    
    response = hook.run(
        endpoint='/api/v1/users',
        data={'date': kwargs['ds']},
        headers={'Authorization': 'Bearer {{ token }}'},
        extra_options={'timeout': 60}
    )
    
    return response.json()
```

---

## 7. Connections

### 创建 Connection

```python
# 通过 UI
# Admin -> Connections -> Create

# 通过 CLI
airflow connections add 'my_postgres' \
    --conn-type 'postgres' \
    --conn-login 'user' \
    --conn-password '***' \
    --conn-host 'localhost' \
    --conn-port '5432' \
    --conn-schema 'mydb'

# 通过环境变量
export AIRFLOW_CONN_MY_POSTGRES='postgresql://user:***@localhost:5432/mydb'

# 通过 JSON
export AIRFLOW_CONN_MY_POSTGRES='postgres://user:password@host:5432/db?sslmode=require'
```

### 使用 Connection

```python
from airflow.hooks.base import BaseHook

# 获取连接信息
conn = BaseHook.get_connection('my_postgres')
print(f"Host: {conn.host}")
print(f"Port: {conn.port}")
print(f"Login: {conn.login}")
print(f"Schema: {conn.schema}")
print(f"Extra: {conn.extra_dejson}")

# 在 Operator 中使用
postgres_task = PostgresOperator(
    task_id='query_postgres',
    postgres_conn_id='my_postgres',
    sql='SELECT * FROM users LIMIT 10',
)
```

### 常用 Connection 类型

| Type | 说明 | 示例 |
|------|------|------|
| postgres | PostgreSQL | `postgres://user:pass@host:5432/db` |
| mysql | MySQL | `mysql://user:pass@host:3306/db` |
| snowflake | Snowflake | `snowflake://user:pass@account/db` |
| aws | AWS | `aws://AKIA.../secret?region=us-east-1` |
| http | HTTP | `http://api.example.com` |
| s3 | S3 | `s3://bucket/prefix` |
| ssh | SSH | `ssh://user@host:22` |
| ftp | FTP | `ftp://user:pass@host:21` |

---

## 8. Variables & XCom

### Variables

```python
from airflow.models import Variable

# 获取变量
env = Variable.get('environment')
api_key = Variable.get('api_key', deserialize_json=True)

# 带默认值
timeout = Variable.get('timeout', default_var=300)

# 设置变量
Variable.set('last_run_date', '2024-01-15')
Variable.set('config', {'key': 'value'}, serialize_json=True)

# 删除变量
Variable.delete('old_config')

# 在模板中使用
bash_task = BashOperator(
    task_id='use_variable',
    bash_command='echo "Environment: {{ var.value.environment }}"',
)
```

### XCom

```python
from airflow.operators.python import PythonOperator

# 推送 XCom
def push_data(**kwargs):
    ti = kwargs['ti']
    ti.xcom_push(key='my_key', value={'data': 'value', 'count': 100})
    return {'result': 'success'}  # 自动推送为 'return_value'

push_task = PythonOperator(
    task_id='push_task',
    python_callable=push_data,
)

# 拉取 XCom
def pull_data(**kwargs):
    ti = kwargs['ti']
    value = ti.xcom_pull(task_ids='push_task', key='my_key')
    print(f"Received: {value}")

pull_task = PythonOperator(
    task_id='pull_task',
    python_callable=pull_data,
)

# 模板中使用 XCom
bash_task = BashOperator(
    task_id='use_xcom',
    bash_command='echo "Value: {{ ti.xcom_pull(task_ids="push_task", key="my_key") }}"',
)

push_task >> pull_task
push_task >> bash_task
```

---

## 9. 调度与执行

### DAG Run 状态

| 状态 | 说明 |
|------|------|
| running | 正在执行 |
| success | 成功完成 |
| failed | 执行失败 |
| queued | 等待执行 |
| scheduled | 已调度 |
| deferred | 延迟执行 |

### Task Instance 状态

| 状态 | 说明 |
|------|------|
| success | 任务成功 |
| failed | 任务失败 |
| running | 正在执行 |
| queued | 等待执行 |
| upstream_failed | 上游任务失败 |
| skipped | 被跳过 |
| deferred | 延迟执行 |
| removed | 被移除 |

### 执行上下文

```python
def my_task(**kwargs):
    # 可用的上下文变量
    dag = kwargs['dag']
    dag_run = kwargs['dag_run']
    task = kwargs['task']
    task_instance = kwargs['ti']
    execution_date = kwargs['execution_date']
    logical_date = kwargs['logical_date']
    data_interval_start = kwargs['data_interval_start']
    data_interval_end = kwargs['data_interval_end']
    params = kwargs['params']
    next_ds = kwargs['next_ds']
    prev_ds = kwargs['prev_ds']
    ds = kwargs['ds']  # execution_date 的日期部分
    ts = kwargs['ts']  # execution_date 的 ISO 格式
```

### 模板变量

```python
bash_task = BashOperator(
    task_id='template_example',
    bash_command="""
        echo "Execution date: {{ ds }}"
        echo "Next execution: {{ next_ds }}"
        echo "Previous execution: {{ prev_ds }}"
        echo "Timestamp: {{ ts }}"
        echo "DAG ID: {{ dag.dag_id }}"
        echo "Task ID: {{ task.task_id }}"
        echo "Run ID: {{ run_id }}"
        echo "Data interval start: {{ data_interval_start }}"
    """
)
```

---

## 10. 任务依赖

### 基础依赖

```python
# 线性依赖
task1 >> task2 >> task3

# 多对多
[task1, task2] >> task3
task1 >> [task3, task4]
[task1, task2] >> [task3, task4]

# 复杂依赖
task1 >> task2
task1 >> task3 >> task4
task2 >> task5
task4 >> task5
```

### 依赖设置方法

```python
# set_upstream / set_downstream
task2.set_upstream(task1)  # task1 >> task2
task1.set_downstream(task2)  # task1 >> task2

# set_dependency
task2.set_dependency(task1)  # task1 >> task2

# chain
from airflow.models.baseoperator import chain

chain(task1, task2, task3, task4)  # task1 >> task2 >> task3 >> task4

# cross_downstream
from airflow.models.baseoperator import cross_downstream

cross_downstream([task1, task2], [task3, task4])
# task1 >> task3, task1 >> task4
# task2 >> task3, task2 >> task4
```

---

## 11. 动态 DAG

### 动态生成 Task

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def process_table(table_name):
    print(f"Processing {table_name}")

with DAG(
    dag_id='dynamic_tables',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
) as dag:
    
    tables = ['users', 'orders', 'products', 'events']
    
    tasks = []
    for table in tables:
        task = PythonOperator(
            task_id=f'process_{table}',
            python_callable=process_table,
            op_args=[table],
        )
        tasks.append(task)
    
    # 并行执行
    # 或者设置依赖
    # tasks[0] >> tasks[1] >> tasks[2] >> tasks[3]
```

### 动态 DAG 生成

```python
# dags/dynamic_dag_generator.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import importlib.util

def load_dag_configs():
    config_dir = '/opt/airflow/dag_configs'
    configs = []
    
    for file in os.listdir(config_dir):
        if file.endswith('.yaml'):
            # 加载 YAML 配置
            import yaml
            with open(os.path.join(config_dir, file)) as f:
                config = yaml.safe_load(f)
                configs.append(config)
    
    return configs

def create_dag(dag_id, schedule, tables):
    def process_table(table):
        print(f"Processing {table}")
    
    with DAG(
        dag_id=dag_id,
        schedule_interval=schedule,
        start_date=datetime(2024, 1, 1),
        catchup=False,
    ) as dag:
        
        tasks = []
        for table in tables:
            task = PythonOperator(
                task_id=f'process_{table}',
                python_callable=process_table,
                op_args=[table],
            )
            tasks.append(task)
    
    return dag

# 动态创建 DAG
configs = load_dag_configs()
for config in configs:
    dag_id = config['dag_id']
    schedule = config['schedule']
    tables = config['tables']
    
    globals()[dag_id] = create_dag(dag_id, schedule, tables)
```

---

## 12. 错误处理与重试

### 重试配置

```python
from datetime import timedelta

default_args = {
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(hours=1),
}

with DAG(
    dag_id='retry_example',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
) as dag:
    
    task = PythonOperator(
        task_id='flaky_task',
        python_callable=unreliable_function,
        retries=5,
        retry_delay=timedelta(minutes=10),
    )
```

### 错误回调

```python
from airflow.utils.email import send_email

def failure_callback(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['execution_date']
    exception = context['exception']
    
    send_email(
        to='admin@example.com',
        subject=f'Airflow Failure: {dag_id}.{task_id}',
        html_content=f"""
            <h3>Task Failed</h3>
            <p>DAG: {dag_id}</p>
            <p>Task: {task_id}</p>
            <p>Execution Date: {execution_date}</p>
            <p>Exception: {exception}</p>
        """
    )

def success_callback(context):
    print(f"Task {context['task_instance'].task_id} succeeded")

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(f"SLA missed for DAG: {dag.dag_id}")

with DAG(
    dag_id='callback_example',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    on_failure_callback=failure_callback,
    on_success_callback=success_callback,
    sla_miss_callback=sla_miss_callback,
) as dag:
    
    task = PythonOperator(
        task_id='my_task',
        python_callable=my_function,
        on_failure_callback=failure_callback,
        on_success_callback=success_callback,
    )
```

### SLA

```python
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.bash import BashOperator

default_args = {
    'sla': timedelta(hours=2),  # 任务 SLA
}

with DAG(
    dag_id='sla_example',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    sla_miss_callback=sla_callback,
) as dag:
    
    task = BashOperator(
        task_id='long_running',
        bash_command='sleep 7200',
        sla=timedelta(hours=1),  # 覆盖默认 SLA
    )
```

---

## 13. 测试

### DAG 测试

```python
# tests/test_dags.py
import pytest
from airflow.models import DagBag

def test_dag_loading():
    """测试所有 DAG 能否正确加载"""
    dag_bag = DagBag(include_examples=False)
    
    assert len(dag_bag.import_errors) == 0, f"DAG 加载错误: {dag_bag.import_errors}"
    
    for dag_id, dag in dag_bag.dags.items():
        assert dag is not None, f"DAG {dag_id} 为 None"

def test_dag_has_tasks():
    """测试 DAG 包含任务"""
    dag_bag = DagBag(include_examples=False)
    
    for dag_id, dag in dag_bag.dags.items():
        assert len(dag.tasks) > 0, f"DAG {dag_id} 没有任务"

def test_dag_dependencies():
    """测试 DAG 依赖关系无环"""
    dag_bag = DagBag(include_examples=False)
    
    for dag_id, dag in dag_bag.dags.items():
        # 检查是否有循环依赖
        assert not dag.has_cycle(), f"DAG {dag_id} 存在循环依赖"
```

### Task 测试

```python
# tests/test_tasks.py
import pytest
from airflow.models import DagBag, TaskInstance
from airflow.utils.db import create_session
from airflow.utils.state import State

@pytest.fixture
def dag():
    dag_bag = DagBag(include_examples=False)
    return dag_bag.get_dag('my_dag')

def test_task_success(dag):
    """测试任务成功执行"""
    task = dag.get_task('my_task')
    
    ti = TaskInstance(task=task, execution_date=None)
    
    with create_session() as session:
        ti.run(ignore_ti_state=True, session=session)
        
    assert ti.state == State.SUCCESS

def test_task_output(dag):
    """测试任务输出"""
    task = dag.get_task('process_data')
    
    ti = TaskInstance(task=task, execution_date=None)
    
    with create_session() as session:
        ti.run(ignore_ti_state=True, session=session)
        
    result = ti.xcom_pull(task_ids='process_data', key='result')
    assert result == 'expected_value'
```

### 单元测试

```python
# tests/test_functions.py
from my_module import process_data

def test_process_data():
    input_data = [1, 2, 3, 4, 5]
    expected = [2, 4, 6, 8, 10]
    
    result = process_data(input_data)
    assert result == expected

def test_process_data_empty():
    result = process_data([])
    assert result == []
```

---

## 14. 部署与架构

### 架构组件

```
┌─────────────┐
│  Scheduler  │  调度任务
└──────┬──────┘
       │
       ├──────────────┐
       │              │
┌──────▼──────┐  ┌────▼─────┐
│  Executor   │  │ Metadata │
│ (Celery/K8s)│  │   DB     │
└──────┬──────┘  └────┬─────┘
       │              │
       ├──────────────┤
       │              │
┌──────▼──────┐  ┌────▼─────┐
│   Workers   │  │  Web UI  │
└─────────────┘  └──────────┘
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

x-airflow-common: &airflow-common
  image: apache/airflow:2.8.0
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:***@postgres/airflow
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:***@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth'
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    - ./config:/opt/airflow/config
  user: "${AIRFLOW_UID:-50000}:0"
  depends_on:
    &airflow-common-depends-on
    redis:
      condition: service_healthy
    postgres:
      condition: service_healthy

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: ***
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5
    restart: always

  redis:
    image: redis:latest
    expose:
      - 6379
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 30s
      retries: 50
    restart: always

  airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - 8080:8080
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler
    healthcheck:
      test: ["CMD-SHELL", 'airflow jobs check --job-type SchedulerJob --hostname "$${HOSTNAME}"']
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-worker:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.providers.celery.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 10s
      timeout: 10s
      retries: 5
    environment:
      <<: *airflow-common-env
      DUMB_INIT_SETSID: "0"
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-triggerer:
    <<: *airflow-common
    command: triggerer
    healthcheck:
      test: ["CMD-SHELL", 'airflow jobs check --job-type TriggererJob --hostname "$${HOSTNAME}"']
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-init:
    <<: *airflow-common
    entrypoint: /bin/bash
    command:
      - -c
      - |
        mkdir -p /sources/logs /sources/dags /sources/plugins
        chown -R "${AIRFLOW_UID}:0" /sources/{logs,dags,plugins}
        exec /entrypoint airflow version
    environment:
      <<: *airflow-common-env
      _AIRFLOW_DB_UPGRADE: 'true'
      _AIRFLOW_WWW_USER_CREATE: 'true'
      _AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow}
      _AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow}
    user: "0:0"
    volumes:
      - .:/sources

volumes:
  postgres-db-volume:
```

### Kubernetes 部署

```yaml
# values.yaml for Helm chart
executor: KubernetesExecutor

images:
  airflow:
    repository: apache/airflow
    tag: 2.8.0

webserver:
  replicas: 2
  resources:
    limits:
      cpu: 1000m
      memory: 2Gi
    requests:
      cpu: 500m
      memory: 1Gi

scheduler:
  replicas: 2
  resources:
    limits:
      cpu: 2000m
      memory: 4Gi
    requests:
      cpu: 1000m
      memory: 2Gi

workers:
  resources:
    limits:
      cpu: 2000m
      memory: 4Gi
    requests:
      cpu: 1000m
      memory: 2Gi

data:
  metadataConnection:
    user: postgres
    pass: ***
    protocol: postgresql
    host: postgres-release
    port: 5432
    db: airflow
```

---

## 15. 最佳实践

### DAG 编写

```python
# ✅ 好的实践
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def process_data():
    # 幂等操作
    # 无副作用
    # 可重试
    pass

with DAG(
    dag_id='best_practice_dag',
    default_args={
        'owner': 'data_team',
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
    },
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['production', 'daily'],
) as dag:
    
    task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
    )
```

### 幂等性

```python
# ✅ 幂等任务
def load_data(**kwargs):
    ds = kwargs['ds']
    
    # 先删除再插入
    hook = PostgresHook()
    hook.run(f"DELETE FROM target_table WHERE date = '{ds}'")
    hook.insert_rows('target_table', rows, target_fields)

# ❌ 非幂等任务
def bad_load_data(**kwargs):
    # 每次运行都会追加数据
    hook = PostgresHook()
    hook.insert_rows('target_table', rows, target_fields)
```

### 任务粒度

```python
# ✅ 合适的粒度
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load,
)

# ❌ 粒度太粗
big_task = PythonOperator(
    task_id='do_everything',
    python_callable=lambda: extract() or transform() or load(),
)

# ❌ 粒度太细
for i in range(1000):
    PythonOperator(
        task_id=f'task_{i}',
        python_callable=process_single_row,
        op_args=[i],
    )
```

### 资源管理

```python
# ✅ 使用连接池
from airflow.providers.postgres.hooks.postgres import PostgresHook

def process_with_pool():
    hook = PostgresHook(postgres_conn_id='my_postgres')
    # Hook 内部管理连接池
    conn = hook.get_conn()
    # 使用连接...
```

### 监控与告警

```python
# 配置告警
default_args = {
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

# SLA 监控
with DAG(
    dag_id='monitored_dag',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    sla_miss_callback=send_sla_alert,
) as dag:
    
    task = PythonOperator(
        task_id='important_task',
        python_callable=process_data,
        sla=timedelta(hours=2),
    )
```

---

## 附录：常用命令

```bash
# 启动 Web UI
airflow webserver --port 8080

# 启动 Scheduler
airflow scheduler

# 启动 Worker (Celery)
airflow celery worker

# 初始化数据库
airflow db init

# 创建用户
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# 列出 DAG
airflow dags list

# 触发 DAG
airflow dags trigger my_dag

# 列出任务
airflow tasks list my_dag

# 测试任务
airflow tasks test my_dag my_task 2024-01-01

# 运行任务
airflow tasks run my_dag my_task 2024-01-01

# 查看日志
airflow tasks logs my_dag my_task 2024-01-01

# 暂停/恢复 DAG
airflow dags pause my_dag
airflow dags unpause my_dag

# 删除 DAG
airflow dags delete my_dag

# 列出连接
airflow connections list

# 添加连接
airflow connections add 'my_conn' \
    --conn-type 'postgres' \
    --conn-login 'user' \
    --conn-password 'password' \
    --conn-host 'localhost' \
    --conn-port '5432'

# 列出变量
airflow variables list

# 设置变量
airflow variables set 'my_key' 'my_value'

# 导入变量
airflow variables import variables.json

# 导出变量
airflow variables export variables.json

# 检查配置
airflow config list

# 版本信息
airflow version
```

---

> 📝 本文档基于 Apache Airflow 最新官方文档整理
> 官方文档：https://airflow.apache.org/docs/
> 更新时间：2026-06-10
