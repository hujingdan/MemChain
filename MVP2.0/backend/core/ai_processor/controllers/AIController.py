"""
AI分析控制器

提供AI分析相关的API端点
"""

import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.ai_processor.services.InsightService import InsightService
from core.data_bunker.database import get_db
from core.data_bunker.repositories.MaterialRepository import MaterialRepository

logger = logging.getLogger(__name__)
router = APIRouter()


# ==================== 请求/响应模型 ====================

class AnalyzeRequest(BaseModel):
    """AI分析请求"""
    material_id: str = Field(..., description="Material ID")
    force_refresh: bool = Field(False, description="是否强制重新分析（忽略缓存）")


class EmotionResponse(BaseModel):
    """情感分析响应"""
    material_id: str
    primary_emotion: str = Field(..., description="主要情感类型")
    confidence: float = Field(..., description="置信度（0-1）", ge=0, le=1)
    description: str = Field(..., description="情感描述")
    emotion_distribution: Dict[str, float] = Field(..., description="情感分布")


class TagsResponse(BaseModel):
    """标签生成响应"""
    material_id: str
    tags: list[str] = Field(..., description="标签列表")
    categories: Dict[str, list[str]] = Field(..., description="按类别分组的标签")


class DescriptionResponse(BaseModel):
    """内容描述响应"""
    material_id: str
    summary: str = Field(..., description="简短摘要")
    description: str = Field(..., description="详细描述")
    key_elements: list[str] = Field(..., description="关键元素列表")


class FullAnalysisResponse(BaseModel):
    """完整分析响应"""
    material_id: str
    emotion: Dict[str, Any]
    tags: list[str]
    tag_categories: Dict[str, list[str]]
    description: Dict[str, str]


# ==================== API端点 ====================

@router.post("/analyze", response_model=FullAnalysisResponse)
async def analyze_material(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    完整分析Material（情感+标签+描述）

    这是主要的AI分析入口点，会并行执行：
    1. 情感分析
    2. 标签生成
    3. 内容描述

    Args:
        request: 分析请求
        db: 数据库会话

    Returns:
        完整分析结果
    """
    try:
        insight_service = InsightService(db)

        result = await insight_service.analyze_material(
            material_id=request.material_id
        )

        return FullAnalysisResponse(**result)

    except ValueError as e:
        logger.warning(f"Material not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error during material analysis")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"分析失败: {str(e)}"
        )


@router.post("/analyze/emotion", response_model=EmotionResponse)
async def analyze_emotion(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    分析Material的情感色彩

    Args:
        request: 分析请求
        db: 数据库会话

    Returns:
        情感分析结果
    """
    try:
        material_repo = MaterialRepository(db)
        material = await material_repo.get_by_id(request.material_id)

        if not material:
            raise ValueError(f"Material不存在: {request.material_id}")

        insight_service = InsightService(db)
        result = await insight_service.analyze_emotion(
            material=material,
            use_cache=not request.force_refresh
        )

        return EmotionResponse(
            material_id=str(material.id),
            primary_emotion=result.primary_emotion.value,
            confidence=result.confidence,
            description=result.description,
            emotion_distribution=result.emotion_distribution
        )

    except ValueError as e:
        logger.warning(f"Material not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error during emotion analysis")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"情感分析失败: {str(e)}"
        )


@router.post("/analyze/tags", response_model=TagsResponse)
async def generate_tags(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    为Material生成描述性标签

    Args:
        request: 分析请求
        db: 数据库会话

    Returns:
        标签生成结果
    """
    try:
        material_repo = MaterialRepository(db)
        material = await material_repo.get_by_id(request.material_id)

        if not material:
            raise ValueError(f"Material不存在: {request.material_id}")

        insight_service = InsightService(db)
        result = await insight_service.generate_tags(material)

        return TagsResponse(
            material_id=str(material.id),
            tags=result.tags,
            categories=result.categories
        )

    except ValueError as e:
        logger.warning(f"Material not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error during tag generation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"标签生成失败: {str(e)}"
        )


@router.post("/analyze/description", response_model=DescriptionResponse)
async def generate_description(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    为Material生成内容描述

    Args:
        request: 分析请求
        db: 数据库会话

    Returns:
        内容描述结果
    """
    try:
        material_repo = MaterialRepository(db)
        material = await material_repo.get_by_id(request.material_id)

        if not material:
            raise ValueError(f"Material不存在: {request.material_id}")

        insight_service = InsightService(db)
        result = await insight_service.generate_description(material)

        return DescriptionResponse(
            material_id=str(material.id),
            summary=result.summary,
            description=result.description,
            key_elements=result.key_elements
        )

    except ValueError as e:
        logger.warning(f"Material not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error during description generation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"描述生成失败: {str(e)}"
        )


@router.get("/material/{material_id}")
async def get_material_analysis(
    material_id: str,
    db: Session = Depends(get_db)
):
    """
    获取Material的完整分析结果（从缓存）

    如果Material未被分析过，返回404

    Args:
        material_id: Material ID
        db: 数据库会话

    Returns:
        Material的完整分析结果
    """
    try:
        material_repo = MaterialRepository(db)
        material = await material_repo.get_by_id(material_id)

        if not material:
            raise ValueError(f"Material不存在: {material_id}")

        # 检查是否有分析结果
        if not material.properties.get("emotion_analysis"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="该Material尚未进行AI分析"
            )

        return {
            "material_id": str(material.id),
            "name": material.name,
            "type": material.type,
            "tags": material.tags,
            "emotional_score": material.emotional_score,
            "emotion_analysis": material.properties.get("emotion_analysis"),
            "content_description": material.properties.get("content_description"),
            "tag_categories": material.properties.get("tag_categories"),
            "created_at": material.created_at.isoformat(),
            "updated_at": material.updated_at.isoformat() if material.updated_at else None
        }

    except ValueError as e:
        logger.warning(f"Material not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error getting material analysis")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取分析结果失败: {str(e)}"
        )
