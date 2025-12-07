"""
核心职责：负责与数据库交互，存储和查询用户素材的元数据。
该仓储层确保：
1. 数据的CRUD操作封装
2. 查询优化和缓存策略
3. 数据一致性维护
4. 支持分页和高效检索
"""
# MVP/backend/core/data_bunker/repositories/MaterialRepository.py
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ..models import Material
from ..schemas.material import MaterialCreate

class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, material_data: MaterialCreate) -> Material:
        """创建素材记录（第一阶段核心）"""
        db_material = Material(
            user_id=material_data.user_id,
            name=material_data.name,
            type=material_data.type,
            path=material_data.path,
            mime_type=material_data.mime_type,
            size=material_data.size,
            properties=material_data.properties
        )
        self.db.add(db_material)
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def get_by_id(self, material_id: UUID) -> Optional[Material]:
        """根据ID获取素材（测试用）"""
        return self.db.query(Material).filter(Material.id == material_id).first()

    def get_by_path(self, path: str) -> Optional[Material]:
        """根据存储路径获取素材（测试用）"""
        return self.db.query(Material).filter(Material.path == path).first()