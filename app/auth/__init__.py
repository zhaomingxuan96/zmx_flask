from flask import Blueprint

# 创建 auth 蓝图
auth_bp = Blueprint('auth', __name__) # 创建一个名为 'auth' 的变量 auth_bp

from . import routes  # 导入当前目录下的 routes.py 文件,其中.表示当前目录