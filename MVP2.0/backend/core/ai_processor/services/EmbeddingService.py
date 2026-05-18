"""
Embedding生成服务

将Material内容转换为向量表示，用于相似度计算和关系构建
"""

import asyncio
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import base64

from sqlalchemy.orm import Session

from core.data_bunker.models import Material, MaterialType
from core.data_bunker.repositories.MaterialRepository import MaterialRepository
from .VolcEngineClient import get_ai_client

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Embedding生成服务 - 将内容转为向量"""

    def __init__(self, db: Session):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db
        self.material_repo = MaterialRepository(db)
        self.ai_client = get_ai_client()

    async def generate_text_embedding(
        self,
        text: str,
        model: Optional[str] = None
    ) -> List[float]:
        """
        为文本生成embedding向量

        Args:
            text: 待处理的文本
            model: 模型名称（可选）

        Returns:
            embedding向量（浮点数列表）
        """
        try:
            # 使用火山方舟的embedding API
            # 注意：DeepSeek v3本身不提供embedding接口
            # 这里我们使用chat接口让模型生成一个简化的向量表示
            # 或者未来可以切换到专门的embedding模型

            prompt = f"""
            请为以下文本生成一个简化的向量表示。
            将文本的情感、主题、关键元素映射为一个10维的数值列表。
            每个维度范围0-1，表示不同特征的重要性。

            文本：{text[:500]}

            只返回JSON格式的数组，例如：[0.8, 0.3, 0.9, 0.1, ...]
            不要返回其他内容。
            """

            response = await self.ai_client.chat(
                prompt=prompt,
                system_prompt="你是一个文本特征提取专家，擅长将文本转换为数值向量表示。",
                model=model,
                response_format={"type": "json_object"}
            )

            # 解析JSON响应
            import json
            vector = json.loads(response)
            if isinstance(vector, dict) and "vector" in vector:
                embedding = vector["vector"]
            elif isinstance(vector, list):
                embedding = vector
            else:
                raise ValueError(f"无法解析embedding响应: {response}")

            # 确保是10维向量
            if len(embedding) > 10:
                embedding = embedding[:10]
            elif len(embedding) < 10:
                embedding = embedding + [0.0] * (10 - len(embedding))

            return embedding

        except Exception as e:
            logger.error(f"文本embedding生成失败: {e}")
            # 返回零向量
            return [0.0] * 10

    async def generate_image_embedding(
        self,
        image_path: str,
        description: Optional[str] = None,
        model: Optional[str] = None
    ) -> List[float]:
        """
        为图片生成embedding向量

        Args:
            image_path: 图片路径
            description: 图片描述（可选，用于辅助生成）
            model: 模型名称（可选）

        Returns:
            embedding向量（浮点数列表）
        """
        try:
            # 构建提示词
            prompt = """
            请分析这张图片，生成一个10维的特征向量。
            向量应该反映：
            1. 情感强度（0-1）
            2. 主题丰富度（0-1）
            3. 人物数量密度（0-1）
            4. 场景复杂度（0-1）
            5. 色彩饱和度（0-1）
            6. 亮度（0-1）
            7. 构图平衡性（0-1）
            8. 动态感（0-1）
            9. 温暖度（0-1）
            10. 活跃度（0-1）

            只返回JSON格式的数组，例如：[0.8, 0.3, 0.9, 0.1, ...]
            """

            if description:
                prompt = f"""
                {prompt}

                附加信息：这张图片的描述是：{description}
                """

            response = await self.ai_client.analyze_image(
                image_path=image_path,
                prompt=prompt,
                system_prompt="你是一个视觉特征提取专家，擅长将图像转换为数值向量表示。",
                model=model
            )

            # 解析JSON响应
            import json
            vector = json.loads(response)
            if isinstance(vector, dict) and "vector" in vector:
                embedding = vector["vector"]
            elif isinstance(vector, list):
                embedding = vector
            else:
                raise ValueError(f"无法解析embedding响应: {response}")

            # 确保是10维向量
            if len(embedding) > 10:
                embedding = embedding[:10]
            elif len(embedding) < 10:
                embedding = embedding + [0.0] * (10 - len(embedding))

            return embedding

        except Exception as e:
            logger.error(f"图片embedding生成失败: {e}")
            # 返回零向量
            return [0.0] * 10

    async def generate_material_embedding(
        self,
        material: Material,
        model: Optional[str] = None
    ) -> Dict[str, List[float]]:
        """
        为Material生成完整的embedding

        Args:
            material: Material对象
            model: 模型名称（可选）

        Returns:
            字典，包含text_embedding和image_embedding
        """
        result = {
            "text_embedding": [0.0] * 10,
            "image_embedding": [0.0] * 10
        }

        # 检查缓存
        if material.properties.get("embeddings"):
            logger.info(f"Material {material.id} 的embedding已存在，使用缓存")
            return material.properties["embeddings"]

        try:
            # 并行生成text和image embedding
            tasks = []

            # 图片embedding
            if material.type == MaterialType.IMAGE.value:
                # 尝试从已有描述生成
                desc = None
                if material.properties.get("content_description"):
                    desc = material.properties["content_description"].get("summary")

                tasks.append(
                    self.generate_image_embedding(material.path, desc, model)
                )

            # 文本embedding
            elif material.type in [MaterialType.TEXT.value, MaterialType.OTHER.value]:
                # 读取文本内容
                try:
                    with open(material.path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                        # 限制长度
                        text_content = text_content[:1000]

                        tasks.append(
                            self.generate_text_embedding(text_content, model)
                        )
                except Exception as e:
                    logger.error(f"读取文本失败: {e}")
            else:
                # 视频和音频暂不支持
                logger.warning(f"Material类型 {material.type} 暂不支持embedding生成")

            # 执行任务
            if tasks:
                embeddings = await asyncio.gather(*tasks)

                if len(embeddings) == 1:
                    if material.type == MaterialType.IMAGE.value:
                        result["image_embedding"] = embeddings[0]
                    else:
                        result["text_embedding"] = embeddings[0]
                elif len(embeddings) == 2:
                    result["text_embedding"] = embeddings[0]
                    result["image_embedding"] = embeddings[1]

            # 保存到properties
            material.properties["embeddings"] = result
            material.updated_at = datetime.utcnow()
            await self.material_repo.update(material)

            logger.info(f"Material {material.id} 的embedding生成完成")

            return result

        except Exception as e:
            logger.exception(f"Material embedding生成失败")
            return result

    async def batch_generate_embeddings(
        self,
        material_ids: List[str],
        model: Optional[str] = None
    ) -> Dict[str, Dict[str, List[float]]]:
        """
        批量生成多个Material的embedding

        Args:
            material_ids: Material ID列表
            model: 模型名称（可选）

        Returns:
            字典，material_id -> embedding字典
        """
        results = {}

        for material_id in material_ids:
            try:
                material = await self.material_repo.get_by_id(material_id)
                if material:
                    embedding = await self.generate_material_embedding(material, model)
                    results[material_id] = embedding

                    # 避免API限流，添加延迟
                    await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"Material {material_id} embedding生成失败: {e}")
                results[material_id] = {
                    "text_embedding": [0.0] * 10,
                    "image_embedding": [0.0] * 10
                }

        return results
