import jwt
import datetime
from flask import request, jsonify,current_app
from app import db, bcrypt
from app.models import User
from app import login_manager
from . import auth_bp  

@auth_bp.route('/register', methods=['POST']) #这是注册路由，@是装饰器，auth_bp是蓝图对象，register是路由函数
def register():
    data = request.get_json() #获取请求体中的JSON数据，关于request是Flask提供的请求对象，get_json()是从请求体中获取JSON数据的方法
    username = data.get('username') #从JSON数据中获取用户名、邮箱和密码
    email = data.get('email')
    password = data.get('password')

# 检查用户名和邮箱是否已存在，具体来说，就是在User模型中查找是否存在username或email字段与传入的数据相同的记录
    if User.query.filter_by(username=username).first(): # User.query是User模型的查询对象，代表了一组操作数据库的功能(例如：filter_by，first，all, get),filter_by是过滤器，第一个参数是字段名，第二个参数是过滤值
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')   #生成密码哈希
    new_user = User(username=username, email=email, password_hash=hashed_password) #创建新用户对象

    db.session.add(new_user) #将对象添加到数据库会话
    db.session.commit() #提交数据库会话，真正写入数据库

    return jsonify({"message": "User registered successfully"}), 201

# 定义用户加载函数，用于从数据库中加载用户信息，用于Flask-Login的用户认证，调用时机是在用户登录成功后，自动调用
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(f"Email: {email}, Password: {password}")
    user = User.query.filter_by(email=email).first() # 查询用户
    if user and bcrypt.check_password_hash(user.password_hash, password):
         # 生成JWT
        token = jwt.encode({
            'user_id': user.id,
             'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)  # 令牌有效期为1天
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401