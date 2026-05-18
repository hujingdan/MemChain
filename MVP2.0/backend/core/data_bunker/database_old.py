# core/data_bunker/database.py
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid

from sqlalchemy.orm import Session

# 生产环境数据库配置（伪代码）
DATABASE_URL = "sqlite:///test.db"  # 实际项目中从配置读取
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user():
    # 实际应用中从身份验证获取用户信息
    # 这里返回模拟用户（使用固定的UUID用于测试）
    return {"id": uuid.UUID("00000000-0000-0000-0000-000000000001"), "username": "test_user"}