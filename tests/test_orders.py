from app.models.user_model import User
from app.models.product_model import Product
from app.db import db
from flask_jwt_extended import create_access_token

def test_create_order(client, app):
    with app.app_context():
        # Создадим пользователя-юзера
        user = User(username="orderuser", email="orderuser@example.com")
        user.set_password("userpass")
        user.role = "user"
        db.session.add(user)
        db.session.commit()

        # Создадим продукты для заказа
        p1 = Product(name="Product1", price=50.0, description="P1")
        p2 = Product(name="Product2", price=100.0, description="P2")
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

        # Получим токен для пользователя orderuser (id=2, т.к. admin был первым)
        user_token = create_access_token(identity="2")

    # Создаём заказ
    response = client.post("/orders",
                           json={
                               "user_id": 2,
                               "product_ids": [1, 2]
                           },
                           headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["user_id"] == 2
    assert len(data["products"]) == 2
    assert data["total_price"] == 150.0  # 50 + 100

def test_get_orders(client):
    # Получаем все заказы
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["total_price"] == 150.0

def test_get_order_by_id(client):
    response = client.get("/orders/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["total_price"] == 150.0

def test_update_order(client, app):
    with app.app_context():
        # Получим токен пользователя, который сделал заказ (id=2)
        user_token = create_access_token(identity="2")

    # Обновляем статус заказа
    response = client.put("/orders/1",
                          json={"status": "completed"},
                          headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "completed"

def test_delete_order(client, app):
    with app.app_context():
        # Токен пользователя (id=2)
        user_token = create_access_token(identity="2")

    response = client.delete("/orders/1",
                             headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Order deleted"

    # Проверим, что заказа больше нет
    response = client.get("/orders/1")
    assert response.status_code == 404
