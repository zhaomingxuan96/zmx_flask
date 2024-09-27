from flask import Blueprint
from app.jwtDecorators import token_required

# 创建 user 蓝图
user_bp = Blueprint('user', __name__)

# 应用 token_required 到整个蓝图
@user_bp.before_request
@token_required
def before_request():
    pass 

from . import routes  # 导入当前目录下的 routes.py 文件