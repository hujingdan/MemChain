"""
相似度计算服务

计算两个Material之间的相似度，用于关系构建
"""

import logging
from typing import List, Dict, Tuple, Optional
import math

from sqlalchemy.orm import Session

from core.data_bunker.models import Material
from core.data_bunker.repositories.MaterialRepository import MaterialRepository

logger = logging.getLogger(__name__)


class SimilarityService:
    """相似度计算服务"""

    def __init__(self, db: Session):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db
        self.material_repo = MaterialRepository(db)

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        计算余弦相似度

        Args:
            vec_a: 向量A
            vec_b: 向量B

        Returns:
            相似度（0-1），1表示完全相同
        """
        try:
            if len(vec_a) != len(vec_b):
                raise ValueError(f"向量维度不匹配: {len(vec_a)} vs {len(vec_b)}")

            # 计算点积
            dot_product = sum(a * b for a, b in zip(vec_a, vec_b))

            # 计算模
            norm_a = math.sqrt(sum(a * a for a in vec_a))
            norm_b = math.sqrt(sum(b * b for b in vec_b))

            # 避免除零
            if norm_a == 0 or norm_b == 0:
                return 0.0

            # 余弦相似度 = 点积 / (模A * 模B)
            similarity = dot_product / (norm_a * norm_b)

            # 确保在[0, 1]范围内
            return max(0.0, min(1.0, similarity))

        except Exception as e:
            logger.error(f"余弦相似度计算失败: {e}")
            return 0.0

    @staticmethod
    def euclidean_distance(vec_a: List[float], vec_b: List[float]) -> float:
        """
        计算欧几里得距离

        Args:
            vec_a: 向量A
            vec_b: 向量B

        Returns:
            距离（0-∞），0表示完全相同
        """
        try:
            if len(vec_a) != len(vec_b):
                raise ValueError(f"向量维度不匹配: {len(vec_a)} vs {len(vec_b)}")

            # 欧几里得距离 = sqrt(sum((a-b)^2))
            distance = math.sqrt(
                sum((a - b) ** 2 for a, b in zip(vec_a, vec_b))
            )

            return distance

        except Exception as e:
            logger.error(f"欧几里得距离计算失败: {e}")
            return float('inf')

    @staticmethod
    def manhattan_distance(vec_a: List[float], vec_b: List[float]) -> float:
        """
        计算曼哈顿距离

        Args:
            vec_a: 向量A
            vec_b: 向量B

        Returns:
            距离（0-∞），0表示完全相同
        """
        try:
            if len(vec_a) != len(vec_b):
                raise ValueError(f"向量维度不匹配: {len(vec_a)} vs {len(vec_b)}")

            # 曼哈顿距离 = sum(|a-b|)
            distance = sum(abs(a - b) for a, b in zip(vec_a, vec_b))

            return distance

        except Exception as e:
            logger.error(f"曼哈顿距离计算失败: {e}")
            return float('inf')

    async def calculate_similarity(
        self,
        material_a_id: str,
        material_b_id: str,
        method: str = "cosine"
    ) -> Dict[str, float]:
        """
        计算两个Material之间的相似度

        Args:
            material_a_id: Material A的ID
            material_b_id: Material B的ID
            method: 相似度计算方法（cosine, euclidean, manhattan）

        Returns:
            字典，包含各维度的相似度分数
        """
        # 获取Material
        material_a = await self.material_repo.get_by_id(material_a_id)
        material_b = await self.material_repo.get_by_id(material_b_id)

        if not material_a or not material_b:
            logger.error(f"Material不存在: {material_a_id} 或 {material_b_id}")
            return {
                "overall": 0.0,
                "text_similarity": 0.0,
                "image_similarity": 0.0,
                "method": method
            }

        # 获取embeddings
        embeddings_a = material_a.properties.get("embeddings", {})
        embeddings_b = material_b.properties.get("embeddings", {})

        if not embeddings_a or not embeddings_b:
            logger.warning(f"Material缺少embedding数据")
            return {
                "overall": 0.0,
                "text_similarity": 0.0,
                "image_similarity": 0.0,
                "method": method
            }

        # 提取向量
        text_emb_a = embeddings_a.get("text_embedding", [0.0] * 10)
        image_emb_a = embeddings_a.get("image_embedding", [0.0] * 10)
        text_emb_b = embeddings_b.get("text_embedding", [0.0] * 10)
        image_emb_b = embeddings_b.get("image_embedding", [0.0] * 10)

        # 计算相似度
        text_sim = 0.0
        image_sim = 0.0

        if method == "cosine":
            # 余弦相似度（0-1，越大越相似）
            text_sim = self.cosine_similarity(text_emb_a, text_emb_b)
            image_sim = self.cosine_similarity(image_emb_a, image_emb_b)
        elif method == "euclidean":
            # 欧几里得距离（0-∞，越小越相似，需要转换）
            text_dist = self.euclidean_distance(text_emb_a, text_emb_b)
            image_dist = self.euclidean_distance(image_emb_a, image_emb_b)
            # 转换为相似度（使用sigmoid函数）
            text_sim = 1.0 / (1.0 + math.exp(text_dist / 5.0))
            image_sim = 1.0 / (1.0 + math.exp(image_dist / 5.0))
        elif method == "manhattan":
            # 曼哈顿距离（0-∞，越小越相似，需要转换）
            text_dist = self.manhattan_distance(text_emb_a, text_emb_b)
            image_dist = self.manhattan_distance(image_emb_a, image_emb_b)
            # 转换为相似度
            text_sim = 1.0 / (1.0 + text_dist / 10.0)
            image_sim = 1.0 / (1.0 + image_dist / 10.0)
        else:
            logger.warning(f"未知的相似度计算方法: {method}，使用cosine")
            text_sim = self.cosine_similarity(text_emb_a, text_emb_b)
            image_sim = self.cosine_similarity(image_emb_a, image_emb_b)

        # 综合相似度（图像权重更高，因为视觉记忆更重要）
        # 如果有一个向量为零向量，则只使用另一个
        weights = [0.4, 0.6]  # [text, image]

        # 检查向量是否有效
        text_valid = any(v != 0.0 for v in text_emb_a + text_emb_b)
        image_valid = any(v != 0.0 for v in image_emb_a + image_emb_b)

        if text_valid and image_valid:
            # 都有效，使用加权平均
            overall_sim = weights[0] * text_sim + weights[1] * image_sim
        elif text_valid:
            # 只有文本有效
            overall_sim = text_sim
        elif image_valid:
            # 只有图像有效
            overall_sim = image_sim
        else:
            # 都无效
            overall_sim = 0.0

        return {
            "overall": round(overall_sim, 4),
            "text_similarity": round(text_sim, 4),
            "image_similarity": round(image_sim, 4),
            "method": method
        }

    async def calculate_temporal_proximity(
        self,
        material_a_id: str,
        material_b_id: str
    ) -> float:
        """
        计算时间临近性分数

        Args:
            material_a_id: Material A的ID
            material_b_id: Material B的ID

        Returns:
            时间临近性分数（0-1），1表示时间非常接近
        """
        material_a = await self.material_repo.get_by_id(material_a_id)
        material_b = await self.material_repo.get_by_id(material_b_id)

        if not material_a or not material_b:
            return 0.0

        if not material_a.created_at or not material_b.created_at:
            return 0.0

        # 计算时间差（秒）
        from datetime import datetime
        time_diff = abs(
            (material_a.created_at - material_b.created_at).total_seconds()
        )

        # 转换为时间临近性分数
        # 1小时以内 = 1.0
        # 1天以内 = 0.8
        # 1周以内 = 0.5
        # 1月以内 = 0.2
        # 更长 = 0.0

        if time_diff < 3600:  # 1小时
            return 1.0
        elif time_diff < 86400:  # 1天
            return 0.8
        elif time_diff < 604800:  # 1周
            return 0.5
        elif time_diff < 2592000:  # 1月
            return 0.2
        else:
            return 0.0

    async def find_similar_materials(
        self,
        material_id: str,
        threshold: float = 0.6,
        limit: int = 20,
        method: str = "cosine"
    ) -> List[Dict[str, any]]:
        """
        找出与指定Material相似的所有Material

        Args:
            material_id: Material ID
            threshold: 相似度阈值（0-1），只有高于此值的才会返回
            limit: 最大返回数量
            method: 相似度计算方法

        Returns:
            相似Material列表，每个元素包含material_id和similarity
        """
        # 获取所有Material
        all_materials = await self.material_repo.get_all()
        all_materials = [m for m in all_materials if m.id != material_id]

        results = []

        # 计算与每个Material的相似度
        for other_material in all_materials[:limit]:  # 限制数量避免太多计算
            similarity = await self.calculate_similarity(
                material_id,
                str(other_material.id),
                method
            )

            # 只保留高于阈值的
            if similarity["overall"] >= threshold:
                results.append({
                    "material_id": str(other_material.id),
                    "similarity": similarity
                })

        # 按相似度排序
        results.sort(key=lambda x: x["similarity"]["overall"], reverse=True)

        return results[:limit]
