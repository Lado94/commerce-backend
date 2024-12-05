from app.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # В реальности храним в зашифрованном виде!
    role = db.Column(db.String(50), default='user')  # Роль: 'user' или 'admin'

    orders = db.relationship('Order', backref='user', lazy=True)  # Связь: Один пользователь — много заказов

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }
