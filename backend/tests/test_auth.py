import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_success(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={
            "email": "email@example.com",
            "username": "username",
            "password": "password",
        },
    )

    response = await client.post(
        "/api/auth/login",
        data={
            "username": "email@example.com",
            "password": "password",
        },
    )

    assert response.status_code == 200


async def test_register_duplicate(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={
            "email": "email@example.com",
            "username": "username",
            "password": "password",
        },
    )

    response = await client.post(
        "/api/auth/register",
        json={
            "email": "email@example.com",
            "username": "username",
            "password": "password",
        },
    )

    assert response.status_code == 400


async def test_login_success(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={
            "email": "success@example.com",
            "username": "successusername",
            "password": "success_password",
        },
    )

    response = await client.post(
        "/api/auth/login",
        data={"username": "success@example.com", "password": "success_password"},
    )

    assert response.status_code == 200


async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={
            "email": "worongpassword@example.com",
            "username": "wrongusername",
            "password": "correct_password",
        },
    )

    response = await client.post(
        "/api/auth/login",
        data={
            "username": "wrongpassword@example.com",
            "password": "incorrect_password",
        },
    )

    assert response.status_code == 401
