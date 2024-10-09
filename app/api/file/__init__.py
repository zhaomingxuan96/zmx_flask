from flask import Blueprint
from app.services.jwt_decorators import token_required

# 创建 user 蓝图
file_bp = Blueprint('file', __name__)

# 应用 token_required 到整个蓝图
@file_bp.before_request
@token_required
def before_request():
    pass 

from . import routes  # 导入当前目录下的 routes.py 文件