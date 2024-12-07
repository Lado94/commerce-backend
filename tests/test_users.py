from app.models.user_model import User
from app.db import db
from flask_jwt_extended import create_access_token

def test_create_user(client):
    # Создаём нового пользователя без токена (судя по вашему коду, create_user не требует авторизации)
    response = client.post("/users", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    # Проверим, что пользователь создался
    # Можно сделать повторный GET запрос, но это потребует токена.
    # На данном этапе достаточно утверждения о статус-коде и структуре ответа.

def test_get_users_unauthorized(client):
    # Попытка получить список пользователей без токена
    response = client.get("/users")
    assert response.status_code == 401
    assert "Missing Authorization Header" in response.get_json()["msg"]

def test_get_users_authorized(client, admin_token):
    # Получаем список пользователей под админом
    response = client.get("/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Мы знаем, что у нас есть admin (из фикстуры) и newuser (созданный в тесте выше)
    # Так что ожидаем минимум 2 пользователя
    assert len(data) >= 2

def test_get_user_by_id(client, admin_token):
    # Предполагаем, что id=1 это админ, id=2 - newuser
    response = client.get("/users/2", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 2
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"

def test_update_user(client, admin_token):
    # Обновим newuser'a
    response = client.put("/users/2",
                          json={"username": "updateduser", "email": "updated@example.com"},
                          headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "updateduser"
    assert data["email"] == "updated@example.com"

def test_delete_user(client, admin_token):
    # Удалим пользователя с id=2 (updateduser)
    response = client.delete("/users/2", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "User deleted"

    # Попытаемся получить удалённого пользователя
    response = client.get("/users/2", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"
