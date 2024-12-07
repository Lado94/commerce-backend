from app.models.order_model import Order
from app.models.product_model import Product
from app.db import db

class OrderController:
    @staticmethod
    def get_all_orders(filters=None, sort_by='id', sort_order='asc'):
        query = Order.query
        if filters:
            if 'user_id' in filters and filters['user_id'] is not None:
                query = query.filter(Order.user_id == filters['user_id'])
            if 'status' in filters and filters['status']:
                query = query.filter(Order.status.ilike(f"%{filters['status']}%"))

        if sort_order == 'desc':
            query = query.order_by(db.desc(getattr(Order, sort_by, Order.id)))
        else:
            query = query.order_by(getattr(Order, sort_by, Order.id))

        return [o.to_dict() for o in query.all()], None, 200

    @staticmethod
    def get_order_by_id(order_id):
        order = Order.query.get(order_id)
        if not order:
            return None, {"error": "Order not found"}, 404
        return order.to_dict(), None, 200

    @staticmethod
    def create_order(data):
        user_id = data.get('user_id')
        product_ids = data.get('product_ids', [])

        if user_id is None:
            return None, {"error": "user_id is required"}, 400
        if not product_ids:
            return None, {"error": "product_ids is required"}, 400

        products = Product.query.filter(Product.id.in_(product_ids)).all()
        if not products:
            return None, {"error": "No valid products found"}, 400

        total_price = sum(p.price for p in products)
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
        order = Order.query.get(order_id)
        if not order:
            return None, {"error": "Order not found"}, 404

        order.status = data.get('status', order.status)
        db.session.commit()
        return order.to_dict(), None, 200

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return None, {"error": "Order not found"}, 404

        db.session.delete(order)
        db.session.commit()
        return {"message": "Order deleted"}, None, 200
