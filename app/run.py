from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.db import db
from app.routes.product_route import product_bp
from app.routes.user_route import user_bp
from app.routes.order_route import order_bp
from app.routes.auth_route import auth_bp



from app.utils.error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация расширений
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Регистрация маршрутов
app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(order_bp, url_prefix='/orders')
app.register_blueprint(auth_bp, url_prefix='/auth')

# Регистрация обработчиков ошибок
register_error_handlers(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



# from app import create_app, db
#
# # Создание экземпляра приложения
# app = create_app()
#
# if __name__ == '__main__':
#     # Убедитесь, что база данных создана перед запуском сервера
#     with app.app_context():
#         db.create_all()
#
#     # Запуск приложения
#     app.run(debug=True)
