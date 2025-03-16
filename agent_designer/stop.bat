@echo off
echo Stopping frontend...
if exist frontend.pid (
    set /p FRONTEND_PID=<frontend.pid
    taskkill /pid %FRONTEND_PID% /f
    del frontend.pid
)

echo Stopping backend...
if exist backend.pid (
    set /p BACKEND_PID=<backend.pid
    taskkill /pid %BACKEND_PID% /f
    del backend.pid
)