# vanna-ai/vanna 代码分析报告

> 分析日期：2026-06-12
> 仓库：https://github.com/vanna-ai/vanna
> 分析范围：src/vanna/ 核心代码（v2 架构）

---

## 一、项目概述

Vanna 是一个开源的 **Text-to-SQL AI Agent 框架**，允许用户通过自然语言提问，自动生成并执行 SQL 查询、返回可视化结果。项目经历了从 v1（单一基类 + 向量数据库插件）到 **v2（插件化 Agent 框架）** 的重大重构，当前代码库中同时保留了 legacy（v1）和 core（v2）两套实现，通过 `legacy/adapter.py` 提供兼容适配。

**核心定位：** 不是简单的 LLM wrapper，而是一个可扩展的、面向数据场景的 Agent 框架，具备完整的工具调用、权限控制、审计日志、可观测性等企业级能力。

---

## 二、整体架构

### 2.1 分层架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Servers 层（服务接入）                        │
│   Flask / FastAPI / CLI / Streamlit / Web Component            │
├─────────────────────────────────────────────────────────────────┤
│                     Agent 层（核心编排）                          │
│   Agent + AgentConfig + SystemPromptBuilder                    │
│   7 个扩展点：lifecycle_hooks / middlewares / recovery /       │
│   enrichers / enhancer / filters / observability              │
├─────────────────────────────────────────────────────────────────┤
│                     Core 层（抽象接口）                          │
│   Tool / LlmService / ConversationStore / UserService          │
│   WorkflowHandler / LifecycleHook / LlmMiddleware              │
│   ConversationFilter / ObservabilityProvider / AuditLogger     │
│   ErrorRecoveryStrategy / ToolContextEnricher                  │
│   LlmContextEnhancer / UserResolver                            │
├─────────────────────────────────────────────────────────────────┤
│                   Capabilities 层（能力基类）                     │
│   AgentMemory / FileSystem / SqlRunner                         │
├─────────────────────────────────────────────────────────────────┤
│                   Integrations 层（具体实现）                     │
│   LLM: OpenAI / Anthropic / Ollama / Gemini / AzureOpenAI     │
│   DB:  Snowflake / Postgres / MySQL / BigQuery / ClickHouse... │
│   Vector: ChromaDB / FAISS / Pinecone / Milvus / Qdrant...    │
│   Misc: Local / Plotly                                         │
├─────────────────────────────────────────────────────────────────┤
│                     Tools 层（内置工具）                         │
│   run_sql / agent_memory / file_system / python / visualize    │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 核心设计原则

| 原则 | 实现方式 |
|------|----------|
| **插件化** | 所有外部依赖通过抽象接口注入，实现可替换 |
| **关注点分离** | 认证、工具执行、LLM 调用、存储各司其职 |
| **流式响应** | `send_message` 返回 `AsyncGenerator[UiComponent]`，支持实时 UI 更新 |
| **企业级就绪** | 内置审计、可观测性、错误恢复、配额控制 |
| **向后兼容** | legacy adapter 包装 v1 API，渐进式迁移 |

---

## 三、核心模块详解

### 3.1 Agent（核心编排器）

**文件：** `core/agent/agent.py`（1407 行，整个项目最大的文件）

Agent 是整个框架的中枢，负责协调 LLM 调用、工具执行、对话管理。其 `__init__` 接受 **7 个扩展点**：

```python
class Agent:
    def __init__(
        self,
        llm_service: LlmService,              # LLM 服务
        tool_registry: ToolRegistry,           # 工具注册表
        user_resolver: UserResolver,           # 用户解析器
        agent_memory: AgentMemory,             # Agent 记忆
        conversation_store: ConversationStore, # 对话存储
        config: AgentConfig,                   # 配置
        system_prompt_builder: SystemPromptBuilder,
        lifecycle_hooks: List[LifecycleHook],     # 扩展点1: 生命周期钩子
        llm_middlewares: List[LlmMiddleware],     # 扩展点2: LLM 中间件
        workflow_handler: WorkflowHandler,        # 扩展点3: 工作流处理
        error_recovery_strategy: ErrorRecoveryStrategy,  # 扩展点4: 错误恢复
        context_enrichers: List[ToolContextEnricher],      # 扩展点5: 上下文丰富
        llm_context_enhancer: LlmContextEnhancer,          # 扩展点6: LLM上下文增强
        conversation_filters: List[ConversationFilter],    # 扩展点7: 对话过滤
        observability_provider: ObservabilityProvider,
        audit_logger: AuditLogger,
    )
```

**核心方法 `send_message` 的执行流程：**

```
用户消息 → RequestContext 解析
    │
    ├─ 1. UserResolver.resolve_user(request_context) → User
    ├─ 2. Conversation 创建/加载
    ├─ 3. LifecycleHook.on_message_start()
    ├─ 4. ConversationFilter 过滤历史消息
    ├─ 5. LlmContextEnhancer 增强系统提示词
    ├─ 6. 构建 LlmRequest（system prompt + tools + history）
    ├─ 7. LlmMiddleware 链式拦截（请求前/响应后）
    ├─ 8. LlmService.chat() / .stream()
    │
    ├─ 如果 LLM 返回 tool_calls:
    │   ├─ ToolRegistry.get_tool() + 权限检查
    │   ├─ ToolContextEnricher 丰富上下文
    │   ├─ LifecycleHook.on_tool_start()
    │   ├─ Tool.execute(context, args)
    │   ├─ LifecycleHook.on_tool_end()
    │   ├─ 审计日志记录
    │   └─ 结果回传 LLM → 循环（直到无 tool_calls）
    │
    ├─ 如果 LLM 返回文本:
    │   ├─ WorkflowHandler 处理结果
    │   ├─ 存储到 ConversationStore
    │   └─ yield UiComponent
    │
    └─ 错误时:
        ├─ ErrorRecoveryStrategy 决定恢复动作
        └─ ObservabilityProvider 记录错误
```

### 3.2 ToolRegistry（工具注册与权限门控）

**文件：** `core/registry.py`（278 行）

ToolRegistry 是工具管理的核心，负责注册、查找、权限验证：

```python
class ToolRegistry:
    def register_tool(self, tool: Tool) -> None
    def get_tool(self, name: str) -> Tool
    def get_schemas(self) -> List[ToolSchema]
    def check_tool_access(self, user: User, tool_name: str) -> bool  # 权限检查
```

**关键设计：** 每个 `ToolSchema` 包含 `access_groups: List[str]`，ToolRegistry 通过比对用户 `group_memberships` 和工具的 `access_groups` 实现访问控制。

### 3.3 Workflow（工作流引擎）

**文件：** `core/workflow/default.py`（789 行）、`core/workflow/base.py`（254 行）

WorkflowHandler 是 Agent 输出结果的后处理管道。`DefaultWorkflowHandler` 内置了对不同类型结果的处理：

- SQL 查询结果 → DataFrame 展示
- 图表生成 → Plotly 渲染
- 错误信息 → 用户友好提示
- 训练数据 → 存入 Agent Memory

### 3.4 AgentMemory（智能记忆系统）

**文件：** `capabilities/agent_memory/base.py`

AgentMemory 是 Vanna 的核心差异化能力，管理三类知识：

| 类型 | 说明 | 用途 |
|------|------|------|
| `ddl` | 表结构定义 | Schema 上下文 |
| `documentation` | 业务文档 | 语义理解 |
| `sql` | SQL 示例 | Few-shot 学习 |
| `question_sql` | 问答对 | 上下文检索 |

底层依赖向量数据库（ChromaDB/FAISS/Pinecone/Milvus/Qdrant/Weaviate 等）做语义检索。

---

## 四、权限控制模块设计（重点）

### 4.1 权限架构全景

Vanna 的权限控制是**多层级、多维度**的设计，覆盖从请求认证到工具执行的完整链路：

```
┌─────────────────────────────────────────────────────────┐
│               Layer 1: 请求认证                          │
│   RequestContext → UserResolver → User                  │
│   (从 HTTP cookie/header 解析身份)                       │
├─────────────────────────────────────────────────────────┤
│               Layer 2: 用户属性                          │
│   User.id / User.username / User.email                  │
│   User.group_memberships: List[str]                     │
│   User.metadata: Dict[str, Any]                         │
├─────────────────────────────────────────────────────────┤
│               Layer 3: 工具级访问控制                     │
│   Tool.access_groups: List[str]                         │
│   ToolRegistry.check_tool_access(user, tool_name)       │
│   匹配: user.group_memberships ∩ tool.access_groups     │
├─────────────────────────────────────────────────────────┤
│               Layer 4: UI 特性级访问控制                  │
│   AgentConfig.UiFeature 枚举                            │
│   ui_feature_access: Dict[UiFeature, List[str]]         │
│   控制用户能否使用特定 UI 功能                             │
├─────────────────────────────────────────────────────────┤
│               Layer 5: 配额与限制                        │
│   LifecycleHook (如 QuotaCheckHook)                     │
│   控制调用频率、token 消耗等                              │
├─────────────────────────────────────────────────────────┤
│               Layer 6: 审计追踪                          │
│   AuditLogger: 记录所有工具访问检查/调用/结果             │
│   事件类型:                                              │
│   - ToolAccessCheckEvent  (权限检查)                     │
│   - ToolInvocationEvent   (工具调用)                     │
│   - ToolResultEvent       (执行结果)                     │
│   - UiFeatureAccessCheckEvent (UI权限检查)               │
│   - AiResponseEvent       (AI响应)                      │
└─────────────────────────────────────────────────────────┘
```

### 4.2 认证层详解

#### RequestContext（请求上下文）

```python
class RequestContext(BaseModel):
    cookies: Dict[str, str]       # HTTP cookies
    headers: Dict[str, str]       # HTTP headers
    remote_addr: Optional[str]    # 客户端 IP
    query_params: Dict[str, str]  # URL 参数
    metadata: Dict[str, Any]      # 扩展元数据

    def get_cookie(self, name: str) -> Optional[str]
    def get_header(self, name: str) -> Optional[str]  # 大小写不敏感
```

#### UserResolver（用户解析器接口）

```python
class UserResolver(ABC):
    @abstractmethod
    async def resolve_user(self, request_context: RequestContext) -> User:
        """从请求上下文解析用户身份"""
        pass
```

**设计亮点：** 抽象为接口，允许自定义实现。官方示例中包含：
- `MockUserResolver` — 测试用
- `EmailCookieResolver` — 从 cookie 读取邮箱
- `JwtUserResolver` — JWT token 验证

#### User（用户模型）

```python
class User(BaseModel):
    id: str                                  # 唯一标识
    username: Optional[str]                  # 用户名
    email: Optional[str]                     # 邮箱
    group_memberships: List[str]             # 所属组（权限核心）
    metadata: Dict[str, Any]                 # 扩展属性
```

**`group_memberships`** 是权限控制的关键字段，后续所有访问控制都基于此做匹配。

### 4.3 工具级访问控制详解

#### Tool 基类的权限定义

```python
class Tool(ABC, Generic[T]):
    @property
    def access_groups(self) -> List[str]:
        """允许访问此工具的组列表"""
        return []  # 默认空 = 所有人可访问

    @abstractmethod
    async def execute(self, context: ToolContext, args: T) -> ToolResult:
        pass
```

#### ToolSchema 中的权限声明

```python
class ToolSchema(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    access_groups: List[str]  # 权限组列表
```

#### ToolRegistry 的访问检查逻辑

```python
def check_tool_access(self, user: User, tool_name: str) -> bool:
    """检查用户是否有权使用指定工具"""
    tool = self.get_tool(tool_name)
    schema = tool.get_schema()

    # 如果工具没有设置 access_groups，则所有人可用
    if not schema.access_groups:
        return True

    # 检查用户的组是否在工具的允许组中
    return bool(set(user.group_memberships) & set(schema.access_groups))
```

**权限模型：基于组的访问控制（Group-Based Access Control, GBAC）**

- 工具声明允许哪些组访问
- 用户声明属于哪些组
- 取交集判断：有交集 = 有权限，无交集 = 拒绝

#### 工具拒绝机制

```python
class ToolRejection(BaseModel):
    reason: str  # 拒绝原因
```

工具可通过 `transform_args` 方法返回 `ToolRejection`，在参数验证阶段拦截不合规的调用（例如：用户无权访问特定数据库/表）。

### 4.4 UI 特性级访问控制

`AgentConfig` 中包含 `UiFeature` 枚举和对应的权限映射：

```python
class UiFeature(Enum):
    """可控制的 UI 特性"""
    CHART_GENERATION = "chart_generation"
    DATAFRAME_DISPLAY = "dataframe_display"
    FILE_OPERATIONS = "file_operations"
    PYTHON_EXECUTION = "python_execution"
    # ...

# AgentConfig 中
ui_feature_access: Dict[UiFeature, List[str]]
# key: UI 特性, value: 允许使用该特性的组列表
```

这层控制比工具级更细粒度——即使某用户能调用 `visualize_data` 工具，也可能被禁止看到图表 UI。

### 4.5 审计系统

```python
class AuditLogger(ABC):
    @abstractmethod
    async def log_event(self, event: AuditEvent) -> None:
        pass

class AuditEventType(Enum):
    TOOL_ACCESS_CHECK = "tool_access_check"
    TOOL_INVOCATION = "tool_invocation"
    TOOL_RESULT = "tool_result"
    UI_FEATURE_ACCESS_CHECK = "ui_feature_access_check"
    AI_RESPONSE = "ai_response"

# 具体事件模型
class ToolAccessCheckEvent(AuditEvent):
    user_id: str
    tool_name: str
    granted: bool          # 是否授权
    reason: Optional[str]  # 拒绝原因

class ToolInvocationEvent(AuditEvent):
    user_id: str
    tool_name: str
    arguments: Dict[str, Any]
    conversation_id: str

class ToolResultEvent(AuditEvent):
    user_id: str
    tool_name: str
    success: bool
    error: Optional[str]
    execution_time_ms: float
```

**审计设计特点：**
- 记录权限检查本身（即使拒绝也会记录）
- 记录完整的工具调用链
- 包含执行时间指标
- 与 ObservabilityProvider 联动

### 4.6 配额与生命周期控制

```python
class LifecycleHook(ABC):
    async def on_message_start(self, context: ...) -> None
    async def on_message_end(self, context: ...) -> None
    async def on_tool_start(self, context: ...) -> None
    async def on_tool_end(self, context: ...) -> None

# 典型实现：QuotaCheckHook
class QuotaCheckHook(LifecycleHook):
    async def on_message_start(self, context):
        # 检查用户是否超出调用配额
        if user.exceeded_quota():
            raise PermissionError("Quota exceeded")
```

### 4.7 权限控制完整数据流

```
HTTP Request
    │
    ▼
RequestContext(cookies, headers, remote_addr)
    │
    ▼
UserResolver.resolve_user() ─────────────────────┐
    │                                             │
    ▼                                             │
User(id, group_memberships)                       │ 审计: AiResponseEvent
    │                                             │
    ▼                                             │
Agent.send_message()                              │
    │                                             │
    ├─ LLM 决定调用工具 ──────────────────────────┤
    │   │                                         │
    │   ▼                                         │
    │   ToolRegistry.check_tool_access(user, tool)│
    │   │                                         │
    │   ├─ ✅ 通过 → AuditLog(ToolAccessCheck: granted=true)
    │   │   │                                     │
    │   │   ▼                                     │
    │   │   Tool.execute(context, args)           │
    │   │   │                                     │
    │   │   ├─ AuditLog(ToolInvocation)           │
    │   │   ├─ ...执行...                         │
    │   │   └─ AuditLog(ToolResult)               │
    │   │                                         │
    │   └─ ❌ 拒绝 → AuditLog(ToolAccessCheck: granted=false)
    │       └─ 返回拒绝消息给 LLM                  │
    │                                             │
    └─ LLM 生成最终响应 ──────────────────────────┘
```

---

## 五、实现流程（端到端）

### 5.1 初始化阶段

```python
# 1. 配置各组件
llm = AnthropicLlmService(api_key="...")
memory = ChromaAgentMemory(path="./memory")
registry = ToolRegistry()
registry.register_tool(RunSqlTool(sql_runner=PostgresSqlRunner(...)))
registry.register_tool(AgentMemoryTool(memory=memory))
registry.register_tool(VisualizeDataTool())

user_resolver = JwtUserResolver()
audit = LocalAuditLogger()

# 2. 组装 Agent
agent = Agent(
    llm_service=llm,
    tool_registry=registry,
    user_resolver=user_resolver,
    agent_memory=memory,
    audit_logger=audit,
    lifecycle_hooks=[QuotaCheckHook()],
    llm_middlewares=[CachingMiddleware()],
)
```

### 5.2 请求处理阶段

```python
# 3. 接收请求
request_context = RequestContext(
    cookies=request.cookies,
    headers=request.headers,
)

# 4. 流式处理
async for component in agent.send_message(request_context, "上月销售额Top10的客户是谁？"):
    # component 可能是:
    # - StatusBarUpdateComponent (状态栏更新)
    # - RichTextComponent (文本输出)
    # - DataFrameComponent (表格数据)
    # - CardComponent (卡片展示)
    # - TaskTrackerUpdateComponent (任务进度)
    yield_to_frontend(component)
```

### 5.3 内部 LLM 交互循环

```
Round 1:
  System Prompt = 基础提示词 + Schema上下文 + 文档上下文 + 相似SQL示例
  User Message = 历史消息 + 当前问题
  Tools = [run_sql, agent_memory_train, visualize_data, ...]

  → LLM 返回: tool_call("agent_memory_train", {sql: "SELECT ...", question: "..."})
  → 执行训练，存储问答对

Round 2:
  → LLM 返回: tool_call("run_sql", {sql: "SELECT customer, SUM(amount) ..."})
  → 执行 SQL，返回结果

Round 3:
  → LLM 返回: tool_call("visualize_data", {sql: "...", chart_type: "bar"})
  → 生成图表

Round 4:
  → LLM 返回: 自然语言总结
  → 结束循环
```

---

## 六、内置工具清单

| 工具 | 文件 | 功能 | access_groups |
|------|------|------|---------------|
| `run_sql` | tools/run_sql.py | 执行 SQL 查询 | 可配置 |
| `agent_memory` | tools/agent_memory.py | 训练/查询记忆 | 可配置 |
| `file_system` | tools/file_system.py | 文件读写 | 可配置 |
| `python` | tools/python.py | 执行 Python 代码 | 可配置 |
| `visualize_data` | tools/visualize_data.py | 生成图表 | 可配置 |

---

## 七、集成生态

### LLM 集成
- OpenAI (GPT-4/4o) / Anthropic (Claude) / Google Gemini
- Azure OpenAI / Ollama (本地部署)

### 数据库集成（SqlRunner）
- PostgreSQL / MySQL / Snowflake / BigQuery
- ClickHouse / MSSQL / SQLite / Oracle
- Hive / Presto / DuckDB

### 向量数据库（AgentMemory）
- ChromaDB / FAISS / Pinecone / Milvus
- Qdrant / Weaviate / Azure AI Search / Marqo / OpenSearch

---

## 八、服务层架构

### 8.1 多 Server 支持

```
servers/
├── fastapi/    → 异步 HTTP 服务（推荐生产用）
├── flask/      → 轻量 HTTP 服务
├── cli/        → 命令行交互
└── base/
    ├── chat_handler.py       → 基础聊天处理
    └── rich_chat_handler.py  → 富组件聊天处理
```

### 8.2 FastAPI 路由

```python
# 核心路由
POST /api/chat          → 发送消息（流式 SSE）
POST /api/train         → 训练 Agent 记忆
GET  /api/conversations → 获取对话列表
GET  /api/config        → 获取配置
```

---

## 九、Legacy 适配层

`legacy/adapter.py`（463 行）将 v2 Agent 包装为 v1 `VannaBase` 接口：

```python
# v1 用法（仍然支持）
from vanna import VannaOpenAI, VannaChromaDB

class MyVanna(VannaOpenAI, VannaChromaDB):
    ...

vn = MyVanna(...)
vn.ask("问题")  # 内部被 adapter 转发到 v2 Agent
```

---

## 十、架构评价

### 优点

1. **插件化程度极高** — 所有外部依赖都是接口，可自由替换
2. **7 个扩展点** — 覆盖了 Agent 生命周期的每个关键节点
3. **权限模型完整** — 从认证→组权限→工具权限→UI权限→配额→审计，层层递进
4. **流式架构** — AsyncGenerator 设计天然适合实时 UI
5. **审计追踪** — 企业级合规需求
6. **向后兼容** — legacy adapter 降低迁移成本

### 可改进点

1. **权限粒度** — 当前 GBAC 只到工具级别，缺少行/列级数据权限（例如：用户 A 只能查部门 A 的数据）
2. **权限热更新** — 组权限变更需要重新实例化 Agent
3. **Agent 文件过大** — agent.py 1407 行，建议拆分（工具执行循环、LLM 交互、错误处理可独立）
4. **测试覆盖** — test_tool_permissions.py 915 行，说明权限逻辑复杂度高，可考虑简化
5. **ToolRejection 机制** — 拒绝逻辑分散在 transform_args 和 execute 中，边界不够清晰

---

## 十一、关键设计模式总结

| 模式 | 应用位置 | 说明 |
|------|----------|------|
| 策略模式 | ErrorRecoveryStrategy | 错误恢复策略可替换 |
| 中间件模式 | LlmMiddleware | LLM 请求/响应拦截链 |
| 观察者模式 | LifecycleHook | 生命周期事件通知 |
| 装饰器模式 | ConversationFilter | 对话历史过滤增强 |
| 工厂模式 | ToolRegistry | 工具注册与查找 |
| 适配器模式 | legacy/adapter.py | v1↔v2 兼容 |
| 管道模式 | WorkflowHandler | 结果处理管道 |
| 上下文对象 | ToolContext/RequestContext | 跨层传递上下文 |

---

*报告生成 by 德柱 🏗️*
