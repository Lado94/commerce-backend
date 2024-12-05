from flask import Blueprint, request, jsonify
from app.controllers.user_controller import UserController

user_bp = Blueprint('user', __name__)

@user_bp.route('', methods=['GET'])
def get_users():
    users = UserController.get_all_users()
    return jsonify(users), 200

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserController.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserController.create_user(data)
    return jsonify(user), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = UserController.update_user(user_id, data)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = UserController.delete_user(user_id)
    if not result:
        return jsonify({"error": "User not found"}), 404
    return jsonify(result), 200
