@echo off
echo Starting frontend...
cd frontend
start "" cmd /c "npm run dev"

echo Starting backend...
cd backend
start "" cmd /c "python app.py"