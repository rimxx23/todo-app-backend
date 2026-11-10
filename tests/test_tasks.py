from fastapi import status

async def test_tasks_without_token(client):
    response = await client.get("/tasks")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

async def test_create_task(client, auth_headers):
    response = await client.post("/tasks", json={"title": "купить хлеб"}, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "купить хлеб"
    assert response.json()["completed"] is False

async def test_list_tasks(client, auth_headers):
    await client.post("/tasks", json={"title": "купить хлеб"}, headers=auth_headers)
    await client.post("/tasks", json={"title": "продать хлеб"}, headers=auth_headers)

    response = await client.get("/tasks", headers=auth_headers)

    assert len(response.json()) == 2
    titles = [task["title"] for task in response.json()]
    assert "купить хлеб" in titles

async def test_user_sees_only_own_tasks(client, auth_headers, other_auth_headers):
    await client.post("/tasks", json={"title": "купить хлеб"}, headers=auth_headers)
    response = await client.get("/tasks", headers=other_auth_headers)
    assert response.json() == []

async def test_cannot_delete_other_user_task(client, auth_headers, other_auth_headers):
    response = await client.post("/tasks", json={"title": "купить хлеб"}, headers=auth_headers)
    task_id = response.json()["id"]
    response_delete = await client.delete(f"/tasks/{task_id}", headers=other_auth_headers)
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND