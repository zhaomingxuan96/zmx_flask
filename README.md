# zmx_flask

## 项目简介
这是一个使用 Flask 框架构建的用户管理系统，支持用户注册、登录、用户信息管理以及文件上传和下载功能。

## 功能特性
- 用户注册与登录
- 用户信息添加、删除、更新和查询
- 文件上传与下载
- 使用 MySQL 数据库存储数据

## 技术栈
- Flask
- MySQL
- Docker


## 安装与配置
### 使用docker部署
克隆仓库：
```bash
git clone https://github.com/zhaomingxuan96/zmx_flask.git

```
构建镜像：
```bash
docker-compose build
```
启动容器[flask和mysql]：
```bash
docker-compose up
```
数据库映射宿主机端口：`3333`
数据库用户名：`root`
数据库密码：`123456`

访问：`http://127.0.0.1:5000/`

## 本地部署
### 1. 项目初始化
首先，确保你已安装 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 或 [Anaconda](https://www.anaconda.com/products/distribution).

### 2. 创建项目目录
在开发环境中创建项目目录 `flask_project`。

### 3. 创建并激活虚拟环境
使用以下命令创建虚拟环境：
```bash
conda create -n flask_env python=3.10
```
然后，使用以下命令激活虚拟环境：
```bash
conda activate flask_env
```

### 4. 克隆仓库
```bash
git clone https://github.com/zhaomingxuan96/zmx_flask.git
```

### 5. 安装依赖
进入项目目录后，安装所需依赖：
```bash
pip install -r requirements.txt
```

### 6. 配置文件
在项目根目录下创建 `.env` 文件，复制.env.example 中的内容到 `.env` 文件中，并修改其中的配置信息。

### 7. 数据库迁移
使用 Flask-Migrate 进行数据库迁移：
```bash
flask db init
flask db migrate -m "create users table"
flask db upgrade
```

### 8. 运行项目
使用以下命令运行项目：
```bash
flask run
```

### 9.使用说明
使用postman等工具，访问 http://127.0.0.1:5000/ 
- **用户注册**：`POST /auth/register`
- **用户登录**：`POST /auth/login`
- **获取用户列表**：`GET /user/list`

### 10.贡献指南
欢迎任何形式的贡献！请提出建议或提交代码。

### 11.许可证
本项目使用 MIT 许可证。