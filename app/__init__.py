from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy  # 导入SQLAlchemy 作用是数据库操作
from flask_migrate import Migrate # 导入Migrate 作用是数据库迁移
from flask_bcrypt import Bcrypt # 导入Bcrypt 作用是密码加密
from flask_login import LoginManager # 导入LoginManager 作用是用户登录s
from config import Config # 导入Config 作用是配置文件，import引入是从根目录开始找config.py文件

db = SQLAlchemy() # 初始化数据库，具体来说是创建一个SQLAlchemy对象，用于与数据库进行交互
migrate = Migrate() # 初始化迁移，具体来说是创建一个Migrate对象，用于与数据库迁移进行交互
bcrypt = Bcrypt() # 初始化加密，具体来说是创建一个Bcrypt对象，用于与密码加密进行交互
login_manager = LoginManager() # 初始化登录，具体来说是创建一个LoginManager对象，用于与用户登录进行交互

def create_app():
    app = Flask(__name__) # 创建Flask应用程序实例 __name__是当前模块的名字，即当前模块所在的包或模块的名字
    app.config.from_object(Config) # 从Config类中读取配置信息，并将其设置为Flask应用程序的配置，这些配置信息包括数据库连接信息、密钥等

    db.init_app(app) # 初始化数据库连接
    migrate.init_app(app, db)   # 初始化数据库迁移
    bcrypt.init_app(app)        # 初始化密码加密
    login_manager.init_app(app) # 初始化登录

    @app.route('/test', methods=['GET'])
    def test():
        return jsonify(message="这是一个测试接口！"), 200
    
    from .auth import auth_bp   # 导入auth_bp蓝图,从当前包下的auth包中导入auth_bp蓝图
    from .user import user_bp   # 导入user_bp蓝图，从当前包下的user包中导入user_bp蓝图
    from .file import file_bp   # 导入file_bp蓝图，从当前包下的file包中导入file_bp蓝图

    app.register_blueprint(auth_bp, url_prefix='/auth') # 注册auth_bp蓝图,url_prefix是路由前缀，用于区分不同蓝图的路由
    app.register_blueprint(user_bp, url_prefix='/user') # 注册user_bp蓝图
    app.register_blueprint(file_bp, url_prefix='/file') # 注册file_bp蓝图

    return app