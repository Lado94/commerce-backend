from app.models.user_model import User
from app.db import db

class UserController:
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [user.to_dict() for user in users]

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        return user.to_dict() if user else None

    @staticmethod
    def create_user(data):
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],  # В реальности используйте хеширование пароля!
            role=data.get('role', 'user')
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        db.session.commit()
        return user.to_dict()

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return None

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}
