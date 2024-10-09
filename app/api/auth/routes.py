from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from . import auth_bp  
from app.services import auth_service

@auth_bp.route('/register', methods=['POST']) #这是注册路由，@是装饰器，auth_bp是蓝图对象，register是路由函数
def register():
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("No data provided")
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({"error": "Username, email, and password are required"}), 400
        
        response, status = auth_service.register_user(username, email, password)
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred"}), 500
    return jsonify(response), status

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        email = data.get('email')
        password = data.get('password')
        response, status = auth_service.authenticate_user(email, password)
    except Exception as e:
        return jsonify({"error": str(e)}), 500   
    return jsonify(response), status