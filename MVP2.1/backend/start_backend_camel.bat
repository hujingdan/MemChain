@echo off
REM 启动后端服务器 - 使用camel环境

echo ========================================
echo 启动MemChain后端服务器
echo ========================================
echo.

REM 切换到backend目录
cd /d "d:\software\VS Code\Code\Python\MemChain\MVP\backend"

REM 使用camel环境的Python
echo Python环境: C:\Users\win11\AppData\Local\conda\conda\envs\camel\python.exe
echo.
echo 启动服务器...
echo.

C:\Users\win11\AppData\Local\conda\conda\envs\camel\python.exe -m uvicorn app:app --reload --port 8000

pause
