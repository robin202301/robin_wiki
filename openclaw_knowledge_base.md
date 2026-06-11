# OpenClaw 知识体系

## 一、概述

OpenClaw 是一个自托管的 AI 代理网关（Gateway），将 Discord、Signal、Telegram、WhatsApp、Slack、iMessage、飞书、Matrix、微信等 20+ 消息平台连接到 AI 代理。单一 Gateway 守护进程管理所有通道、代理运行时和工具系统。

**核心特点：**
- 自托管，数据本地存储
- 35+ 模型提供者（Anthropic、OpenAI、Google、本地模型等）
- 20+ 消息通道一个网关搞定
- 可插拔的上下文引擎、记忆系统、技能系统
- 完整的移动节点支持（iOS/Android/macOS）
- 多代理路由与隔离

**官方资源：**
- 文档：https://docs.openclaw.ai
- 源码：https://github.com/openclaw/openclaw

---

## 二、系统架构

### 2.1 Gateway 架构
```
┌─────────────────────────────────────────────────────┐
│                    Gateway (daemon)                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────────┐ │
│  │ Agent   │  │ Session │  │   Channel Manager    │ │
│  │ Runtime │  │ Manager │  │ (WhatsApp/Telegram/  │ │
│  │         │  │         │  │  Discord/Slack/...)  │ │
│  └────┬────┘  └────┬────┘  └──────────┬──────────┘ │
│       │            │                   │             │
│  ┌────┴────────────┴───────────────────┴──────────┐ │
│  │          WebSocket API (port 18789)             │ │
│  └─────────────────────┬──────────────────────────┘ │
└────────────────────────┼────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │  CLI    │    │ Web UI  │    │  Nodes  │
    │ (终端)  │    │(控制面板)│    │(iOS/    │
    │         │    │         │    │Android) │
    └─────────┘    └─────────┘    └─────────┘
```

### 2.2 核心组件

| 组件 | 职责 |
|------|------|
| **Gateway** | 核心守护进程，管理所有连接、通道、代理运行时 |
| **Agent Runtime** | 嵌入式代理运行时，处理模型推理 + 工具执行 |
| **Session Manager** | 会话管理、隔离、生命周期 |
| **Channel Manager** | 消息通道连接与路由 |
| **Context Engine** | 可插拔的上下文组装与压缩 |
| **Memory System** | Markdown 文件 + 向量搜索 |
| **Tool System** | 内建工具 + 插件工具 |
| **Plugin System** | 扩展能力（通道、模型、工具、钩子） |

### 2.3 通信协议
- **传输层**：WebSocket，JSON 文本帧
- **握手**：第一帧必须是 `connect`
- **请求/响应**：`{type:"req", id, method, params}` → `{type:"res", id, ok, payload}`
- **事件推送**：`{type:"event", event, payload}`
- **认证**：共享密钥 token/password，或 Tailscale/trusted-proxy 模式

---

## 三、安装与部署

### 3.1 安装方式
```bash
# Node.js 安装
npm install -g openclaw

# Docker
docker run -d openclaw/openclaw

# macOS 应用
# 下载 .dmg 安装

# 一键引导
openclaw onboard
```

### 3.2 支持平台
| 平台 | 状态 |
|------|------|
| macOS | ✅ 完整支持（菜单栏应用） |
| Linux | ✅ 完整支持 |
| Windows | ✅ Windows Hub |
| Docker | ✅ 支持 |
| Kubernetes | ✅ 支持 |
| Raspberry Pi | ✅ 支持 |
| 云平台 | ✅ DigitalOcean / Hetzner / Oracle / Fly / Azure / GCP |

### 3.3 快速启动
```bash
# 1. 安装并引导
openclaw onboard

# 2. 启动 Gateway
openclaw gateway --port 18789

# 3. 连接消息通道
openclaw channels login

# 4. 检查状态
openclaw status
```

---

## 四、配置系统

### 4.1 配置文件
主配置：`~/.openclaw/openclaw.json`（JSON5 格式）

```json5
{
  // Gateway 配置
  gateway: {
    mode: "local",
    auth: {
      mode: "token",       // token | password | tailscale | trusted-proxy
      token: "your-secret"
    }
  },

  // 代理配置
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "anthropic/claude-sonnet-4-20250514" },
      thinkingDefault: "high",
      timeoutSeconds: 1800,
      heartbeat: { every: "30m" }
    }
  },

  // 通道配置
  channels: {
    whatsapp: { allowFrom: ["+15555550123"] },
    telegram: { botToken: "..." },
    discord: { botToken: "..." }
  },

  // 会话配置
  session: {
    scope: "per-sender",
    dmScope: "per-channel-peer",
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 10080
    }
  }
}
```

### 4.2 模型提供者

支持 35+ 模型提供者：

| 类别 | 提供者 |
|------|--------|
| 主流商业 | Anthropic, OpenAI, Google, xAI |
| 云服务商 | AWS Bedrock, Azure, Vertex AI |
| 开源/本地 | Ollama, vLLM, SGLang, LM Studio |
| 聚合平台 | OpenRouter, Together, Fireworks, DeepInfra |
| 中国模型 | 阿里 (Qwen), 百度 (千帆), Moonshot (Kimi), 小米, 字节 (Volcengine) |
| 语音 | Deepgram, ElevenLabs, Azure Speech |
| 图像/视频 | fal, Runway, PixVerse, Comfy |

### 4.3 模型引用格式
```
provider/model-name
例：anthropic/claude-sonnet-4-20250514
例：openrouter/moonshotai/kimi-k2
例：ollama/qwen3:8b
```

---

## 五、消息通道

### 5.1 内建通道
- WhatsApp（通过 Baileys）
- Telegram（通过 grammY）
- Discord
- Signal
- Slack
- iMessage
- IRC
- Google Chat
- WebChat

### 5.2 插件通道
- 飞书 (Feishu)
- Matrix
- Microsoft Teams
- Mattermost
- LINE
- QQ Bot
- Nostr
- Twitch
- Nextcloud Talk
- Synology Chat
- Zalo
- Tlon
- 微信 (WeChat)

### 5.3 通道安全
```json5
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],  // 白名单
      groups: {
        "*": { requireMention: true }  // 群聊需 @
      }
    }
  }
}
```

---

## 六、代理运行时

### 6.1 Agent Loop（代理循环）
```
消息接收 → 上下文组装 → 模型推理 → 工具执行 → 流式回复 → 持久化
    │           │           │          │          │          │
    └───────────┴───────────┴──────────┴──────────┴──────────┘
                          循环直到完成
```

### 6.2 生命周期事件
| 阶段 | 说明 |
|------|------|
| `lifecycle:start` | 代理开始执行 |
| `assistant` (stream) | 流式文本输出 |
| `tool` (stream) | 工具调用事件 |
| `compaction` | 上下文压缩 |
| `lifecycle:end` | 执行完成 |
| `lifecycle:error` | 执行出错 |

### 6.3 队列管理
| 模式 | 行为 |
|------|------|
| `steer` (默认) | 新消息插入当前运行 |
| `followup` | 等待当前运行完成后处理 |
| `collect` | 批量收集后处理 |
| `interrupt` | 中断当前运行 |

---

## 七、工作空间系统

### 7.1 目录结构
```
~/.openclaw/workspace/
├── AGENTS.md          # 操作指令（必须）
├── SOUL.md            # 人格与边界
├── TOOLS.md           # 工具使用笔记
├── IDENTITY.md        # 代理身份
├── USER.md            # 用户画像
├── MEMORY.md          # 长期记忆（可选）
├── HEARTBEAT.md       # 心跳检查清单
├── BOOTSTRAP.md       # 首次启动仪式（一次性）
├── memory/            # 日常记忆笔记
│   ├── 2026-06-10.md
│   └── 2026-06-11.md
├── skills/            # 自定义技能
│   └── my-skill/
│       └── SKILL.md
└── DREAMS.md          # Dreaming 日记（可选）
```

### 7.2 核心文件说明

**AGENTS.md** — 操作手册
- 运行规则、工作流程
- 记忆管理策略
- 群聊行为规范
- 安全红线

**SOUL.md** — 灵魂定义
- 人格特质
- 沟通风格
- 价值观
- 边界原则

**TOOLS.md** — 工具笔记
- 本地设备名称
- SSH 主机
- 摄像头位置
- TTS 偏好

**IDENTITY.md** — 身份卡
- 名字、生物类型
- 氛围、签名 emoji
- 头像

**USER.md** — 用户档案
- 称呼、时区
- 偏好、项目上下文

### 7.3 Bootstrap 文件注入
每个新会话第一轮，OpenClaw 自动将这些文件内容注入系统提示词的 Project Context 部分。空白文件跳过，大文件会被截断。

---

## 八、记忆系统

### 8.1 记忆层次

| 层级 | 文件 | 加载方式 | 用途 |
|------|------|----------|------|
| 长期记忆 | `MEMORY.md` | 每个 DM 会话自动加载 | 持久事实、偏好、决策 |
| 日常笔记 | `memory/YYYY-MM-DD.md` | 今天+昨天自动加载 | 工作日志、原始上下文 |
| 梦境日记 | `DREAMS.md` | 可选 | Dreaming 审查记录 |

### 8.2 记忆工具
- **`memory_search`** — 语义搜索（混合向量 + 关键词）
- **`memory_get`** — 精确读取记忆文件

### 8.3 记忆后端

| 后端 | 特点 |
|------|------|
| **Builtin** (默认) | SQLite，支持关键词 + 向量 + 混合搜索 |
| **QMD** | 本地 sidecar，支持重排、查询扩展 |
| **Honcho** | AI 原生跨会话记忆，用户建模 |
| **LanceDB** | LanceDB 向量库，支持本地 Ollama 嵌入 |

### 8.4 Dreaming（梦境整理）
可选的后台记忆整理系统：
1. 收集短期信号
2. 评分候选项
3. 达标后提升到长期记忆
4. 写入 `DREAMS.md` 供人工审查

```json5
{
  agents: {
    defaults: {
      dreaming: {
        enabled: true,
        schedule: "0 3 * * *"  // 每天凌晨3点
      }
    }
  }
}
```

### 8.5 Memory Wiki
将持久记忆编译为结构化知识库：
- 确定性页面结构
- 声明与证据追踪
- 矛盾和新鲜度检测
- Obsidian 兼容

### 8.6 记忆搜索配置
```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai",  // 或 gemini, voyage, mistral, ollama, bedrock
        // ...
      }
    }
  }
}
```

---

## 九、工具系统

### 9.1 内建工具分类

| 类别 | 代表工具 | 用途 |
|------|----------|------|
| **运行时** | `exec`, `process`, `code_execution` | 执行命令、管理进程 |
| **文件** | `read`, `write`, `edit`, `apply_patch` | 读写文件 |
| **Web** | `web_search`, `web_fetch` | 搜索和获取网页 |
| **浏览器** | `browser` | 浏览器自动化 |
| **消息** | `message` | 发送消息 |
| **会话** | `sessions_*`, `subagents`, `session_status` | 会话管理、委派 |
| **自动化** | `cron` | 定时任务 |
| **媒体** | `image`, `image_generate`, `video_generate`, `tts` | 媒体处理 |
| **网关** | `gateway`, `nodes` | 系统状态 |

### 9.2 工具策略
```json5
{
  tools: {
    allow: ["exec", "read", "write"],  // 白名单
    deny: ["browser"],                  // 黑名单
    exec: {
      applyPatch: true,
      approvals: {
        mode: "auto",  // auto | manual | off
      }
    },
    fs: {
      workspaceOnly: true  // 限制文件访问范围
    }
  }
}
```

### 9.3 搜索引擎支持
Brave, DuckDuckGo, Exa, Firecrawl, Gemini, Grok, Kimi, MiniMax, Ollama, Perplexity, SearXNG, Tavily

---

## 十、技能系统（Skills）

### 10.1 技能加载顺序（高→低优先）
1. 工作空间：`<workspace>/skills`
2. 项目代理技能：`<workspace>/.agents/skills`
3. 个人代理技能：`~/.agents/skills`
4. 管理/本地：`~/.openclaw/skills`
5. 内建技能（随安装附带）
6. 额外目录：`skills.load.extraDirs`

### 10.2 SKILL.md 结构
```markdown
---
name: my-skill
description: 做什么用的
version: sha256:xxx
---

# 技能指令

## 何时使用
描述触发条件

## 步骤
1. 第一步
2. 第二步
3. ...
```

### 10.3 Skill Workshop
生成的技能提案工作流：
- `create` — 创建新提案
- `revise` — 修订待审提案
- `apply` — 应用到正式技能
- `reject` — 拒绝提案
- `quarantine` — 隔离可疑提案
- `list` / `inspect` — 查看提案

---

## 十一、会话管理

### 11.1 会话路由
| 来源 | 行为 |
|------|------|
| 私聊 (DM) | 默认共享会话 |
| 群聊 | 按群隔离 |
| 房间/频道 | 按房间隔离 |
| Cron 任务 | 每次运行新会话 |
| Webhook | 按 hook 隔离 |

### 11.2 DM 隔离模式
```json5
{
  session: {
    dmScope: "per-channel-peer"
    // "main"               — 所有 DM 共享（默认）
    // "per-peer"           — 按发送者隔离
    // "per-channel-peer"   — 按通道+发送者隔离（推荐）
    // "per-account-channel-peer" — 按账号+通道+发送者
  }
}
```

### 11.3 会话生命周期
- **每日重置**：默认凌晨 4:00 新建会话
- **空闲重置**：可配置空闲超时
- **手动重置**：`/new` 或 `/reset`
- **上下文压缩**：`/compact`

### 11.4 会话存储
```
~/.openclaw/agents/<agentId>/sessions/
├── sessions.json          # 会话元数据
├── <sessionId>.jsonl      # 会话记录
└── ...
```

---

## 十二、上下文引擎

### 12.1 架构
可插拔的上下文组装系统，4 个生命周期点：

| 阶段 | 说明 |
|------|------|
| **Ingest** | 新消息入库/索引 |
| **Assemble** | 模型运行前组装上下文 |
| **Compact** | 上下文窗口满时压缩 |
| **After Turn** | 运行后持久化/后台任务 |

### 12.2 Legacy 引擎（默认）
- Ingest: 直通（Session Manager 直接持久化）
- Assemble: 直通（运行时管道处理）
- Compact: 内建摘要压缩
- After Turn: 无操作

### 12.3 插件引擎
```json5
{
  plugins: {
    slots: {
      contextEngine: "my-plugin-engine"
    }
  }
}
```

---

## 十三、自动化系统

### 13.1 Cron 定时任务
```json5
// 一次性
{ schedule: { kind: "at", at: "2026-06-12T09:00:00+08:00" } }

// 周期性
{ schedule: { kind: "every", everyMs: 3600000 } }

// Cron 表达式
{ schedule: { kind: "cron", expr: "0 9 * * 1", tz: "Asia/Shanghai" } }
```

### 13.2 Heartbeat 心跳
```json5
{
  agents: {
    defaults: {
      heartbeat: { every: "30m" }
    }
  }
}
```
- 定期检查 HEARTBEAT.md
- 执行周期性任务
- HEARTBEAT_OK 表示无事可做

### 13.3 TaskFlow
持久化多步骤任务协调：
- 状态跟踪
- 子任务委派
- 等待与恢复

### 13.4 Hooks 钩子
- `agent:bootstrap` — 引导文件构建时
- `message_received` — 消息接收时
- `message_sending` — 消息发送前
- `session_start` / `session_end` — 会话生命周期
- `gateway_start` / `gateway_stop` — 网关生命周期

---

## 十四、插件系统

### 14.1 插件能力
- 注册工具 (tools)
- 注册通道 (channels)
- 注册模型提供者 (providers)
- 注册钩子 (hooks)
- 注册技能 (skills)
- 上下文引擎 (context engine)
- 记忆后端 (memory)

### 14.2 安装
```bash
# 从 npm
openclaw plugins install @openclaw/some-plugin

# 从本地
openclaw plugins install -l ./my-plugin

# 从 git
openclaw plugins install git+https://github.com/...
```

### 14.3 配置
```json5
{
  plugins: {
    entries: {
      "some-plugin": {
        enabled: true,
        config: { ... }
      }
    },
    slots: {
      contextEngine: "legacy",
      memory: "memory-core"
    }
  }
}
```

---

## 十五、安全模型

### 15.1 层次
```
┌─────────────────────────────┐
│     Tool Policy             │  ← 工具可见性（allow/deny）
├─────────────────────────────┤
│     Sandbox                 │  ← 文件系统/进程隔离
├─────────────────────────────┤
│     Exec Approvals          │  ← 命令审批（auto/manual/off）
├─────────────────────────────┤
│     Elevated Exec           │  ← 提权执行控制
└─────────────────────────────┘
```

### 15.2 沙箱模式
- `workspaceOnly`: 文件操作限制在工作空间
- 进程隔离
- 网络隔离

### 15.3 设备配对
- 所有 WS 客户端需要设备身份
- 新设备需配对审批
- 本地回环可自动审批
- 非本地连接必须显式审批

---

## 十六、移动节点

### 16.1 iOS 节点
- 配对连接
- Canvas 渲染
- 摄像头控制
- 屏幕录制
- 位置服务
- 语音对话

### 16.2 Android 节点
- 配对连接
- 聊天界面
- 语音对话
- Canvas 渲染
- 摄像头控制
- 设备命令

### 16.3 macOS 应用
- 菜单栏常驻
- Canvas 宿主
- Peekaboo（屏幕感知）
- 语音唤醒
- 子进程管理

---

## 十七、媒体能力

### 17.1 输入
- 图片（分析/OCR）
- 音频（语音转文字）
- 视频（分析）
- 文档（PDF、Office）

### 17.2 输出
- 图像生成（fal, Comfy 等）
- 视频生成（Runway, PixVerse 等）
- 音乐生成
- TTS 语音合成（ElevenLabs, Deepgram 等）

### 17.3 媒体格式
```json
{
  "message": "这是生成的图片",
  "mediaUrl": "https://example.com/image.png"
}
```

---

## 十八、多代理系统

### 18.1 配置
```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        groupChat: {
          mentionPatterns: ["@openclaw", "assistant"]
        }
      },
      {
        id: "coder",
        model: { primary: "anthropic/claude-sonnet-4-20250514" },
        workspace: "~/.openclaw/workspaces/coder"
      }
    ]
  }
}
```

### 18.2 子代理
```
sessions_spawn → 创建隔离子会话
sessions_send  → 向另一个会话发送消息
sessions_yield → 等待子代理完成
```

### 18.3 ACP 代理
Agent Communication Protocol 支持外部代理协调。

---

## 十九、CLI 命令参考

### 19.1 核心命令
```bash
openclaw status           # 状态检查
openclaw gateway          # 启动网关
openclaw gateway restart  # 重启网关
openclaw doctor           # 诊断修复
openclaw dashboard        # 打开控制面板
```

### 19.2 通道命令
```bash
openclaw channels login   # 登录通道（QR 等）
openclaw channels list    # 列出通道
```

### 19.3 会话命令
```bash
openclaw sessions         # 列出会话
openclaw sessions cleanup # 清理旧会话
```

### 19.4 记忆命令
```bash
openclaw memory status    # 索引状态
openclaw memory search    # 搜索记忆
openclaw memory index     # 重建索引
```

### 19.5 聊天命令
```
/new              # 新建会话
/reset            # 重置会话
/compact          # 压缩上下文
/status           # 查看状态
/context list     # 列出上下文内容
/queue steer      # 切换队列模式
```

---

## 二十、运维与监控

### 20.1 健康检查
```bash
openclaw status --all     # 完整诊断
openclaw status --deep    # 深度健康探测
openclaw health --json    # JSON 健康快照
```

### 20.2 日志
- 默认路径：`/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- 级别配置：`logging.level`

### 20.3 Prometheus 指标
```json5
{
  plugins: {
    entries: {
      "diagnostics-prometheus": { enabled: true }
    }
  }
}
```

### 20.4 OpenTelemetry
```json5
{
  plugins: {
    entries: {
      "diagnostics-otel": { enabled: true }
    }
  }
}
```

---

## 二十一、关键概念速查

| 概念 | 说明 |
|------|------|
| Gateway | 核心守护进程，一切的中枢 |
| Agent Runtime | 嵌入式代理执行引擎 |
| Workspace | 代理的工作目录和记忆之家 |
| Session | 对话上下文隔离单元 |
| Channel | 消息平台连接器 |
| Context Engine | 可插拔上下文组装 |
| Memory | Markdown 文件 + 向量搜索 |
| Skills | SKILL.md 指令包 |
| Plugins | 能力扩展模块 |
| Node | 移动/桌面设备节点 |
| Heartbeat | 周期性主动检查 |
| Cron | 定时任务调度 |
| Compaction | 上下文压缩摘要 |
| Dreaming | 后台记忆整理提升 |
| Steering | 运行中新消息注入 |
| Block Streaming | 分块发送长回复 |

---

## 二十二、架构图总结

```
用户消息 → Channel → Gateway → Session → Agent Loop
                                          │
                              ┌────────────┼────────────┐
                              │            │            │
                         Context      Model API     Tool Exec
                         Assembly    (35+ 提供者)   (exec/browser/
                          │            │          web/files/...)
                          │            │            │
                     Memory +      Streaming     Results →
                     History       Reply →        Reply
                                    Channel → 用户
```

---

*最后更新：2026-06-11*
