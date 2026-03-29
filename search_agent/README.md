# Search Agent

智能搜索问答服务，基于本地大语言模型 + 搜索增强。

## 功能特性

- **智能问答**: 结合搜索结果与本地 LLM 生成回答
- **搜索增强**: 支持 SearXNG 自建搜索和 Tavily API
- **自动降级**: 搜索不可用时自动切换为纯本地 LLM 回答
- **流式输出**: SSE 流式返回，响应速度快

## 技术架构

```
search_agent/
├── main.py              # FastAPI 入口
├── app/
│   ├── agent.py         # LangChain Agent 实现
│   ├── search.py        # 搜索实现 (SearXNG/Tavily)
│   ├── llm.py          # LLM 客户端 (ChatOpenAI)
│   └── config.py       # 配置加载
├── requirements.txt    # 依赖
├── .env                # 环境变量
├── start.sh            # 启动脚本
└── stop.sh             # 停止脚本
```

## 快速开始

### 安装依赖

```bash
cd search_agent
pip install -r requirements.txt
```

### 配置环境变量

编辑 `.env` 文件，配置以下内容：

```env
# 服务配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=info

# LLM 配置 (支持 Ollama 或其他 OpenAI 兼容 API)
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen:7b
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2048

# 搜索配置 (二选一)
SEARCH_ENGINE=searxng  # 或 tavily

# SearXNG 配置
SEARXNG_API_URL=http://127.0.0.1:8080
SEARXNG_MAX_RESULTS=5

# Tavily 配置
TAVILY_API_KEY=your-tavily-api-key
TAVILY_MAX_RESULTS=5
```

### 启动服务

```bash
# 方式一：使用启动脚本
./start.sh

# 方式二：手动启动
source .env
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 前置要求

1. **LLM 服务**: 需要运行 Ollama 或其他 OpenAI 兼容的 API 服务
   ```bash
   # Ollama 示例
   ollama serve
   ollama run qwen:7b
   ```

2. **搜索服务** (二选一):
   - **SearXNG**: 自建搜索实例，参考 [SearXNG 官方文档](https://docs.searxng.org/)
   - **Tavily**: 获取 API Key [tavily.com](https://tavily.com)

## API 接口

### 健康检查

```bash
GET /
```

返回 HTML 页面，显示服务状态。

### 服务状态

```bash
GET /status
```

返回：
```json
{
  "status": "running",
  "search_engine": "searxng",
  "model": "qwen:7b"
}
```

### 智能问答

```bash
POST /api/chat?query=你的问题
```

流式返回回答。

**curl 示例:**

```bash
curl -X POST "http://localhost:8000/api/chat?query=什么是人工智能"
```

## 工作原理

1. 客户端发送问题到 `/api/chat`
2. 服务首先尝试调用搜索工具获取联网信息
3. 若搜索成功：使用 LangChain Agent 结合搜索结果生成回答
4. 若搜索失败：自动降级为纯本地 LLM 直接回答
5. 通过 SSE 流式返回结果

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 搜索服务不可用 | 自动降级为纯本地 LLM 回答 |
| LLM 服务不可用 | 返回错误信息 |
| 参数缺失 | FastAPI 自动验证并返回 422 错误 |

## 扩展开发

### 添加新的搜索后端

在 `app/search.py` 中添加新的搜索函数：

```python
def new_search_engine(query: str) -> str | None:
    # 实现搜索逻辑
    pass

# 在 web_search 函数中调用
```

### 调整 Agent Prompt

修改 `app/agent.py` 中的 prompt 模板：

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "你的新系统提示词"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
```

## 常见问题

**Q: 搜索返回为空怎么办？**
A: 检查 SearXNG 服务是否正常运行，或确认 Tavily API Key 是否有效。

**Q: LLM 响应很慢？**
A: 尝试使用更小的模型，或检查本地 LLM 服务资源占用。

**Q: 如何修改端口？**
A: 修改 `.env` 中的 `SERVER_PORT` 或在启动命令中指定：`uvicorn main:app --port 8080`
