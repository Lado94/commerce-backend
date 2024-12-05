from app.models.order_model import Order
from app.models.product_model import Product
from app.db import db

class OrderController:
    @staticmethod
    def get_all_orders(filters=None, sort_by='id', sort_order='asc'):
        """
        Получить все заказы с фильтрацией и сортировкой.
        """
        query = Order.query

        # Применяем фильтры
        if filters:
            if 'user_id' in filters and filters['user_id'] is not None:
                query = query.filter(Order.user_id == filters['user_id'])
            if 'status' in filters and filters['status']:
                query = query.filter(Order.status.ilike(f"%{filters['status']}%"))

        # Применяем сортировку
        if sort_order == 'desc':
            query = query.order_by(db.desc(getattr(Order, sort_by, Order.id)))
        else:
            query = query.order_by(getattr(Order, sort_by, Order.id))

        return [order.to_dict() for order in query.all()]

    @staticmethod
    def get_order_by_id(order_id):
        """
        Получить заказ по ID.
        """
        order = Order.query.get(order_id)
        return order.to_dict() if order else None

    @staticmethod
    def create_order(data):
        """
        Создать новый заказ.
        """
        user_id = data['user_id']
        product_ids = data.get('product_ids', [])

        # Проверяем, существуют ли продукты
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        if not products:
            return None, {"error": "No valid products found"}, 400

        # Подсчитываем общую стоимость
        total_price = sum(product.price for product in products)

        # Создаём заказ
        new_order = Order(
            user_id=user_id,
            total_price=total_price,
            status=data.get('status', 'pending')
        )
        new_order.products.extend(products)
        db.session.add(new_order)
        db.session.commit()
        return new_order.to_dict(), None, 201

    @staticmethod
    def update_order(order_id, data):
        """
        Обновить существующий заказ.
        """
        order = Order.query.get(order_id)
        if not order:
            return None

        # Обновляем статус заказа
        order.status = data.get('status', order.status)
        db.session.commit()
        return order.to_dict()

    @staticmethod
    def delete_order(order_id):
        """
        Удалить заказ по ID.
        """
        order = Order.query.get(order_id)
        if not order:
            return None

        db.session.delete(order)
        db.session.commit()
        return {"message": "Order deleted"}
