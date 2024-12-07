from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.product_controller import ProductController

product_bp = Blueprint('product', __name__)

@product_bp.route('', methods=['GET'])
def get_products():
    filters = {
        "name": request.args.get('name'),
        "min_price": request.args.get('min_price', type=float),
        "max_price": request.args.get('max_price', type=float)
    }
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    products, error, status = ProductController.get_all_products(filters, sort_by, sort_order)
    if error:
        return jsonify(error), status
    return jsonify(products), status

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product, error, status = ProductController.get_product_by_id(product_id)
    if error:
        return jsonify(error), status
    return jsonify(product), status

@product_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    product, error, status = ProductController.create_product(data)
    if error:
        return jsonify(error), status
    return jsonify(product), status

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.get_json()
    product, error, status = ProductController.update_product(product_id, data)
    if error:
        return jsonify(error), status
    return jsonify(product), status

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    result, error, status = ProductController.delete_product(product_id)
    if error:
        return jsonify(error), status
    return jsonify(result), status
