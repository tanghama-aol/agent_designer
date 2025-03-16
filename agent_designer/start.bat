@echo off
echo Starting frontend...
cd frontend
start "" npm run dev

echo Starting backend...
cd ..\backend
start "" python app.py