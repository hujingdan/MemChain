"""
StorageService.py - 文件存储服务
负责所有与文件系统打交道的操作：保存、删除、验证、路径管理。
Controller不直接操作文件，而是通过这里的方法间接操作。
"""
import os
import uuid
import shutil
import mimetypes
from pathlib import Path
from typing import Optional, Tuple

# 上传文件根目录
UPLOAD_ROOT = Path(__file__).parent.parent.parent.parent / "uploads"

# 允许上传的文件类型映射
# key: 类型目录名, value: 允许的MIME类型前缀
TYPE_MAP = {
    "images": ["image/"],
    "audio": ["audio/"],
    "text": ["text/"],
    "documents": ["application/pdf"],
}

# 所有允许的MIME类型前缀（扁平化，用于快速检查）
ALL_ALLOWED_TYPES = []
for prefixes in TYPE_MAP.values():
    ALL_ALLOWED_TYPES.extend(prefixes)

# 单个文件最大大小：10MB
MAX_FILE_SIZE = 10 * 1024 * 1024


class StorageService:
    """
    文件存储服务类。
    所有方法均为类方法（@classmethod），因为Service本身无状态，
    只接收输入、操作文件系统、返回结果。
    """

    @classmethod
    def get_upload_dir(cls) -> Path:
        """获取并确保上传根目录存在。"""
        UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
        return UPLOAD_ROOT

    @classmethod
    def validate_file(cls, filename: str, content_type: str, size: int) -> Tuple[bool, str]:
        """
        验证文件是否允许上传。
        返回: (是否通过, 错误信息)
        """
        # 1. 检查文件大小
        if size > MAX_FILE_SIZE:
            return False, f"文件过大，最大允许 {MAX_FILE_SIZE / 1024 / 1024:.0f}MB"

        # 2. 检查文件类型
        effective_type = content_type or mimetypes.guess_type(filename)[0] or ""
        
        is_allowed = False
        for allowed in ALL_ALLOWED_TYPES:
            if effective_type.startswith(allowed) or effective_type == allowed:
                is_allowed = True
                break
        
        if not is_allowed:
            return False, f"不支持的文件类型: {effective_type}"

        # 3. 检查文件名安全（防止路径遍历）
        if ".." in filename or "/" in filename or "\\" in filename:
            return False, "文件名包含非法字符"

        return True, ""

    @classmethod
    def get_type_folder(cls, content_type: str) -> str:
        """根据MIME类型确定存储子目录。"""
        for folder, prefixes in TYPE_MAP.items():
            for prefix in prefixes:
                if content_type.startswith(prefix) or content_type == prefix:
                    return folder
        return "others"

    @classmethod
    def save_file(cls, file_content: bytes, original_name: str, content_type: str) -> Tuple[str, Path]:
        """
        保存文件到磁盘，按类型分类存储。
        返回: (文件ID, 完整保存路径)
        """
        file_id = str(uuid.uuid4())
        ext = Path(original_name).suffix
        stored_name = f"{file_id}{ext}"

        type_folder = cls.get_type_folder(content_type)
        target_dir = cls.get_upload_dir() / type_folder
        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / stored_name
        with open(file_path, "wb") as f:
            f.write(file_content)

        return file_id, file_path

    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """删除指定路径的文件。"""
        path = Path(file_path)
        if path.exists() and path.is_file():
            path.unlink()
            return True
        return False

    @classmethod
    def get_file_info(cls, file_path: str) -> Optional[dict]:
        """获取文件信息。"""
        path = Path(file_path)
        if not path.exists():
            return None
        
        stat = path.stat()
        return {
            "name": path.name,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "extension": path.suffix,
        }