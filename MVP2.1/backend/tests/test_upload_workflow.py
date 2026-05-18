# tests/test_upload_workflow.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
import uuid

# 导入您的控制器和模型
from backend.core.data_bunker.controllers.UploadController import router as upload_router
from backend.core.data_bunker.repositories.MaterialRepository import MaterialRepository
from backend.core.data_bunker.models import Base
from backend.core.data_bunker.services import StorageService
from backend.config.development import Settings, get_settings
from backend.core.data_bunker.database import get_db,get_current_user




# 创建FastAPI应用并添加路由
from fastapi import FastAPI
app = FastAPI()
app.include_router(upload_router)

# 测试数据库配置
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建测试数据库表
Base.metadata.create_all(bind=engine)

# 覆盖依赖
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 模拟身份验证依赖
def override_get_current_user():
    return {"id": str(uuid.uuid4()), "username": "test_user"}

# 覆盖配置
def override_get_settings():
    class TestSettings:
        STORAGE_TYPE = "local"
        LOCAL_STORAGE_PATH = "/tmp/test_storage"
        TEMP_STORAGE_PATH = "/tmp/test_temp"
        ALLOWED_FILE_TYPES = ["image/*", "text/plain"]
        UPLOAD_CHUNK_SIZE = 5 * 1024 * 1024  # 5MB
    return TestSettings()


# 应用依赖覆盖
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_settings] = override_get_settings

@pytest.fixture(scope="session", autouse=True)
def setup_test_storage():
    # 创建测试存储目录
    settings = override_get_settings()
    Path(settings.LOCAL_STORAGE_PATH).mkdir(parents=True, exist_ok=True)
    Path(settings.TEMP_STORAGE_PATH).mkdir(parents=True, exist_ok=True)
    yield
    # 测试结束后清理
    import shutil
    shutil.rmtree(settings.LOCAL_STORAGE_PATH, ignore_errors=True)
    shutil.rmtree(settings.TEMP_STORAGE_PATH, ignore_errors=True)

@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)

def test_complete_upload_workflow(client):
    """测试完整上传流程"""
    # 1. 创建上传会话
    session_response = client.post("/upload/session", json={
        "filename": "test.jpg",
        "filetype": "image/jpeg",
        "filesize": 1024
    })
    assert session_response.status_code == 200
    session_id = session_response.json()["session_id"]
    
    # 2. 上传分块（模拟单块上传）
    chunk_data = b"test" * 256  # 1KB测试数据
    chunk_response = client.put("/upload/chunk", data={
        "session_id": session_id,
        "chunk_index": 0,
        "chunk_count": 1
    }, files={"file": ("chunk", chunk_data)})
    assert chunk_response.status_code == 200
    
    # 3. 完成上传
    complete_response = client.post("/upload/complete", json={
        "session_id": session_id,
        "user_metadata": {"custom_field": "test_value"}  # 注意：参数名是user_metadata
    })
    assert complete_response.status_code == 200
    material_data = complete_response.json()
    
    # 4. 验证数据库记录
    # 由于我们覆盖了get_db，这里可以直接使用TestingSessionLocal
    db = TestingSessionLocal()
    try:
        repo = MaterialRepository(db)
        db_material = repo.get_by_id(material_data["id"])
        assert db_material is not None
        assert db_material.path == material_data["path"]
        assert db_material.size == 1024
        assert "custom_field" in db_material.properties
    finally:
        db.close()
    
    # 5. 验证文件存储
    # 根据配置的存储路径检查文件是否存在
    settings = override_get_settings()
    stored_file_path = Path(settings.LOCAL_STORAGE_PATH) / material_data["path"]
    assert stored_file_path.exists()
    assert stored_file_path.stat().st_size == 1024
    
    # 6. 验证元数据提取
    # 由于我们上传的是测试数据，可能没有真实的元数据，但可以检查是否有基础元数据
    assert "file_size" in db_material.properties
    assert db_material.properties["file_size"] == 1024

def test_direct_upload_workflow(client):
    """测试直接上传流程"""
    # 创建测试文件
    test_file = Path("test_direct.txt")
    test_file.write_text("This is a test file for direct upload")
    
    # 直接上传
    with open(test_file, "rb") as f:
        direct_response = client.post("/upload/direct", 
            files={"file": ("test_direct.txt", f, "text/plain")},
            data={"user_metadata": {"description": "Test direct upload"}}
        )
    
    # 清理测试文件
    test_file.unlink()
    
    assert direct_response.status_code == 200
    material_data = direct_response.json()
    
    # 验证数据库记录
    db = TestingSessionLocal()
    try:
        repo = MaterialRepository(db)
        db_material = repo.get_by_id(material_data["id"])
        assert db_material is not None
        assert db_material.name == "test_direct.txt"
        assert "description" in db_material.properties
    finally:
        db.close()
    
    # 验证文件存储
    settings = override_get_settings()
    stored_file_path = Path(settings.LOCAL_STORAGE_PATH) / material_data["path"]
    assert stored_file_path.exists()
    assert stored_file_path.stat().st_size > 0

def test_invalid_file_type(client):
    """测试无效文件类型处理"""
    # 尝试创建不支持的文件类型会话
    response = client.post("/upload/session", json={
        "filename": "invalid.exe",
        "filetype": "application/exe",
        "filesize": 1024
    })
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]["error"]

def test_chunk_validation_failure(client):
    """测试分块验证失败处理"""
    # 创建有效会话
    session_response = client.post("/upload/session", json={
        "filename": "test.jpg",
        "filetype": "image/jpeg",
        "filesize": 1024
    })
    session_id = session_response.json()["session_id"]
    
    # 尝试上传无效分块（索引超出范围）
    chunk_data = b"test" * 256
    response = client.put("/upload/chunk", data={
        "session_id": session_id,
        "chunk_index": 2,  # 无效索引
        "chunk_count": 1
    }, files={"file": ("chunk", chunk_data)})
    
    assert response.status_code == 400
    assert "Invalid chunk index" in response.json()["detail"]["error"]