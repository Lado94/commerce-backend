from flask import Blueprint, request, jsonify
from app.controllers.order_controller import OrderController

# Создаем Blueprint для заказов
order_bp = Blueprint('order', __name__)

# Маршрут для получения всех заказов
@order_bp.route('', methods=['GET'])
def get_orders():
    # Получаем параметры фильтрации и сортировки
    filters = {
        "user_id": request.args.get('user_id', type=int),  # Фильтрация по user_id
        "status": request.args.get('status')  # Фильтрация по статусу
    }
    sort_by = request.args.get('sort_by', 'id')  # Поле для сортировки (по умолчанию id)
    sort_order = request.args.get('sort_order', 'asc')  # Порядок сортировки: asc или desc

    # Получаем список заказов через контроллер
    orders = OrderController.get_all_orders(filters, sort_by, sort_order)
    return jsonify(orders), 200

# Маршрут для получения заказа по ID
@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = OrderController.get_order_by_id(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200

# Маршрут для создания нового заказа
@order_bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    order, error, status = OrderController.create_order(data)
    if error:
        return jsonify(error), status
    return jsonify(order), status

# Маршрут для обновления заказа
@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    order = OrderController.update_order(order_id, data)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200

# Маршрут для удаления заказа
@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    result = OrderController.delete_order(order_id)
    if not result:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(result), 200
