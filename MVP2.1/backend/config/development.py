"""
开发环境配置文件

包含以下配置项：

1. 数据库配置
   SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/memchain_dev'
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   DATABASE_POOL_SIZE = 5
   DATABASE_MAX_OVERFLOW = 10

2. 存储配置
   STORAGE_TYPE = 'local'  # 本地存储
   LOCAL_STORAGE_PATH = './storage'
   MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'txt', 'pdf'}

3. AI处理配置
   AI_MODEL_PATH = './models'
   BATCH_SIZE = 32
   MAX_SEQUENCE_LENGTH = 512
   INFERENCE_TIMEOUT = 30  # 秒

4. 缓存配置
   CACHE_TYPE = 'simple'
   CACHE_DEFAULT_TIMEOUT = 300

5. 安全配置
   SECRET_KEY = 'dev-secret-key'
   JWT_SECRET_KEY = 'dev-jwt-secret'
   JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时

6. 调试配置
   DEBUG = True
   TESTING = False
   LOG_LEVEL = 'DEBUG'

7. 服务配置
   HOST = 'localhost'
   PORT = 5000
   WORKERS = 1

注意：此配置仅用于开发环境，包含详细的日志和调试信息。
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DevelopmentSettings:
    # 文件类型设置（前后端统一）
    ALLOWED_FILE_TYPES = [
        "image/jpeg",
        "image/png",
        "image/heic",
        "image/webp",
        "image/gif",
        "video/mp4",
        "video/quicktime",
        "audio/mpeg",
        "audio/wav",
        "text/plain",
        "application/pdf",
        "image/*"
    ]
    
    # 存储配置
    STORAGE_TYPE = "local"
    LOCAL_STORAGE_PATH = "/var/data/uploads"
    TEMP_STORAGE_PATH = "/var/data/tmp"
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024 * 1024  # 10GB
    UPLOAD_CHUNK_SIZE = 5 * 1024 * 1024  # 5MB
    
    # AWS配置
    AWS_ACCESS_KEY = "your-access-key"
    AWS_SECRET_KEY = "your-secret-key"
    AWS_REGION = "us-east-1"
    S3_BUCKET = "your-bucket-name"
    S3_BASE_PATH = "uploads/"

#测试
class Settings:
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///test.db")

    # 存储配置
    STORAGE_TYPE = os.getenv("STORAGE_TYPE", "local")
    LOCAL_STORAGE_PATH = os.getenv("LOCAL_STORAGE_PATH", "uploads")
    TEMP_STORAGE_PATH = os.getenv("TEMP_STORAGE_PATH", "temp")
    ALLOWED_FILE_TYPES = ["image/*", "audio/*", "text/*"]
    UPLOAD_CHUNK_SIZE = int(os.getenv("UPLOAD_CHUNK_SIZE", str(5 * 1024 * 1024)))  # 5MB

    # AI配置 - 火山方舟平台（从环境变量读取）
    VOLCENGINE_API_KEY = os.getenv("VOLCENGINE_API_KEY", "your-volcengine-api-key")
    VOLCENGINE_ENDPOINT = os.getenv("VOLCENGINE_ENDPOINT", "https://ark.cn-beijing.volces.com/api/v3")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-v3")
    AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "30"))  # API调用超时时间（秒）
    AI_MAX_RETRIES = int(os.getenv("AI_MAX_RETRIES", "3"))  # 最大重试次数

def get_settings():
    return Settings()

