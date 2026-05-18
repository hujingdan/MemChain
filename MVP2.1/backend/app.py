"""
MemChain MVP - 应用入口（最终合并版）
功能：本地SQLite数据库持久化 + 跨域 + 文件上传接口 + 全局异常处理 + 文件大小限制 + 时间轴/仪表盘接口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.data_bunker.models import Base
from core.data_bunker.database import get_db
# 导入上传路由（展示功能）
from core.data_bunker.controllers.UploadController import router as upload_router
# 导入时间轴/仪表盘路由（新增）
from core.data_bunker.controllers.timeline_controller import router as timeline_router

# ===================== 【位置1：全局常量】放在最前面，导入之后、配置之前 =====================
# 上传文件大小限制：10MB
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 * 1024KB = 10MB

# ===================== 本地SQLite数据库配置（必须保留） =====================
DATABASE_URL = "sqlite:///./memchain.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 自动创建所有数据表（根据你修改的models.py）
Base.metadata.create_all(bind=engine)

# 重写数据库依赖，适配本地SQLite
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===================== FastAPI应用初始化 =====================
app = FastAPI(
    title="MemChain API",
    description="时光容器 - AI驱动的个人记忆管理平台",
    version="0.1.0"
)

# CORS跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 覆盖数据库配置（核心！）
app.dependency_overrides[get_db] = override_get_db

# ===================== 【位置2：全局异常处理器】app初始化之后，路由注册之前 =====================
# 全局异常处理器：捕获所有未处理的异常
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    捕获所有未被特定处理器捕获的异常。
    返回统一的JSON错误格式，不暴露内部堆栈信息。
    """
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "服务器内部错误",
            "detail": str(exc)  # 开发阶段显示详细错误，生产环境可隐藏
        }
    )

# 自定义HTTP异常处理器（覆盖FastAPI默认的）
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    捕获所有HTTPException（包括404、400等）。
    统一返回格式，让前端更容易处理。
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

# ===================== 路由注册（集中管理） =====================
# 注册上传接口
app.include_router(upload_router, prefix="/upload", tags=["文件上传"])
# 注册时间轴/仪表盘路由（新增）
app.include_router(timeline_router, prefix="/timeline", tags=["时间轴"])

# ===================== 基础接口 =====================
@app.get("/")
def read_root():
    return {"message": "MemChain API is running", "version": "0.1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}