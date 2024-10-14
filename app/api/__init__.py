from .auth import auth_bp 
from .user import user_bp 
from .file import file_bp 
from .lilly import lilly_bp
  # 蓝图列表
blueprints = [
        (auth_bp, '/auth'),
        (user_bp, '/user'),
        (file_bp, '/file'),
        (lilly_bp, '/lilly')
    ]