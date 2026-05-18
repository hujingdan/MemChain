# 文件路径：backend/core/data_bunker/services/metadata/metadata_service.py
import os
import importlib
import inspect
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Type, List
from .base_extractor import BaseMetadataExtractor

# 尝试导入 magic，如果不可用则使用备用方法
try:
    import magic
    MAGIC_AVAILABLE = True
except (ImportError, OSError) as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"python-magic 不可用: {e}。将使用备用方法检测文件类型")
    MAGIC_AVAILABLE = False

    MAGIC_AVAILABLE = True
except (ImportError, OSError) as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"python-magic 不可用: {e}。将使用备用方法检测文件类型")
    MAGIC_AVAILABLE = False
from .base_extractor import BaseMetadataExtractor

# 尝试导入 magic，如果不可用则使用备用方法
try:
    import magic
    MAGIC_AVAILABLE = True
except (ImportError, OSError) as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"python-magic 不可用: {e}。将使用备用方法检测文件类型")
    MAGIC_AVAILABLE = False

logger = logging.getLogger(__name__)

class ExtractionError(Exception):
    """自定义元数据提取异常"""
    def __init__(self, message, file_path=None, mime_type=None):
        super().__init__(message)
        self.file_path = file_path
        self.mime_type = mime_type
        self.message = f"{message} (File: {file_path}, Type: {mime_type})"

class MetadataService:
    # 提取器包路径 - 自动发现核心!
    EXTRACTORS_PACKAGE = "core.data_bunker.services.metadata"
    
    def __init__(self, enable_dynamic_loading: bool = True):
        self._extractors = {}      # MIME类型 → 提取器映射
        self._category_extractors = {}  # 类别前缀 → 提取器映射
        self._extractor_classes = []  # 所有提取器类型
        
        # 注册内置提取器
        self._register_builtin_extractors()
        
        # 动态加载额外提取器
        if enable_dynamic_loading:
            self._load_dynamic_extractors()
        
        logger.info(f"Metadata service initialized with {len(self._extractors)} extractors")

    def _register_builtin_extractors(self):
        """注册核心内置提取器"""
        from .image_extractor import ImageMetadataExtractor
        from .video_extractor import VideoMetadataExtractor
        from .audio_extractor import AudioMetadataExtractor
        from .text_extractor import TextMetadataExtractor
        
        # 注册标准提取器
        for extractor_class in [
            ImageMetadataExtractor,
            VideoMetadataExtractor,
            AudioMetadataExtractor,
            TextMetadataExtractor
        ]:
            self._register_extractor(extractor_class())
    
    def _load_dynamic_extractors(self):
        """动态发现和加载提取器模块"""
        try:
            extractor_dir = Path(__file__).parent
            
            # 遍历提取器目录中的所有Python文件
            for file_path in extractor_dir.glob("*.py"):
                if file_path.name.startswith("_") or file_path.name == "base_extractor.py":
                    continue
                    
                module_name = file_path.stem
                full_module_path = f"{self.EXTRACTORS_PACKAGE}.{module_name}"
                
                try:
                    module = importlib.import_module(full_module_path)
                    
                    # 查找所有继承BaseMetadataExtractor的类
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if (
                            issubclass(obj, BaseMetadataExtractor) and 
                            obj != BaseMetadataExtractor and
                            obj not in self._extractor_classes
                        ):
                            self._register_extractor(obj())
                            logger.debug(f"Loaded dynamic extractor: {obj.__name__}")
                            
                except ImportError as e:
                    logger.warning(f"Failed to load extractor module {module_name}: {str(e)}")
                    
        except Exception as e:
            logger.exception("Critical error during dynamic extractor loading")

    def _register_extractor(self, extractor: BaseMetadataExtractor):
        """注册提取器实例"""
        self._extractor_classes.append(type(extractor))
        
        # 直接MIME类型映射
        for mime_type in extractor.supported_mime_types():
            if '/' in mime_type:  # 排除无效类型
                self._extractors[mime_type] = extractor
        
        # 通配符类型映射
        for mime_type in extractor.supported_category_types():
            category = mime_type.split('/*', 1)[0] + '/*'
            self._category_extractors[category] = extractor

    def get_extractor(self, mime_type: str) -> Optional[BaseMetadataExtractor]:
        """获取最适合的提取器"""
        # 1. 精确匹配
        if extractor := self._extractors.get(mime_type):
            return extractor
            
        # 2. 通配符匹配 (如 image/*)
        category = mime_type.split('/', 1)[0] + '/*'
        if extractor := self._category_extractors.get(category):
            return extractor
            
        # 3. 回退到通用二进制提取器
        return None

    def extract_metadata(self, file_path: Path) -> Dict:
        """执行完整的元数据提取流程"""
        # 1. 基础文件属性
        try:
            file_size = os.path.getsize(file_path)
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
        except OSError as e:
            raise ExtractionError(f"File access error: {str(e)}", file_path) from e
        
        # 2. 精确检测文件类型 (使用libmagic)
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(2048)
                actual_mime = magic.from_buffer(chunk, mime=True)
        except Exception as e:
            logger.error(f"MIME detection failed: {str(e)}")
            actual_mime = 'application/octet-stream'
        
        # 3. 构建基础元数据
        base_meta = {
            'actual_mime': actual_mime,
            'file_size': file_size,
            'created_at': creation_time,
            'checksum': self._calculate_checksum(file_path),
            'processing_time': datetime.utcnow().isoformat()
        }
        
        # 4. 特定类型元数据提取
        extractor = self.get_extractor(actual_mime)
        if extractor:
            try:
                logger.info(f"Extracting metadata for {file_path} using {type(extractor).__name__}")
                specific_meta = extractor.extract(file_path)
                # 合并数据时需要防止覆盖基础字段
                return {**base_meta, **specific_meta}
            except Exception as e:
                logger.error(f"Extraction failed for {file_path}: {str(e)}")
                base_meta['extraction_error'] = str(e)
                return base_meta
        
        # 5. 对未知类型的基础处理
        logger.warning(f"No extractor available for {actual_mime}")
        return base_meta

    def list_supported_types(self) -> Dict[str, List[str]]:
        """获取支持的文件类型列表（调试/诊断用）"""
        types = {}
        for extractor in set(self._extractors.values()):
            types[type(extractor).__name__] = extractor.supported_mime_types()
        return types

    def _calculate_checksum(self, file_path: Path) -> str:
        """计算文件的SHA-256校验和（带进度指示）"""
        sha256 = hashlib.sha256()
        file_size = os.path.getsize(file_path)
        processed = 0
        progress_interval = max(10 * 1024 * 1024, file_size // 20)  # 5%或10MB间隔
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
                processed += len(chunk)
                
                # 调试级进度输出（大型文件）
                if logger.isEnabledFor(logging.DEBUG):
                    if processed % progress_interval == 0:
                        percent = (processed / file_size) * 100
                        logger.debug(f"Checksum progress: {percent:.1f}%")
        
        return sha256.hexdigest()