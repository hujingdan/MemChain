import sys
sys.path.insert(0, r'D:\software\VS Code\Code\Python\MemChain\MVP\backend')

try:
    from core.data_bunker.services.metadata import MetadataService
    from core.data_bunker.services.metadata import ImageMetadataExtractor
    from core.data_bunker.services.metadata import VideoMetadataExtractor
    from core.data_bunker.services.metadata import AudioMetadataExtractor
    from core.data_bunker.services.metadata import TextMetadataExtractor
    from core.data_bunker.services.metadata import BaseMetadataExtractor
    print("SUCCESS: All metadata imports working!")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
