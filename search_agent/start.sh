#!/bin/bash
DIR=$(cd "$(dirname "$0")"; pwd)
cd "$DIR"

# 加载环境变量
source .env

LOG="$DIR/server.log"

# ====================
# 优化点：启动前先停止
# ====================
echo "🔸 先停止旧服务..."
pkill -f "uvicorn main:app"
sleep 1

echo "🚀 启动新服务..."
nohup uvicorn main:app \
  --host "$SERVER_HOST" \
  --port "$SERVER_PORT" \
  --log-level "$LOG_LEVEL" \
  > "$LOG" 2>&1 &

echo "✅ 服务已启动 PID: $!"
echo "📄 日志: $LOG"
echo "🌐 访问: http://127.0.0.1:$SERVER_PORT"