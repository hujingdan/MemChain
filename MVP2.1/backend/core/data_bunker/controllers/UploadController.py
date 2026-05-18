"""
UploadController.py（重构版）
职责：接收HTTP请求，调用StorageService处理文件，调用Repository操作数据库。
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from pathlib import Path

from ..database import get_db
from ..repositories.MaterialRepository import MaterialRepository
from ..services.StorageService import StorageService
from ...ai_processor.services.InsightService import InsightService

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """上传文件：验证 -> 保存到磁盘 -> 写入数据库。"""
    content = await file.read()
    file_size = len(content)

    # 用StorageService验证
    is_valid, error_msg = StorageService.validate_file(
        filename=file.filename or "",
        content_type=file.content_type or "",
        size=file_size
    )
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # 用StorageService保存文件（自动按类型分类）
    try:
        file_id, file_path = StorageService.save_file(
            file_content=content,
            original_name=file.filename or "unnamed",
            content_type=file.content_type or "application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

    # 写入数据库
    try:
        material = MaterialRepository.create(
            db=db,
            id=file_id,
            # ===================== 修复：补上 user_id =====================
            user_id="demo_user",
            name=file.filename or "unnamed",
            type=StorageService.get_type_folder(file.content_type or ""),
            path=str(file_path),
            mime_type=file.content_type or "application/octet-stream",
            size=file_size,
            properties={"original_filename": file.filename, "stored_name": file_path.name}
        )
    except Exception as e:
        StorageService.delete_file(str(file_path))  # 回滚
        raise HTTPException(status_code=500, detail=f"数据库记录失败: {str(e)}")

    # AI分析（图片才分析）
    if material.type == "images":
        ai_result = InsightService.analyze_image(str(file_path))
        if ai_result:
            material.properties = {**(material.properties or {}), **ai_result}
            db.commit()
            db.refresh(material)

    # 返回结果（包含AI分析信息）
    return JSONResponse({
        "success": True,
        "message": "文件上传成功",
        "data": {
            "id": material.id, "name": material.name, "type": material.type,
            "mime_type": material.mime_type, "size": material.size,
            "created_at": material.created_at.isoformat() if material.created_at else None,
            "ai_analysis": material.properties,  # 新增：返回AI分析结果
        }
    })


@router.get("/files")
async def list_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取文件列表（分页）。"""
    materials = MaterialRepository.list_all(db, skip=skip, limit=limit)
    return {
        "total": len(materials), "skip": skip, "limit": limit,
        "files": [{"id": m.id, "name": m.name, "type": m.type,
                   "mime_type": m.mime_type, "size": m.size,
                   "created_at": m.created_at.isoformat() if m.created_at else None,"properties": m.properties}
                  for m in materials]
    }


@router.get("/files/{file_id}")
async def get_file_detail(file_id: str, db: Session = Depends(get_db)):
    """获取单个文件详情（含磁盘信息）。"""
    material = MaterialRepository.get_by_id(db, file_id)
    if not material:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    file_info = StorageService.get_file_info(material.path)
    return {
        "id": material.id, "name": material.name, "type": material.type,
        "mime_type": material.mime_type, "size": material.size,
        "path": material.path, "disk_info": file_info,
        "created_at": material.created_at.isoformat() if material.created_at else None,
        "properties": material.properties,
    }


@router.delete("/files/{file_id}")
async def delete_file(file_id: str, db: Session = Depends(get_db)):
    """删除文件：删数据库 + 删磁盘。"""
    material = MaterialRepository.get_by_id(db, file_id)
    if not material:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    MaterialRepository.delete(db, file_id)
    StorageService.delete_file(material.path)
    return {"success": True, "message": "文件已删除"}


@router.get("/preview/{file_id}")
async def preview_file(file_id: str, db: Session = Depends(get_db)):
    """预览文件：直接返回文件内容（图片可在浏览器直接显示）。"""
    material = MaterialRepository.get_by_id(db, file_id)
    if not material:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    file_path = Path(material.path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件已从磁盘删除")
    
    return FileResponse(path=file_path, media_type=material.mime_type, filename=material.name)