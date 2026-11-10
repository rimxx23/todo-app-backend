import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.db.session import get_db
from app.main import app
from app.models.base import Base


settings = get_settings()
TEST_DATABASE_URL = settings.DATABASE_URL.rsplit("/", 1)[0] + "/todo_test"


@pytest.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def client(engine):
    TestSession = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
async def auth_headers(client):
    await client.post("/auth/register", json={"username": "alice", "password": "password"})
    response = await client.post("/auth/login", data={"username": "alice", "password": "password"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def other_auth_headers(client):
    await client.post("/auth/register", json={"username": "bob", "password": "password"})
    response = await client.post("/auth/login", data={"username": "bob", "password": "password"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}