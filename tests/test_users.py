def test_create_user(client):
    response = client.post("/users", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "role": "user"
    })
    assert response.status_code == 201
    assert response.get_json()["username"] == "newuser"

def test_get_users(client):
    client.post("/users", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123",
        "role": "user"
    })
    client.post("/users", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "password123",
        "role": "admin"
    })
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == 2
