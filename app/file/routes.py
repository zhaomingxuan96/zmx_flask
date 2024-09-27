from flask import request, jsonify
from flask import send_from_directory
import os
from flask import current_app
from . import file_bp  # 导入父模块中的 auth_bp

@file_bp.route('/upload', methods=['POST'])
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

@file_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)