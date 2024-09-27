from app import db, bcrypt #这里的db和bcrypt分别是SQLAlchemy和Bcrypt类的实例，用于数据库操作和密码哈希

# 定义用户模型，继承自db.Model其中db.Model是SQLAlchemy类的实例
# User继承自 db.Model, 让User 类成为一个 ORM（对象关系映射）模型。简单来说，通过继承 db.Model，User 类就被视为一个数据库表。
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)# id是主键，整型,db.Integer是SQLAlchemy中的整型字段,总的来说，这里定义了一个整型的主键字段id
    username = db.Column(db.String(20), unique=True, nullable=False)# username是字符串类型，长度为20，唯一且不能为空
    email = db.Column(db.String(120), unique=True, nullable=False)# email也是字符串类型，长度为120，唯一且不能为空
    password_hash = db.Column(db.String(60), nullable=False) # password_hash也是字符串类型，长度为60，不能为空

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)# 使用bcrypt的check_password_hash方法来检查密码是否正确
