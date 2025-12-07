# core/data_bunker/exceptions.py
"""
自定义异常类
"""
from typing import Optional


class StorageException(Exception):
    """存储操作异常基类"""
    def __init__(self, message: str, file_path: Optional[str] = None):
        super().__init__(message)
        self.file_path = file_path
        self.message = f"{message} (File: {file_path})" if file_path else message

    def __str__(self):
        return self.message

class ValidationException(Exception):
    """数据验证异常"""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message)
        self.field = field
        self.message = f"{message} (Field: {field})" if field else message

    def __str__(self):
        return self.message

class ExtractionError(StorageException):
    """元数据提取异常"""
    pass

class SessionException(StorageException):
    """上传会话异常"""
    pass