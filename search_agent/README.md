# Search Agent

智能搜索问答服务，基于本地大语言模型 + 搜索增强。

## 功能特性

- **智能问答**: 结合搜索结果与大语言模型生成回答
- **免费搜索**: 基于 DuckDuckGo，无需 API 密钥，完全免费
- **对话记忆**: 支持多会话，本地持久化存储，服务重启记忆不丢失

## 技术架构

```
search_agent/
├── main.py              # FastAPI 入口
├── app/
│   ├── agent.py         # LangChain Agent 实现（含记忆模块）
│   ├── search.py        # DuckDuckGo 搜索实现
│   ├── llm.py          # LLM 客户端（OpenAI 兼容）
│   └── config.py        # 配置加载
├── chat.html            # 前端聊天界面
├── requirements.txt     # 依赖
├── .env                 # 环境变量
├── install.sh           # 安装依赖脚本
├── start.sh             # 启动脚本
└── stop.sh             # 停止脚本
```

## 快速开始

### 1. 安装依赖

```bash
cd search_agent
./install.sh
```

### 2. 配置环境变量

编辑 `.env` 文件：

```env
# 服务配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=info

# LLM 配置（支持 Ollama、火山引擎方舟、OpenAI 等所有兼容 OpenAI 格式的服务）
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3/chat/completions
LLM_MODEL=doubao-seed-2-0-lite-260215
LLM_API_KEY=your-api-key-here
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=2048

# DuckDuckGo 搜索配置（可选，无需 API 密钥）
DDG_REGION=zh-cn
DDG_MAX_RESULTS=5
DDG_TIMEOUT=10

# 记忆配置
MEMORY_MAX_MESSAGES=10
```

### 3. 启动服务

```bash
./start.sh
```

### 4. 访问使用

| 功能 | 地址 |
|------|------|
| 聊天界面 | http://localhost:8000/v1/chat |
| 接口文档 | http://localhost:8000/docs |

## API 接口

### 聊天接口（OpenAI 兼容）

```bash
POST /v1/chat/completions
```

**请求体：**

```json
{
  "query": "问题内容",
  "session_id": "会话ID（可选，默认default）"
}
```

**curl 示例：**

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"query": "什么是Python", "session_id": "test"}'
```

**响应：** SSE 流式返回

### 服务状态

```bash
GET /status
```

返回：

```json
{
  "status": "running",
  "search_engine": "duckduckgo",
  "model": "doubao-seed-2-0-lite-260215"
}
```

## 工作原理

1. 客户端发送问题到 `/v1/chat/completions`
2. LangChain Agent 自动处理：
   - 自动调用 DuckDuckGo 搜索工具获取联网信息
   - 结合历史对话上下文生成回答
3. 通过 SSE 流式返回结果
4. 对话内容保存在本地 SQLite 数据库（chat_memory.db）中，相同 session_id 可记住之前对话，服务重启记忆不丢失

## 对话记忆

- **多会话支持**：不同 session_id 对应独立记忆
- **本地持久化**：记忆保存在 chat_memory.db 文件中，服务重启记忆不丢失
- **前端自动管理**：前端自动生成并保存 session_id 到 localStorage

### 前端使用

访问 http://localhost:8000/v1/chat 会自动：
1. 生成会话 ID 并保存到本地存储
2. 每次对话携带 session_id
3. 多轮对话自动记住之前内容

### 清除会话

点击页面上的「清除会话」按钮可重置当前会话记忆。

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 搜索不可用 | 自动降级为纯本地 LLM 回答 |
| LLM 不可用 | 返回错误信息 |
| 参数缺失 | FastAPI 自动验证返回 422 错误 |
| 网络错误 | 前端显示"网络错误，请稍后重试" |

## 常见问题

**Q: 搜索返回为空怎么办？**
A: 检查网络连接是否正常，DuckDuckGo 是否可访问。

**Q: LLM 响应很慢？**
A: 尝试使用更小的模型，或检查 LLM 服务资源占用。

**Q: 对话记忆重启后丢失？**
A: 当前为内存级记忆，重启服务会丢失。如需持久化可配置 PostgreSQL 存储。

**Q: 如何修改端口？**
A: 修改 `.env` 中的 `SERVER_PORT`，或启动时指定：`./start.sh`（默认8000）

## 环境变量说明

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| SERVER_HOST | 0.0.0.0 | 服务监听地址 |
| SERVER_PORT | 8000 | 服务监听端口 |
| LLM_BASE_URL | - | LLM API 地址 |
| LLM_MODEL | - | LLM 模型名称 |
| LLM_API_KEY | - | LLM API 密钥 |
| LLM_TEMPERATURE | 0.1 | LLM 温度参数 |
| LLM_MAX_TOKENS | 2048 | LLM 最大 tokens |
| DDG_REGION | zh-cn | DuckDuckGo 搜索区域 |
| DDG_MAX_RESULTS | 5 | 搜索返回结果数 |
| DDG_TIMEOUT | 10 | 搜索超时时间（秒） |
