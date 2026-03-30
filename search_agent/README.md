# Search Agent

基于 **FastAPI + LangChain/LangGraph + DuckDuckGo + OpenAI 兼容 LLM** 的搜索问答服务。

项目提供：

- Web 聊天界面：`/v1/chat`
- OpenAI 风格流式接口：`/v1/chat/completions`
- DuckDuckGo 免费联网搜索
- 基于 `session_id` 的多会话记忆
- 本地 SQLite 记忆文件 `chat_memory.db`

---

## 1. 功能特性

- **智能问答**：使用 LangChain Agent 调度模型与搜索工具
- **免费搜索**：使用 DuckDuckGo，无需单独申请搜索 API Key
- **流式输出**：接口以 `text/event-stream` 返回生成结果
- **多会话记忆**：不同 `session_id` 彼此隔离
- **本地记忆持久化**：记忆写入 `chat_memory.db`，服务重启后仍可继续使用
- **OpenAI 风格接口**：接口路径为 `/v1/chat/completions`

---

## 2. 项目结构

```text
search_agent/
├── app/
│   ├── agent.py         # LangChain Agent 与记忆调度
│   ├── config.py        # 环境变量加载
│   ├── llm.py           # OpenAI 兼容 LLM 客户端封装
│   └── search.py        # DuckDuckGo 搜索工具
├── chat.html            # Web 聊天页面
├── main.py              # FastAPI 入口
├── requirements.txt     # Python 依赖
├── install.sh           # 安装依赖脚本
├── start.sh             # 启动脚本
├── stop.sh              # 停止脚本
├── .env                 # 本地环境变量（默认不应提交真实密钥）
├── server.log           # 服务日志
└── chat_memory.db       # SQLite 记忆库（运行后生成）
```

---

## 3. 运行环境

- Python 3.14（当前环境）
- 需要一个 **OpenAI 兼容**的大模型服务
- 默认端口：`8000`

支持的模型服务示例：

- Ollama 的 OpenAI 兼容接口
- OpenAI API
- 火山引擎方舟 / Doubao OpenAI 兼容接口
- 其他兼容 OpenAI Chat Completions 协议的服务

---

## 4. 安装依赖

### 方式一：推荐使用脚本

```bash
cd search_agent
./install.sh
```

`install.sh` 实际执行的是：

```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

### 方式二：手动安装

```bash
cd search_agent
python3 -m pip install --break-system-packages -r requirements.txt
```

---

## 5. 配置 .env

请根据你的模型服务修改 `.env`：

```env
# 服务配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=info

# LLM 配置（必须）
LLM_BASE_URL=https://your-openai-compatible-endpoint/v1/chat/completions
LLM_MODEL=your-model-name
LLM_API_KEY=your-api-key-here
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=2048

# DuckDuckGo 搜索配置
DDG_REGION=zh-cn
DDG_MAX_RESULTS=5
DDG_TIMEOUT=10

# 记忆配置
MEMORY_MAX_MESSAGES=10
```

### 配置说明

| 变量名 | 说明 |
|---|---|
| `SERVER_HOST` | 服务监听地址 |
| `SERVER_PORT` | 服务监听端口 |
| `LOG_LEVEL` | uvicorn 日志级别 |
| `LLM_BASE_URL` | OpenAI 兼容接口地址 |
| `LLM_MODEL` | 模型名称 |
| `LLM_API_KEY` | 模型服务密钥 |
| `LLM_TEMPERATURE` | 温度参数 |
| `LLM_MAX_TOKENS` | 最大输出 token |
| `DDG_REGION` | DuckDuckGo 搜索地区 |
| `DDG_MAX_RESULTS` | 最大搜索结果数 |
| `DDG_TIMEOUT` | 搜索超时时间 |
| `MEMORY_MAX_MESSAGES` | 记忆配置项，当前代码中尚未裁剪消息长度 |

> 注意：`LLM_BASE_URL` 在代码里会自动去掉尾部 `/chat/completions`，因此你填完整地址或基础地址都可兼容。

---

## 6. 启动与停止

### 启动

```bash
./start.sh
```

`start.sh` 会：

1. 切换到项目目录
2. 加载 `.env`
3. 停止旧的 `uvicorn main:app`
4. 用 `python3 -m uvicorn` 后台启动服务
5. 日志输出到 `server.log`

### 停止

```bash
./stop.sh
```

---

## 7. 访问地址

| 功能 | 地址 |
|---|---|
| 首页 | `http://localhost:8000/` |
| 聊天页面 | `http://localhost:8000/v1/chat` |
| Swagger 文档 | `http://localhost:8000/docs` |
| 服务状态 | `http://localhost:8000/status` |

---

## 8. API 说明

### 8.1 聊天接口

```http
POST /v1/chat/completions
Content-Type: application/json
```

请求体：

```json
{
  "query": "请介绍一下 Python",
  "session_id": "default"
}
```

字段说明：

| 字段 | 必填 | 说明 |
|---|---|---|
| `query` | 是 | 用户问题 |
| `session_id` | 否 | 会话 ID，默认 `default` |

返回类型：

- `text/event-stream`
- 每一段输出形如：

```text
data: 你好

data: 我可以帮你介绍 Python
```

### 8.2 curl 示例

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"query":"什么是 Python？","session_id":"default"}'
```

### 8.3 状态接口

```bash
GET /status
```

响应示例：

```json
{
  "status": "running",
  "search_engine": "duckduckgo",
  "model": "doubao-seed-2-0-lite-260215"
}
```

---

## 9. Web 聊天页面说明

聊天页面位于：

```text
GET /v1/chat
```

页面行为：

1. 自动生成或读取 `localStorage` 中的 `chat_session_id`
2. 点击发送后，向 `/v1/chat/completions` 发起 POST JSON 请求
3. 用 SSE 流读取回答并逐段渲染
4. 点击“清除会话”会清空本地 `session_id` 与当前页面消息

---

## 10. LangChain / LangGraph 调度原理

核心流程：

1. FastAPI 接收 `query` 和 `session_id`
2. `main.py` 调用 `stream_answer(query, session_id)`
3. `app/agent.py` 内部：
   - 创建/复用 LLM 客户端
   - 打开 SQLite checkpointer
   - 调用 `create_agent(...)`
4. LangChain Agent 根据用户问题决定是否调用 `search_tool`
5. `search_tool` 内部调用 DuckDuckGo 搜索
6. 模型结合搜索结果和会话历史生成回答
7. `astream_events()` 将模型输出逐段流式返回
8. LangGraph 将会话状态写入 SQLite

简化调用链：

```text
HTTP -> stream_answer -> create_agent -> search_tool(可选) -> LLM -> SSE 输出
                                      \-> AsyncSqliteSaver(thread_id=session_id)
```

---

## 11. 搜索机制

搜索工具定义在 `app/search.py`：

- 主入口：`web_search(query)`
- 当前实现：`duckduckgo_search(query)`
- 优先抓取 DuckDuckGo HTML 搜索页
- 若 HTML 结果为空，则降级到 DuckDuckGo Instant Answer API

返回值约定：

- 成功：格式化后的文本
- 失败：`None`

Agent 层把它包装为 LangChain Tool：

```python
@tool
def search_tool(query: str) -> str:
    return web_search(query) or "搜索不可用"
```

---

## 12. 记忆机制

### 12.1 当前实现

当前项目使用：

```python
AsyncSqliteSaver.from_conn_string(chat_memory.db)
```

因此记忆是：

- **按 `session_id` 隔离**
- **写入本地 SQLite 文件**
- **服务重启后仍可恢复**

### 12.2 记忆文件位置

默认文件：

```text
search_agent/chat_memory.db
```

也就是项目根目录下，与 `main.py` 同级。

### 12.3 如何验证记忆

同一个 `session_id` 连续发送：

1. `记住：我叫徐良`
2. `我叫什么名字？`

理论上第二问应该能回答出“徐良”。

---

## 13. 验收建议

建议至少做以下验收：

### 基础接口

```bash
curl http://localhost:8000/status
curl http://localhost:8000/docs
curl http://localhost:8000/v1/chat
```

### 搜索能力

```bash
python3 -c "from app.search import web_search; print(web_search('Python教程') is not None)"
```

### 记忆能力

使用同一个 `session_id` 连续提问验证上下文。

### 持久化能力

1. 先完成一轮对话
2. 重启服务
3. 再次用同一 `session_id` 提问
4. 确认 `chat_memory.db` 仍存在且历史可读

---

## 14. 常见问题

### Q1：聊天页面提示“网络错误，请稍后重试”

常见原因：

- 服务未启动
- LLM 上游接口不可用
- 前端请求已发出，但流式结果迟迟未返回

建议先看：

```bash
cat server.log
```

### Q2：DuckDuckGo 搜索返回 None

先单独测试：

```bash
python3 -c "from app.search import web_search; print(web_search('Python教程'))"
```

### Q3：记忆没有生效

先确认两点：

1. 两次请求是否使用同一个 `session_id`
2. LLM 是否真的成功完成了上一轮对话

### Q4：重启后记忆丢失

先确认：

- `chat_memory.db` 是否存在
- 运行目录是否正确
- 当前代码是否正常走到 SQLite checkpointer

### Q5：接口为什么不是完全 OpenAI 原生返回格式？

因为当前接口路径采用 OpenAI 风格，但响应仍是本项目自定义的 SSE 文本流，并未完整实现 OpenAI 官方的 chunk JSON 格式。

---

## 15. 依赖列表

当前 `requirements.txt`：

```text
fastapi
uvicorn[standard]
langchain
langchain-community
langchain-openai
langgraph
langgraph-checkpoint-sqlite
python-dotenv
requests
beautifulsoup4
aiosqlite
```

---

## 16. 注意事项

1. `.env` 不应提交真实密钥
2. `chat_memory.db` 属于运行产物，通常不应提交
3. 当前依赖安装脚本使用 `--break-system-packages`，适合当前机器环境，但不适合所有生产环境
4. 如果模型服务超时，接口虽然返回 200，但流式内容可能迟迟不返回

---

## 17. 后续可优化项

- 补上 `MEMORY_MAX_MESSAGES` 的真正裁剪逻辑
- 将 `/v1/chat/completions` 改成更完整的 OpenAI chunk JSON 协议
- 增加 LLM 健康检查接口
- 增加更清晰的错误码和异常信息
- 增加自动化测试
