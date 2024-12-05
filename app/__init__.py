from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

# Создание экземпляра базы данных
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Настройка конфигурации
    app.config.from_object('app.config.Config')

    # Настройка переменной окружения для JWT_SECRET_KEY
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_secret_key')

    # Настройка JWT
    jwt = JWTManager(app)

    # Инициализация базы данных
    db.init_app(app)

    # Регистрация маршрутов
    from app.routes.auth_route import auth_bp
    from app.routes.product_route import product_bp
    from app.routes.user_route import user_bp
    from app.routes.order_route import order_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(order_bp, url_prefix='/orders')

    return app
