from app.extensions import db, bcrypt
from app.models import User
from sqlalchemy.exc import SQLAlchemyError

def delete_user_by_id(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while deleting the user"}, 500

def update_user_by_id(id, data):
    try:
        user = User.query.get_or_404(id)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)

        if 'password' in data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user.password_hash = hashed_password

        db.session.commit()
        return {"message": "User updated successfully"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while updating the user"}, 500

def users_list():
    try:
        users = User.query.all()
        user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        return user_list, 200
    except SQLAlchemyError as e:
        return {"error": "An error occurred while retrieving users"}, 500