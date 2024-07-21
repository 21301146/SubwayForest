from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from enity.User import User
import json
from flask_cors import CORS
import pymysql
from datetime import datetime, timedelta
import random


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:9876"}})

# 设置数据库连接地址
DB_URI = 'mysql+pymysql://root:YJzj0610&@localhost:3306/subway'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# 是否追踪数据库修改，一般不开启, 会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 是否显示底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True

# 初始化db,关联flask 项目
#可以通过这个实例进行数据库的操作和管理
db = SQLAlchemy(app)

random_int = random.randint(200, 500)


def czmysql():
    # MySQL 连接配置
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'YJzj0610&',
        'db': 'subway',
        'charset': 'utf8mb4',
    }

    # 创建数据库连接
    conn = pymysql.connect(**config)

    # 创建游标对象
    cursor = conn.cursor()
    return cursor



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')

        if not all([username,password]):
            return json.dumps({"Code":200,"data":False,"msg":"参数不完整"})
        else:
            # new_user = User.query.filter(username==username,password==password)
            try:
                cursor = czmysql()
                cursor.execute("SELECT * FROM tb_user WHERE username=%s AND password=%s", (username, password))
                user = cursor.fetchone()
                if(user):
                    return json.dumps({"Code":200,"data":True,"msg":"登录成功"})
            except:
                return json.dumps({"Code": 200, "data": False, "msg": "登录失败"})


@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        username = request.args.get('usename')
        password = request.args.get('password')

        if not all([username,password]):
            return json.dumps({"Code":200,"data":False,"msg":"参数不完整"})
        else:
            new_user = User(username=username,password=password)
            if(new_user):
                db.session.add(new_user)
                db.session.commit()
                return json.dumps({"Code":200,"data":True,"msg":"注册成功"})



#扇形图占比
@app.route("/Turnoverforaccounted",methods=['GET','POST'])
def Turnoverforaccounted():
    if request.method == 'GET':
        query = "select station,sum(deal_money) from tb_data GROUP BY station ORDER BY sum(deal_money) desc LIMIT 10"
        cursor = czmysql()
        cursor.execute(query)
        results = cursor.fetchall()
        # 将结果转换为字典，并返回 JSON 格式的数据
        data = [{'name': row[0], 'value': row[1]} for row in results if row[1] != 0.0]
        return json.dumps({"Code":200,"data":data,"msg":"查询成功"})


#进出口信息
@app.route("/subwayinfomation",methods=['GET','POST'])
def subwayinfomation():
    if request.method == 'GET':
        query = "select station,sum(deal_value) from tb_data GROUP BY station ORDER BY sum(deal_value) desc LIMIT 10"
        cursor = czmysql()
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
        # 将结果转换为字典，并返回 JSON 格式的数据
        data = [{'name': row[0], 'value1': row[1] , 'value2': row[1] - random_int} for row in results if row[1] != 0.0]
        print(data[:6])
        return json.dumps({"Code":200,"data":data[:6],"msg":"查询成功"})

#营业额top10
@app.route("/subwaydealmoneytop10",methods=['GET','POST'])
def subwaydealmoneytop10():
    if request.method == 'GET':
        query = "select station,sum(deal_money) as dm from tb_data GROUP BY station ORDER BY dm DESC LIMIT 10;"
        cursor = czmysql()
        cursor.execute(query)
        results = cursor.fetchall()
        # 将结果转换为字典，并返回 JSON 格式的数据
        data = [{'name': row[0], 'value': row[1]} for row in results]
        return json.dumps({"Code":200,"data":data,"msg":"查询成功"})

#地图展示预测信息
@app.route("/subwaymapinfo",methods=['GET','POST'])
def subwaymapinfo():
    if request.method == 'GET':
        id = 0
        current_time = datetime.now()
        formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        later_time = current_time + timedelta(hours=1)
        formatted_later_time = later_time.strftime("%Y-%m-%d %H:%M:%S")
        later_time2 = current_time + timedelta(hours=12)
        formatted_later_time2 = later_time2.strftime("%Y-%m-%d %H:%M:%S")
        query = "select * from tb_predict_data"
        cursor = czmysql()
        cursor.execute(query)
        results = cursor.fetchall()
        data = []
        for row in results:
            id += 1
            rs = {
                'id' : id,
                'position' : {
                    'lng' : row[1],
                    'lat' : row[2]
                },
                'title' : row[6] +  " 预测结果: ",
                'content1' : formatted_current_time + " 客流量: " + row[3],
                'content2' : formatted_later_time + " 客流量: " + row[4],
                'content3' : formatted_later_time2 +" 客流量: " + row[5]
                # 'content' :row[6] +  " 预测结果: \n" + formatted_current_time + " 客流量: " + row[3] + "\n" + formatted_later_time + " 客流量: " + row[4] + "\n" + formatted_later_time2 +" 客流量: " + row[5]
            }
            data.append(rs)

        # # 将结果转换为字典，并返回 JSON 格式的数据
        # data = [{'id':1 ,'name': row[0], 'value': row[1]} for row in results]
        return json.dumps({"Code":200,"data":data,"msg":"查询成功"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
