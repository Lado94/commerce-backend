from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.order_controller import OrderController

order_bp = Blueprint('order', __name__)

@order_bp.route('', methods=['GET'])
def get_orders():
    filters = {
        "user_id": request.args.get('user_id', type=int),
        "status": request.args.get('status')
    }
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    orders, error, status = OrderController.get_all_orders(filters, sort_by, sort_order)
    if error:
        return jsonify(error), status
    return jsonify(orders), status

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order, error, status = OrderController.get_order_by_id(order_id)
    if error:
        return jsonify(error), status
    return jsonify(order), status

@order_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    order, error, status = OrderController.create_order(data)
    if error:
        return jsonify(error), status
    return jsonify(order), status

@order_bp.route('/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    data = request.get_json()
    order, error, status = OrderController.update_order(order_id, data)
    if error:
        return jsonify(error), status
    return jsonify(order), status

@order_bp.route('/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    result, error, status = OrderController.delete_order(order_id)
    if error:
        return jsonify(error), status
    return jsonify(result), status
