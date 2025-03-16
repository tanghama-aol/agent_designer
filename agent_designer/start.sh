#!/bin/bash
# 启动前端和后端服务
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend started with PID $FRONTEND_PID"

echo "Starting backend..."
cd ../backend
python app.py &
BACKEND_PID=$!
echo "Backend started with PID $BACKEND_PID"

# 保存PID到文件
echo $FRONTEND_PID > /tmp/agent_designer_frontend.pid
echo $BACKEND_PID > /tmp/agent_designer_backend.pid