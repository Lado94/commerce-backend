from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user_model import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Регистрация пользователя
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Проверка уникальности email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Вход пользователя
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

# Защищённый маршрут (пример)
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Welcome, user {current_user_id}!"}), 200
