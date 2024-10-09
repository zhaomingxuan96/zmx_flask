from flask import Blueprint
from app.services import jwt_decorators

# 创建 user 蓝图
user_bp = Blueprint('user', __name__)

# 应用 token_required 到整个蓝图
@user_bp.before_request 
@jwt_decorators.token_required 
def before_request():
    pass 

from . import routes  # 导入当前目录下的 routes.py 文件