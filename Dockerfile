# 使用 Python 3.10 作为基础镜像
FROM python:3.10

# 更新源并安装必要的依赖库
RUN apt-get update && \
    apt-get install -y build-essential libmariadb-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件并安装依赖
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 复制项目所有文件到 /app 目录
COPY . .

# 安装环境变量管理工具
RUN pip install python-dotenv

# 设置环境变量
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# 公开端口
EXPOSE 5000

# 复制 wait-for-it.sh 脚本到工作目录
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# 运行数据库迁移并启动 Flask
CMD /wait-for-it.sh db:3306 -- flask db upgrade && flask run --host=0.0.0.0
