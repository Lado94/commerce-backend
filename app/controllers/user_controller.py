from app.models.user_model import User
from app.db import db

class UserController:
    @staticmethod
    def create_user(data):
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "user")

        if not email or not username or not password:
            return None, {"error": "Missing required fields"}, 400

        if User.query.filter_by(email=email).first():
            return None, {"error": "Email already exists"}, 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.role = role

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict(), None, 201
        except Exception as e:
            db.session.rollback()
            return None, {"error": str(e)}, 500

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, {"error": "User not found"}, 404
        return user.to_dict(), None, 200

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [u.to_dict() for u in users], None, 200

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None, {"error": "User not found"}, 404

        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        if "password" in data:
            user.set_password(data["password"])
        user.role = data.get("role", user.role)

        db.session.commit()
        return user.to_dict(), None, 200

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, {"error": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, None, 200

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
