"""
database.py - 数据库连接和会话管理
整个后端的所有数据库操作，都通过这个模块获取会话。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# SQLite数据库文件路径（存放在backend目录下）
DATABASE_URL = "sqlite:///./memchain.db"

# 创建数据库引擎
# connect_args={"check_same_thread": False} 是SQLite特有配置，
# 因为FastAPI用多线程处理请求，SQLite默认不允许跨线程共享连接
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # echo=True会打印所有SQL语句，调试时打开，生产环境关闭
)

# 创建会话工厂
# autocommit=False: 不会自动提交，需要手动session.commit()
# autoflush=False: 不会自动刷新，减少不必要的数据库操作
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    获取数据库会话的生成器函数。
    被FastAPI的Depends使用，每个请求都会自动获得一个独立的db会话。
    """
    db = SessionLocal()  # 从工厂创建一个会话
    try:
        yield db         # 把会话交给接口函数使用
    finally:
        db.close()       # 请求结束后，无论成功或报错，都会关闭会话


def init_db():
    """
    初始化数据库：根据models.py中的模型定义，自动创建所有表。
    通常在应用启动时调用一次。
    """
    from .models import Base
    Base.metadata.create_all(bind=engine)