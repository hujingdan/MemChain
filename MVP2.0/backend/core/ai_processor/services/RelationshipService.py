"""
关系构建服务

使用AI和相似度计算自动发现Material之间的关系
"""

import asyncio
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from core.data_bunker.models import Material, MaterialType, Relationship, RelationshipType
from core.data_bunker.repositories.MaterialRepository import MaterialRepository
from .SimilarityService import SimilarityService

logger = logging.getLogger(__name__)


class RelationStrategy(str, Enum):
    """关系构建策略"""
    SEMANTIC = "semantic"  # 基于语义相似度
    TEMPORAL = "temporal"  # 基于时间临近性
    THEMATIC = "thematic"  # 基于主题标签
    HYBRID = "hybrid"  # 混合策略


class RelationshipService:
    """关系构建服务 - 自动发现Material之间的关系"""

    def __init__(self, db: Session):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db
        self.material_repo = MaterialRepository(db)
        self.similarity_service = SimilarityService(db)

    async def build_relationships_for_material(
        self,
        material_id: str,
        strategy: RelationStrategy = RelationStrategy.HYBRID,
        max_relationships: int = 10,
        similarity_threshold: float = 0.65,
        temporal_threshold_hours: int = 24
    ) -> List[Dict]:
        """
        为指定Material构建关系

        Args:
            material_id: Material ID
            strategy: 关系构建策略
            max_relationships: 最大关系数量
            similarity_threshold: 相似度阈值（0-1）
            temporal_threshold_hours: 时间阈值（小时）

        Returns:
            创建的关系列表
        """
        material = await self.material_repo.get_by_id(material_id)
        if not material:
            raise ValueError(f"Material不存在: {material_id}")

        logger.info(f"开始为Material {material_id} 构建关系（策略: {strategy}）")

        relationships = []

        if strategy in [RelationStrategy.SEMANTIC, RelationStrategy.HYBRID]:
            # 语义相似度关系
            semantic_rels = await self._build_semantic_relationships(
                material,
                max_relationships,
                similarity_threshold
            )
            relationships.extend(semantic_rels)

        if strategy in [RelationStrategy.TEMPORAL, RelationStrategy.HYBRID]:
            # 时间临近性关系
            temporal_rels = await self._build_temporal_relationships(
                material,
                max_relationships,
                temporal_threshold_hours
            )
            relationships.extend(temporal_rels)

        if strategy in [RelationStrategy.THEMATIC, RelationStrategy.HYBRID]:
            # 主题标签关系
            thematic_rels = await self._build_thematic_relationships(
                material,
                max_relationships
            )
            relationships.extend(thematic_rels)

        # 去重并排序
        unique_rels = self._deduplicate_relationships(relationships)
        unique_rels.sort(key=lambda x: x["strength"], reverse=True)

        # 限制数量
        unique_rels = unique_rels[:max_relationships]

        # 保存到数据库
        for rel in unique_rels:
            await self._save_relationship(
                material_id,
                rel["target_id"],
                rel["relationship_type"],
                rel["strength"]
            )

        logger.info(f"为Material {material_id} 构建了{len(unique_rels)}个关系")

        return unique_rels

    async def _build_semantic_relationships(
        self,
        material: Material,
        max_count: int,
        threshold: float
    ) -> List[Dict]:
        """构建语义相似度关系"""
        results = []

        # 获取所有其他Material
        all_materials = await self.material_repo.get_all()
        others = [m for m in all_materials if m.id != material.id]

        # 逐一计算相似度
        for other in others[:max_count * 3]:  # 多计算一些，后面筛选
            similarity = await self.similarity_service.calculate_similarity(
                str(material.id),
                str(other.id),
                method="cosine"
            )

            # 只保留高于阈值的
            if similarity["overall"] >= threshold:
                # 确定关系类型
                if similarity["overall"] > 0.85:
                    rel_type = RelationshipType.EMOTIONAL_SIMILARITY.value
                elif similarity["overall"] > 0.75:
                    rel_type = RelationshipType.SAME_EVENT.value
                else:
                    rel_type = RelationshipType.SEMANTIC_SIMILARITY.value

                results.append({
                    "target_id": str(other.id),
                    "relationship_type": rel_type,
                    "strength": similarity["overall"],
                    "metadata": {
                        "method": "semantic_similarity",
                        "text_sim": similarity["text_similarity"],
                        "image_sim": similarity["image_similarity"]
                    }
                })

        return results

    async def _build_temporal_relationships(
        self,
        material: Material,
        max_count: int,
        threshold_hours: int
    ) -> List[Dict]:
        """构建时间临近性关系"""
        results = []

        # 获取所有其他Material
        all_materials = await self.material_repo.get_all()
        others = [m for m in all_materials if m.id != material.id]

        # 计算时间临近性
        for other in others[:max_count * 3]:
            # 检查是否在时间阈值内
            if not material.created_at or not other.created_at:
                continue

            time_diff = abs((material.created_at - other.created_at).total_seconds())

            if time_diff <= threshold_hours * 3600:  # 转换为秒
                # 计算时间临近性分数
                proximity_score = await self.similarity_service.calculate_temporal_proximity(
                    str(material.id),
                    str(other.id)
                )

                # 确定关系类型
                if proximity_score > 0.9:
                    rel_type = RelationshipType.TEMPORAL_PROXIMITY.value
                else:
                    rel_type = RelationshipType.SAME_EVENT.value

                results.append({
                    "target_id": str(other.id),
                    "relationship_type": rel_type,
                    "strength": proximity_score,
                    "metadata": {
                        "method": "temporal_proximity",
                        "time_diff_hours": time_diff / 3600
                    }
                })

        return results

    async def _build_thematic_relationships(
        self,
        material: Material,
        max_count: int
    ) -> List[Dict]:
        """构建主题标签关系"""
        results = []

        # 获取Material的标签
        if not material.tags:
            return results

        material_tags = set(material.tags)

        # 获取所有其他Material
        all_materials = await self.material_repo.get_all()
        others = [m for m in all_materials if m.id != material.id and m.tags]

        # 计算标签重叠度
        for other in others[:max_count * 3]:
            if not other.tags:
                continue

            other_tags = set(other.tags)

            # 计算Jaccard相似度 = |A∩B| / |A∪B|
            intersection = len(material_tags & other_tags)
            union = len(material_tags | other_tags)
            jaccard = intersection / union if union > 0 else 0

            # 只保留重叠度高的
            if jaccard >= 0.3:  # 至少30%标签重叠
                results.append({
                    "target_id": str(other.id),
                    "relationship_type": RelationshipType.THEMATIC_SIMILARITY.value,
                    "strength": jaccard,
                    "metadata": {
                        "method": "thematic_similarity",
                        "overlap_tags": list(material_tags & other_tags),
                        "jaccard_index": jaccard
                    }
                })

        return results

    def _deduplicate_relationships(self, relationships: List[Dict]) -> List[Dict]:
        """去重关系（同一对Material只保留最强的一个）"""
        seen = set()
        unique = []

        for rel in relationships:
            # 创建唯一键（排序确保一致性）
            key = tuple(sorted([rel["target_id"], rel["relationship_type"]]))

            if key not in seen:
                seen.add(key)
                unique.append(rel)

        return unique

    async def _save_relationship(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        strength: float
    ):
        """保存关系到数据库"""
        try:
            # 检查是否已存在
            # TODO: 实现数据库查询逻辑
            logger.debug(f"保存关系: {source_id} -> {target_id} ({rel_type}, {strength:.2f})")

        except Exception as e:
            logger.error(f"保存关系失败: {e}")
            await self.db.rollback()

    async def batch_build_relationships(
        self,
        user_id: Optional[str] = None,
        strategy: RelationStrategy = RelationStrategy.HYBRID,
        max_per_material: int = 10,
        similarity_threshold: float = 0.65
    ) -> Dict[str, int]:
        """
        批量为所有Material构建关系

        Args:
            user_id: 用户ID（如果指定，只处理该用户的Material）
            strategy: 关系构建策略
            max_per_material: 每个Material的最大关系数
            similarity_threshold: 相似度阈值

        Returns:
            统计信息字典
        """
        logger.info(f"开始批量构建关系（策略: {strategy}）")

        # 获取所有Material
        if user_id:
            materials = await self.material_repo.get_by_user(user_id)
        else:
            materials = await self.material_repo.get_all()

        total = len(materials)
        created_count = 0
        failed_count = 0

        # 逐个处理
        for idx, material in enumerate(materials):
            try:
                rels = await self.build_relationships_for_material(
                    str(material.id),
                    strategy=strategy,
                    max_relationships=max_per_material,
                    similarity_threshold=similarity_threshold
                )
                created_count += len(rels)

                # 避免API限流
                if idx < len(materials) - 1:
                    await asyncio.sleep(0.3)

            except Exception as e:
                logger.error(f"Material {material.id} 关系构建失败: {e}")
                failed_count += 1

        logger.info(f"批量关系构建完成：{created_count}个成功，{failed_count}个失败")

        return {
            "total_materials": total,
            "relationships_created": created_count,
            "relationships_failed": failed_count
        }

    async def get_relationships(
        self,
        material_id: str,
        relationship_type: Optional[str] = None
    ) -> List[Dict]:
        """
        获取Material的所有关系

        Args:
            material_id: Material ID
            relationship_type: 关系类型过滤（可选）

        Returns:
            关系列表
        """
        # TODO: 实现数据库查询逻辑
        return []

    async def get_related_materials(
        self,
        material_id: str,
        min_strength: float = 0.5
    ) -> List[Dict]:
        """
        获取相关的Material（带详细信息）

        Args:
            material_id: Material ID
            min_strength: 最小关系强度

        Returns:
            相关Material列表
        """
        relationships = await self.get_relationships(material_id)

        result = []
        for rel in relationships:
            if rel["strength"] >= min_strength:
                # 获取目标Material信息
                target_material = await self.material_repo.get_by_id(rel["target_id"])

                if target_material:
                    result.append({
                        "material": {
                            "id": str(target_material.id),
                            "name": target_material.name,
                            "type": target_material.type,
                            "created_at": target_material.created_at.isoformat()
                        },
                        "relationship": {
                            "type": rel["relationship_type"],
                            "strength": rel["strength"]
                        }
                    })

        # 按关系强度排序
        result.sort(key=lambda x: x["relationship"]["strength"], reverse=True)

        return result
