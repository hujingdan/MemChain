#本地电脑用的是 SQLite（轻量本地数据库，无需安装、开箱即用），适合本地跑项目
#PostgreSQL是大型云端数据库，适合部署上线

"""
核心职责：定义应用的数据库模型结构。
包含以下主要模型：

1. Material（素材）模型
   - id: UUID, 主键
   - user_id: UUID, 关联用户
   - type: Enum, 素材类型（图片、音频、文本等）
   - path: String, 存储路径
   - mime_type: String, 文件MIME类型
   - size: Integer, 文件大小
   - created_at: DateTime, 创建时间
   - metadata: JSON, 扩展元数据
   - tags: Array, 标签列表
   - emotional_score: Float, 情感分数
   - location: JSON, 地理位置信息
   - is_archived: Boolean, 归档状态

2. Knowledge（知识）模型
   - id: UUID, 主键
   - user_id: UUID, 关联用户
   - key_insight: Text, 核心洞察
   - pattern_type: Enum, 模式类型
   - confidence_score: Float, 可信度
   - related_materials: Array[UUID], 关联素材ID列表
   - generated_at: DateTime, 生成时间
   - last_reviewed_at: DateTime, 最后回顾时间
   - status: Enum, 状态（活跃、归档等）
   - context: JSON, 上下文信息

3. Relationship（关系）模型
   - id: UUID, 主键
   - source_id: UUID, 源素材ID
   - target_id: UUID, 目标素材ID
   - relationship_type: Enum, 关系类型
   - strength: Float, 关系强度
   - created_at: DateTime, 创建时间
   - metadata: JSON, 关系元数据

使用 SQLAlchemy ORM 进行模型定义，确保：
1. 类型安全
2. 关系完整性
3. 索引优化
4. 软删除支持
"""


# MVP/backend/core/data_bunker/models.py
import uuid
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional

from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Float, ForeignKey
# 注释掉PostgreSQL特有类型，使用跨平台替代方案
# from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class MaterialType(str, Enum):
    """素材类型枚举"""
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    TEXT = 'text'
    OTHER = 'other'

class Material(Base):
    """素材模型 - 第一阶段核心模型"""
    __tablename__ = 'materials'

    # 主键 - 替换为String(36)存储UUID，兼容SQLite
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    
    # 用户关联 - 替换为String(36)
    user_id = Column(String(36), index=True, nullable=False)
    
    # 核心元数据
    name = Column(String(255), nullable=False)
    type = Column(String(20), nullable=False)  # 使用MaterialType枚举的值
    path = Column(String(512), nullable=False, unique=True)
    mime_type = Column(String(100), nullable=False)
    size = Column(Integer, nullable=False)  # 文件大小（字节）
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    
    # 扩展元数据（JSON格式）
    properties = Column(JSON, nullable=False, default={})
    
    # 标签和情感分析（第一阶段预留字段）
    tags = Column(JSON, default=list, nullable=True)
    emotional_score = Column(Float, nullable=True)
    
    # 地理位置信息（预留）
    location = Column(JSON, nullable=True)
    
    # 状态管理
    is_archived = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # 软删除标志

    # 关系（第二阶段）
    knowledge_entries = relationship("Knowledge", back_populates="material")
    relationships = relationship("Relationship", back_populates="material")

    def __repr__(self):
        return f"<Material(id={self.id}, name='{self.name}', type='{self.type}')>"

    def to_dict(self) -> Dict:
        """将模型转换为字典（用于API响应）"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "type": self.type,
            "path": self.path,
            "mime_type": self.mime_type,
            "size": self.size,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,  # type: ignore
            "properties": self.properties,
            "tags": self.tags,
            "emotional_score": self.emotional_score,
            "location": self.location,
            "is_archived": self.is_archived,
            "is_deleted": self.is_deleted
        }

# 第二阶段模型（预留接口）
class KnowledgeType(str, Enum):
    """知识类型枚举"""
    EVENT = 'event'
    PERSON = 'person'
    LOCATION = 'location'
    EMOTION = 'emotion'
    THEME = 'theme'

class KnowledgeStatus(str, Enum):
    """知识状态枚举"""
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    REVIEW_NEEDED = 'review_needed'

class Knowledge(Base):
    """知识模型 - 第二阶段实现"""
    __tablename__ = 'knowledge'
    
    # 全部替换为String(36)兼容SQLite
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), index=True, nullable=False)
    material_id = Column(String(36), ForeignKey('materials.id'), nullable=False)
    
    key_insight = Column(String(500), nullable=False)
    pattern_type = Column(String(50), nullable=False)  # 使用KnowledgeType枚举的值
    confidence_score = Column(Float, default=0.0)
    
    generated_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed_at = Column(DateTime, nullable=True)
    
    status = Column(String(20), default=KnowledgeStatus.ACTIVE)  # 使用KnowledgeStatus枚举的值
    context = Column(JSON, nullable=True)
    
    material = relationship("Material", back_populates="knowledge_entries")

class RelationshipType(str, Enum):
    """关系类型枚举"""
    SAME_EVENT = 'same_event'
    SAME_PERSON = 'same_person'
    SAME_LOCATION = 'same_location'
    EMOTIONAL_SIMILARITY = 'emotional_similarity'
    TEMPORAL_PROXIMITY = 'temporal_proximity'

class Relationship(Base):
    """关系模型 - 第二阶段实现"""
    __tablename__ = 'relationships'
    
    # 全部替换为String(36)兼容SQLite
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    material_id = Column(String(36), ForeignKey('materials.id'), nullable=False)
    
    source_id = Column(String(36), nullable=False)
    target_id = Column(String(36), nullable=False)
    relationship_type = Column(String(50), nullable=False)  # 使用RelationshipType枚举的值
    strength = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    relationship_metadata = Column(JSON, nullable=True)
    
    material = relationship("Material", back_populates="relationships")