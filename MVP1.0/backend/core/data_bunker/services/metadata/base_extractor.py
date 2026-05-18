# 文件路径：backend/core/data_bunker/services/metadata/base_extractor.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Type
import logging
import inspect

logger = logging.getLogger(__name__)

class ExtractionError(Exception):
    """元数据提取异常基类"""
    def __init__(self, message: str, file_path: Optional[Path] = None):
        super().__init__(message)
        self.file_path = file_path
        self.message = f"{message} (File: {file_path})" if file_path else message

class BaseMetadataExtractor(ABC):
    """元数据提取器抽象基类
    
    职责：
    1. 定义统一接口
    2. 提供公共工具方法
    3. 强制实现核心功能
    4. 支持插件式扩展
    
    设计原则：
    - 单一职责：每个提取器只处理特定文件类型
    - 开闭原则：通过继承扩展而非修改
    - 防御式编程：所有操作都应有错误处理
    """
    
    @abstractmethod
    def extract(self, file_path: Path) -> Dict:
        """执行元数据提取
        
        参数:
            file_path: 要处理的文件路径
            
        返回:
            包含提取元数据的字典
            
        异常:
            应捕获具体实现中的异常并记录，返回部分结果
        """
        pass
    
    @abstractmethod
    def supported_mime_types(self) -> List[str]:
        """返回支持的具体MIME类型列表
        
        示例: ['image/jpeg', 'image/png']
        """
        pass
    
    def supported_category_types(self) -> List[str]:
        """返回支持的类别通配符类型
        
        默认实现: 根据具体类型生成通配符 (如 image/*)
        可被具体类覆盖以提供更精确的控制
        
        示例: ['image/*', 'video/*']
        """
        return [f"{mime.split('/')[0]}/*" for mime in self.supported_mime_types()]
    
    def is_supported(self, mime_type: str) -> bool:
        """检查是否支持给定的MIME类型
        
        参数:
            mime_type: 要检查的MIME类型
            
        返回:
            True如果支持，False否则
        """
        return (
            mime_type in self.supported_mime_types() or
            any(mime_type.startswith(cat.split('/*')[0]) 
                for cat in self.supported_category_types())
        )
    
    def extract_with_fallback(self, file_path: Path) -> Dict:
        """带安全回退的提取方法
        
        参数:
            file_path: 要处理的文件路径
            
        返回:
            提取的元数据，包含错误信息如果失败
        """
        try:
            return self.extract(file_path)
        except ExtractionError as e:
            logger.error(f"Extraction failed: {e.message}")
            return {'extraction_error': e.message}
        except Exception as e:
            logger.exception(f"Unexpected extraction error for {file_path}")
            return {
                'extraction_error': f"Unexpected error: {str(e)}",
                'file_path': str(file_path)
            }
    
    @classmethod
    def get_extractor_name(cls) -> str:
        """获取提取器的人类可读名称"""
        return cls.__name__
    
    @classmethod
    def get_extractor_version(cls) -> str:
        """获取提取器版本（默认为类定义位置）"""
        try:
            return inspect.getsourcefile(cls) or "unknown"
        except Exception:
            return "unknown"
    
    def __repr__(self) -> str:
        """提取器的可读表示"""
        return f"<{self.get_extractor_name()} supporting {len(self.supported_mime_types())} types>"