# MyClaw

AI 助手，支持多模态对话、定时任务、长期记忆、MCP 工具调用等能力。


## 快速开始

### 1. 配置环境变量

> **重要：** 必须先配置环境变量，否则启动时会报错。

前往 [阿里云百炼平台](https://bailian.console.aliyun.com/) 注册并创建 API Key：

1. 登录百炼控制台
2. 进入「API-KEY管理」页面
3. 点击「创建API-KEY」，复制生成的 Key

在项目根目录创建 `.env` 文件：

```bash
DASHSCOPE_API_KEY=你的百炼API_KEY
```

### 2. 环境准备

**要求：** Python >= 3.11，推荐使用 [uv](https://docs.astral.sh/uv/) 管理依赖。

```bash
# 克隆项目
git clone https://github.com/akamyc/MyClaw.git
cd myclaw

# 安装依赖
uv sync
```

### 3. 启动服务

```bash
uv run server.py
```

启动后访问 `http://localhost:8009` 即可使用。


## 功能概览

| 功能 | 说明 |
|------|------|
| 多模态对话 | 支持文本 + 图片输入，基于 Qwen3.5-Plus 多模态理解 |
| 流式响应 | SSE 实时流式输出，打字机效果 |
| 工具调用 | ReAct 推理 + 并行工具调用（文件读写、Shell、联网搜索等） |
| MCP 集成 | Playwright 浏览器、八字算命等 MCP 服务 |
| 定时任务 | Cron 表达式调度，支持秒级精度 |
| 长期记忆 | ReMe 自动压缩上下文 + Markdown 持久化 + 语义检索 |
| 深度研究 | Agentic Planning 模式，可视化任务拆解与进度 |
| Subagent | 复杂任务自动委托给子代理独立执行 |
| 人格设定 | 在线编辑 AGENTS.md / SOUL.md / USER.md，热更新 |
| Skill 系统 | 输入 `/` 触发技能提示，可扩展 SOP 流程 |


## 配置说明

编辑 `conf.py` 开关各功能模块：

```python
FLAGS = {
    "enable_playwright_mcp":        True,   # Playwright 浏览器 MCP
    "enable_bazi_mcp":              True,   # 八字算命 MCP
    "enable_websearch":             True,   # 联网搜索
    "enable_view_text_file":        True,   # 查看文件
    "enable_write_text_file":       True,   # 写入文件
    "enable_insert_text_file":      True,   # 插入文件
    "enable_execute_shell_command": True,   # 执行 Shell
    "enable_subagent":              True,   # 子代理
    "enable_cron":                  True,   # 定时任务
    "enable_reme":                  True,   # 长期记忆
}
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18 + Three.js |
| 后端 | FastAPI + AgentScope |
| 模型 | Qwen3.5-Plus（推荐） |
| 工具协议 | MCP (Model Context Protocol) |
| 会话存储 | JSON 文件持久化 |
| 长期记忆 | ReMe（向量检索 + 摘要压缩） |

## 项目结构

```
├── server.py          # FastAPI 入口
├── superagent.py      # Agent 生命周期与会话管理
├── tools.py           # 工具注册与系统提示词
├── session.py         # 会话管理与 MCP 客户端生命周期
├── cron_manager.py    # 定时任务调度
├── model.py           # 自定义模型封装（缓存控制、多模态 Token 计数）
├── datamodel.py       # 数据模型定义
├── conf.py            # 功能开关与配置
├── chat.html          # 前端页面
├── .agent/            # 人格设定与技能目录
│   ├── defines/       # AGENTS.md / SOUL.md / USER.md
│   └── skills/        # 可扩展技能
└── ReMe/              # 长期记忆模块（Git submodule）
```
