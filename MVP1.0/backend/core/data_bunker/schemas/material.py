# MVP/backend/core/data_bunker/schemas/material.py
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Dict, Optional, List

class MaterialCreate(BaseModel):
    """创建素材的输入模型"""
    user_id: UUID
    name: str
    type: str
    path: str
    mime_type: str
    size: int
    properties: Dict = Field(default_factory=dict)

class MaterialResponse(BaseModel):
    """素材响应模型"""
    id: UUID
    user_id: UUID
    name: str
    type: str
    path: str
    mime_type: str
    size: int
    created_at: datetime
    updated_at: Optional[datetime]
    properties: Dict
    tags: Optional[List[str]]
    emotional_score: Optional[float]
    location: Optional[Dict]
    is_archived: bool
    is_deleted: bool

    class Config:
        orm_mode = True