# 元数据提取器包定义
"""
主要职责：
1. 定义包的公共接口
2. 隐藏模块实现细节
3. 提供便捷的导入路径
"""

# 1. 导出公共接口
from .metadata_service import MetadataService
from .base_extractor import BaseMetadataExtractor
from .image_extractor import ImageMetadataExtractor
from .video_extractor import VideoMetadataExtractor
from .audio_extractor import AudioMetadataExtractor
from .text_extractor import TextMetadataExtractor

__all__ = [
    'MetadataService',
    'BaseMetadataExtractor',
    'ImageMetadataExtractor',
    'VideoMetadataExtractor',
    'AudioMetadataExtractor',
    'TextMetadataExtractor',
]
