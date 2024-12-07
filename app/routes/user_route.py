from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.user_controller import UserController

user_bp = Blueprint('user', __name__)

@user_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    users, error, status = UserController.get_all_users()
    if error:
        return jsonify(error), status
    return jsonify(users), status

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user, error, status = UserController.get_user_by_id(user_id)
    if error:
        return jsonify(error), status
    return jsonify(user), status

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    user, error, status = UserController.create_user(data)
    if error:
        return jsonify(error), status
    return jsonify(user), status

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user, error, status = UserController.update_user(user_id, data)
    if error:
        return jsonify(error), status
    return jsonify(user), status

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    result, error, status = UserController.delete_user(user_id)
    if error:
        return jsonify(error), status
    return jsonify(result), status
