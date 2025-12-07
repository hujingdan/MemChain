# MVP/backend/core/data_bunker/services/StorageService.py
import os
import shutil
import uuid
import io
import logging
from pathlib import Path
from contextlib import contextmanager
from boto3.s3.transfer import TransferConfig
import boto3

from backend.config.development import get_settings
from backend.core.data_bunker.exceptions.exceptions import StorageException, ValidationException
from .metadata.metadata_service import MetadataService

logger = logging.getLogger(__name__)

class StorageService:
    """专业级存储服务
    
    关键特性:
    1. 统一类型验证系统
    2. 分块上传管理
    3. 支持本地/S3存储
    4. 与元数据服务集成
    """
    
    _sessions = {}
    _metadata_service = MetadataService()
    
    @classmethod
    def get_accepted_types(cls) -> list[str]:
        """获取系统支持的MIME类型列表(供前端使用)"""
        settings = get_settings()
        return settings.ALLOWED_FILE_TYPES
    
    @classmethod
    def validate_file_type(cls, file_type: str) -> bool:
        """使用统一配置验证文件类型"""
        allowed_types = cls.get_accepted_types()
        return (
            file_type in allowed_types or
            any(file_type.startswith(cat.split('/*')[0]) 
                for cat in allowed_types if '/*' in cat)
        )
    
    @classmethod
    def session_exists(cls, session_id: str) -> bool:
        """检查上传会话是否存在"""
        return session_id in cls._sessions
    
    @classmethod
    def create_session(cls, session_id: str, filename: str, filetype: str, filesize: int):
        """初始化新的上传会话"""
        # 使用统一类型验证
        if not cls.validate_file_type(filetype):
            raise ValidationException(f"Unsupported file type: {filetype}")
        
        # 验证文件大小
        max_size = get_settings().MAX_UPLOAD_SIZE
        if filesize > max_size:
            raise ValidationException(f"File exceeds maximum size of {max_size} bytes")
        
        # 初始化会话
        cls._sessions[session_id] = {
            'chunks': {},
            'chunk_count': None,
            'filename': filename,
            'filetype': filetype,
            'filesize': filesize,
            'temp_path': cls._create_temp_path(session_id)
        }
        
        # 确保临时目录存在
        cls._sessions[session_id]['temp_path'].mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def _create_temp_path(cls, session_id: str) -> Path:
        """创建会话临时目录"""
        temp_root = Path(get_settings().TEMP_STORAGE_PATH)
        return temp_root / f"upload_{session_id}"
    
    @classmethod
    def is_session_complete(cls, session_id: str) -> bool:
        """检查是否所有分块都已上传"""
        session = cls._sessions.get(session_id)
        if not session:
            return False
            
        chunk_count = session.get('chunk_count')
        if chunk_count is None:
            return False
            
        return len(os.listdir(session['temp_path'])) == chunk_count
    
    @classmethod
    def save_chunk(
        cls,
        session_id: str,
        chunk_index: int,
        chunk_count: int,
        chunk_data: bytes
    ):
        """保存上传的分块到临时文件"""
        session = cls._sessions.get(session_id)
        if not session:
            raise StorageException("Invalid session ID")
        
        # 第一次上传时设置总块数
        if session['chunk_count'] is None:
            session['chunk_count'] = chunk_count
        
        # 验证块索引范围
        if chunk_index < 0 or chunk_index >= chunk_count:
            raise ValidationException(f"Invalid chunk index: {chunk_index}")
            
        # 保存块到临时文件
        chunk_path = session['temp_path'] / f"chunk_{chunk_index:05d}.bin"
        with open(chunk_path, 'wb') as f:
            f.write(chunk_data)
    
    @classmethod
    def finalize_upload(cls, session_id: str) -> Path:
        """合并分块并保存最终文件"""
        session = cls._sessions.get(session_id)
        if not session or not cls.is_session_complete(session_id):
            raise StorageException("Incomplete session")
        
        try:
            # 创建最终文件路径
            final_path = cls._get_final_path(
                session['filename'], 
                session['filetype']
            )
            
            # 流式合并文件块
            with open(final_path, 'wb') as output:
                for i in range(session['chunk_count']):
                    chunk_path = session['temp_path'] / f"chunk_{i:05d}.bin"
                    with open(chunk_path, 'rb') as input_chunk:
                        shutil.copyfileobj(input_chunk, output)
            
            # 使用元数据服务验证实际文件类型
            actual_mime = cls._metadata_service.detect_mime_type(final_path)
            if not cls.validate_file_type(actual_mime):
                os.remove(final_path)
                raise ValidationException(
                    f"Detected invalid file type: {actual_mime}"
                )
            
            return final_path
        finally:
            # 清理临时资源
            cls.clean_session(session_id)
    
    @classmethod
    def _get_final_path(cls, filename: str, filetype: str) -> Path:
        """生成最终存储路径"""
        settings = get_settings()
        storage_path = cls.get_storage_path()
        
        # 生成唯一文件名
        file_ext = '.' + filetype.split('/')[-1] if '/' in filetype else ''
        unique_id = uuid.uuid4().hex
        return storage_path / f"{unique_id}{file_ext}"
    
    @classmethod
    def clean_session(cls, session_id: str):
        """清理会话数据"""
        if session_id in cls._sessions:
            # 删除临时文件
            session = cls._sessions[session_id]
            if 'temp_path' in session and session['temp_path'].exists():
                shutil.rmtree(session['temp_path'])
            
            del cls._sessions[session_id]
    
    @classmethod
    def get_storage_path(cls) -> Path:
        """根据配置获取存储路径"""
        settings = get_settings()
        if settings.STORAGE_TYPE == 'local':
            path = Path(settings.LOCAL_STORAGE_PATH)
            path.mkdir(parents=True, exist_ok=True)
            return path
        elif settings.STORAGE_TYPE == 's3':
            return Path(settings.S3_BASE_PATH)
        else:
            raise StorageException("Invalid storage type configuration")
    
    @classmethod
    def store_file_direct(cls, file_path: Path, file_type: str) -> Path:
        """直接存储已存在的文件（非分块上传）"""
        # 使用统一类型验证
        if not cls.validate_file_type(file_type):
            raise ValidationException(f"Unsupported file type: {file_type}")
        
        # 使用元数据服务验证实际文件类型
        actual_mime = cls._metadata_service.detect_mime_type(file_path)
        if not cls.validate_file_type(actual_mime):
            raise ValidationException(
                f"Detected invalid file type: {actual_mime}"
            )
        
        # 创建最终存储路径
        final_path = cls._get_final_path(file_path.name, file_type)
        
        # 根据配置选择存储方式
        settings = get_settings()
        if settings.STORAGE_TYPE == 'local':
            shutil.copy(file_path, final_path)
        elif settings.STORAGE_TYPE == 's3':
            s3 = boto3.client('s3',
                aws_access_key_id=settings.AWS_ACCESS_KEY,
                aws_secret_access_key=settings.AWS_SECRET_KEY,
                region_name=settings.AWS_REGION
            )
            config = TransferConfig(
                multipart_threshold=settings.UPLOAD_CHUNK_SIZE,
                max_concurrency=10
            )
            with open(file_path, 'rb') as f:
                s3.upload_fileobj(
                    f,
                    settings.S3_BUCKET,
                    str(final_path),
                    Config=config
                )
        else:
            raise StorageException("Invalid storage configuration")
        
        return final_path