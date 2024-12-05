def test_register_user(client):
    # Отправляем запрос на регистрацию
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"

def test_login_user(client):
    # Регистрируем пользователя
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    # Пытаемся войти
    response = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_protected_route(client):
    # Регистрируем пользователя и получаем токен
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    login_response = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    token = login_response.get_json()["access_token"]

    # Тестируем защищённый маршрут
    response = client.get("/auth/protected", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert "Welcome" in response.get_json()["message"]
