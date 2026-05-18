# backend/core/data_bunker/dependencies.py
from sqlalchemy.orm import Session
# from .database import get_db

def get_current_user():
    # 实际应用中从身份验证获取用户信息
    # 这里返回模拟用户
    return {"id": "test_user_id", "username": "test_user"}