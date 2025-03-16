#!/bin/bash
# 停止前端和后端服务
if [ -f /tmp/agent_designer_frontend.pid ]; then
  FRONTEND_PID=$(cat /tmp/agent_designer_frontend.pid)
  echo "Stopping frontend with PID $FRONTEND_PID..."
  kill $FRONTEND_PID
  rm /tmp/agent_designer_frontend.pid
fi

if [ -f /tmp/agent_designer_backend.pid ]; then
  BACKEND_PID=$(cat /tmp/agent_designer_backend.pid)
  echo "Stopping backend with PID $BACKEND_PID..."
  kill $BACKEND_PID
  rm /tmp/agent_designer_backend.pid
fi