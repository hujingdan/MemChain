"""
生产环境配置文件

包含以下配置项：

1. 数据库配置
   SQLALCHEMY_DATABASE_URI = 'postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}/${DB_NAME}'
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   DATABASE_POOL_SIZE = 20
   DATABASE_MAX_OVERFLOW = 40

2. 存储配置
   STORAGE_TYPE = 's3'  # AWS S3存储
   S3_BUCKET = '${S3_BUCKET_NAME}'
   S3_REGION = '${AWS_REGION}'
   MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'txt', 'pdf'}

3. AI处理配置
   AI_MODEL_PATH = '/opt/models'
   BATCH_SIZE = 64
   MAX_SEQUENCE_LENGTH = 512
   INFERENCE_TIMEOUT = 20  # 秒

4. 缓存配置
   CACHE_TYPE = 'redis'
   REDIS_URL = '${REDIS_URL}'
   CACHE_DEFAULT_TIMEOUT = 600

5. 安全配置
   SECRET_KEY = '${SECRET_KEY}'
   JWT_SECRET_KEY = '${JWT_SECRET_KEY}'
   JWT_ACCESS_TOKEN_EXPIRES = 1800  # 30分钟

6. 生产环境配置
   DEBUG = False
   TESTING = False
   LOG_LEVEL = 'INFO'

7. 服务配置
   HOST = '0.0.0.0'
   PORT = 8000
   WORKERS = 4

8. 监控配置
   SENTRY_DSN = '${SENTRY_DSN}'
   PROMETHEUS_METRICS = True

注意：此配置用于生产环境，所有敏感信息通过环境变量注入。
确保性能优化和安全加固。
"""
