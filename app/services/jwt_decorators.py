import jwt
from flask import request, jsonify, current_app
from functools import wraps
from app.models import User

def token_required(f):
    @wraps(f) 
    def decorated(*args, **kwargs):

         # 检查是否豁免某些路由
        exempt_routes = ['/user/add']  # 在这里添加需要豁免的路由
        # 检查请求路径是否在豁免路由列表中
        if request.path in exempt_routes:
            return f(*args, **kwargs)

        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header and len(auth_header.split(" ")) == 2 and auth_header.split(" ")[0] == 'Bearer':
                token = auth_header.split(" ")[1]
            else:
                return jsonify({'message': 'Token is missing or invalid!'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)
    return decorated
