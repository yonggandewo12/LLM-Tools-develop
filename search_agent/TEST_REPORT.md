# Search Agent 端到端测试报告

## 1. 测试目标
验证项目核心链路是否可用：

- 服务是否正常启动
- Web/文档/状态接口是否可访问
- 聊天接口是否可流式返回
- 同一 `session_id` 下记忆是否生效

---

## 2. 测试环境
- 项目：`search_agent`
- 服务地址：`http://localhost:8000`
- 模型配置：`qwen/qwen3.6-plus-preview:free`
- 搜索引擎：`duckduckgo`

---

## 3. 测试范围
### 覆盖项
1. `GET /`
2. `GET /v1/chat`
3. `GET /docs`
4. `GET /status`
5. `POST /v1/chat/completions`
6. SQLite 会话记忆能力

### 未覆盖项
- DuckDuckGo 搜索结果质量
- 前端真实浏览器交互细节
- 高并发压测
- 异常容错场景

---

## 4. 测试结果汇总

| 测试项 | 结果 | 说明 |
|---|---|---|
| 首页 `/` | 通过 | HTTP 200 |
| 聊天页 `/v1/chat` | 通过 | HTTP 200 |
| Swagger `/docs` | 通过 | HTTP 200 |
| 状态接口 `/status` | 通过 | 返回 running |
| 聊天接口流式返回 | 通过 | 收到 `data:` 分段输出 |
| 会话记忆 | 通过 | 能记住并正确回忆名字 |

---

## 5. 详细测试记录

### 5.1 服务状态接口
请求：
```http
GET /status
```

返回：
```json
{"status":"running","search_engine":"duckduckgo","model":"qwen/qwen3.6-plus-preview:free"}
```

结论：
- 服务正常运行
- 当前模型与搜索引擎配置已生效

---

### 5.2 基础页面访问
#### 首页
```http
GET /
```
结果：`200`

#### 聊天页
```http
GET /v1/chat
```
结果：`200`

#### 文档页
```http
GET /docs
```
结果：`200`

结论：
- 基础路由均正常
- 前端页面与接口文档可访问

---

### 5.3 聊天接口流式测试
请求：
```json
{"query":"你好","session_id":"e2e_basic_retry"}
```

返回片段：
```text
data: 你好！有什么
data: 我可以帮你的吗
data: ？
```

结论：
- `POST /v1/chat/completions` 正常工作
- 返回类型符合 SSE 流式输出预期
- 前后端主链路可用

---

### 5.4 会话记忆测试
#### 第一次请求
请求：
```json
{"query":"请记住：我的名字叫测试员阿明。","session_id":"e2e_memory_001"}
```

返回片段：
```text
data: 好的，我已经
data: 记住了，
data: 您的名字是**
data: 测试
data: 员阿明**。
```

#### 第二次请求
请求：
```json
{"query":"我叫什么名字？只回答名字。","session_id":"e2e_memory_001"}
```

返回：
```text
data: 测试员
data: 阿明
```

结论：
- 同一 `session_id` 下历史会话被正确恢复
- SQLite 持久化记忆链路正常

---

## 6. 发现的问题

### 上游模型限流
日志中出现多次：
```text
openai.RateLimitError: 429
qwen/qwen3.6-plus-preview:free is temporarily rate-limited upstream
```

影响：
- 部分请求会中断
- SSE 连接可能被提前关闭
- 需要重试才成功

问题归因：
- 主要是 **OpenRouter 免费模型上游限流**
- 不是项目本地路由逻辑直接导致

---

## 7. 风险评估

| 风险项 | 级别 | 说明 |
|---|---|---|
| 免费模型限流 | 中 | 影响稳定性，偶发失败 |
| 搜索链路未单独验收 | 中 | 未确认 DuckDuckGo 实际可用性 |
| 前端未做真实浏览器测试 | 低 | 页面接口已通，但未验证完整交互体验 |

---

## 8. 最终结论
本次端到端测试结论：

**整体通过。**

### 已验证通过
- 服务启动与访问
- 基础页面
- API 文档
- 状态接口
- 流式聊天
- 会话记忆

### 当前主要问题
- 上游免费模型存在限流，导致稳定性受影响

---

## 9. 建议后续动作
1. 更换为更稳定的付费模型或自有 Key
2. 给聊天接口增加上游异常兜底返回
3. 补做 DuckDuckGo 搜索专项测试
4. 补做浏览器真实交互测试
5. 增加自动化测试脚本
