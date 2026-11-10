from fastapi import status

async def test_register(client):
    response = await client.post("/auth/register", json={"username": "alice", "password": "password"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data
    assert "hashed_password" not in data

async def test_register_duplicate(client):
    await client.post("/auth/register", json={"username": "alice", "password": "password"})

    response = await client.post("/auth/register", json={"username": "alice", "password": "password"})

    assert response.status_code == status.HTTP_409_CONFLICT

async def test_register_short_password(client):
    response = await client.post("/auth/register", json={"username": "alice", "password": "1"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

async def test_login(client):
    await client.post("/auth/register", json={"username": "alice", "password": "password"})
    response = await client.post("/auth/login", data={"username": "alice", "password": "password"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

async def test_login_wrong_password(client):
    await client.post("/auth/register", json={"username": "alice", "password": "password"})
    response = await client.post("/auth/login", data={"username": "alice", "password": "password1"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "access_token" not in response.json()
    

async def test_me_without_token(client):
    response = await client.get("/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED