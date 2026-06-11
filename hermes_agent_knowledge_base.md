# Hermes Agent 知识体系

## 一、概述

Hermes 是一个自托管（self-hosted）的 AI 个人助手代理平台。它允许用户在自有设备上运行 AI 代理，连接多种消息渠道，执行工具调用，并拥有持久化记忆系统。Hermes 是 OpenClaw 的前身/同类产品，OpenClaw 提供了从 Hermes 迁移的完整路径。

---

## 二、核心架构

### 2.1 整体设计
- **自托管 Gateway**：单一守护进程管理所有消息通道和代理运行时
- **配置文件**：`config.yaml` 作为核心配置
- **工作空间**：独立目录存放代理的指令、记忆和技能
- **本地优先**：数据存储在本地，用户完全掌控

### 2.2 目录结构
```
~/.hermes/
├── config.yaml          # 核心配置（模型、提供者、MCP 等）
├── auth.json            # OAuth 凭证
├── .env                 # 环境变量（API keys 等）
├── SOUL.md              # 代理人格定义
├── AGENTS.md            # 操作指令
├── memories/
│   ├── MEMORY.md        # 长期记忆
│   └── USER.md          # 用户画像
├── skills/              # 技能包
│   └── <name>/
│       └── SKILL.md
├── plugins/             # 插件
├── sessions/            # 会话记录
├── logs/                # 日志
├── cron/                # 定时任务
├── mcp-tokens/          # MCP token 存储
└── state.db             # 状态数据库
```

---

## 三、配置系统

### 3.1 模型配置（config.yaml）
```yaml
# 默认模型选择
model: "anthropic/claude-3-opus"

# 模型提供者
providers:
  - name: "openai"
    apiKey: "${OPENAI_API_KEY}"
  - name: "anthropic"
    apiKey: "${ANTHROPIC_API_KEY}"

# 自定义 OpenAI 兼容端点
custom_providers:
  - name: "local-llm"
    baseUrl: "http://localhost:8080/v1"
    apiKey: "not-needed"
```

### 3.2 MCP 服务器
```yaml
mcp_servers:
  - name: "filesystem"
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem"]
  # 或
mcp:
  servers:
    - name: "..."
```

### 3.3 认证系统
- `auth.json`：存储 OAuth 令牌（如 OpenAI OAuth）
- `.env`：支持的环境变量 key（API keys）
- 凭证为遗留状态，迁移时需手动重新认证

---

## 四、工作空间文件

### 4.1 SOUL.md — 人格与边界
定义代理的：
- 核心性格特质
- 沟通风格与语气
- 行为边界
- 价值观和原则

### 4.2 AGENTS.md — 操作指令
包含：
- 运行规则和工作流程
- 工具使用指南
- 记忆管理策略
- 群聊行为规范
- 安全红线

### 4.3 memories/MEMORY.md — 长期记忆
- 持久化的事实、偏好、决策
- 跨会话保持的重要上下文
- 从日常笔记中提炼的精华

### 4.4 memories/USER.md — 用户画像
- 用户基本信息
- 偏好和习惯
- 项目上下文

---

## 五、技能系统（Skills）

### 5.1 结构
```
skills/
└── <skill-name>/
    ├── SKILL.md          # 技能指令文档
    ├── examples/         # 示例文件
    ├── scripts/          # 辅助脚本
    └── templates/        # 模板文件
```

### 5.2 技能配置
```yaml
# config.yaml
skills:
  config:
    <skill-name>:
      key: value
```

### 5.3 技能加载
- 从 `skills/<name>/SKILL.md` 加载
- 按需注入代理提示词
- 支持配置门控（条件启用）

---

## 六、记忆系统

### 6.1 记忆层次
| 层级 | 文件 | 用途 |
|------|------|------|
| 长期记忆 | `memories/MEMORY.md` | 持久事实、偏好、决策 |
| 用户画像 | `memories/USER.md` | 用户相关信息 |
| 日常笔记 | 日期格式文件 | 每日工作记录 |

### 6.2 记忆管理
- 代理自主读写记忆文件
- 日常笔记定期提炼到长期记忆
- 过时信息需要主动清理

---

## 七、MCP 集成

### 7.1 Model Context Protocol
Hermes 支持 MCP 服务器，允许代理使用外部工具：
- 文件系统操作
- 数据库查询
- API 调用
- 自定义工具服务

### 7.2 配置方式
```yaml
mcp_servers:
  - name: "server-name"
    command: "..."
    args: ["..."]
    env:
      KEY: "value"
```

---

## 八、会话管理

### 8.1 会话存储
- 会话记录存储在 `sessions/` 目录
- 每个会话包含完整对话历史
- 支持会话重置和新建

### 8.2 会话隔离
- DM 对话共享会话
- 群组对话独立隔离
- 定时任务使用独立会话

---

## 九、自动化

### 9.1 定时任务（Cron）
- 存储在 `cron/` 目录
- 支持周期性任务执行
- 独立的会话上下文

### 9.2 插件系统
- 插件位于 `plugins/` 目录
- 扩展代理能力
- 支持自定义工具和服务

---

## 十、迁移到 OpenClaw

### 10.1 迁移工具
```bash
# 预览迁移计划
openclaw migrate hermes --dry-run

# 执行迁移
openclaw migrate apply hermes --yes

# 或通过引导向导
openclaw onboard --flow import
```

### 10.2 迁移内容
| 项目 | 迁移方式 |
|------|----------|
| 模型配置 | 自动导入 |
| MCP 服务器 | 自动导入 |
| SOUL.md / AGENTS.md | 复制到工作空间 |
| MEMORY.md / USER.md | 追加到 OpenClaw 文件 |
| 技能 | 复制技能目录和配置 |
| auth.json | 需手动重新认证 |
| .env keys | 选择性导入 |

### 10.3 保留为归档（不自动导入）
- `plugins/`
- `sessions/`
- `logs/`
- `cron/`
- `mcp-tokens/`
- `state.db`

---

## 十一、与 OpenClaw 对比

| 特性 | Hermes | OpenClaw |
|------|--------|----------|
| 配置格式 | config.yaml | openclaw.json |
| 记忆路径 | memories/ | workspace root |
| 消息通道 | 有限 | 20+ 通道 |
| 模型提供者 | 多个 | 35+ |
| 上下文引擎 | 内置 | 可插拔 |
| 记忆搜索 | 基础 | 混合搜索 |
| Dreaming | 无 | 支持 |
| 多代理 | 基础 | 完整路由 |
| 移动节点 | 无 | iOS/Android |
| 技能工坊 | 无 | Skill Workshop |

---

## 十二、关键概念总结

1. **自托管优先**：所有数据在本地，用户完全控制
2. **Markdown 驱动**：人格、指令、记忆都是 Markdown 文件
3. **技能扩展**：通过 SKILL.md 教代理新工作流
4. **MCP 集成**：标准化外部工具协议
5. **迁移友好**：可向 OpenClaw 平滑迁移

---

*最后更新：2026-06-11*
