from app import db, bcrypt  # 从 app 导入 bcrypt 和 db
from flask import request, jsonify
from app import db
from app.models import User
from flask import send_from_directory
import os
from flask import current_app
from . import user_bp  # 导入父模块中的 auth_bp

@user_bp.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully"}), 201

@user_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"}), 200

@user_bp.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    if 'password' in data:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.password_hash = hashed_password

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

@user_bp.route('/list', methods=['GET'])
def list_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]

    return jsonify(user_list), 200

@user_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully"}), 201

@user_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)