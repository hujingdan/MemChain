"""
后端服务健康检查脚本

检查MemChain后端是否正常运行
"""

import sys
import time
import requests

API_BASE = "http://localhost:8000"

print("=" * 60)
print("  MemChain 后端健康检查")
print("=" * 60)
print()

print(f"正在连接到后端: {API_BASE}")
print()

# 尝试连接
max_retries = 5
for i in range(max_retries):
    try:
        print(f"尝试 {i + 1}/{max_retries}...", end=" ")

        response = requests.get(f"{API_BASE}/", timeout=2)

        if response.status_code == 200:
            print("✅ 成功！")
            print()
            print("后端服务正常运行！")
            print()
            print("你可以：")
            print(f"  1. 查看API文档: {API_BASE}/docs")
            print(f"  2. 运行AI测试: python test_ai_analysis.py --photo your-photo.jpg")
            print()
            sys.exit(0)
        else:
            print(f"❌ 返回状态码: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ 连接被拒绝")
    except requests.exceptions.Timeout:
        print("❌ 连接超时")
    except Exception as e:
        print(f"❌ 错误: {e}")

    if i < max_retries - 1:
        print("   等待3秒后重试...")
        time.sleep(3)

print()
print("=" * 60)
print("❌ 无法连接到后端服务")
print("=" * 60)
print()
print("可能的原因：")
print("  1. 后端服务未启动")
print("     解决方法：python -m uvicorn app:app --reload --port 8000")
print()
print("  2. 后端服务正在启动中")
print("     解决方法：等待几秒后重新运行此脚本")
print()
print("  3. 端口被占用")
print("     解决方法：检查8000端口或使用其他端口")
print()
print("  4. Python代码有错误")
print("     解决方法：查看后端终端的错误信息")
print()
sys.exit(1)
