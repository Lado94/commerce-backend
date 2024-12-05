from flask import Blueprint, request, jsonify
from app.controllers.product_controller import ProductController

product_bp = Blueprint('product', __name__)

@product_bp.route('', methods=['GET'])
def get_products():
    # Получаем параметры фильтрации и сортировки
    filters = {
        "name": request.args.get('name'),
        "min_price": request.args.get('min_price', type=float),
        "max_price": request.args.get('max_price', type=float)
    }
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    products = ProductController.get_all_products(filters, sort_by, sort_order)
    return jsonify(products), 200

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductController.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

@product_bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    product = ProductController.create_product(data)
    return jsonify(product), 201

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = ProductController.update_product(product_id, data)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = ProductController.delete_product(product_id)
    if not result:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(result), 200
