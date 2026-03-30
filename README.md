# LLM-Tools-Develop

基于本地大语言模型的 AI 工具集，包含两个独立的微服务应用。

## 项目简介

本项目提供两个基于 FastAPI + 本地 LLM 的 AI 服务：

| 项目 | 功能描述 | 核心技术 |
|------|----------|----------|
| **search_agent** | 智能搜索问答服务 | FastAPI + LangChain + 本地 LLM |
| **tour_agent** | 旅游助手 API | FastAPI + LangChain + 旅游场景增强 |

## 目录结构

```
llm_skills/
├── README.md                 # 本文件
├── search_agent/            # 搜索问答服务
│   ├── main.py              # FastAPI 入口
│   ├── app/
│   │   ├── agent.py         # LangChain Agent
│   │   ├── search.py        # 搜索实现 (SearXNG/Tavily)
│   │   ├── llm.py           # LLM 客户端
│   │   └── config.py        # 配置加载
│   ├── requirements.txt
│   ├── .env                 # 环境配置
│   ├── start.sh             # 启动脚本
│   └── stop.sh              # 停止脚本
│
└── tour_agent/              # 旅游助手服务
    ├── main.py              # FastAPI 入口
    ├── core/
    │   ├── agent.py         # Agent 实现
    │   ├── search.py        # 搜索模块 (Bocha)
    │   ├── weather.py       # 天气查询 (QWeather)
    │   ├── tour.py          # 景点推荐
    │   ├── llm.py           # LLM 客户端
    │   └── config.py        # 配置加载
    ├── requirements.txt
    └── .env                 # 环境配置
```

## 快速开始

### 前置要求

- Python 3.10+
- 本地运行的 LLM 服务（Ollama 或兼容 OpenAI API 的服务）

### 安装与运行

#### 1. search_agent（搜索问答服务）

```bash
cd search_agent
pip install -r requirements.txt

# 启动 Ollama（或其他兼容 API 的 LLM 服务）
# ollama serve

# 启动服务
./start.sh
# 或手动: uvicorn main:app --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

#### 2. tour_agent（旅游助手服务）

```bash
cd tour_agent
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload
```

访问 http://localhost:8001/docs 查看 API 文档

## API 概览

### search_agent 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/status` | GET | 服务状态 |
| `/api/chat` | POST | 智能问答（流式返回）|

### tour_agent 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/api/search` | GET | 联网搜索 |
| `/api/weather` | GET | 天气查询 |
| `/api/tour/recommend` | GET | 景点推荐 |
| `/api/chat` | GET | 智能问答 |

## 配置说明

各子项目的详细配置请参考各自目录下的 `.env` 文件和 README.md。

## 技术栈

- **Web 框架**: FastAPI
- **LLM 框架**: LangChain + ChatOpenAI
- **本地 LLM**: Ollama (search_agent) / Doubao (tour_agent)
- **搜索**: SearXNG / Tavily / Bocha
- **天气**: QWeather

## 注意事项

- 两个服务使用不同的端口，请确保端口不冲突
- 首次运行需配置对应的 API Key（见各子项目 .env 文件）
- search_agent 搜索不可用时会自动退化为纯本地 LLM 回答
