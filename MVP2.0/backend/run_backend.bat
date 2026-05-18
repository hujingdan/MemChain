@echo off
echo Starting backend server...
cd /d "d:\software\VS Code\Code\Python\MemChain\MVP\backend"

C:\Users\win11\AppData\Local\conda\conda\envs\camel\python.exe -m uvicorn app:app --reload --port 8000 2>&1

pause
