"""
核心职责：处理上传请求，将用户上传的素材存储到指定位置（本地或云存储），并记录元数据到数据库。
该控制器确保：
1. 文件上传的安全性和完整性验证
2. 支持断点续传和大文件分片上传
3. 生成统一的文件元数据结构
4. 调用适当的存储服务进行持久化

重构要点：
1. 集成新的MetadataService
2. 适配重构后的StorageService
3. 增强错误处理和日志
4. 支持用户身份验证（占位符）
5. 提供异步处理扩展点
"""
import logging
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from pathlib import Path

from backend.core.data_bunker.services.StorageService import StorageService
from backend.core.data_bunker.services.metadata.metadata_service import MetadataService
from backend.core.data_bunker.repositories.MaterialRepository import MaterialRepository
from backend.core.data_bunker.schemas.material import MaterialCreate
from backend.config.development import Settings,get_settings
from backend.core.data_bunker.exceptions.exceptions import StorageException, ValidationException
from backend.core.data_bunker.database import get_current_user  # 身份验证依赖

logger = logging.getLogger(__name__)
router = APIRouter()

class UploadSessionCreate(BaseModel):
    filename: str = Field(..., examples="vacation.jpg")
    filetype: str = Field(..., examples="image/jpeg")
    filesize: int = Field(..., examples=5242880)

class UploadSessionResponse(BaseModel):
    session_id: str
    chunk_size: int

class ChunkUploadRequest(BaseModel):
    session_id: str
    chunk_index: int
    chunk_count: int

class ChunkUploadResponse(BaseModel):
    session_id: str
    chunk_index: int
    received_size: int

class MaterialResponse(BaseModel):
    id: str
    user_id: str
    name: str
    type: str
    size: int
    path: str
    created_at: datetime
    properties: Dict[str, Any]

# 新增端点
@router.get("/supported-types", response_model=list[str])
async def get_supported_types():
    """获取系统支持的文件类型列表"""
    return StorageService.get_accepted_types()

@router.post("/session", response_model=UploadSessionResponse)
async def create_upload_session(
    session_data: UploadSessionCreate,
    current_user: dict = Depends(get_current_user)  # 身份验证
):
    """初始化上传会话并验证文件参数"""
    try:
        # 创建唯一会话ID
        session_id = str(uuid4())
        
        # 初始化存储会话
        StorageService.create_session(
            session_id,
            session_data.filename,
            session_data.filetype,
            session_data.filesize
        )
        
        return {
            "session_id": session_id,
            "chunk_size": Settings.UPLOAD_CHUNK_SIZE
        }
    except ValidationException as e:
        logger.warning(f"Validation failed for session creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )
    except Exception as e:
        logger.exception("Unexpected error during session creation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error"}
        )

@router.put("/chunk")
async def upload_file_chunk(
    chunk_request: ChunkUploadRequest = Depends(),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)  # 身份验证
):
    """处理文件分块上传"""
    try:
        # 处理分块上传
        chunk_data = await file.read()
        StorageService.save_chunk(
            chunk_request.session_id, 
            chunk_request.chunk_index, 
            chunk_request.chunk_count, 
            chunk_data
        )
        
        return {
            "session_id": chunk_request.session_id,
            "chunk_index": chunk_request.chunk_index,
            "received_size": len(chunk_data)
        }
    except ValidationException as e:
        logger.warning(f"Chunk validation failed: {str(e)}")
        StorageService.clean_session(chunk_request.session_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )
    except StorageException as e:
        logger.error(f"Storage error during chunk upload: {str(e)}")
        StorageService.clean_session(chunk_request.session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Storage operation failed"}
        )
    except Exception as e:
        logger.exception("Unexpected error during chunk upload")
        StorageService.clean_session(chunk_request.session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error"}
        )

@router.post("/complete", response_model=MaterialResponse)
async def complete_upload(
    session_id: str,
    user_metadata: Optional[Dict[str, Any]] = None,  # 用户提供的元数据
    current_user: dict = Depends(get_current_user)  # 身份验证
):
    """完成上传并存储元数据"""
    try:
        # 合并文件块
        file_path = StorageService.finalize_upload(session_id)
        
        # 使用元数据服务提取完整元数据
        metadata_service = MetadataService()
        technical_metadata = metadata_service.extract_metadata(file_path)
        
        # 合并元数据（技术元数据优先）
        full_metadata = {
            **(user_metadata or {}),
            **technical_metadata
        }
        
        # 获取文件名（优先使用用户提供的）
        filename = user_metadata.get('name') if user_metadata else file_path.name
        
        # 保存到数据库
        material_data = MaterialCreate(
            user_id=current_user["id"],  # 从身份验证获取
            name=filename,
            mime_type ,            
            type=technical_metadata.get('actual_mime', 'application/octet-stream'),
            size=technical_metadata.get('file_size', 0),
            path=str(file_path),
            properties=full_metadata
            )
        material = MaterialRepository.create(material_data)
        
        # 触发异步处理（AI分析等）
        await trigger_post_upload_processing(material.id, file_path, full_metadata)
        
        return material
    except ValidationException as e:
        logger.error(f"Upload completion validation failed: {str(e)}")
        StorageService.clean_session(session_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )
    except StorageException as e:
        logger.error(f"Storage error during upload completion: {str(e)}")
        StorageService.clean_session(session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Storage operation failed"}
        )
    except Exception as e:
        logger.exception("Unexpected error during upload completion")
        StorageService.clean_session(session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error"}
        )

async def trigger_post_upload_processing(material_id: str, file_path: Path, metadata: dict):
    """触发上传后的异步处理（AI分析等）"""
    # 在实际应用中，这里会调度异步任务
    # 示例：celery.delay(process_uploaded_material, material_id, str(file_path), metadata)
    logger.info(f"Triggering post-upload processing for material {material_id}")
    
    # 根据文件类型调度不同的处理
    mime_type = metadata.get('actual_mime', '')
    if mime_type.startswith('image/'):
        logger.debug(f"Scheduling image analysis for {file_path}")
    elif mime_type.startswith('video/'):
        logger.debug(f"Scheduling video analysis for {file_path}")
    elif mime_type.startswith('audio/'):
        logger.debug(f"Scheduling audio analysis for {file_path}")
    elif mime_type.startswith('text/'):
        logger.debug(f"Scheduling text analysis for {file_path}")

@router.post("/direct", response_model=MaterialResponse)
async def direct_upload(
    file: UploadFile,
    user_metadata: Optional[Dict[str, Any]] = None,
    current_user: dict = Depends(get_current_user)  # 身份验证
):
    """直接上传整个文件（非分块）"""
    try:
        # 保存文件到临时位置
        temp_path = save_to_temp(file)
        
        # 使用存储服务直接保存
        file_path = StorageService.store_file_direct(
            temp_path, 
            file.content_type
        )
        
        # 使用元数据服务提取完整元数据
        metadata_service = MetadataService()
        technical_metadata = metadata_service.extract_metadata(file_path)
        
        # 合并元数据
        full_metadata = {
            **(user_metadata or {}),
            **technical_metadata
        }
        
        # 保存到数据库
        material_data = MaterialCreate(
            user_id=current_user["id"],
            name=file.filename,
            mime_type ,
            type=technical_metadata.get('actual_mime', file.content_type),
            size=technical_metadata.get('file_size', 0),
            path=str(file_path),
            properties=full_metadata
        )
        material = MaterialRepository.create(material_data)

        # 触发异步处理
        await trigger_post_upload_processing(material.id, file_path, full_metadata)
        
        return material
    except ValidationException as e:
        logger.error(f"Direct upload validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )
    except StorageException as e:
        logger.error(f"Storage error during direct upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Storage operation failed"}
        )
    except Exception as e:
        logger.exception("Unexpected error during direct upload")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error"}
        )
    finally:
        # 清理临时文件
        if temp_path and temp_path.exists():
            temp_path.unlink()

def save_to_temp(file: UploadFile) -> Path:
    """保存上传文件到临时位置"""
    temp_dir = Path(get_settings().temp_storage_path)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    temp_path = temp_dir / f"upload_{uuid4().hex}{Path(file.filename).suffix}"
    
    with open(temp_path, "wb") as buffer:
        while chunk := file.file.read(8192):
            buffer.write(chunk)
    
    return temp_path