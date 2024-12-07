import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token
from app.models.user_model import User

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
        # Создадим пользователя-админа для тестов (чтобы создавать продукты)
        admin_user = User(username="admin", email="admin@example.com")
        admin_user.set_password("adminpass")
        admin_user.role = "admin"
        db.session.add(admin_user)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_token(app):
    with app.app_context():
        # Получим токен для админа (id=1)
        token = create_access_token(identity="1")  # здесь identity — строка
        return token
