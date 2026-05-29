# CodeAct：让 LLM 用代码作为行动的 Agent 范式

## 1. 背景与原理

### 1.1 什么是 CodeAct？

CodeAct 是一种 Agent 范式，其核心思想是：**让 LLM 用编写和执行代码的方式来完成动作（Action），而不是通过结构化的函数调用（Function Calling/Tool Use）**。

在传统的 Tool-Use Agent 中，LLM 的每一步行动都需要选择一个工具并填写结构化的参数（通常是 JSON），由 Agent 框架负责调用工具并返回结果。而在 CodeAct 中，LLM 生成一段 Python 代码，代码中包含对工具的调用，整个代码块被送入一个沙箱执行，执行结果反馈给 LLM 作为下一步的输入。

### 1.2 核心区别

| 维度 | Tool-Use Agent | CodeAct Agent |
|------|---------------|---------------|
| 动作表示 | 结构化 JSON（工具名 + 参数） | 可执行代码 |
| 每步动作数 | 1 次 API 调用 | 可包含多次调用 + 控制流 |
| 中间结果处理 | 由框架管理，LLM 只看到返回值 | LLM 可在代码中用变量传递 |
| 灵活性 | 受限于预定义 schema | 可组合任意逻辑 |
| 错误处理 | 框架捕获异常，返回错误消息 | 代码中 try/catch，更灵活 |
| 执行环境 | 无/有限 | 完整 Python 沙箱 |

### 1.3 为什么 CodeAct 有吸引力？

1. **组合能力**：一次代码执行可以串联多个 API 调用，用 Python 变量传递中间结果，无需 LLM 记忆和回传
2. **控制流**：循环、条件判断等逻辑可以直接写在代码中，减少 LLM 的多轮交互次数
3. **数据处理**：可以直接在代码中对 API 返回值进行过滤、排序、计算等操作
4. **表达力**：代码是 LLM 最自然的输出格式之一，尤其对于代码能力强的模型
5. **确定性**：代码执行确定性（deterministic）的——同样的代码、同样的输入，执行结果完全一致。这意味着 LLM 生成代码后，执行结果不受运行时随机因素影响，可复现、可调试。相比之下，Function Calling 模式中 LLM 每一步都需要重新决策，每步的随机性会累积，同一任务多次运行可能走完全不同的路径

## 2. 实现方式

### 2.1 架构概览

核心对比：**ReAct** 每次 LLM 只发出一个工具调用，每个动作之间都要回传给模型。**CodeAct** 让 LLM 生成一段程序，多个工具调用在一次代码执行中完成，之后才再次调用模型。

**ReAct** —— 每轮一个工具调用，无沙箱：

```mermaid
flowchart TB
    Ru((User))
    subgraph Rh["HOST PROCESS"]
        direction TB
        Rl["Agent Loop<br/>(LLM driver)"]
        Rr["Tool Router"]
        Rl <-->|"tool_call ↕ result"| Rr
    end
    subgraph Rt["TOOLS"]
        direction LR
        Rloc["Host-local function"]
        Rmcp["MCP server"]
    end
    Ru -->|"task"| Rl
    Rr --> Rloc
    Rr --> Rmcp
    Rl -->|"final answer"| Ru
```

**CodeAct** —— 代码即动作，沙箱执行 + 回调宿主：

```mermaid
flowchart TB
    Cu((User))
    subgraph Ch["HOST PROCESS"]
        direction TB
        Cl["Agent Loop<br/>(LLM driver)"]
        Cr["Tool Router / ToolServer<br/>owns: credentials, sessions,<br/>connection pools"]
    end
    subgraph Cs["CODE EXECUTION SANDBOX<br/>Docker (IPython)"]
        direction TB
        Cc["LLM-authored code"]
        Cstub["call_tool() proxy<br/>(HTTP stub)"]
        Cc -.->|"calls"| Cstub
    end
    subgraph Ct["TOOLS"]
        direction LR
        Cloc["Host-local function"]
        Cmcp["MCP server"]
    end
    Cu -->|"task"| Cl
    Cl <==>|"code ↕ result"| Cc
    Cstub <==>|"HTTP JSON-RPC"| Cr
    Cr --> Cloc
    Cr --> Cmcp
    Cl -->|"final answer"| Cu
```

两者的关键差异：

| | ReAct | CodeAct |
|---|---|---|
| 动作单元 | 一次工具调用 | 一段代码 |
| N 次工具调用的 LLM 交互次数 | **N**（每次调用都要回传模型） | **1**（所有调用在一次执行中完成） |
| 是否需要沙箱 | 否 | 是 |
| Agent Loop ↔ Tool Router 关系 | Loop 逐个发出工具调用 | Router 处理来自沙箱的工具调用请求 |
| 凭证/会话存储位置 | Router（宿主） | Router（宿主）—— 相同 |
| 跨调用组合能力（循环、条件） | LLM 必须逐步规划和发出 | 沙箱内原生 Python 支持 |


### 2.2 以 Demo 为例理解架构

为了帮助用户理解的架构，我们用 AgentScope CodeAct demo 中的"北京三亚温差"任务来具体说明。demo 中注册了 `get_weather` 和 `get_news` 两个宿主端工具，以及 `run_python_code` 沙箱执行工具。

**实际部署架构**：

```
┌─────────────────────────────────────────────────────── Host ────────────────────────────────────────┐
│                                                                                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  ReActAgent                                                                                   │  │
│  │  ┌──────────────┐  ┌──────────────────────────────────────────────────────────────────────┐   │  │
│  │  │ LLM (qwen)   │  │ Toolkit                                                              │   │  │
│  │  │              │  │  ├─ run_python_code  (from CodeAct Sandbox)                          │   │  │
│  │  │  sys_prompt: │  │  ├─ get_weather      (direct, host-side)                             │   │  │
│  │  │  CODEACT_    │  │  └─ get_news         (direct, host-side)                             │   │  │
│  │  │  SYSTEM_     │  │                                                                      │   │  │
│  │  │  PROMPT      │  │                                                                      │   │  │
│  │  └──────────────┘  └──────────────────────────────────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────────────────────────────────┘  │
│          │                                    │                      │                              │
│          │  UserAgent ←→ ReActAgent loop      │                      │  Direct tool calls           │
│          │                                    │                      │  (no sandbox)                │
│          │                                    ▼                      ▼                              │
│  ┌───────────────────┐         ┌─────────────────────────────────────────────────────────────────┐  │
│  │   UserAgent       │         │  ToolServer (FastAPI + Uvicorn)                                 │  │
│  │                   │         │  ┌──────────────────────────────────────────────────────────┐   │  │
│  └───────────────────┘         │  │  POST /call/{tool_name}                                  │   │  │
│                                │  │  └─ get_weather(**kwargs)  →  ToolResponse               │   │  │
│                                │  └──────────────────────────────────────────────────────────┘   │  │
│                                └───────────────────────┬─────────────────────────────────────────┘  │
│                                                        │  HTTP (Docker bridge IP)                   │
│                                                        │                                            │
└────────────────────────────────────────────────────────┼────────────────────────────────────────────┘
                                                         │
                          ┌──────────────────────────────┼───────────────────────────────────┐
                          │  Docker Sandbox              │                                   │
                          │                              ▼                                   │
                          │  ┌────────────────────────────────────────────────────────────┐  │
                          │  │  IPython Environment                                       │  │
                          │  │                                                            │  │
                          │  │  Pre-injected: call_tool(name, **kwargs)                   │  │
                          │  │    │                                                       │  │
                          │  │    │  HTTP POST → http://{host_ip}:{port}/call/{tool_name} │  │
                          │  │    └───────────────────────────────────────────────────────┼──┼──► ToolServer
                          │  │                                                            │  │
                          │  │  User code:                                                │  │
                          │  │    result = call_tool('get_weather', city='Beijing')       │  │
                          │  │    print(result['temperature_c'])                          │  │
                          │  │                                                            │  │
                          │  └────────────────────────────────────────────────────────────┘  │
                          └──────────────────────────────────────────────────────────────────┘
```

注意上图中的**双通道设计**：Toolkit 中既注册了 `run_python_code`（走沙箱执行），也注册了 `get_weather`、`get_news` 等宿主端工具（Agent 可直接调用，无需经过沙箱）。只有通过 `call_tool()` 在沙箱内调用的工具才经过 ToolServer 的 HTTP 链路。

**请求流程**：

1. **ReActAgent** 决定是直接调用宿主端工具，还是通过 `run_python_code` 执行代码
2. **直接调用**：Agent 通过 Toolkit 直接调用宿主端函数，无需沙箱
3. **代码执行**：Agent 调用 `run_python_code(code)` → `CodeActEnv.run_python_code()` → `sandbox.run_ipython_cell(code)`
4. 沙箱内代码使用 `call_tool(name, **kwargs)` 发送 HTTP 请求到宿主端 ToolServer
5. **ToolServer** 将调用分发到注册的函数并返回结果

**组件角色对照**：

| 组件 | 职责 | 我们的实现 |
|---|---|---|
| **Agent Loop** | 运行 LLM，决定何时执行代码 vs 返回结果 | AgentScope `ReActAgent` |
| **Tool Router** | 将工具名解析为具体运行时；持有密钥和会话句柄 | `ToolServer`（FastAPI HTTP） |
| **Sandbox** | 在隔离环境中执行 LLM 编写的代码；暴露工具代理 | Docker + IPython（`BaseSandboxAsync`） |
| **Tool Stubs** | 沙箱内的语言原生包装函数，通过 RPC 回调宿主 | `call_tool()`（HTTP proxy） |
| **Tools** | 执行实际工作；运行在物理上合理的位置 | Host-local function   |

**调用序列**：

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant AL as Agent Loop<br/>(ReActAgent)
    participant R as Tool Router<br/>(ToolServer)
    participant S as Sandbox<br/>(Docker/IPython)

    U->>AL: "beijing sanya temperature diff"
    AL->>AL: prompt LLM, 收到代码块

    AL->>R: run_python_code(code)
    R->>S: sandbox.run_ipython_cell(code)

    Note over S: beijing = call_tool("get_weather",<br/>city="Beijing")

    S->>R: HTTP POST /call/get_weather
    Note over R: get_weather(city="Beijing")<br/>→ ToolResponse
    R-->>S: {"temperature_c": 32, ...}

    Note over S: sanya = call_tool("get_weather",<br/>city="Sanya")

    S->>R: HTTP POST /call/get_weather
    Note over R: get_weather(city="Sanya")<br/>→ ToolResponse
    R-->>S: {"temperature_c": 36, ...}

    Note over S: diff = abs(beijing["temperature_c"]<br/>- sanya["temperature_c"])<br/>print(f"温差 {diff}°C")

    S-->>R: stdout + stderr
    R-->>AL: ToolResponse
    AL-->>U: "The temperature difference is 4°C."
```

关键观察：**步骤 4-9 中的两次 `get_weather` 调用都在一次代码执行内完成**，LLM 不需要在中间被再次调用。如果用 ReAct，LLM 需要先调 `get_weather(city="Beijing")`，拿到结果后再调 `get_weather(city="Sanya")`，最后再计算——至少 3 轮 LLM 交互，而 CodeAct 只需 1 轮。

**实际对话记录**：

**User**: beijing sanya temperature diff

**Friday** (Agent) 选择调用 `run_python_code`，生成代码：

```json
{
    "type": "tool_use",
    "name": "run_python_code",
    "input": {
        "code": "beijing_weather = call_tool('get_weather', city='Beijing')\nsanya_weather = call_tool('get_weather', city='Sanya')\ntemperature_diff = abs(beijing_weather['temperature_c'] - sanya_weather['temperature_c'])\nprint(f\"The temperature difference between Beijing and Sanya is {temperature_diff}°C.\")"
    }
}
```

**执行结果**（ToolResponse）：

```json
{
    "type": "tool_result",
    "name": "run_python_code",
    "output": [
        {
            "type": "text",
            "text": "The temperature difference between Beijing and Sanya is 4°C.\n"
        }
    ]
}
```

**Friday**: The temperature difference between Beijing and Sanya is 4°C.

### 2.3 核心实现

#### CodeActEnv 管理

`CodeActEnv` 是整个系统的核心，管理沙箱生命周期和工具代理注入：

```python
class CodeActEnv:
    """Manages a sandbox + host tool server."""
    ...

    def register_callable_tool(self, func, output_model=None):
        """Register a tool that can be called from the sandbox."""
        ...

    async def start(self):
        """Start ToolServer + Sandbox + inject call_tool proxy."""
        self.tool_server.start()
        self.sandbox = BaseSandboxAsync()
        await self.sandbox.__aenter__()
        # 注入 call_tool 到沙箱
        call_tool_code = _generate_call_tool_code(host_tool_url)
        await self.sandbox.run_ipython_cell(code=call_tool_code)
```

#### 沙箱侧 `call_tool` 代理函数

注入到沙箱中的 `call_tool` 是 LLM 在代码中调用工具的唯一入口：

```python
def call_tool(tool_name, **kwargs):
    """Call a tool on the host tool server by name."""
    import requests as _req
    _resp = _req.post(
        f"http://{HOST_IP}:{PORT}/call/" + tool_name,
        json={"arguments": kwargs},
        timeout=30,
    )
    _resp.raise_for_status()
    _data = _resp.json()
    if 'isError' in _data and _data['isError']:
        print(f'<tool_call_error>{tool_name}({kwargs}): {_data}</tool_call_error>')
        if 'exception' in _data:
            raise RuntimeError(_data['exception'])
    if 'metadata' in _data and 'isError' not in _data:
        print(f'<tool_call_result>{tool_name}({kwargs}): {_data["metadata"]}</tool_call_result>')
        return _data['metadata']

    return _data
```

#### `run_python_code` 的工具描述

CodeAct 的关键在于：LLM 通过 `run_python_code` 这一个工具的描述来了解所有可用工具。工具描述中内嵌了完整的工具列表、输入输出 schema（参考[hyperlight](https://github.com/microsoft/agent-framework/tree/51ad460d5fcedba289d8cf0d41952de09c30eec2/python/packages/hyperlight/agent_framework_hyperlight)）。

**关键点**：LLM 必须知道每个工具的返回结构，才能在代码中正确解析和使用返回值。例如，`get_weather` 返回 `{'temperature_c': ..., 'condition': ...}`，LLM 需要这个字段名才能在后续代码中写 `result['temperature_c']`。如果没有 output schema，LLM 只能猜测返回值的字段名，极易出错。

## 3. 在 AppWorld 中的表现

### 3.1 AppWorld 简介

AppWorld 是 ACL'24 最佳资源论文，是一个可控制的 App 世界，用于评测函数调用和交互式编码 Agent：

- **9 个日常应用**：Spotify, Venmo, Phone, Gmail, Amazon 等
- **457 个 API**：覆盖音乐、支付、通讯、购物等场景
- **~100 个人物**：有完整的数字生活数据
- **评测方式**：给定自然语言任务，Agent 需自主调用 API 完成，最终与 ground truth 对比


### 3.2 批跑综合结果

> 以下结果仅覆盖 AppWorld 中 Spotify 相关的 78 个任务（369 个测试用例），未涉及 Venmo、Phone、Gmail 等其他 App 的任务。

#### 总体对比

| 指标 | AppWorld (原始) | CodeAct (实现) | 差异 |
|------|-----------------|-----------------|------|
| 总测试数 | 369 | 369 | - |
| 失败数 | 14 | 31 | +17 |
| 通过率 | 96.2% | 91.6% | -4.6pp |
| 总步数 | 783 | 837 | +54 |
| 平均步数/任务 | 10.0 | 10.7 | +0.7 |
| 任务失败率 | 5/78 (6.4%) | 14/78 (17.9%) | +11.5pp |

#### 按 Task Group 对比

| Task Group | AppWorld 通过/总数 | 通过率 | 平均步数 | CodeAct 通过/总数 | 通过率 | 平均步数 | 通过率差异 | 步数变化 |
|------------|-------------------|--------|---------|------------------|--------|---------|-----------|----------|
| 07b42fd | 15/15 | 100% | 10.0 | 15/15 | 100% | 7.3 | +0% | -2.7 ↓ |
| 229360a | 18/18 | 100% | 9.7 | 18/18 | 100% | 12.0 | +0% | +2.3 |
| 27e1026 | 6/6 | 100% | 9.0 | 6/6 | 100% | 9.3 | +0% | +0.3 |
| 287e338 | 6/6 | 100% | 7.7 | 6/6 | 100% | 5.3 | +0% | -2.4 ↓ |
| 396c5a2 | 18/18 | 100% | 10.7 | 18/18 | 100% | 24.7 | +0% | +14.0 |
| **3ab5b8b** | 10/18 | 56% | 9.0 | 13/18 | 72% | 8.0 | **+17% ↑** | -1.0 ↓ |
| 4ec8de5 | 6/6 | 100% | 8.7 | 6/6 | 100% | 8.0 | +0% | -0.7 ↓ |
| 50e1ac9 | 6/6 | 100% | 8.3 | 6/6 | 100% | 11.7 | +0% | +3.4 |
| **57c3486** | 15/15 | 100% | 12.3 | 9/15 | 60% | 20.0 | **-40% ↓** | +7.7 |
| 6104387 | 24/30 | 80% | 15.7 | 24/30 | 80% | 13.3 | +0% | -2.4 ↓ |
| 6171bbc | 21/21 | 100% | 13.0 | 20/21 | 95% | 9.3 | -5% | -3.7 ↓ |
| 692c77d | 21/21 | 100% | 8.7 | 21/21 | 100% | 7.7 | +0% | -1.0 ↓ |
| 6bdbc26 | 6/6 | 100% | 8.3 | 6/6 | 100% | 5.0 | +0% | -3.3 ↓ |
| 82e2fac | 6/6 | 100% | 8.0 | 6/6 | 100% | 6.7 | +0% | -1.3 ↓ |
| aa8502b | 12/12 | 100% | 10.7 | 12/12 | 100% | 8.3 | +0% | -2.4 ↓ |
| **b0a8eae** | 15/15 | 100% | 19.0 | 10/15 | 67% | 21.7 | **-33% ↓** | +2.7 |
| b119b1f | 18/18 | 100% | 8.3 | 18/18 | 100% | 6.3 | +0% | -2.0 ↓ |
| b7a9ee9 | 12/12 | 100% | 8.0 | 12/12 | 100% | 8.3 | +0% | +0.3 |
| c901732 | 18/18 | 100% | 10.3 | 18/18 | 100% | 14.0 | +0% | +3.7 |
| ccb4494 | 15/15 | 100% | 9.3 | 15/15 | 100% | 7.7 | +0% | -1.6 ↓ |
| **ce359b5** | 24/24 | 100% | 12.3 | 20/24 | 83% | 11.0 | **-17% ↓** | -1.3 ↓ |
| d4e9306 | 18/18 | 100% | 8.3 | 18/18 | 100% | 7.3 | +0% | -1.0 ↓ |
| e3d6c94 | 27/27 | 100% | 9.0 | 27/27 | 100% | 9.0 | +0% | ±0 |
| e7a10f8 | 6/6 | 100% | 8.7 | 6/6 | 100% | 6.7 | +0% | -2.0 ↓ |
| **e85d92a** | 6/6 | 100% | 7.3 | 4/6 | 67% | 22.3 | **-33% ↓** | +15.0 |
| **fac291d** | 6/6 | 100% | 10.7 | 4/6 | 67% | 8.0 | **-33% ↓** | -2.7 ↓ |

#### Task Group 通过情况分类

| 分类 | 数量 |
|------|------|
| 两者都全通过 | 18 |
| 仅 AppWorld 全通过 | 6 |
| 仅 CodeAct 全通过 | 0 |
| 两者都未全通过 | 2 |

#### 关键发现

**CodeAct 通过率下降 4.6pp (96.2% → 91.6%)，主要拖累来自 6 个 Task Group：**

- **57c3486** (-40pp)：步数也大幅增加 (12.3 → 20.0)，最严重的退化
- **b0a8eae** (-33pp)：1/3 的子任务从全过变为全挂
- **e85d92a** (-33pp)：步数暴增 (7.3 → 22.3)，CodeAct 可能在循环空转
- **fac291d** (-33pp)：2/3 子任务失败
- **ce359b5** (-17pp)：4/24 测试失败
- **6171bbc** (-5pp)：仅 1 个测试失败

**唯一的亮点：3ab5b8b 提升 17pp** (56% → 72%)，这是两者都未全通过的 group。

**步数方面**

CodeAct 在失败 case 上往往步数更多（如 e85d92a 7.3→22.3、57c3486 12.3→20.0），但在成功 case 上有时步数更少（如 6bdbc26 8.3→5.0、287e338 7.7→5.3），说明 CodeAct 在简单任务上更高效，但在复杂任务上容易陷入多轮重试。

### 3.3 案例分析

#### 一个完美的结果

> **Task ID**: 82e2fac_1
>
> **Supervisor**: Joyce Weaver (joyce-weav@gmail.com)
>
> **Instruction**: What is the title of the most-liked song in my Spotify playlists.

LLM 在**一步代码执行**中完成了整个任务，共发起 **39 次 API 调用**，仅用 2 轮 LLM 交互即给出正确答案。

**Step 1** — LLM 生成一段完整代码，一次性串联所有操作：

```python
# 1. 获取 Spotify 密码
passwords = call_tool('show_account_passwords')
for entry in passwords:
    if entry['account_name'].lower() == 'spotify':
        spotify_password = entry['password']
        break

# 2. 用 supervisor 邮箱登录
response = call_tool('spotify_login', username='joyce-weav@gmail.com', password=spotify_password)
access_token = response['access_token']

# 3. 获取所有播放列表
playlists = call_tool('show_playlist_library', access_token=access_token)

# 4. 遍历每个播放列表的每首歌，追踪 like_count 最高的
for playlist in playlists:
    for song_id in playlist['song_ids']:
        song = call_tool('show_song', song_id=song_id)
        if song['like_count'] > max_like_count:
            max_like_count = song['like_count']
            most_liked_song_id = song_id

# 5. 输出答案并提交
most_liked_song = call_tool('show_song', song_id=most_liked_song_id)
call_tool('complete_task', answer=most_liked_song['title'])
```

**执行结果**：代码成功执行，`show_song` 逐一查到 song_id=78 的 "A Love That Never Was"（like_count=18）为最高，输出答案。

**Step 2** — LLM 总结：*"The title of the most-liked song in your Spotify playlists is 'A Love That Never Was'."*

**关键观察**：这正是 CodeAct 组合能力的体现——39 次 API 调用（1 次 `show_account_passwords` + 1 次 `spotify_login` + 1 次 `show_playlist_library` + 36 次 `show_song` + 1 次 `complete_task`）在一次代码执行中完成，LLM 只需被调用 2 次。如果用 ReAct 模式，至少需要 39+ 轮 LLM 交互。

#### 一个失败的结果

> **Task ID**: 82e2fac_1（同一任务，另一次运行）
>
> **Instruction**: What is the title of the most-liked song in my Spotify playlists.

同一次任务的另一次运行，LLM 在第 1 步就出错了，最终经过 **7 轮 LLM 交互**后放弃，标记任务失败。

**Step 1** — LLM 假设 `show_account_passwords()` 返回的字段中包含 `username`，写出：

```python
for account in credentials:
    if account['account_name'] == 'spotify':
        spotify_username = account['username']  # ❌ KeyError!
```

实际返回结构只有 `account_name` 和 `password`，没有 `username` 字段 → **KeyError: 'username'**。

**Step 2** — LLM 改用 `account.get('username', '')` 避免异常，但仍然没有 username → 输出 "Could not find Spotify credentials."

**Step 3** — LLM 转而调用 `show_api_doc` 查看 API 文档，确认返回结构确实没有 `username`。

**Step 4** — LLM 打印 `credentials` 观察，确认只有 `account_name` 和 `password`。

**Step 5** — LLM 尝试用 `account_name`（即 `"spotify"`）作为用户名登录 → `spotify_login(username='spotify', password='qge1k1L')` → **"Invalid credentials"**。

**Step 6** — LLM 放弃，调用 `complete_task(status='fail')`。

**Step 7** — LLM 总结失败原因。

**关键观察**：

1. **Output Schema 误读**：`show_account_passwords` 的 output schema 清楚写明只有 `account_name` 和 `password`，但 LLM 仍然假设有 `username` 字段。这说明即使提供了 output schema，LLM 也可能因为工具列表过长而忽略或混淆字段
2. **恢复路径错误**：LLM 在发现没有 `username` 后，没有联想到用 supervisor 的邮箱作为用户名（成功案例中 LLM 正确地用了 `joyce-weav@gmail.com`），而是用 `account_name` 凑数，导致认证失败
3. **偶然性**：同一任务、同一 prompt、同一工具集，仅因 LLM 对 schema 的不同理解，一次成功、一次失败。这体现了 CodeAct 模式下结果的**不稳定性**


### 3.4 CodeAct 的缺点与 Insight

#### 3.4.1 Schema 强依赖：缺少校验与 Output Schema 是致命伤

Function Calling 模式下，框架会自动校验参数名、类型、必填项，类型错误会被拦截并返回结构化错误。CodeAct 模式下，`call_tool("spotify_login", username="x", password="y")` 中的参数名、类型全靠 LLM 从文本描述中记忆，没有任何运行时校验——拼错参数名、传错类型、漏传必填参数都只会在运行时才暴露。

更关键的是 **Output Schema**：CodeAct 模式下，LLM 需要根据返回值结构来写后续代码（如 `result["access_token"]`）。如果缺少 output schema，LLM 只能猜测返回结构，极易写出错误的字段名。Function Calling 模式下即使没有 output schema，返回值也会被框架结构化地呈现给 LLM，不存在这个问题。

**实例 1**：LLM 错误假设 `show_account_passwords()` 返回的字段中包含 `username`，写出 `account['username']` → KeyError。实际返回结构只有 `account_name` 和 `password`。

**实例 2**：`spotify_login` 的 `username` 参数应为 e-mail，但 LLM 传了 `'spotify'`（account_name）→ "Invalid credentials"。

> <tool_call_error>spotify_login({'username': 'spotify', 'password': 'qge1k1L'}): {'content': [], 'metadata': {'message': 'Invalid credentials'}, 'isError': True}</tool_call_error>

**Tool 数量加剧问题**：`run_python_code` 的工具描述中需要列出所有可用的 `call_tool` 函数。当工具数量增多时（我们的实验中有 ~100 个），描述变得非常长，LLM 需要从一大段文本中准确找到目标工具，更容易混淆工具名或参数。Function Calling 模式下工具是独立注册的，LLM 只需从列表中选择，schema 是结构化约束，不存在这个问题。

#### 3.4.2 错误信息丢失：出错没有合适出口

Code box 中请求的 tool_call 如果缺少出错信息的打印，工具调用的返回值就完全丢失，LLM 无法知道调用是否成功、返回了什么：

```mermaid
flowchart LR
    subgraph SB1["CodeBox"]
        direction TB
        B1["LLM 生成代码块<br/>result = call_tool('login', …);<br/>token = result['token']"]
        B2["等待返回"]
        B2 -- "收到 {error: 'invalid credentials'}<br/>（未打印，信息丢失）" --> B3["继续执行<br/>token = result['token']<br/>❌ KeyError: 'token' not found"]
    end
    subgraph SB2[" HOST "]
        direction TB
        TC["ToolServer<br/>执行 login"] --> TR["返回<br/>{error: 'invalid credentials'}"]
    end
    B1 -- "HTTP 请求" --> TC
    TR -- "HTTP 响应" --> B2
    B3 --> B4["LLM 只看到 KeyError<br/>不知道根因是invalid credentials<br/>→ 盲猜下一步"]

    style B3 fill:#fbb,stroke:#e88,color:#000
    style B4 fill:#fbb,stroke:#e88,color:#000
```

Function Calling 模式下，工具的错误返回是结构化的（如 `{"isError": true, "message": "..."}`），LLM 容易理解；CodeAct 模式下，代码中的异常可能来自 Python 运行时、沙箱环境、HTTP 调用等多个层面，无法统一，对于api出错信息，当前使用tool_call强制进行打印。

#### 3.4.3 中间结果的两难：不可见 vs 重复打印

在 Function Calling（单步执行）模式下，每一步工具调用的结果会立刻被 LLM 消化，LLM 根据该结果决定下一步行动——反馈链路天然畅通。但在 CodeAct（多步执行）模式下，LLM 一次性生成包含多个 `call_tool` 调用的代码块，所有调用在一次执行中完成，LLM 只能看到最终的整体输出。这带来一个两难困境：

- **不 print**：中间每步 `call_tool` 的返回值仅存在于 Python 变量中，LLM 无法知晓各步的状态，相当于"盲飞"——如果中间某步返回了意外结果（如空列表、错误信息），后续代码仍会基于错误假设继续执行
- **print**：如果 LLM 在代码中对每个 `call_tool` 的结果都 `print(result)`，那么该结果会出现在 stdout 中反馈给 LLM。但 LLM 在总结时往往会再次用自己的话复述这些结果，导致同一信息在对话中出现两次——一次是代码执行的原始输出，一次是 LLM 的自然语言总结，浪费 token 且可能引入不一致

```
┌─ 单步执行（Function Calling） ─────────────────────────────┐
│                                                          │
│  LLM ──call_tool──► Tool ──result──► LLM 消化并决策下一步  │
│                         ✓ 每步结果都被 LLM 看到            │
│                                                          │
└──────────────────────────────────────────────────────────┘

┌─ 多步执行（CodeAct） ──────────────────────────────────────┐
│                                                          │
│  LLM ──code──► [step1: r1=call_tool(...)]                │
│                [step2: r2=call_tool(...)]  ──stdout──►   │
│                [step3: r3=call_tool(...)]                │
│                                                          │
│  不 print: r1, r2, r3 对 LLM 不可见 → 盲飞                 │
│  print:    r1, r2, r3 出现在 stdout，但 LLM 总结时         │
│            会再次复述 → 同一信息重复，浪费 token             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

这本质上是 CodeAct **批处理**特性的副作用：用减少 LLM 交互轮次换取效率，但代价是丧失了逐步反馈的能力。代码中的逻辑是 LLM 在执行前一次性写好的，无法根据中间结果动态调整。可以要求 LLM 每次只写小段代码（如我们的 instruction 中说"Write small chunks of code"），但这又回到了多轮交互的模式，削弱了 CodeAct 的优势。

#### 3.4.4 串联脆弱性：多步 API 调用的级联风险

AppWorld 的典型任务需要多步 API 串联：先查密码 → 登录获取 token → 用 token 查数据 → 修改数据 → 完成任务。在 CodeAct 中，这些步骤往往在一次代码执行中完成：

- 串联的**优势**：一次代码可以完成多步操作，减少 LLM 交互轮次
- 串联的**风险**：代码中任何一步失败（如 API 返回错误），后续代码都会出错或无法执行，形成级联失败
- 尤其是当中间步骤的返回值结构不确定时（如分页、空结果），LLM 很难在代码中写出健壮的错误处理

#### 3.4.5 API 过多时 CodeAct 优势严重退化

当 API 数量增多时，CodeAct 的核心优势——一次代码完成多步操作——反而成了负担。LLM 需要在一个代码块中同时记住多个 API 的名称、参数、返回结构，并在它们之间写出正确的串联逻辑。API 越多，LLM 一次写对完整代码的概率越低，出错后进入多轮修复循环，交互轮次反超 Function Calling。

```
API 数量少（< 10）           API 数量多（> 20）

CodeAct:                    CodeAct:
  Step 1: 完整代码 ✓          Step 1: 代码出错 ✗
  Step 2: LLM 总结            Step 2: 修复，又出错 ✗
  → 2 轮搞定                  Step 3: 再修复 ✗
                              ...
                              → N 轮才搞定（或放弃）

Function Calling:            Function Calling:
  每步 1 次 call              每步 1 次 call
  → 步数 = API 调用数         → 步数 = API 调用数
  → 稳定可预测                → 稳定可预测
```

本质原因：CodeAct 的效率前提是 **LLM 一次写对代码**。当 API 少、逻辑简单时，这个前提容易满足；当 API 多、串联复杂时，这个前提几乎不成立，CodeAct 退化为"写代码 → 出错 → 修代码"的循环，每轮都消耗完整代码生成的 token，效率反而不如 Function Calling 的单步调用。


## 4. 总结与 Takeaway

### 4.1 什么时候适合用 CodeAct？

**适合的场景**：
1. **工具数量较少（<10 个工具）**：工具描述短，LLM 不容易混淆
2. **任务需要数据处理**：需要在 API 调用之间做计算、过滤、排序等操作
3. **工具 schema 简单明确**：输入输出结构清晰，字段名直观
4. **任务步骤相对独立**：每步操作不依赖上一步的复杂结果

**不适合的场景**：
1. **工具数量过多（> 20个工具）**：描述过长，工具过多，LLM 容易混淆
2. **API 串联步骤多**（> 3-4 步串联）：出错概率急剧上升
3. **API 返回结构复杂**：嵌套深、字段多、大小写敏感
4. **需要精细的错误处理**：每个步骤都可能失败，需要针对性处理
5. **对稳定性要求高**：随机性的代码错误不可接受

### 4.2 如何将 CodeAct 的能力发挥到最大？

1. **精简工具集**：每次只注册任务相关的工具，减少描述长度和混淆
2. **提供完整的 Output Schema**：让 LLM 知道返回值的精确结构
3. **要求 LLM 写小段代码**：每步只做一件事，观察结果后再继续 （AppWorld自身的实现方案）
4. **在代码模板中提供示例**：如有可能，增加oneshot，能显著提高代码准确率
5. **增强错误信息的可读性**：对沙箱中的异常进行格式化和截断，突出关键错误
6. **增加重试机制**：当代码执行失败时，自动重试或提供更友好的错误提示

### 4.3 对 Agent 开发者的建议

| 建议 | 原因 |
|------|------|
| 先用 Function Calling 验证 | 确认工具链路通畅后再迁移到 CodeAct |
| 工具描述越精确越好 | LLM 完全依赖描述来写代码，模糊的描述 = 错误的代码 |
| 不要贪多 | 宁可分 3 步小代码执行，也不要 1 步大代码冒险 |
| Output Schema 是必需品 | 没有它，LLM 无法正确写后续数据处理代码 |
| 监控代码执行的成功率 | 区分"API 错误"和"代码错误"，针对性优化 |

---

## 参考文献

1. Xingyao Wang, Yangqiu Song, et al. "CodeAct: A Code Action Framework for LLM Agents." arXiv:2402.01030, 2024.
2. DSPy CodeAct Agent Architecture. https://github.com/ekzhu/dspy/blob/claude/dspy-rlm-tool-execution-F7n9h/docs/docs/deep-dive/codeact-agent-architecture.md
3. Microsoft Agent Framework - Hyperlight CodeAct. https://learn.microsoft.com/en-us/agent-framework/integrations/hyperlight
4. NousResearch Hermes Agent - Code Execution Tool. https://github.com/NousResearch/hermes-agent/blob/main/tools/code_execution_tool.py
5. LangGraph CodeAct. https://github.com/langchain-ai/langgraph-codeact
6. Harsh Trivedi et al. "AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents." ACL 2024 (Best Resource Paper).


