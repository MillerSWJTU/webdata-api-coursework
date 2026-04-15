import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.core.config import settings

# 给测试专用的“内存 SQLite”数据库。速度极快，每次运行结束即刻销毁，不会污染真实数据。
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # 每次测试前建表
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 测试结束后删表
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    # 核心：将真实应用中获取数据库的函数，覆盖替换为获取测试内存库的函数
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # 测试结束恢复原状
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def auth_headers():
    # 提取我们在依赖注入中配置的默认安全秘钥，作为测试发包的请求头
    api_key = getattr(settings, "API_KEY", "xjco3011-secret-key")
    return {"X-API-Key": api_key}
