"""
情感分析服务

使用AI分析Material内容，提取情感、标签、描述等信息
"""

import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import json
import logging

from sqlalchemy.orm import Session
from sqlalchemy import and_

from core.data_bunker.models import Material, MaterialType
from core.data_bunker.repositories.MaterialRepository import MaterialRepository
from .VolcEngineClient import get_ai_client, ModelType

logger = logging.getLogger(__name__)


class EmotionType(str, Enum):
    """情感类型枚举"""
    JOY = "joy"  # 喜悦
    SADNESS = "sadness"  # 悲伤
    CALM = "calm"  # 平静
    EXCITEMENT = "excitement"  # 兴奋
    NOSTALGIA = "nostalgia"  # 怀旧
    ANGER = "anger"  # 愤怒
    FEAR = "fear"  # 恐惧
    LOVE = "love"  # 爱
    SURPRISE = "surprise"  # 惊讶
    NEUTRAL = "neutral"  # 中性


class EmotionAnalysisResult:
    """情感分析结果"""
    def __init__(
        self,
        primary_emotion: EmotionType,
        confidence: float,
        emotion_distribution: Dict[str, float],
        description: str
    ):
        self.primary_emotion = primary_emotion  # 主要情感
        self.confidence = confidence  # 置信度（0-1）
        self.emotion_distribution = emotion_distribution  # 情感分布
        self.description = description  # 情感描述


class TagGenerationResult:
    """标签生成结果"""
    def __init__(
        self,
        tags: List[str],
        categories: Dict[str, List[str]]
    ):
        self.tags = tags  # 所有标签
        self.categories = categories  # 按类别分组的标签
        # 例如: {"人物": ["张三", "李四"], "地点": ["北京", "公园"]}


class ContentDescriptionResult:
    """内容描述结果"""
    def __init__(
        self,
        description: str,
        summary: str,
        key_elements: List[str]
    ):
        self.description = description  # 详细描述
        self.summary = summary  # 简短摘要
        self.key_elements = key_elements  # 关键元素列表


class InsightService:
    """洞察服务 - AI分析Material内容"""

    def __init__(self, db: Session):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db
        self.material_repo = MaterialRepository(db)
        self.ai_client = get_ai_client()

    async def analyze_emotion(
        self,
        material: Material,
        use_cache: bool = True
    ) -> EmotionAnalysisResult:
        """
        分析Material的情感色彩

        Args:
            material: 待分析的Material对象
            use_cache: 是否使用缓存（如果已有分析结果）

        Returns:
            情感分析结果
        """
        # 检查缓存
        if use_cache and material.properties.get("emotion_analysis"):
            cached = material.properties["emotion_analysis"]
            return EmotionAnalysisResult(
                primary_emotion=EmotionType(cached["primary_emotion"]),
                confidence=cached["confidence"],
                emotion_distribution=cached["emotion_distribution"],
                description=cached["description"]
            )

        # 根据Material类型选择分析方法
        if material.type == MaterialType.IMAGE.value:
            return await self._analyze_image_emotion(material)
        elif material.type in [MaterialType.TEXT.value, MaterialType.OTHER.value]:
            return await self._analyze_text_emotion(material)
        elif material.type == MaterialType.VIDEO.value:
            return await self._analyze_video_emotion(material)
        elif material.type == MaterialType.AUDIO.value:
            return await self._analyze_audio_emotion(material)
        else:
            # 默认返回中性情感
            return EmotionAnalysisResult(
                primary_emotion=EmotionType.NEUTRAL,
                confidence=0.5,
                emotion_distribution={"neutral": 1.0},
                description="无法分析情感"
            )

    async def _analyze_image_emotion(
        self,
        material: Material
    ) -> EmotionAnalysisResult:
        """分析图片的情感"""
        prompt = """
        请分析这张图片的情感色彩。

        返回JSON格式，包含以下字段：
        1. primary_emotion: 主要情感类型（从以下选择：joy, sadness, calm, excitement, nostalgia, anger, fear, love, surprise, neutral）
        2. confidence: 置信度（0-1之间的浮点数）
        3. emotion_distribution: 各情感的强度分布（0-1之间的浮点数），例如：{"joy": 0.8, "calm": 0.2}
        4. description: 用一句话描述这张图片传达的情感（中文）

        例如：
        {
          "primary_emotion": "joy",
          "confidence": 0.85,
          "emotion_distribution": {"joy": 0.85, "excitement": 0.15},
          "description": "这张照片展现了人们欢乐聚会的场景，充满了幸福的氛围"
        }
        """

        try:
            response = await self.ai_client.analyze_image(
                image_path=material.path,
                prompt=prompt,
                system_prompt="你是一个专业的情感分析专家，擅长从视觉内容中识别情感色彩。",
                model=ModelType.DEEPSEEK_V3.value
            )

            # 解析JSON响应
            result = json.loads(response)

            return EmotionAnalysisResult(
                primary_emotion=EmotionType(result["primary_emotion"]),
                confidence=float(result["confidence"]),
                emotion_distribution=result["emotion_distribution"],
                description=result["description"]
            )

        except Exception as e:
            logger.error(f"图片情感分析失败: {e}")
            # 返回默认中性情感
            return EmotionAnalysisResult(
                primary_emotion=EmotionType.NEUTRAL,
                confidence=0.5,
                emotion_distribution={"neutral": 1.0},
                description="情感分析暂时不可用"
            )

    async def _analyze_text_emotion(
        self,
        material: Material
    ) -> EmotionAnalysisResult:
        """分析文本的情感"""
        # 读取文本内容
        try:
            with open(material.path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        except Exception as e:
            logger.error(f"读取文本文件失败: {e}")
            return EmotionAnalysisResult(
                primary_emotion=EmotionType.NEUTRAL,
                confidence=0.5,
                emotion_distribution={"neutral": 1.0},
                description="无法读取文本内容"
            )

        prompt = """
        请分析以下文本内容的情感色彩。

        返回JSON格式，包含以下字段：
        1. primary_emotion: 主要情感类型（从以下选择：joy, sadness, calm, excitement, nostalgia, anger, fear, love, surprise, neutral）
        2. confidence: 置信度（0-1之间的浮点数）
        3. emotion_distribution: 各情感的强度分布（0-1之间的浮点数）
        4. description: 用一句话描述这段文本传达的情感（中文）
        """

        try:
            response = await self.ai_client.analyze_text(
                text=text_content,
                prompt=prompt,
                system_prompt="你是一个专业的情感分析专家，擅长从文字中识别情感色彩。",
                model=ModelType.DEEPSEEK_V3.value
            )

            result = json.loads(response)

            return EmotionAnalysisResult(
                primary_emotion=EmotionType(result["primary_emotion"]),
                confidence=float(result["confidence"]),
                emotion_distribution=result["emotion_distribution"],
                description=result["description"]
            )

        except Exception as e:
            logger.error(f"文本情感分析失败: {e}")
            return EmotionAnalysisResult(
                primary_emotion=EmotionType.NEUTRAL,
                confidence=0.5,
                emotion_distribution={"neutral": 1.0},
                description="情感分析暂时不可用"
            )

    async def _analyze_video_emotion(
        self,
        material: Material
    ) -> EmotionAnalysisResult:
        """分析视频的情感（简化版：基于封面和元数据）"""
        # TODO: 实现视频情感分析（可以抽帧分析）
        # 暂时返回中性情感
        return EmotionAnalysisResult(
            primary_emotion=EmotionType.NEUTRAL,
            confidence=0.5,
            emotion_distribution={"neutral": 1.0},
            description="视频情感分析功能开发中"
        )

    async def _analyze_audio_emotion(
        self,
        material: Material
    ) -> EmotionAnalysisResult:
        """分析音频的情感（简化版）"""
        # TODO: 实现音频情感分析（需要转文字）
        # 暂时返回中性情感
        return EmotionAnalysisResult(
            primary_emotion=EmotionType.NEUTRAL,
            confidence=0.5,
            emotion_distribution={"neutral": 1.0},
            description="音频情感分析功能开发中"
        )

    async def generate_tags(
        self,
        material: Material,
        max_tags: int = 10
    ) -> TagGenerationResult:
        """
        为Material生成描述性标签

        Args:
            material: Material对象
            max_tags: 最大标签数量

        Returns:
            标签生成结果
        """
        # 检查缓存
        if material.tags and len(material.tags) > 0:
            # 已有标签，按类别分组
            return TagGenerationResult(
                tags=material.tags,
                categories={"all": material.tags}
            )

        if material.type == MaterialType.IMAGE.value:
            return await self._generate_image_tags(material, max_tags)
        elif material.type in [MaterialType.TEXT.value, MaterialType.OTHER.value]:
            return await self._generate_text_tags(material, max_tags)
        else:
            return TagGenerationResult(tags=[], categories={})

    async def _generate_image_tags(
        self,
        material: Material,
        max_tags: int
    ) -> TagGenerationResult:
        """为图片生成标签"""
        prompt = f"""
        请分析这张图片，生成{max_tags}个描述性标签。

        返回JSON格式，包含以下字段：
        1. tags: 标签列表（中文，最多{max_tags}个）
        2. categories: 按类别分组的标签，包括：
           - 人物（person）
           - 地点（location）
           - 物体（object）
           - 活动（activity）
           - 主题（theme）
           - 其他（other）

        例如：
        {{
          "tags": ["海滩", "日落", "朋友", "度假", "夏天"],
          "categories": {{
            "person": ["朋友"],
            "location": ["海滩"],
            "object": ["太阳"],
            "activity": ["度假"],
            "theme": ["夏天", "自由"],
            "other": []
          }}
        }}
        """

        try:
            response = await self.ai_client.analyze_image(
                image_path=material.path,
                prompt=prompt,
                system_prompt="你是一个专业的内容分析师，擅长从图片中识别关键元素和主题。",
                model=ModelType.DEEPSEEK_V3.value
            )

            result = json.loads(response)

            return TagGenerationResult(
                tags=result["tags"],
                categories=result["categories"]
            )

        except Exception as e:
            logger.error(f"图片标签生成失败: {e}")
            return TagGenerationResult(tags=[], categories={})

    async def _generate_text_tags(
        self,
        material: Material,
        max_tags: int
    ) -> TagGenerationResult:
        """为文本生成标签"""
        try:
            with open(material.path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        except Exception as e:
            logger.error(f"读取文本文件失败: {e}")
            return TagGenerationResult(tags=[], categories={})

        prompt = f"""
        请分析以下文本，生成{max_tags}个描述性标签。

        返回JSON格式，包含以下字段：
        1. tags: 标签列表（中文，最多{max_tags}个）
        2. categories: 按类别分组的标签，包括：
           - 人物（person）
           - 地点（location）
           - 事件（event）
           - 主题（theme）
           - 关键词（keyword）
           - 其他（other）

        待分析文本：
        """

        try:
            response = await self.ai_client.analyze_text(
                text=text_content,
                prompt=prompt,
                system_prompt="你是一个专业的内容分析师，擅长从文本中提取关键信息。",
                model=ModelType.DEEPSEEK_V3.value
            )

            result = json.loads(response)

            return TagGenerationResult(
                tags=result["tags"],
                categories=result["categories"]
            )

        except Exception as e:
            logger.error(f"文本标签生成失败: {e}")
            return TagGenerationResult(tags=[], categories={})

    async def generate_description(
        self,
        material: Material
    ) -> ContentDescriptionResult:
        """
        为Material生成内容描述

        Args:
            material: Material对象

        Returns:
            内容描述结果
        """
        # 检查缓存
        if material.properties.get("content_description"):
            cached = material.properties["content_description"]
            return ContentDescriptionResult(
                description=cached["description"],
                summary=cached["summary"],
                key_elements=cached["key_elements"]
            )

        if material.type == MaterialType.IMAGE.value:
            return await self._generate_image_description(material)
        elif material.type in [MaterialType.TEXT.value, MaterialType.OTHER.value]:
            return await self._generate_text_description(material)
        else:
            return ContentDescriptionResult(
                description="暂不支持此类型的描述生成",
                summary="N/A",
                key_elements=[]
            )

    async def _generate_image_description(
        self,
        material: Material
    ) -> ContentDescriptionResult:
        """为图片生成描述"""
        prompt = """
        请详细描述这张图片的内容。

        返回JSON格式，包含以下字段：
        1. description: 详细描述（100-200字，中文）
        2. summary: 一句话摘要（20-30字，中文）
        3. key_elements: 关键元素列表（5-10个，中文）

        例如：
        {
          "description": "这是一张拍摄于夏日黄昏时分的照片。画面中，几位年轻人正坐在海滩上，眺望远方的日落。天空呈现出橙红色和紫色的渐变，海面波光粼粼。大家的脸上洋溢着幸福的笑容，享受着美好的时光。",
          "summary": "年轻人在海滩上欣赏日落，氛围轻松愉快",
          "key_elements": ["海滩", "日落", "年轻人", "笑容", "大海", "黄昏", "聚会", "休闲"]
        }
        """

        try:
            response = await self.ai_client.analyze_image(
                image_path=material.path,
                prompt=prompt,
                system_prompt="你是一个专业的内容描述专家，擅长用生动准确的语言描述视觉内容。",
                model=ModelType.DEEPSEEK_V3.value
            )

            result = json.loads(response)

            return ContentDescriptionResult(
                description=result["description"],
                summary=result["summary"],
                key_elements=result["key_elements"]
            )

        except Exception as e:
            logger.error(f"图片描述生成失败: {e}")
            return ContentDescriptionResult(
                description="描述生成失败",
                summary="N/A",
                key_elements=[]
            )

    async def _generate_text_description(
        self,
        material: Material
    ) -> ContentDescriptionResult:
        """为文本生成描述"""
        try:
            with open(material.path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        except Exception as e:
            logger.error(f"读取文本文件失败: {e}")
            return ContentDescriptionResult(
                description="无法读取文本",
                summary="N/A",
                key_elements=[]
            )

        prompt = """
        请分析以下文本内容，生成描述信息。

        返回JSON格式，包含以下字段：
        1. description: 详细描述（100-200字，中文）
        2. summary: 一句话摘要（20-30字，中文）
        3. key_elements: 关键元素列表（5-10个，中文）
        """

        try:
            response = await self.ai_client.analyze_text(
                text=text_content,
                prompt=prompt,
                system_prompt="你是一个专业的内容分析专家，擅长总结文本要点。",
                model=ModelType.DEEPSEEK_V3.value
            )

            result = json.loads(response)

            return ContentDescriptionResult(
                description=result["description"],
                summary=result["summary"],
                key_elements=result["key_elements"]
            )

        except Exception as e:
            logger.error(f"文本描述生成失败: {e}")
            return ContentDescriptionResult(
                description="描述生成失败",
                summary="N/A",
                key_elements=[]
            )

    async def analyze_material(
        self,
        material_id: str
    ) -> Dict:
        """
        完整分析Material（情感+标签+描述）

        Args:
            material_id: Material ID

        Returns:
            分析结果字典
        """
        material = await self.material_repo.get_by_id(material_id)
        if not material:
            raise ValueError(f"Material不存在: {material_id}")

        # 并行执行三个分析任务
        emotion_result, tag_result, description_result = await asyncio.gather(
            self.analyze_emotion(material),
            self.generate_tags(material),
            self.generate_description(material)
        )

        # 更新Material
        material.tags = tag_result.tags
        material.emotional_score = emotion_result.confidence
        material.properties["emotion_analysis"] = {
            "primary_emotion": emotion_result.primary_emotion.value,
            "confidence": emotion_result.confidence,
            "emotion_distribution": emotion_result.emotion_distribution,
            "description": emotion_result.description
        }
        material.properties["content_description"] = {
            "description": description_result.description,
            "summary": description_result.summary,
            "key_elements": description_result.key_elements
        }
        material.properties["tag_categories"] = tag_result.categories
        material.updated_at = datetime.utcnow()

        # 保存到数据库
        await self.material_repo.update(material)

        logger.info(f"Material {material_id} 分析完成")

        return {
            "material_id": str(material.id),
            "emotion": {
                "primary": emotion_result.primary_emotion.value,
                "confidence": emotion_result.confidence,
                "description": emotion_result.description
            },
            "tags": tag_result.tags,
            "tag_categories": tag_result.categories,
            "description": {
                "summary": description_result.summary,
                "detail": description_result.description
            }
        }
