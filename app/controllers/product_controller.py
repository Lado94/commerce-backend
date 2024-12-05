from app.models.product_model import Product
from app.db import db

class ProductController:
    @staticmethod
    def get_all_products(filters=None, sort_by='id', sort_order='asc'):
        """
        Получить все продукты с фильтрацией и сортировкой.
        """
        query = Product.query

        # Применяем фильтры
        if filters:
            if 'name' in filters and filters['name']:
                query = query.filter(Product.name.ilike(f"%{filters['name']}%"))
            if 'min_price' in filters and filters['min_price'] is not None:
                query = query.filter(Product.price >= filters['min_price'])
            if 'max_price' in filters and filters['max_price'] is not None:
                query = query.filter(Product.price <= filters['max_price'])

        # Применяем сортировку
        if sort_order == 'desc':
            query = query.order_by(db.desc(getattr(Product, sort_by, Product.id)))
        else:
            query = query.order_by(getattr(Product, sort_by, Product.id))

        return [product.to_dict() for product in query.all()]

    @staticmethod
    def get_product_by_id(product_id):
        """
        Получить продукт по ID.
        """
        product = Product.query.get(product_id)
        return product.to_dict() if product else None

    @staticmethod
    def create_product(data):
        """
        Создать новый продукт.
        """
        new_product = Product(
            name=data['name'],
            price=data['price'],
            description=data.get('description', '')
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict()

    @staticmethod
    def update_product(product_id, data):
        """
        Обновить продукт по ID.
        """
        product = Product.query.get(product_id)
        if not product:
            return None

        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.description = data.get('description', product.description)
        db.session.commit()
        return product.to_dict()

    @staticmethod
    def delete_product(product_id):
        """
        Удалить продукт по ID.
        """
        product = Product.query.get(product_id)
        if not product:
            return None

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}
