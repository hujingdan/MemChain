"""
导入诊断脚本 - 简单版本
"""

import sys

print("=" * 70)
print("  测试Python环境和导入")
print("=" * 70)
print()

sys.path.insert(0, r'D:\software\VS Code\Code\Python\MemChain\MVP\backend')

# 测试1: 环境信息
print("【1】Python环境")
print(f"  可执行文件: {sys.executable}")
print(f"  版本: {sys.version.split()[0]}")
print()

# 测试2: 关键包
print("\n【2】检查关键包")
try:
    import fastapi
    print("✅ fastapi: 已安装")
except ImportError as e:
    print(f"❌ fastapi: {e}")

try:
    import uvicorn
    print("✅ uvicorn: 已安装")
except ImportError as e:
    print(f"❌ uvicorn: {e}")

try:
    import sqlalchemy
    print("✅ sqlalchemy: 已安装")
except ImportError as e:
    print(f"❌ sqlalchemy: {e}")

try:
    from PIL import Image
    print("✅ Pillow: 已安装")
except ImportError as e:
    print(f"❌ Pillow: {e}")

print()

# 测试3: 尝试导入
print("\n【3】测试关键模块导入")

modules = [
    ("core.data_bunker.services.metadata", "from core.data_bunker.services.metadata import MetadataService"),
    ("core.data_bunker.services.metadata.image_extractor", "from core.data_bunker.services.metadata.image_extractor import ImageMetadataExtractor"),
]

success_count = 0
fail_count = 0

for module_name, import_stmt in modules:
    try:
        print(f"\n测试: {module_name}")
        exec(import_stmt, globals())
        print(f"✅ 成功")
        success_count += 1
    except Exception as e:
        print(f"❌ 失败: {type(e).__name__}: {e}")
        fail_count += 1

print()
print("=" * 70)
print(f"结果: {success_count}个成功, {fail_count}个失败")
print()

if fail_count == 0:
    print("\n🎉 所有导入测试通过！现在可以启动后端了")
elif fail_count > 0:
    print(f"\n⚠️  有{fail_count}个导入问题，需要先修复")
    print("建议：")
    print("  1. 运行 'python diagnose_imports.py' 查看详细错误")
    print("  2. 检查模块文件中是否有语法错误")
else:
    input("\n按回车键退出...")
