"""
MaterialRepository.py - 素材数据访问层
负责所有Material模型的数据库操作：增、删、查。
Controller层通过调用这里的函数来操作数据库，不直接写SQL。
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Material


class MaterialRepository:
    """
    Material的Repository类。
    所有方法都是@staticmethod，因为Repository本身不保存状态，
    只接收db会话和数据，执行数据库操作。
    """

    @staticmethod
    def create(db: Session, **kwargs) -> Material:
        """
        创建一个新的Material记录。

        参数:
            db: 数据库会话
            **kwargs: Material模型的字段值（name, type, path, mime_type, size等）

        返回:
            创建成功的Material对象（已包含数据库生成的id）
        """
        db_material = Material(**kwargs)  # 用传进来的字段值创建Material对象
        db.add(db_material)                # 把对象加入会话的"待插入"队列
        db.commit()                        # 提交事务，真正执行INSERT
        db.refresh(db_material)            # 刷新对象，获取数据库生成的默认值（如id、created_at）
        return db_material

    @staticmethod
    def get_by_id(db: Session, material_id: str) -> Optional[Material]:
        """
        根据ID查询单个Material。

        参数:
            db: 数据库会话
            material_id: 素材的UUID字符串

        返回:
            找到的Material对象，找不到返回None
        """
        return db.query(Material).filter(Material.id == material_id).first()

    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[Material]:
        """
        查询Material列表（支持分页）。

        参数:
            db: 数据库会话
            skip: 跳过前多少条（用于分页）
            limit: 最多返回多少条

        返回:
            Material对象列表
        """
        return db.query(Material).offset(skip).limit(limit).all()

    @staticmethod
    def delete(db: Session, material_id: str) -> bool:
        """
        根据ID删除Material（物理删除）。

        参数:
            db: 数据库会话
            material_id: 要删除的素材ID

        返回:
            删除成功返回True，找不到返回False
        """
        material = db.query(Material).filter(Material.id == material_id).first()
        if material:
            db.delete(material)   # 标记为待删除
            db.commit()           # 执行DELETE
            return True
        return False