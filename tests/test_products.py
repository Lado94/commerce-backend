def test_create_product_unauthorized(client):
    # Попытка создать продукт без токена
    response = client.post("/products", json={
        "name": "Test Product",
        "price": 100.0,
        "description": "Simple product"
    })
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Missing Authorization Header"

def test_create_product_authorized(client, admin_token):
    # Создание продукта под админом
    response = client.post("/products",
                           json={
                               "name": "Test Product",
                               "price": 100.0,
                               "description": "Simple product"
                           },
                           headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Product"
    assert data["price"] == 100.0
    assert data["description"] == "Simple product"

def test_get_products_list(client):
    # Получить список продуктов
    response = client.get("/products")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1  # Мы создали один продукт выше

def test_get_product_by_id(client):
    # Получаем продукт по ID
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Test Product"

def test_update_product(client, admin_token):
    # Обновим продукт
    response = client.put("/products/1",
                          json={"name": "Updated Product", "price": 200.0},
                          headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 200.0

def test_delete_product(client, admin_token):
    # Удалим продукт
    response = client.delete("/products/1",
                             headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Product deleted"

    # Проверим, что продукт удалён
    response = client.get("/products/1")
    assert response.status_code == 404
