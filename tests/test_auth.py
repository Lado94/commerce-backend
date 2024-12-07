import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test_secret_key",
    })
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"

def test_login_user(client):
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    response = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()
