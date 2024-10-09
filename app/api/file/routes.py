from flask import request, jsonify, send_from_directory, current_app
import os
from werkzeug.utils import secure_filename
from . import file_bp

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    # return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return True

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(file_path)
            return jsonify({"message": "File uploaded successfully"}), 201
        except Exception as e:
            return jsonify({"message": f"Failed to save file: {str(e)}"}), 500
    else:
        return jsonify({"message": "File type not allowed"}), 400

@file_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(file_path):
        try:
            return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
        except Exception as e:
            return jsonify({"message": f"Failed to send file: {str(e)}"}), 500
    else:
        return jsonify({"message": "File not found"}), 404