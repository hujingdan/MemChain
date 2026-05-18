"""
Python环境诊断工具
不需要任何依赖，直接运行即可
"""

import sys
import os

print("=" * 70)
print("  Python 环境诊断")
print("=" * 70)
print()

print("当前 Python 信息：")
print(f"  可执行文件: {sys.executable}")
print(f"  版本: {sys.version}")
print(f"  路径: {sys.prefix}")
print()

print("检查关键包：")
packages = ["fastapi", "uvicorn", "sqlalchemy", "aiohttp"]
for pkg in packages:
    try:
        __import__(pkg)
        print(f"  ✅ {pkg}: 已安装")
    except ImportError:
        print(f"  ❌ {pkg}: 未安装")
print()

print("conda 环境：")
conda_env = os.getenv("CONDA_DEFAULT_ENV", "")
if conda_env:
    print(f"  当前环境: {conda_env}")
else:
    print("  ⚠️  不在conda环境中")
print()

print("需要的操作：")
print()
print("如果你看到上面的 '❌ fastapi: 未安装' 或 '❌ uvicorn: 未安装'：")
print("  说明你当前使用的Python不是camel环境")
print()
print("解决方法：")
print("  1. 在VS Code中按 Ctrl+Shift+P")
print("  2. 输入: Python: Select Interpreter")
print("  3. 在列表中找到并选择包含 'camel' 的Python")
print("  4. 重新运行此脚本确认")
print()
print("=" * 70)

input("按回车键退出...")
