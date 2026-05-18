"""
核心职责：实现数据聚合逻辑，从各种数据源（上传的文件、第三方API等）拉取数据，转换为统一的数据模型。
该服务负责：
1. 数据源适配器管理
2. 数据格式统一化处理
3. 元数据提取和标准化
4. 数据质量控制和验证
"""

# MVP/backend/core/data_bunker/services/DataAggregationService.py
from .metadata.metadata_service import MetadataService
from ..repositories import MaterialRepository
from pathlib import Path

class DataAggregationService:
    def __init__(self):
        self.metadata_service = MetadataService()
    
    def process_uploaded_file(self, file_path: Path):
        """处理新上传文件"""
        # 提取元数据
        metadata = self.metadata_service.extract_metadata(file_path)
        
        # 转换为统一数据模型
        normalized_data = self._normalize_metadata(metadata)
        
        # 存储到数据库
        MaterialRepository.create_with_metadata(normalized_data)
        
        # 异步触发其他处理
        self._trigger_ai_processing(file_path, metadata)
    
    def aggregate_from_sources(self, sources: list):
        """从多个数据源聚合数据"""
        # 使用各源的适配器获取数据
        raw_data = [self._get_source_data(source) for source in sources]
        
        # 转换为统一模型
        unified_data = [self._normalize_source(item) for item in raw_data]
        
        # 持久化
        MaterialRepository.bulk_create(unified_data)
    
    def _normalize_metadata(self, metadata: dict) -> dict:
        """标准化元数据结构"""
        # 实现映射逻辑...
        return {
            'type': metadata.get('actual_mime', ''),
            'dimensions': metadata.get('dimensions'),
            'duration': metadata.get('duration'),
            # 其他字段...
        }
    
    def _trigger_ai_processing(self, file_path: Path, metadata: dict):
        """触发AI处理流程"""
        # 根据文件类型调度不同的AI任务
        if metadata['actual_mime'].startswith('image/'):
            self._schedule_image_ai_processing(file_path, metadata)
        elif metadata['actual_mime'].startswith('video/'):
            self._schedule_video_ai_processing(file_path, metadata)
        # ...