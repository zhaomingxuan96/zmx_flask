from flask import Flask,request, jsonify
from flask import render_template
from app.api import blueprints
from app.config import Config # 导入Config 作用是配置文件，import引入是从根目录开始找config.py文件
from app.extensions import db, migrate, bcrypt

def create_app():
    app = Flask(__name__) # 创建Flask应用程序实例 __name__是当前模块的名字，即当前模块所在的包或模块的名字
    app.config.from_object(Config) # 从Config类中读取配置信息，并将其设置为Flask应用程序的配置，这些配置信息包括数据库连接信息、密钥等

    db.init_app(app) # 初始化数据库连接
    migrate.init_app(app, db)   # 初始化数据库迁移
    bcrypt.init_app(app)        # 初始化密码加密

    @app.route('/', methods=['GET'])
    def test():
        return render_template('hello.html'),200
    
    # 注册 api 模块中的蓝图
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

    return app