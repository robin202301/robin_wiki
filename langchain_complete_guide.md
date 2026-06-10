# LangChain 完整知识体系

> 基于 LangChain 2026 最新官方文档 | 更新时间：2026-06-10
> 官方文档：https://docs.langchain.com

---

## 📚 目录

- [第一部分：核心概念](#第一部分核心概念)
  - [1.1 什么是 LangChain](#11-什么是-langchain)
  - [1.2 产品矩阵](#12-产品矩阵)
  - [1.3 核心公式](#13-核心公式agent--model--harness)
  - [1.4 消息系统（Messages）](#14-消息系统messages)
  - [1.5 模型（Models）](#15-模型models)
  - [1.6 工具（Tools）](#16-工具tools)
  - [1.7 Agent（智能体）](#17-agent智能体)
  - [1.8 记忆系统（Memory）](#18-记忆系统memory)
  - [1.9 中间件（Middleware）](#19-中间件middleware)
  - [1.10 结构化输出](#110-结构化输出structured-output)
- [第二部分：高级架构](#第二部分高级架构)
  - [2.1 Deep Agents](#21-deep-agents)
  - [2.2 LangGraph 编排引擎](#22-langgraph-编排引擎)
  - [2.3 多Agent系统](#23-多agent系统)
  - [2.4 RAG（检索增强生成）](#24-rag检索增强生成)
  - [2.5 MCP 协议集成](#25-mcp-协议集成)
- [第三部分：开发流程](#第三部分开发流程)
  - [3.1 环境搭建](#31-环境搭建)
  - [3.2 第一个Agent](#32-第一个agent)
  - [3.3 添加记忆](#33-添加记忆)
  - [3.4 添加中间件](#34-添加中间件)
  - [3.5 测试调试](#35-测试调试)
  - [3.6 生产部署](#36-生产部署)
- [第四部分：实战代码Demo](#第四部分实战代码demo)
  - [Demo 1: 基础对话Agent](#demo-1-基础对话agent)
  - [Demo 2: RAG知识库问答](#demo-2-rag知识库问答)
  - [Demo 3: 工具调用Agent](#demo-3-工具调用agent)
  - [Demo 4: 多Agent协作](#demo-4-多agent协作)
  - [Demo 5: Deep Agent完整示例](#demo-5-deep-agent完整示例)

---

# 第一部分：核心概念

## 1.1 什么是 LangChain

LangChain 是一个用于构建 AI Agent 应用的开源框架。它提供了标准化的接口来连接大语言模型、工具和数据源，让开发者可以快速构建复杂的 AI 应用。

**核心理念：**
- **标准化**：统一的模型接口，支持 OpenAI、Anthropic、Google 等多家提供商
- **可组合**：模块化设计，组件可自由组合
- **可观测**：与 LangSmith 集成，提供追踪、调试、评估能力

## 1.2 产品矩阵

LangChain 生态系统由四个核心产品组成：

| 产品 | 定位 | 适用场景 | 入口函数 |
|------|------|----------|----------|
| **LangChain** | 高度可配置的 Agent 框架 | 需要精细控制的 Agent 应用 | `create_agent()` |
| **Deep Agents** | 开箱即用的高级 Agent | 复杂多步任务、文件操作 | `create_deep_agent()` |
| **LangGraph** | 底层编排引擎 | 自定义工作流、混合逻辑 | `StateGraph()` |
| **LangSmith** | 可观测性平台 | 追踪、调试、评估、部署 | - |

**选型决策树：**
```
需要构建 AI Agent？
├── 快速原型/简单任务 → Deep Agents（开箱即用）
├── 高度自定义 Agent → LangChain `create_agent`
├── 确定性 + Agent 混合工作流 → LangGraph
└── 需要可观测性/部署 → LangSmith（必选）
```

## 1.3 核心公式：Agent = Model + Harness

```
Agent = Model + Harness
```

- **Model（模型）**：大语言模型，负责推理和决策
- **Harness（工具链）**：围绕模型的一切——Prompt、Tools、Middleware

> Agent 是一个在循环中调用工具直到任务完成的模型。Harness 的职责是在正确的时间给模型提供正确的上下文。

## 1.4 消息系统（Messages）

消息是 LangChain 中模型交互的基本单元。

### 消息类型

| 类型 | 角色 | 说明 |
|------|------|------|
| `SystemMessage` | system | 系统指令，定义模型行为 |
| `HumanMessage` | user | 用户输入 |
| `AIMessage` | assistant | 模型输出，包含 tool_calls |
| `ToolMessage` | tool | 工具执行结果 |

### 代码示例

```python
from langchain.messages import (
    SystemMessage, HumanMessage, AIMessage, ToolMessage
)
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-5.4")

# 构建消息列表
messages = [
    SystemMessage("你是一个有帮助的编程助手。"),
    HumanMessage("如何创建一个 REST API？"),
]

# 调用模型
response = model.invoke(messages)  # 返回 AIMessage
print(response.text)

# 访问工具调用信息
for tool_call in response.tool_calls:
    print(f"工具: {tool_call['name']}")
    print(f"参数: {tool_call['args']}")

# 访问 token 使用统计
print(response.usage_metadata)
# {'input_tokens': 50, 'output_tokens': 200, 'total_tokens': 250}
```

### 消息格式

```python
# 方式一：消息对象
from langchain.messages import HumanMessage
response = model.invoke([HumanMessage("你好")])

# 方式二：字典格式（OpenAI 兼容）
messages = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"}
]
response = model.invoke(messages)

# 方式三：字符串（快捷方式，等同于单个 HumanMessage）
response = model.invoke("你好")
```

## 1.5 模型（Models）

### 初始化模型

```python
from langchain.chat_models import init_chat_model

# 推荐方式：init_chat_model
model = init_chat_model(
    "openai:gpt-5.4",  # 格式: "provider:model"
    temperature=0.7,    # 随机性 (0=确定, 1=创意)
    max_tokens=4096,    # 最大输出长度
    timeout=60,         # 超时秒数
    max_retries=3,      # 重试次数
)

# 直接使用模型类
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-5.4", temperature=0.7)
```

### 支持的提供商

| 提供商 | 安装命令 | 模型示例 |
|--------|----------|----------|
| OpenAI | `pip install "langchain[openai]"` | gpt-5.4, o1 |
| Anthropic | `pip install "langchain[anthropic]"` | claude-sonnet-4-6 |
| Google | `pip install "langchain[google-genai]"` | gemini-2.5-flash |
| Azure | `pip install "langchain[openai]"` | gpt-5.4 (Azure部署) |
| AWS Bedrock | `pip install "langchain[aws]"` | claude-3-5-sonnet |
| Ollama | `pip install langchain-ollama` | llama3, mistral |
| OpenRouter | `pip install langchain-openrouter` | 多模型路由 |

### 关键方法

```python
# 同步调用
response = model.invoke("你好")

# 流式输出
for chunk in model.stream("讲一个故事"):
    print(chunk.text, end="")

# 批量调用
responses = model.batch(["你好", "再见"])
```

### 模型能力

- **Tool Calling**：调用外部工具（数据库、API等）
- **Structured Output**：输出符合指定 schema 的结构化数据
- **Multimodality**：处理图像、音频、视频
- **Reasoning**：多步推理

```python
# 工具调用示例
def get_weather(location: str) -> str:
    """获取天气信息"""
    return f"{location}: 晴, 25°C"

model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("北京天气如何？")

# 模型会返回 tool_calls
print(response.tool_calls)
# [{'name': 'get_weather', 'args': {'location': '北京'}, 'id': 'call_xxx'}]
```

## 1.6 工具（Tools）

工具让 Agent 能够执行实际操作——查询数据库、调用 API、搜索网页等。

### 定义工具

```python
from langchain.tools import tool

# 基础定义
@tool
def search_database(query: str, limit: int = 10) -> str:
    """搜索数据库中的记录。
    
    Args:
        query: 搜索关键词
        limit: 最大返回数量
    """
    return f"找到 {limit} 条关于 '{query}' 的结果"

# 自定义名称和描述
@tool("web_search", description="在网络上搜索信息")
def search(query: str) -> str:
    return f"搜索结果: {query}"
```

### 高级 Schema 定义

```python
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    location: str = Field(description="城市名称或坐标")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius", description="温度单位"
    )
    include_forecast: bool = Field(default=False, description="是否包含5天预报")

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", 
                include_forecast: bool = False) -> str:
    """获取天气信息"""
    temp = 25 if units == "celsius" else 77
    result = f"{location}: {temp}°{units[0].upper()}"
    if include_forecast:
        result += "\n未来5天: 晴"
    return result
```

### 工具运行时上下文（ToolRuntime）

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_user_context(runtime: ToolRuntime) -> str:
    """获取当前用户上下文信息"""
    # 访问对话历史
    messages = runtime.state["messages"]
    
    # 访问用户ID等上下文
    user_id = runtime.context.user_id
    
    # 访问长期记忆
    preferences = runtime.store.get(("users",), user_id)
    
    return f"用户: {user_id}, 偏好: {preferences}"
```

| 上下文组件 | 说明 | 用途 |
|-----------|------|------|
| `runtime.state` | 短期记忆（消息、状态） | 访问对话历史 |
| `runtime.context` | 不可变配置（用户ID） | 个性化响应 |
| `runtime.store` | 长期记忆（跨会话） | 用户偏好存储 |
| `runtime.stream_writer` | 流式写入器 | 实时进度输出 |
| `runtime.tool_call_id` | 工具调用ID | 日志关联 |

## 1.7 Agent（智能体）

### 创建 Agent

```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"搜索结果: {query}"

@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    return str(eval(expression))

# 创建 Agent
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search, calculate],
    system_prompt="""你是一个研究助手。
    
## 能力
- `search`: 搜索信息
- `calculate`: 进行计算

## 规则
- 始终基于工具结果回答
- 不确定的时候说不知道
""",
)

# 调用 Agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "中国人口是多少？"}]}
)
print(result["messages"][-1].text)
```

### 对话持久化

```python
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search],
    checkpointer=InMemorySaver(),  # 启用短期记忆
)

config = {"configurable": {"thread_id": "conversation-1"}}

# 第一轮
agent.invoke(
    {"messages": [{"role": "user", "content": "我叫小明"}]},
    config=config,
)

# 第二轮（记住之前的对话）
result = agent.invoke(
    {"messages": [{"role": "user", "content": "我叫什么名字？"}]},
    config=config,
)
# 模型会回答"小明"
```

### 上下文传递

```python
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id: str
    role: str = "user"

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search],
    context_schema=UserContext,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "你好"}]},
    config={"configurable": {"thread_id": "1"}},
    context=UserContext(user_id="u_123", role="admin"),
)
```

## 1.8 记忆系统（Memory）

### 短期记忆（Short-term Memory）

短期记忆 = 单个对话线程内的持久化状态，主要是对话历史。

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

# 开发环境：内存
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[],
    checkpointer=InMemorySaver(),
)

# 生产环境：PostgreSQL
DB_URI = "postgresql://user:pass@localhost:5432/agent_db"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()  # 自动创建表
    agent = create_agent(
        model="openai:gpt-5.4",
        tools=[],
        checkpointer=checkpointer,
    )
```

**支持的 Checkpointer 后端：**
- `InMemorySaver` - 开发/测试
- `PostgresSaver` - 生产推荐
- `SqliteSaver` - 轻量级持久化
- `CosmosDBSaver` - Azure 环境

### 长期记忆（Long-term Memory）

长期记忆 = 跨对话/线程的持久化数据。

```python
from langchain.agents import create_agent
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore
from langchain.tools import tool, ToolRuntime

# 创建 Store
store = InMemoryStore()  # 开发
# store = PostgresStore.from_conn_string(DB_URI)  # 生产

# 创建带长期记忆的 Agent
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[],
    store=store,
)

# 工具中读写长期记忆
@tool
def save_preference(runtime: ToolRuntime, key: str, value: str) -> str:
    """保存用户偏好"""
    user_id = runtime.context.user_id
    runtime.store.put(("preferences",), user_id, {key: value})
    return "偏好已保存"

@tool
def get_preference(runtime: ToolRuntime, key: str) -> str:
    """获取用户偏好"""
    user_id = runtime.context.user_id
    result = runtime.store.get(("preferences",), user_id)
    return result.value.get(key, "未设置") if result else "未设置"
```

**记忆存储结构：**
```
Store
├── namespace: ("users",)
│   └── key: "user_123"
│       └── value: {"name": "小明", "lang": "zh"}
├── namespace: ("preferences",)
│   └── key: "user_123"
│       └── value: {"theme": "dark", "notify": true}
└── namespace: ("history", "user_123")
    └── key: "2024-01"
        └── value: {"topics": ["AI", "编程"]}
```

### 记忆类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 语义记忆 | 事实和知识 | 用户偏好、产品知识 |
| 情景记忆 | 具体经历 | 对话历史、事件 |
| 程序记忆 | 技能和方法 | 工具使用模式 |

## 1.9 中间件（Middleware）

中间件在 Agent 循环的每个步骤前后注入逻辑。

### 内置中间件

```python
from langchain.agents import create_agent
from langchain.agents.middleware import (
    SummarizationMiddleware,    # 上下文压缩
    HumanInTheLoopMiddleware,   # 人工审批
    ToolRetryMiddleware,        # 工具重试
    ModelFallbackMiddleware,    # 模型降级
    ModelCallLimitMiddleware,   # 调用限制
    PIIDetectionMiddleware,     # PII 检测
)

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[send_email, search],
    middleware=[
        SummarizationMiddleware(),
        HumanInTheLoopMiddleware(
            interrupt_on={"send_email": True}  # 发邮件需人工审批
        ),
        ToolRetryMiddleware(max_retries=3),
        ModelCallLimitMiddleware(max_calls=20),
    ],
)
```

### 自定义中间件

```python
from langchain.agents.middleware import Middleware

class LoggingMiddleware(Middleware):
    def before_model(self, state, config):
        print(f"🤖 调用模型，消息数: {len(state['messages'])}")
        return state
    
    def after_model(self, state, config, response):
        print(f"✅ 模型响应: {response.text[:100]}...")
        return state
    
    def before_tool(self, state, config, tool_call):
        print(f"🔧 调用工具: {tool_call['name']}")
        return state
    
    def after_tool(self, state, config, tool_result):
        print(f"✅ 工具结果: {tool_result[:100]}...")
        return state

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search],
    middleware=[LoggingMiddleware()],
)
```

## 1.10 结构化输出（Structured Output）

让 Agent 返回符合指定 schema 的结构化数据。

### 自动策略选择

```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent

class ProductReview(BaseModel):
    """产品评论分析"""
    rating: int = Field(description="评分 1-5", ge=1, le=5)
    sentiment: str = Field(description="情感: positive/negative")
    key_points: list[str] = Field(description="关键要点")

# 直接传入 schema，LangChain 自动选择最佳策略
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[],
    response_format=ProductReview,  # 自动选择 ProviderStrategy 或 ToolStrategy
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "分析评论: '产品很好，5星好评，就是有点贵'"
    }]
})

# 获取结构化响应
review = result["structured_response"]
print(review.rating)      # 5
print(review.sentiment)   # positive
print(review.key_points)  # ['质量好', '价格高']
```

### 显式策略配置

```python
from langchain.agents.structured_output import (
    ProviderStrategy,  # 使用模型原生结构化输出
    ToolStrategy,      # 使用工具调用实现结构化输出
)

# ProviderStrategy: 最可靠（OpenAI, Anthropic 支持）
agent = create_agent(
    model="openai:gpt-5.4",
    response_format=ProviderStrategy(ProductReview, strict=True),
)

# ToolStrategy: 兼容所有支持工具调用的模型
agent = create_agent(
    model="ollama:llama3",
    response_format=ToolStrategy(
        ProductReview,
        handle_errors=True,  # 验证失败时自动重试
    ),
)
```

### 支持的 Schema 类型

```python
# Pydantic Model（推荐）
class Review(BaseModel):
    rating: int
    text: str

# Dataclass
from dataclasses import dataclass
@dataclass
class Review:
    rating: int
    text: str

# TypedDict
from typing_extensions import TypedDict
class Review(TypedDict):
    rating: int
    text: str

# JSON Schema
review_schema = {
    "type": "object",
    "properties": {
        "rating": {"type": "integer"},
        "text": {"type": "string"}
    },
    "required": ["rating", "text"]
}
```

---

# 第二部分：高级架构

## 2.1 Deep Agents

Deep Agents 是"电池全装好"的高级 Agent 框架，内置复杂任务所需的全部能力。

### 核心能力

| 能力 | 说明 |
|------|------|
| 任务规划 | `write_todos` 工具自动拆解任务 |
| 虚拟文件系统 | 读写文件、管理上下文 |
| 子Agent派生 | `task` 工具创建子Agent |
| Shell执行 | 运行命令、测试、构建 |
| 上下文压缩 | 自动压缩历史消息 |
| 长期记忆 | 跨会话持久化 |
| 人机协作 | 关键决策点审批 |
| MCP集成 | 标准协议连接外部系统 |

### 创建 Deep Agent

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="openai:gpt-5.4",
    tools=[],  # 内置工具自动加载
    system_prompt="你是一个能读写文件、执行代码的研究助手",
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "研究 AI 最新趋势，写一份报告保存到 report.md"
    }]
})
```

### Deep Agents vs LangChain vs LangGraph

| 维度 | Deep Agents | LangChain | LangGraph |
|------|------------|-----------|-----------|
| 复杂度 | 开箱即用 | 高度自定义 | 低层控制 |
| 文件系统 | ✅ 内置 | ❌ 需自建 | ❌ 需自建 |
| 子Agent | ✅ `task` 工具 | ❌ 需自建 | ⚠️ 手动编排 |
| 上下文压缩 | ✅ 自动 | ⚠️ 中间件 | ⚠️ 需自建 |
| 适用场景 | 复杂多步任务 | 自定义Agent | 混合工作流 |

## 2.2 LangGraph 编排引擎

LangGraph 是底层状态机引擎，LangChain 的 Agent 构建在其之上。

### 基本概念

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    should_continue: bool

def agent_node(state: AgentState):
    # 调用模型
    response = model.invoke(state["messages"])
    return {"messages": [response], "should_continue": bool(response.tool_calls)}

def tool_node(state: AgentState):
    # 执行工具
    last_message = state["messages"][-1]
    results = []
    for tool_call in last_message.tool_calls:
        result = execute_tool(tool_call)
        results.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
    return {"messages": results}

def should_continue(state: AgentState):
    return "tools" if state["should_continue"] else END

# 构建图
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()
```

## 2.3 多Agent系统

### 多Agent模式对比

| 模式 | 工作原理 | 优势 |
|------|----------|------|
| **Subagents** | 主Agent将子Agent作为工具调用 | 上下文隔离、并行化 |
| **Handoffs** | Agent间通过工具调用转移控制权 | 状态保持、直接交互 |
| **Skills** | 单Agent按需加载专业知识 | 简单、上下文共享 |
| **Router** | 路由层分类输入分发到专业Agent | 清晰职责、并行 |

### 模式选择

| 需求 | 推荐模式 |
|------|----------|
| 需要并行处理 | Subagents / Router |
| 需要状态传递 | Handoffs / Skills |
| 需要分布式开发 | Subagents / Skills |
| 需要直接与用户交互 | Handoffs / Skills |

### Subagents 示例

```python
from langchain.agents import create_agent

# 创建专业子Agent
research_agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search_web, read_paper],
    name="researcher",
    system_prompt="你是研究员，负责搜索和整理信息",
)

writing_agent = create_agent(
    model="openai:gpt-5.4",
    tools=[write_file],
    name="writer",
    system_prompt="你是写作者，负责将研究结果组织成文章",
)

# 主Agent协调子Agent
from langgraph.graph import StateGraph, START, END

graph = StateGraph(AgentState)
graph.add_node("researcher", research_agent)
graph.add_node("writer", writing_agent)
graph.add_edge(START, "researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", END)
app = graph.compile()
```

## 2.4 RAG（检索增强生成）

RAG 让 Agent 能够访问外部知识库。

### RAG 架构

```
文档 → 分割 → 向量化 → 存储 → 检索 → 增强Prompt → LLM → 回答
```

### 代码实现

```python
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 1. 加载文档
loader = TextLoader("knowledge_base.txt")
docs = loader.load()

# 2. 分割文档
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 3. 向量化并存储
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. 创建检索工具
@tool
def search_knowledge_base(query: str) -> str:
    """搜索知识库获取相关信息"""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in docs])

# 5. 创建 RAG Agent
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search_knowledge_base],
    system_prompt="""你是知识库问答助手。
    
## 规则
- 始终先使用 search_knowledge_base 搜索
- 基于搜索结果回答
- 如果搜索结果不足，说明信息不足
""",
)
```

## 2.5 MCP 协议集成

MCP (Model Context Protocol) 是连接 Agent 与外部系统的标准协议。

```python
from deepagents import create_deep_agent

# MCP 工具可以来自任何 MCP 服务器
agent = create_deep_agent(
    model="openai:gpt-5.4",
    tools=[
        # 数据库 MCP 工具
        # 文件系统 MCP 工具
        # API MCP 工具
    ],
)
```

---

# 第三部分：开发流程

## 3.1 环境搭建

```bash
# 创建项目
mkdir my-agent && cd my-agent
python -m venv .venv && source .venv/bin/activate

# 安装核心包
pip install -U langchain "langchain[openai]" deepagents

# 可选：持久化支持
pip install langgraph-checkpoint-postgres

# 设置环境变量
export OPENAI_API_KEY="***"
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="your-langsmith-key"
```

## 3.2 第一个Agent

```python
from langchain.agents import create_agent
from langchain.tools import tool

# 定义工具
@tool
def search(query: str) -> str:
    """搜索网络获取信息"""
    # 实际实现：调用搜索API
    return f"关于'{query}'的搜索结果..."

# 创建Agent
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search],
    system_prompt="你是一个有帮助的助手，使用工具回答问题。",
)

# 运行
result = agent.invoke({
    "messages": [{"role": "user", "content": "今天的新闻有哪些？"}]
})
print(result["messages"][-1].text)
```

## 3.3 添加记忆

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search],
    system_prompt="你是一个有帮助的助手。",
    checkpointer=InMemorySaver(),  # 短期记忆
    store=InMemoryStore(),          # 长期记忆
)

# 使用 thread_id 保持对话
config = {"configurable": {"thread_id": "chat-001"}}
agent.invoke(
    {"messages": [{"role": "user", "content": "你好，我叫小明"}]},
    config=config
)
```

## 3.4 添加中间件

```python
from langchain.agents.middleware import (
    SummarizationMiddleware,
    HumanInTheLoopMiddleware,
)

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[search, send_email],
    system_prompt="你是一个研究助手。",
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(),  # 自动压缩长对话
        HumanInTheLoopMiddleware(
            interrupt_on={"send_email": True}  # 发邮件需审批
        ),
    ],
)
```

## 3.5 测试调试

```python
# 启用 LangSmith 追踪
import os
os.environ["LANGSMITH_TRACING"] = "true"

# 测试
config = {"configurable": {"thread_id": "test-001"}}
result = agent.invoke(
    {"messages": [{"role": "user", "content": "帮我研究一下量子计算"}]},
    config=config
)

# 在 LangSmith UI 查看：
# - 每一步的模型调用
# - 工具调用详情
# - Token 使用情况
# - 延迟和错误
```

## 3.6 生产部署

```python
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

DB_URI = "postgresql://user:pass@host:5432/agent_db"

# 初始化数据库
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()

# 创建生产级Agent
agent = create_agent(
    model="openai:gpt-5.4",
    tools=[...],
    system_prompt="...",
    checkpointer=checkpointer,
    store=store,
    middleware=[
        SummarizationMiddleware(),
        ModelCallLimitMiddleware(max_calls=50),
    ],
)

# 部署到 LangSmith
# 参考: https://docs.langchain.com/langsmith/deployment
```

---

# 第四部分：实战代码Demo

## Demo 1: 基础对话Agent

```python
"""
基础对话Agent - 支持多轮对话和记忆
"""
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

def main():
    agent = create_agent(
        model="openai:gpt-5.4",
        tools=[],
        system_prompt="你是一个友好的聊天伙伴。用中文回复。",
        checkpointer=InMemorySaver(),
    )
    
    config = {"configurable": {"thread_id": "demo-1"}}
    
    print("💬 开始对话（输入 'quit' 退出）")
    while True:
        user_input = input("你: ")
        if user_input.lower() == "quit":
            break
        
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config
        )
        print(f"助手: {result['messages'][-1].text}\n")

if __name__ == "__main__":
    main()
```

## Demo 2: RAG知识库问答

```python
"""
RAG知识库问答 - 基于本地文档的智能问答
"""
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langgraph.checkpoint.memory import InMemorySaver

# 加载和索引文档
def build_knowledge_base(docs_dir: str = "./docs"):
    loader = DirectoryLoader(docs_dir, glob="**/*.txt")
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)
    
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(chunks, embeddings)

def main():
    # 构建知识库
    print("📚 正在构建知识库...")
    vectorstore = build_knowledge_base()
    
    # 创建检索工具
    @tool
    def search_docs(query: str) -> str:
        """在知识库中搜索相关信息"""
        docs = vectorstore.similarity_search(query, k=5)
        if not docs:
            return "未找到相关信息"
        return "\n\n---\n\n".join([
            f"【来源: {doc.metadata.get('source', 'unknown')}】\n{doc.page_content}"
            for doc in docs
        ])
    
    # 创建Agent
    agent = create_agent(
        model="openai:gpt-5.4",
        tools=[search_docs],
        system_prompt="""你是知识库问答助手。

## 工作流程
1. 理解用户问题
2. 使用 search_docs 搜索相关知识
3. 基于搜索结果组织回答
4. 引用信息来源

## 规则
- 始终基于文档内容回答
- 如果文档中没有相关信息，明确告知用户
- 保持回答简洁准确
""",
        checkpointer=InMemorySaver(),
    )
    
    config = {"configurable": {"thread_id": "rag-demo"}}
    
    print("🤖 知识库问答就绪（输入 'quit' 退出）")
    while True:
        question = input("\n问题: ")
        if question.lower() == "quit":
            break
        
        result = agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config=config
        )
        print(f"\n回答: {result['messages'][-1].text}")

if __name__ == "__main__":
    main()
```

## Demo 3: 工具调用Agent

```python
"""
工具调用Agent - 多工具协作
"""
import json
import requests
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

@tool
def get_weather(city: str) -> str:
    """获取城市天气信息"""
    # 模拟天气API
    weather_data = {
        "北京": {"temp": 25, "condition": "晴", "humidity": 40},
        "上海": {"temp": 28, "condition": "多云", "humidity": 65},
        "深圳": {"temp": 30, "condition": "阵雨", "humidity": 80},
    }
    data = weather_data.get(city)
    if data:
        return f"{city}天气: {data['condition']}, {data['temp']}°C, 湿度{data['humidity']}%"
    return f"暂无{city}的天气数据"

@tool
def translate(text: str, target_lang: str = "english") -> str:
    """翻译文本到目标语言"""
    # 模拟翻译
    translations = {
        ("你好", "english"): "Hello",
        ("谢谢", "english"): "Thank you",
        ("Hello", "chinese"): "你好",
    }
    return translations.get((text, target_lang), f"[翻译结果]: {text} -> {target_lang}")

@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"

@tool
def search_web(query: str) -> str:
    """搜索网络信息"""
    # 模拟搜索结果
    return f"关于'{query}'的搜索结果:\n1. 相关文章...\n2. 新闻报道...\n3. 学术资料..."

def main():
    agent = create_agent(
        model="openai:gpt-5.4",
        tools=[get_weather, translate, calculate, search_web],
        system_prompt="""你是一个多功能助手，可以使用以下工具：
- get_weather: 查询天气
- translate: 翻译文本
- calculate: 数学计算
- search_web: 网络搜索

根据用户需求选择合适的工具，可以组合使用多个工具。""",
        checkpointer=InMemorySaver(),
    )
    
    config = {"configurable": {"thread_id": "tools-demo"}}
    
    test_queries = [
        "北京今天天气怎么样？",
        "把'你好世界'翻译成英文",
        "计算 (123 + 456) * 789",
        "搜索 LangChain 最新版本",
    ]
    
    for query in test_queries:
        print(f"\n👤 用户: {query}")
        result = agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=config
        )
        print(f"🤖 助手: {result['messages'][-1].text}")

if __name__ == "__main__":
    main()
```

## Demo 4: 多Agent协作

```python
"""
多Agent协作 - 研究+写作工作流
"""
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain.messages import HumanMessage

# 共享状态
class ResearchState(TypedDict):
    messages: list
    research_notes: str
    draft: str

# 研究Agent的工具
@tool
def search_papers(topic: str) -> str:
    """搜索学术论文"""
    return f"找到关于'{topic}'的论文:\n1. 'Deep Learning Advances' (2024)\n2. 'Transformer Architecture' (2023)"

@tool
def search_news(topic: str) -> str:
    """搜索最新新闻"""
    return f"相关新闻:\n- 'AI突破: 新模型发布' (今天)\n- '行业趋势报告' (昨天)"

# 写作Agent的工具
@tool
def outline_structure(topic: str) -> str:
    """生成文章大纲"""
    return f"""文章大纲 - {topic}:
1. 引言
2. 背景介绍
3. 核心内容
4. 分析与讨论
5. 结论"""

@tool
def save_draft(content: str) -> str:
    """保存草稿"""
    return f"草稿已保存，共 {len(content)} 字"

def main():
    # 研究员Agent
    researcher = create_agent(
        model="openai:gpt-5.4",
        tools=[search_papers, search_news],
        system_prompt="""你是研究员。
任务：收集用户指定主题的最新信息。
要求：全面、准确、有引用来源。""",
        name="researcher",
    )
    
    # 写作者Agent
    writer = create_agent(
        model="openai:gpt-5.4",
        tools=[outline_structure, save_draft],
        system_prompt="""你是专业写作者。
任务：基于研究结果撰写高质量文章。
要求：结构清晰、语言流畅、有深度。""",
        name="writer",
    )
    
    # 编辑Agent
    editor = create_agent(
        model="openai:gpt-5.4",
        tools=[],
        system_prompt="""你是资深编辑。
任务：审阅和润色文章。
要求：检查逻辑、优化表达、确保质量。
输出最终的修改建议或直接输出定稿。""",
        name="editor",
    )
    
    # 构建工作流
    def research_node(state: ResearchState):
        result = researcher.invoke({"messages": state["messages"]})
        return {
            "messages": state["messages"],
            "research_notes": result["messages"][-1].text,
            "draft": state.get("draft", ""),
        }
    
    def write_node(state: ResearchState):
        prompt = f"基于以下研究结果撰写文章:\n\n{state['research_notes']}"
        result = writer.invoke({
            "messages": [{"role": "user", "content": prompt}]
        })
        return {
            "messages": state["messages"],
            "research_notes": state["research_notes"],
            "draft": result["messages"][-1].text,
        }
    
    def edit_node(state: ResearchState):
        prompt = f"请审阅并润色以下文章:\n\n{state['draft']}"
        result = editor.invoke({
            "messages": [{"role": "user", "content": prompt}]
        })
        return {
            "messages": state["messages"],
            "research_notes": state["research_notes"],
            "draft": result["messages"][-1].text,
        }
    
    # 组装工作流
    graph = StateGraph(ResearchState)
    graph.add_node("research", research_node)
    graph.add_node("write", write_node)
    graph.add_node("edit", edit_node)
    
    graph.add_edge(START, "research")
    graph.add_edge("research", "write")
    graph.add_edge("write", "edit")
    graph.add_edge("edit", END)
    
    workflow = graph.compile()
    
    # 运行
    topic = "2024年人工智能发展趋势"
    result = workflow.invoke({
        "messages": [HumanMessage(f"请写一篇关于{topic}的文章")],
        "research_notes": "",
        "draft": "",
    })
    
    print(f"📝 最终文章:\n\n{result['draft']}")

if __name__ == "__main__":
    main()
```

## Demo 5: Deep Agent完整示例

```python
"""
Deep Agent - 完整的编码助手
"""
from deepagents import create_deep_agent
from langchain.tools import tool

@tool
def run_python(code: str) -> str:
    """执行Python代码"""
    try:
        # 注意：生产环境需要沙箱执行
        exec_globals = {}
        exec(code, exec_globals)
        return str(exec_globals.get('result', '执行成功'))
    except Exception as e:
        return f"错误: {e}"

@tool
def read_file(path: str) -> str:
    """读取文件内容"""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"读取错误: {e}"

@tool
def write_file(path: str, content: str) -> str:
    """写入文件"""
    try:
        with open(path, 'w') as f:
            f.write(content)
        return f"已写入 {path}"
    except Exception as e:
        return f"写入错误: {e}"

def main():
    agent = create_deep_agent(
        model="openai:gpt-5.4",
        tools=[run_python, read_file, write_file],
        system_prompt="""你是一个高级编程助手。

## 能力
- 编写和运行Python代码
- 读写文件
- 分析问题和设计解决方案

## 工作流程
1. 理解需求
2. 设计解决方案
3. 编写代码
4. 测试验证
5. 输出结果

## 规则
- 代码要有注释
- 先规划再执行
- 遇到问题时分析原因
""",
    )
    
    print("🚀 Deep Agent 就绪")
    print("示例任务: 写一个快速排序算法并测试")
    
    while True:
        task = input("\n任务 (输入 'quit' 退出): ")
        if task.lower() == 'quit':
            break
        
        result = agent.invoke({
            "messages": [{"role": "user", "content": task}]
        })
        
        print(f"\n📋 结果:\n{result['messages'][-1].text}")

if __name__ == "__main__":
    main()
```

---

## 附录：常用资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.langchain.com |
| Python API | https://python.langchain.com |
| API Reference | https://reference.langchain.com/python |
| LangSmith | https://smith.langchain.com |
| GitHub | https://github.com/langchain-ai |
| LangGraph 文档 | https://docs.langchain.com/oss/python/langgraph |
| Deep Agents 文档 | https://docs.langchain.com/oss/python/deepagents |

---

> 📝 本文档基于 LangChain 2026 年最新官方文档整理
> 作者：Robin 的 AI 助手
> 最后更新：2026-06-10
