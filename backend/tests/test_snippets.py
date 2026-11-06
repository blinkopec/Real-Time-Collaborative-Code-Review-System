import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_snippet_success(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={
            "email": "snippet_creator@example.com",
            "username": "creator",
            "password": "secret123",
        },
    )

    login_response = await client.post(
        "/api/auth/login",
        data={"username": "snippet_creator@example.com", "password": "secret123"},
    )
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        "/api/snippets",
        headers=headers,
        json={
            "title": "My First Snippet",
            "language": "python",
            "code": "print('Hello, World!')",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My First Snippet"
    assert "id" in data
    assert "author_id" in data


async def test_create_comment_success(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={
            "email": "snippet_creator@example.com",
            "username": "creator",
            "password": "secret123",
        },
    )

    login_response = await client.post(
        "/api/auth/login",
        data={"username": "snippet_creator@example.com", "password": "secret123"},
    )
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    snippet = await client.post(
        "/api/snippets",
        headers=headers,
        json={
            "title": "My First Snippet",
            "language": "python",
            "code": "print('Hello, World!')",
        },
    )

    snippet_id = snippet.json()["id"]

    response = await client.post(
        f"/api/snippets/{snippet_id}/comments",
        headers=headers,
        json={"line_number": 1, "body": "Nice"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["body"] == "Nice"
    assert "id" in data


async def test_list_snippets(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={
            "email": "snippet_creator@example.com",
            "username": "creator",
            "password": "secret123",
        },
    )

    login_response = await client.post(
        "/api/auth/login",
        data={"username": "snippet_creator@example.com", "password": "secret123"},
    )
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    await client.post(
        "/api/snippets",
        headers=headers,
        json={
            "title": "My First Snippet",
            "language": "python",
            "code": "print('Hello, World!')",
        },
    )

    response = await client.get("/api/snippets", headers=headers)
    assert response.status_code == 200


async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/snippets")

    assert response.status_code == 401
