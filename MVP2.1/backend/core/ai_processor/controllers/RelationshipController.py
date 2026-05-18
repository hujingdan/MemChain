"""
关系和Embedding API控制器

提供Material关系构建和Embedding生成的API端点
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.ai_processor.services.EmbeddingService import EmbeddingService
from core.ai_processor.services.SimilarityService import SimilarityService
from core.ai_processor.services.RelationshipService import RelationshipService, RelationStrategy
from core.data_bunker.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


# ==================== 请求/响应模型 ====================

class GenerateEmbeddingRequest(BaseModel):
    """生成Embedding请求"""
    material_id: str = Field(..., description="Material ID")
    force_refresh: bool = Field(False, description="是否强制重新生成")


class EmbeddingResponse(BaseModel):
    """Embedding响应"""
    material_id: str
    text_embedding: List[float] = Field(..., description="文本向量（10维）")
    image_embedding: List[float] = Field(..., description="图像向量（10维）")


class SimilarityRequest(BaseModel):
    """相似度计算请求"""
    material_a_id: str = Field(..., description="Material A的ID")
    material_b_id: str = Field(..., description="Material B的ID")
    method: str = Field("cosine", description="计算方法：cosine, euclidean, manhattan")


class SimilarityResponse(BaseModel):
    """相似度响应"""
    material_a_id: str
    material_b_id: str
    overall: float = Field(..., description="综合相似度（0-1）")
    text_similarity: float = Field(..., description="文本相似度")
    image_similarity: float = Field(..., description="图像相似度")
    method: str = Field(..., description="计算方法")


class BuildRelationshipsRequest(BaseModel):
    """构建关系请求"""
    material_id: str = Field(..., description="Material ID")
    strategy: str = Field("hybrid", description="构建策略：semantic, temporal, thematic, hybrid")
    max_relationships: int = Field(10, description="最大关系数量", ge=1, le=50)
    similarity_threshold: float = Field(0.65, description="相似度阈值（0-1）", ge=0, le=1)
    temporal_threshold_hours: int = Field(24, description="时间阈值（小时）", ge=1, le=720)


class RelationshipResponse(BaseModel):
    """关系响应"""
    material_id: str
    relationships: List[Dict[str, Any]] = Field(..., description="创建的关系列表")
    count: int = Field(..., description="关系数量")


class GetRelatedRequest(BaseModel):
    """获取相关Material请求"""
    material_id: str
    min_strength: float = Field(0.5, description="最小关系强度", ge=0, le=1)


class RelatedMaterialsResponse(BaseModel):
    """相关Material响应"""
    material_id: str
    related_materials: List[Dict[str, Any]]


# ==================== API端点 ====================

@router.post("/embedding/generate", response_model=EmbeddingResponse)
async def generate_embedding(
    request: GenerateEmbeddingRequest,
    db: Session = Depends(get_db)
):
    """
    为Material生成Embedding向量

    将Material内容转换为10维向量表示，用于后续的相似度计算

    Args:
        request: 生成请求
        db: 数据库会话

    Returns:
        Embedding向量
    """
    try:
        embedding_service = EmbeddingService(db)
        material_repo = embedding_service.material_repo

        material = await material_repo.get_by_id(request.material_id)
        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Material不存在: {request.material_id}"
            )

        # 生成embedding
        embeddings = await embedding_service.generate_material_embedding(
            material,
            force_refresh=request.force_refresh
        )

        return EmbeddingResponse(
            material_id=request.material_id,
            text_embedding=embeddings.get("text_embedding", [0.0] * 10),
            image_embedding=embeddings.get("image_embedding", [0.0] * 10)
        )

    except ValueError as e:
        logger.warning(f"Material not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error during embedding generation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Embedding生成失败: {str(e)}"
        )


@router.post("/similarity/calculate", response_model=SimilarityResponse)
async def calculate_similarity(
    request: SimilarityRequest,
    db: Session = Depends(get_db)
):
    """
    计算两个Material之间的相似度

    Args:
        request: 相似度计算请求
        db: 数据库会话

    Returns:
        相似度分数
    """
    try:
        similarity_service = SimilarityService(db)
        material_repo = similarity_service.material_repo

        # 验证Material存在
        material_a = await material_repo.get_by_id(request.material_a_id)
        material_b = await material_repo.get_by_id(request.material_b_id)

        if not material_a or not material_b:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="一个或两个Material不存在"
            )

        # 计算相似度
        similarity = await similarity_service.calculate_similarity(
            request.material_a_id,
            request.material_b_id,
            method=request.method
        )

        return SimilarityResponse(
            material_a_id=request.material_a_id,
            material_b_id=request.material_b_id,
            **similarity
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error during similarity calculation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"相似度计算失败: {str(e)}"
        )


@router.post("/relationships/build", response_model=RelationshipResponse)
async def build_relationships(
    request: BuildRelationshipsRequest,
    db: Session = Depends(get_db)
):
    """
    为Material构建关系

    根据指定策略自动发现相关Material并创建关系

    Args:
        request: 构建请求
        db: 数据库会话

    Returns:
        创建的关系列表
    """
    try:
        relationship_service = RelationshipService(db)

        # 映射策略字符串到枚举
        try:
            strategy = RelationStrategy(request.strategy)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的策略: {request.strategy}"
            )

        # 构建关系
        relationships = await relationship_service.build_relationships_for_material(
            material_id=request.material_id,
            strategy=strategy,
            max_relationships=request.max_relationships,
            similarity_threshold=request.similarity_threshold,
            temporal_threshold_hours=request.temporal_threshold_hours
        )

        return RelationshipResponse(
            material_id=request.material_id,
            relationships=relationships,
            count=len(relationships)
        )

    except ValueError as e:
        logger.warning(f"Material not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error during relationship building")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"关系构建失败: {str(e)}"
        )


@router.get("/relationships/{material_id}", response_model=RelatedMaterialsResponse)
async def get_related_materials(
    material_id: str,
    min_strength: float = Query(0.5, ge=0, le=1, description="最小关系强度"),
    db: Session = Depends(get_db)
):
    """
    获取与指定Material相关的所有Material

    Args:
        material_id: Material ID
        min_strength: 最小关系强度
        db: 数据库会话

    Returns:
        相关Material列表
    """
    try:
        relationship_service = RelationshipService(db)

        related = await relationship_service.get_related_materials(
            material_id=material_id,
            min_strength=min_strength
        )

        return RelatedMaterialsResponse(
            material_id=material_id,
            related_materials=related
        )

    except ValueError as e:
        logger.warning(f"Material not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error getting related materials")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取相关Material失败: {str(e)}"
        )


@router.post("/batch/build-relationships")
async def batch_build_relationships(
    user_id: Optional[str] = Query(None, description="用户ID（可选）"),
    strategy: str = Query("hybrid", description="构建策略"),
    max_per_material: int = Query(10, ge=1, le=50),
    similarity_threshold: float = Query(0.65, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    批量为所有Material构建关系

    Args:
        user_id: 用户ID（如果指定，只处理该用户的Material）
        strategy: 构建策略
        max_per_material: 每个Material的最大关系数
        similarity_threshold: 相似度阈值
        db: 数据库会话

    Returns:
        批量处理统计
    """
    try:
        relationship_service = RelationshipService(db)

        try:
            strategy = RelationStrategy(strategy)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的策略: {strategy}"
            )

        # 批量构建
        stats = await relationship_service.batch_build_relationships(
            user_id=user_id,
            strategy=strategy,
            max_per_material=max_per_material,
            similarity_threshold=similarity_threshold
        )

        return stats

    except Exception as e:
        logger.exception(f"Error during batch relationship building")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量关系构建失败: {str(e)}"
        )
