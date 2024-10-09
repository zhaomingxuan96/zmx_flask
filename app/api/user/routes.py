from flask import request, jsonify
from . import user_bp
from app.services import auth_service
from app.services import user_service
from werkzeug.exceptions import BadRequest

@user_bp.route('/add', methods=['POST'])
def add_user():
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

@user_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        response, status = user_service.delete_user_by_id(id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(response), status

@user_bp.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        response, status = user_service.update_user_by_id(id, data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(response), status

@user_bp.route('/list', methods=['GET'])
def list_users():
    try:
        response, status = user_service.users_list()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(response), status