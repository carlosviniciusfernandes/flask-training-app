import pytest
from models import User

test_user_data = {
    "first_name": "Carlos",
    "last_name": "Fernandes",
}


@pytest.mark.asyncio
async def test_add_user(test_client):
    payload = {**test_user_data}
    response = await test_client.post("/users/add", json=payload)

    data = await response.get_json()
    assert response.status_code == 201
    assert type(data.get("id")) == str

    created_user = await User.get(data["id"])
    assert created_user is not None
    assert created_user.first_name == payload["first_name"]
    assert created_user.last_name == payload["last_name"]


@pytest.mark.asyncio
async def test_get_user(test_client):
    user = User(**test_user_data)
    await user.insert()
    response = await test_client.get(f"/users/{user.id}")

    data = await response.get_json()
    assert response.status_code == 200
    assert data.get("id") == str(user.id)
    assert data.get("first_name") == user.first_name
    assert data.get("last_name") == user.last_name


@pytest.mark.asyncio
async def test_update_user(test_client):
    user = User(**test_user_data)
    await user.insert()
    payload = {"last_name": "Vinicius"}
    response = await test_client.patch(f"/users/{user.id}", json=payload)

    data = await response.get_json()
    assert response.status_code == 200
    assert data.get("last_name") == payload["last_name"]

    updated_user = await User.get(user.id)
    assert updated_user.last_name == payload["last_name"]


@pytest.mark.asyncio
async def test_delete_user(test_client):
    user = User(**test_user_data)
    await user.insert()

    response = await test_client.delete(f"/users/{user.id}")

    assert response.status_code == 204
    assert await User.get(user.id) is None
