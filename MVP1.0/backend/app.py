"""
核心职责：应用入口，初始化FastAPI应用，注册路由等。
该模块负责：
1. 应用配置加载
2. 中间件注册
3. 路由注册
4. 依赖注入配置
5. 错误处理中间件
6. CORS和安全配置
"""

# backend/app.py
from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.data_bunker.controllers import UploadController
from core.data_bunker.database import get_db

# 创建FastAPI应用
app = FastAPI()

# 包含路由
app.include_router(UploadController.router, prefix="/upload")

# 数据库配置（测试用）
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 覆盖生产环境的数据库依赖
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
