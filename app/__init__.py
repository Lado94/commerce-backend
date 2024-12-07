from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.db import db
from app.utils.error_handlers import register_error_handlers
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Инициализация БД
    db.init_app(app)

    # Инициализация JWT
    jwt = JWTManager(app)

    # Регистрация Blueprints
    from app.routes.auth_route import auth_bp
    from app.routes.product_route import product_bp
    from app.routes.order_route import order_bp
    from app.routes.user_route import user_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(user_bp, url_prefix='/users')

    # Регистрация хендлеров ошибок
    register_error_handlers(app)

    return app
