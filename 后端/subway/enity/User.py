from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 设置数据库连接地址
DB_URI = 'mysql+pymysql://root:YJzj0610&@localhost:3306/subway'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# 是否追踪数据库修改，一般不开启, 会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 是否显示底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True

# 初始化db,关联flask 项目
db = SQLAlchemy(app)


# 定义一个用户及密码的数据库
class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(16))
