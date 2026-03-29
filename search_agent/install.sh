#!/bin/bash
# 安装搜索智能体所需依赖
echo "🔧 开始安装依赖..."

cd "$(dirname "$0")"

# 强制安装系统级Python依赖
python3 -m pip install --break-system-packages -r requirements.txt

echo ""
echo "✅ 依赖安装完成！"
echo ""
echo "🚀 启动服务："
echo "   ./start.sh"
echo ""
echo "🌐 访问地址："
echo "   http://localhost:8000/chat"
