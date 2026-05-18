"""
快速测试所有元数据提取器是否能正常导入
"""
import sys
sys.path.insert(0, r'D:\software\VS Code\Code\Python\MemChain\MVP\backend')

print("=" * 70)
print("  测试元数据提取器导入")
print("=" * 70)
print()

print(f"Python: {sys.executable}")
print(f"Version: {sys.version.split()[0]}")
print()

# 测试导入
extractors = [
    ("BaseMetadataExtractor", "from core.data_bunker.services.metadata.base_extractor import BaseMetadataExtractor"),
    ("ImageMetadataExtractor", "from core.data_bunker.services.metadata.image_extractor import ImageMetadataExtractor"),
    ("VideoMetadataExtractor", "from core.data_bunker.services.metadata.video_extractor import VideoMetadataExtractor"),
    ("AudioMetadataExtractor", "from core.data_bunker.services.metadata.audio_extractor import AudioMetadataExtractor"),
    ("TextMetadataExtractor", "from core.data_bunker.services.metadata.text_extractor import TextMetadataExtractor"),
    ("MetadataService", "from core.data_bunker.services.metadata import MetadataService"),
]

success_count = 0
fail_count = 0

for name, import_stmt in extractors:
    try:
        print(f"导入 {name}...", end=" ")
        exec(import_stmt, globals())
        print("✅")
        success_count += 1
    except Exception as e:
        print(f"❌ {type(e).__name__}: {e}")
        fail_count += 1

print()
print("=" * 70)
if fail_count == 0:
    print(f"🎉 全部成功！{success_count}/{len(extractors)} 个导入测试通过")
    print()
    print("可以启动后端服务器了：")
    print("  C:\\Users\\win11\\AppData\\Local\\conda\\conda\\envs\\camel\\python.exe -m uvicorn app:app --reload --port 8000")
else:
    print(f"⚠️  有 {fail_count} 个导入失败")
print("=" * 70)
