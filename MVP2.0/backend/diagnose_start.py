"""
简化的后端启动测试

用于诊断后端启动问题
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("  MemChain 后端启动诊断")
print("=" * 60)
print()

# 步骤1: 检查Python版本
print("步骤1: 检查Python版本")
print(f"  Python版本: {sys.version}")
print(f"  Python路径: {sys.executable}")
print()

# 步骤2: 尝试导入FastAPI
print("步骤2: 导入FastAPI")
try:
    from fastapi import FastAPI
    print("  ✅ FastAPI导入成功")
except Exception as e:
    print(f"  ❌ FastAPI导入失败: {e}")
    sys.exit(1)
print()

# 步骤3: 尝试导入app
print("步骤3: 导入app模块")
try:
    from app import app
    print("  ✅ app模块导入成功")
    print(f"  应用类型: {type(app)}")
    print(f"  应用路由数: {len(app.routes)}")
    print()
    print("  已注册的路由:")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            methods = getattr(route, 'methods', set())
            print(f"    {list(methods)} {route.path}")
except Exception as e:
    print(f"  ❌ app导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# 步骤4: 尝试启动服务器
print("步骤4: 准备启动服务器")
print("  如果看到以下信息，说明服务器已成功启动：")
print("    INFO:     Uvicorn running on http://127.0.0.1:8000")
print()
print("  按 Ctrl+C 停止服务器")
print()
print("=" * 60)

try:
    import uvicorn
    print("  ✅ 启动Uvicorn服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
except KeyboardInterrupt:
    print()
    print("=" * 60)
    print("  服务器已停止")
    print("=" * 60)
except Exception as e:
    print()
    print("=" * 60)
    print("  ❌ 服务器启动失败")
    print("=" * 60)
    print(f"错误信息: {e}")
    import traceback
    traceback.print_exc()
