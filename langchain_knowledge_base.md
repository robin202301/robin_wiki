# LangChain 官方文档知识库 & 开发流程指南

> 基于 LangChain 2026 最新官方文档整理 | 更新时间：2026-06-09
> 官方文档：https://docs.langchain.com | https://python.langchain.com

---

## 📑 目录

1. [架构总览](#1-架构总览)
2. [核心组件：模型（Models）](#2-核心组件模型models)
3. [核心组件：工具（Tools）](#3-核心组件工具tools)
4. [核心组件：Agent](#4-核心组件agent)
5. [记忆系统（Memory）](#5-记忆系统memory)
6. [中间件（Middleware）](#6-中间件middleware)
7. [Deep Agents（高级Agent框架）](#7-deep-agents高级agent框架)
8. [LangGraph（底层编排引擎）](#8-langgraph底层编排引擎)
9. [LangSmith（可观测性与调试）](#9-langsmith可观测性与调试)
10. [多Agent系统](#10-多agent系统)
11. [MCP 协议集成](#11-mcp-协议集成)
12. [RAG（检索增强生成）](#12-rag检索增强生成)
13. [结构化输出](#13-结构化输出)
14. [完整开发流程](#14-完整开发流程)
15. [最佳实践与设计模式](#15-最佳实践与设计模式)
16. [生态系统与选型指南](#16-生态系统与选型指南)

---

## 1. 架构总览

### 1.1 LangChain 产品矩阵

LangChain 生态系统由四个核心产品组成：

| 产品 | 定位 | 适用场景 |
|------|------|----------|
| **LangChain** (`create_agent`) | 高度可配置的 Agent 框架 | 需要自定义的 Agent 应用 |
| **Deep Agents** (`create_deep_agent`) | "电池全装好"的 Agent | 开箱即用的复杂任务 Agent |
| **LangGraph** | 底层编排引擎 | 高级工作流 + 确定性/Agent混合 |
| **LangSmith** | 可观测性平台 | 追踪、调试、评估、部署 |

### 1.2 核心公式

```
Agent = Model + Harness
```

- **Model**：大语言模型（推理引擎）
- **Harness**：围绕模型的一切——Prompt、Tools、Middleware
- LangChain 提供 `create_agent`：一个最小化、高度可配置的 harness

### 1.3 支持模型提供商

OpenAI、Anthropic、Google Gemini、Azure OpenAI、AWS Bedrock、HuggingFace、Ollama、OpenRouter、Fireworks、Baseten 等。

---

## 2. 核心组件：模型（Models）

### 2.1 初始化模型

```python
from langchain.chat_models import init_chat_model

# 方式一：init_chat_model（推荐）
model = init_chat_model(
    "openai:gpt-5.4",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)

# 方式二：直接使用模型类
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-5.4", temperature=0.5)
```

### 2.2 模型参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | str | 模型名称，格式 `"provider:model"` |
| `api_key` | str | API 密钥 |
| `temperature` | float | 随机性控制（高=创意，低=确定） |
| `max_tokens` | int | 最大输出 token 数 |
| `timeout` | int | 超时时间（秒） |
| `max_retries` | int | 最大重试次数（默认6） |

### 2.3 模型能力

- **Tool Calling**：调用外部工具（数据库查询、API调用等）
- **Structured Output**：约束模型输出为定义好的格式
- **Multimodality**：处理图像、音频、视频等多模态数据
- **Reasoning**：多步推理

### 2.4 关键方法

| 方法 | 说明 |
|------|------|
| `invoke()` | 同步调用，等待完整响应 |
| `stream()` | 流式输出，实时获取生成内容 |
| `batch()` | 批量请求，提高效率 |

### 2.5 各提供商安装

```bash
# OpenAI
pip install -U "langchain[openai]"

# Anthropic
pip install -U "langchain[anthropic]"

# Google Gemini
pip install -U "langchain[google-genai]"

# AWS Bedrock
pip install -U "langchain[aws]"

# Ollama（本地模型）
pip install -U "langchain-ollama"

# OpenRouter（多模型路由）
pip install -U "langchain-openrouter"
```

---

## 3. 核心组件：工具（Tools）

### 3.1 什么是工具

工具是 Agent 扩展能力的方式——让 Agent 可以获取实时数据、执行代码、查询数据库、与外部系统交互。

工具底层是带有明确输入/输出的可调用函数，由 Chat Model 决定何时调用。

### 3.2 定义工具

#### 基础定义（@tool 装饰器）

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```

> ⚠️ 类型提示**必须**有，函数文档字符串会成为工具描述

#### 自定义工具名称和描述

```python
@tool("web_search")  # 自定义名称
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

@tool("calculator", description="Performs arithmetic. Use for math problems.")
def calc(expression: str) -> str:
    return str(eval(expression))
```

#### 高级 Schema 定义（Pydantic）

```python
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius", description="Temperature unit"
    )
    include_forecast: bool = Field(default=False, description="Include 5-day forecast")

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    return f"Weather in {location}: 22 degrees"
```

### 3.3 工具运行时上下文（ToolRuntime）

工具可以通过 `ToolRuntime` 参数访问运行时信息：

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_last_user_message(runtime: ToolRuntime) -> str:
    """Get the most recent user message."""
    messages = runtime.state["messages"]
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return message.content
    return "No user messages"
```

| 组件 | 说明 | 用途 |
|------|------|------|
| **State** | 短期记忆（消息、计数器等） | 访问对话历史 |
| **Context** | 不可变配置（用户ID、会话信息） | 个性化响应 |
| **Store** | 长期记忆（跨会话持久化） | 用户偏好、知识库 |
| **Stream Writer** | 实时进度输出 | 长任务进度展示 |
| **Execution Info** | 执行身份信息 | 线程ID、运行ID |
| **Tool Call ID** | 当前工具调用唯一标识 | 日志关联 |

> ⚠️ 保留参数名：`config` 和 `runtime` 不能使用，需用 `ToolRuntime` 参数

### 3.4 工具更新状态

```python
from langchain.agents import AgentState
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

class CustomState(AgentState):
    user_name: str

@tool
def set_user_name(new_name: str, runtime: ToolRuntime[None, CustomState]) -> Command:
    """Set the user's name in state."""
    return Command(
        update={
            "user_name": new_name,
            "messages": [ToolMessage(content=f"Name set to {new_name}.", tool_call_id=runtime.tool_call_id)],
        }
    )
```

---

## 4. 核心组件：Agent

### 4.1 Agent = 模型 + Harness

Agent 是一个在循环中调用工具直到任务完成的模型。

### 4.2 创建 Agent

```python
from langchain.agents import create_agent

# 基础 Agent
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# 调用 Agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in SF?"}]}
)
```

### 4.3 核心组件

#### 模型配置
```python
agent = create_agent("openai:gpt-5.4", tools=tools)
```

#### 工具配置
```python
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent("openai:gpt-5.4", tools=[search])
```

#### 系统提示词
```python
agent = create_agent(
    "openai:gpt-5.4",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

#### 结构化输出
```python
from pydantic import BaseModel

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent("openai:gpt-5.4", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

### 4.4 对话持久化

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "conversation-1"}}

# 第一轮
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    config=config,
)

# 第二轮（记住之前的对话）
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config=config,
)
```

### 4.5 上下文传递

```python
from dataclasses import dataclass

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hello"}]},
    config={"configurable": {"thread_id": "1"}},
    context=Context(user_id="user-123"),
)
```

---

## 5. 记忆系统（Memory）

### 5.1 短期记忆（Short-term Memory）

短期记忆 = 单个对话/线程内的记忆，主要是**对话历史**。

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[],
    checkpointer=InMemorySaver(),  # 短期记忆
)
```

**生产环境使用 PostgreSQL：**
```python
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://user:pass@localhost:5432/db"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()
    agent = create_agent("gpt-5.5", tools=[], checkpointer=checkpointer)
```

**支持的 Checkpointer 后端：**
- InMemorySaver（开发/测试）
- PostgresSaver（生产推荐）
- SQLiteSaver
- Azure Cosmos DB

### 5.2 长期记忆（Long-term Memory）

长期记忆 = 跨对话/线程的持久化记忆。

```python
from langchain.agents import create_agent
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
agent = create_agent("claude-sonnet-4-6", tools=[], store=store)
```

**存储结构：**
- 数据以 JSON 文档形式存储
- 按 namespace（类似文件夹）和 key（类似文件名）组织
- 支持层级组织和跨 namespace 搜索

**工具中读写长期记忆：**

```python
@tool
def get_user_info(runtime: ToolRuntime) -> str:
    """Look up user info."""
    user_id = runtime.context.user_id
    user_info = runtime.store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

@tool
def save_preference(runtime: ToolRuntime, pref: str, value: str) -> str:
    """Save user preference."""
    runtime.store.put(("users", "preferences"), runtime.context.user_id, {pref: value})
    return "Preference saved"
```

**生产环境 Store：**
```python
from langgraph.store.postgres import PostgresStore

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()
    agent = create_agent("claude-sonnet-4-6", tools=[], store=store)
```

### 5.3 记忆类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **语义记忆** | 事实和知识 | 用户偏好、产品知识 |
| **情景记忆** | 具体经历 | 对话历史、事件记录 |
| **程序记忆** | 技能和方法 | 工具使用模式、工作流程 |

---

## 6. 中间件（Middleware）

### 6.1 概述

中间件在 Agent 循环的每一步前后提供钩子，用于：

- 📊 追踪和调试（日志、分析）
- 🔄 变换 Prompt、工具选择、输出格式
- 🔁 添加重试、降级、提前终止
- 🛡️ 速率限制、护栏、PII 检测

### 6.2 使用中间件

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[...],
    middleware=[
        SummarizationMiddleware(...),
        HumanInTheLoopMiddleware(...)
    ],
)
```

### 6.3 内置中间件

| 中间件 | 功能 |
|--------|------|
| `SummarizationMiddleware` | 自动压缩上下文 |
| `HumanInTheLoopMiddleware` | 关键操作人工审批 |
| `ToolRetryMiddleware` | 工具调用重试 |
| `ModelFallbackMiddleware` | 模型降级 |
| `ModelCallLimitMiddleware` | 调用次数限制 |
| `PIIDetectionMiddleware` | 个人信息检测 |
| `LLMToolSelector` | 动态工具选择 |

### 6.4 在 LangGraph 中使用

中间件可以嵌入更大的 StateGraph 工作流中：

```python
from langgraph.graph import START, StateGraph

email_agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[read_email, send_email],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"send_email": True})],
)

graph = (
    StateGraph(AgentState)
    .add_node("classify", classify_node)
    .add_node("email_agent", email_agent)
    .add_edge(START, "classify")
    .add_conditional_edges("classify", route)
    .compile()
)
```

---

## 7. Deep Agents（高级Agent框架）

### 7.1 概述

Deep Agents 是 LangChain 生态中"电池全装好"的 Agent 框架，内置：

- 📋 **任务规划**：自动拆解复杂任务为离散步骤
- 📂 **虚拟文件系统**：管理上下文，卸载大文件
- 🤖 **子Agent派生**：并行处理子任务
- 💾 **长期记忆**：跨线程持久化
- 👤 **人机协作**：关键决策点审批
- 📊 **流式输出**：实时事件流

### 7.2 创建 Deep Agent

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="openai:gpt-5.4",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

### 7.3 核心能力

| 能力 | 说明 |
|------|------|
| **Planning & Task Decomposition** | `write_todos` 工具自动规划 |
| **Context Compression** | 自动压缩历史消息、卸载大结果 |
| **Virtual Filesystem** | 可插拔后端（内存/磁盘/LangGraph Store） |
| **Shell Execution** | 执行测试、构建、git 操作 |
| **Subagent Spawning** | `task` 工具派生子Agent |
| **Async Subagents** | 后台运行、进度检查、取消 |
| **Streaming** | 类型化事件流，子Agent独立流 |
| **MCP Integration** | Model Context Protocol 标准接口 |
| **Filesystem Permissions** | 读写权限控制 |

### 7.4 Deep Agents vs LangChain vs LangGraph

| 维度 | Deep Agents | LangChain | LangGraph |
|------|------------|-----------|-----------|
| 复杂度 | 开箱即用 | 高度自定义 | 低层控制 |
| 文件系统 | ✅ 内置 | ❌ 需自建 | ❌ 需自建 |
| 子Agent | ✅ 内置 `task` 工具 | ❌ 需自建 | ⚠️ 手动编排 |
| 上下文压缩 | ✅ 自动 | ⚠️ 中间件 | ⚠️ 需自建 |
| 适用场景 | 复杂多步任务 | 自定义Agent | 混合工作流 |

---

## 8. LangGraph（底层编排引擎）

### 8.1 概述

LangGraph 是 LangChain 生态系统的底层编排引擎，提供：

- 持久化执行（Durable Execution）
- 人机协作（Human-in-the-loop）
- 流式处理
- 状态管理

### 8.2 核心概念

```python
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    messages: list
    current_step: str

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")
app = graph.compile()
```

### 8.3 Checkpointer 库

| 库 | 后端 | 安装 |
|---|---|---|
| InMemorySaver | 内存 | langgraph (内置) |
| PostgresSaver | PostgreSQL | langgraph-checkpoint-postgres |
| SqliteSaver | SQLite | langgraph-checkpoint-sqlite |
| CosmosDBSaver | Azure Cosmos DB | langgraph-checkpoint-azure |

---

## 9. LangSmith（可观测性与调试）

### 9.1 功能

- 🔍 **Tracing**：追踪每次模型调用、工具调用、Agent 步骤
- 🐛 **Debugging**：可视化执行路径、状态转换
- 📊 **Evaluation**：实验对比、自动评估
- 🚀 **Deployment**：部署 Agent 到生产环境
- 🔔 **Alerts**：监控和告警
- 📈 **Dashboards**：项目仪表盘

### 9.2 快速启用

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-api-key"
```

### 9.3 LangSmith Engine

自动监控追踪数据，检测问题，提出修复建议。

---

## 10. 多Agent系统

### 10.1 使用子图（Subgraph）

```python
from langgraph.graph import StateGraph

# 多个专业 Agent 组成工作流
graph = (
    StateGraph(AgentState)
    .add_node("researcher", research_agent)
    .add_node("writer", writing_agent)
    .add_node("reviewer", review_agent)
    .add_edge(START, "researcher")
    .add_edge("researcher", "writer")
    .add_edge("writer", "reviewer")
    .add_edge("reviewer", END)
    .compile()
)
```

### 10.2 Agent 名称

```python
agent = create_agent(
    "openai:gpt-5.4",
    tools=tools,
    name="research_assistant",  # 子图节点名称
)
```

---

## 11. MCP 协议集成

### 11.1 Model Context Protocol

MCP 是连接 Agent 与外部系统的标准协议，支持：
- 数据库连接
- API 集成
- 文件系统访问
- 第三方服务

### 11.2 使用 MCP 工具

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="openai:gpt-5.4",
    tools=[...],  # 包含 MCP 工具
)
```

---

## 12. RAG（检索增强生成）

### 12.1 RAG 架构

```
文档 → 分割 → 向量化 → 存储 → 检索 → 增强Prompt → LLM → 回答
```

### 12.2 核心组件

| 组件 | 功能 | LangChain 集成 |
|------|------|----------------|
| **Document Loaders** | 加载各类文档 | langchain-community |
| **Text Splitters** | 文本分割 | RecursiveCharacterTextSplitter |
| **Embeddings** | 文本向量化 | OpenAIEmbeddings, etc. |
| **Vector Stores** | 向量存储 | FAISS, Pinecone, Chroma, etc. |
| **Retrievers** | 检索器 | VectorStoreRetriever |

### 12.3 在 Agent 中实现 RAG

通过工具将 RAG 集成到 Agent 中：

```python
@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base for relevant information."""
    docs = retriever.invoke(query)
    return "\n".join([doc.page_content for doc in docs])
```

---

## 13. 结构化输出

### 13.1 使用 Pydantic 模型

```python
from pydantic import BaseModel, Field

class ResearchResult(BaseModel):
    topic: str = Field(description="Research topic")
    summary: str = Field(description="Brief summary")
    key_findings: list[str] = Field(description="Key findings")
    confidence: float = Field(description="Confidence score 0-1")

agent = create_agent(
    "openai:gpt-5.4",
    tools=[search_web, read_paper],
    response_format=ResearchResult,
)
```

---

## 14. 完整开发流程

### Phase 1：环境搭建

```bash
# 1. 创建项目
mkdir my-agent-project && cd my-agent-project
uv init && uv add langchain deepagents langgraph-checkpoint-postgres

# 或 pip
pip install -U langchain deepagents "langchain[openai]"

# 2. 设置 API Keys
export OPENAI_API_KEY="your-key"
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="your-langsmith-key"
```

### Phase 2：定义 Agent

```python
from langchain.agents import create_agent
from langchain.tools import tool

# 1. 定义工具
@tool
def search(query: str) -> str:
    """Search for information online."""
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

# 2. 创建 Agent
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search, calculate],
    system_prompt="""You are a research assistant.
    
    ## Capabilities
    - `search`: Find information online
    - `calculate`: Perform calculations
    
    Always ground your answers in tool results.""",
)
```

### Phase 3：添加记忆

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search, calculate],
    checkpointer=InMemorySaver(),  # 短期记忆
    store=InMemoryStore(),         # 长期记忆
)
```

### Phase 4：添加中间件

```python
from langchain.agents.middleware import (
    SummarizationMiddleware,
    HumanInTheLoopMiddleware,
)

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search, calculate],
    middleware=[
        SummarizationMiddleware(),
        HumanInTheLoopMiddleware(interrupt_on={"search": True}),
    ],
)
```

### Phase 5：测试与调试

```python
# 启用 LangSmith 追踪
import os
os.environ["LANGSMITH_TRACING"] = "true"

# 测试
config = {"configurable": {"thread_id": "test-1"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is quantum computing?"}]},
    config=config,
)
print(result["messages"][-1].content)
```

### Phase 6：生产部署

```python
# 1. 使用数据库后端
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

DB_URI = "postgresql://user:pass@localhost:5432/agent_db"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()
    with PostgresStore.from_conn_string(DB_URI) as store:
        store.setup()
        
        agent = create_agent(
            model="openai:gpt-5.4",
            tools=[...],
            checkpointer=checkpointer,
            store=store,
            middleware=[SummarizationMiddleware()],
        )

# 2. 部署到 LangSmith
# 参考：https://docs.langchain.com/langsmith/deployment
```

### Phase 7：监控与优化

- LangSmith Tracing → 查看执行路径
- LangSmith Evaluation → 对比模型/Prompt效果
- LangSmith Alerts → 设置异常告警
- LangSmith Dashboards → 监控性能指标

---

## 15. 最佳实践与设计模式

### 15.1 Prompt 设计

```python
SYSTEM_PROMPT = """You are a literary data assistant.

## Capabilities
- `fetch_text_from_url`: loads document text from a URL
- `search_database`: search internal knowledge base

## Guidelines
- Do not guess—ground answers in tool results
- Be concise and accurate
- If uncertain, say so
"""
```

### 15.2 工具设计原则

1. **名称用 snake_case**（如 `web_search` 而非 `Web Search`）
2. **文档字符串要详细**（模型依赖它理解工具用途）
3. **类型提示必须完整**（定义输入 Schema）
4. **每个工具只做一件事**
5. **错误处理要完善**

### 15.3 错误处理

```python
from langchain.agents.middleware import ToolRetryMiddleware

agent = create_agent(
    model="gpt-5.4",
    tools=[...],
    middleware=[ToolRetryMiddleware(max_retries=3)],
)
```

### 15.4 安全护栏

```python
from langchain.agents.middleware import (
    PIIetectionMiddleware,    # PII 检测
    ModelCallLimitMiddleware, # 调用次数限制
)

agent = create_agent(
    model="gpt-5.4",
    tools=[...],
    middleware=[
        PIIetectionMiddleware(),
        ModelCallLimitMiddleware(max_calls=20),
        HumanInTheLoopMiddleware(interrupt_on={"send_email": True}),
    ],
)
```

### 15.5 上下文工程

- 使用 `SummarizationMiddleware` 自动压缩历史
- Deep Agents 自动将大结果卸载到虚拟文件系统
- 使用 `thread_id` 管理对话生命周期
- 使用 `context` 传递不可变运行时数据

---

## 16. 生态系统与选型指南

### 16.1 核心包

| 包 | 用途 |
|---|---|
| `langchain` | 核心框架 |
| `langchain-openai` | OpenAI 集成 |
| `langchain-anthropic` | Anthropic 集成 |
| `langchain-google-genai` | Google Gemini 集成 |
| `langchain-aws` | AWS Bedrock 集成 |
| `langchain-ollama` | Ollama 本地模型 |
| `langchain-openrouter` | OpenRouter 多模型路由 |
| `langgraph` | 编排引擎 |
| `langgraph-checkpoint-postgres` | PostgreSQL 持久化 |
| `langgraph-store-postgres` | PostgreSQL 存储 |
| `deepagents` | 高级 Agent 框架 |

### 16.2 选型决策树

```
需要构建 AI Agent？
├── 快速原型/简单任务 → Deep Agents（开箱即用）
├── 高度自定义 Agent → LangChain `create_agent`
├── 确定性 + Agent 混合工作流 → LangGraph
└── 需要可观测性/部署 → LangSmith（必选）
```

### 16.3 官方资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.langchain.com |
| Python 文档 | https://python.langchain.com |
| API Reference | https://reference.langchain.com/python |
| LangSmith | https://smith.langchain.com |
| GitHub | https://github.com/langchain-ai |
| LangChain Skills | https://github.com/langchain-ai/langchain-skills |
| MCP Server | 给 AI 编码助手提供文档访问 |

---

> 📝 本文档基于 LangChain 2026 年最新官方文档整理。
> 如有更新或补充，请联系 Robin。
