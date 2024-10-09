from app.extensions import db, bcrypt
from app.models import User
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
import jwt
import datetime

def register_user(username, email, password):
    try:
        # 检查用户名和邮箱是否存在
        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400
        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 400

        # 生成密码哈希并创建新用户
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)

        # 保存到数据库
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while registering the user"}, 500
    except Exception as e:
        return {"error": "Unexpected error occurred: " + str(e)}, 500

def authenticate_user(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            # 生成JWT
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
            }, current_app.config['SECRET_KEY'], algorithm='HS256')

            return {'token': token}, 200
        else:
            return {"message": "Invalid email or password"}, 401
    except SQLAlchemyError as e:
        return {"error": "An error occurred during authentication"}, 500
    except Exception as e:
        return {"error": "Unexpected error occurred: " + str(e)}, 500