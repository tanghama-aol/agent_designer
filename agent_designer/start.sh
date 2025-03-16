#!/bin/bash
# 启动前端服务
echo "Starting frontend..."
cd frontend
npm run dev

# 启动后端服务
echo "Starting backend..."
cd backend
python app.py