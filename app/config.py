import os
from dotenv import load_dotenv  # 导入 dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class Config:
    # 从环境变量中获取 SECRET_KEY，如果没有则使用默认值
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

    # 从环境变量中获取 SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭SQLAlchemy的跟踪修改功能

    # 定义上传文件夹路径
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
