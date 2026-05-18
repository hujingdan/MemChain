# 文件路径：backend/core/data_bunker/services/metadata/__init__.py

"""
元数据提取器包定义
主要职责：
1. 定义包的公共接口
2. 隐藏模块实现细节
3. 提供便捷的导入路径
"""

# 1. 导出公共接口
from .metadata_service import MetadataService
from .base_extractor import BaseMetadataExtractor

# 2. 可选：自动加载所有提取器（避免手动导入）
import importlib
import pkgutil

# 自动发现并注册所有子模块
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    if not module_name.startswith('__'):
        __all__.append(module_name)
        module = importlib.import_module(f".{module_name}", __name__)
        globals().update({name: getattr(module, name) for name in dir(module)})

# 3. 包级初始化
print(f"Initializing metadata extractor package with {len(__all__)} modules")