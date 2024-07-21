import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta
import random
import requests
import pymysql
import mysql.connector
from sklearn.metrics import r2_score

import schedule
import time

# 获取深圳地区的经纬度
def get_geocode(address):
    url = 'http://api.map.baidu.com/geocoding/v3/?address={}&city=深圳市&output=json&ak=pLqEB5nrCO5pjq4ki1QLY6ffTBIcEBBy'.format(
        address)
    response = requests.get(url)
    data = response.json()
    if data['status'] == 0:
        location = data['result']['location']
        longitude = location['lng']
        latitude = location['lat']
        return longitude, latitude
    else:
        return None


def job():
    print("执行定时任务")

    # 建立数据库连接
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='YJzj0610&',
        database='subway'
    )

    # 创建游标对象
    cursor = cnx.cursor()

    # 1. 读取数据
    query = "SELECT deal_date, deal_value, station FROM tb_data LIMIT 5000"
    cursor.execute(query)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows, columns=['deal_date', 'deal_value', 'station'])

    predict_data = []
    # 根据某列的内容进行分类
    grouped_data = data.groupby("station")
    for group_name, group_data in grouped_data:
        longitude, latitude = get_geocode(group_name + "深圳")

        # 2. 准备数据
        data['deal_date'] = pd.to_datetime(data['deal_date'])
        data['day'] = data['deal_date'].dt.day
        data['hour'] = data['deal_date'].dt.hour
        data['minute'] = data['deal_date'].dt.minute

        # # 3. 划分数据集
        train_data, test_data, train_target, test_target = train_test_split(
            data[['day', 'hour', 'minute']], data['deal_value'], test_size=0.2, random_state=42)

        # # 4. 构建模型
        model = RandomForestRegressor(n_estimators=100, max_depth=10)

        # 5. 训练模型
        model.fit(train_data, train_target)

        # 6. 进行预测
        predictions = model.predict(test_data)
        #
        # 7. 评估模型
        mse = mean_squared_error(test_target, predictions)
        accuracy = r2_score(test_target, predictions)
        print('均方根误差（RMSE）：', mse ** 0.5)
        print('预测准确率:', accuracy)

        # 8. 预测未来几天的客流量
        # 假设有一个包含未来几天日期的数据集"future_data"
        current_time = datetime.now()
        second_time = current_time + timedelta(hours=1)
        three_time = current_time + timedelta(hours=12)

        future_data = pd.DataFrame({
            'day': [current_time.day, second_time.day, three_time.day],
            'hour': [current_time.hour, second_time.hour, three_time.hour],
            'minute': [current_time.minute, second_time.minute, three_time.minute],
        })

        future_predictions = model.predict(future_data)

        print(group_name + " 经纬度 : " + str(longitude) + "," + str(latitude))
        print(group_name + '未来几小时的客流量预测：', future_predictions)
        print(future_predictions[0])
        print(future_predictions[1])
        print(future_predictions[2])
        pds = {
            'longiude': longitude,
            'lastiude': latitude,
            'current_time_data': str(future_predictions[0]),
            'second_time_data': str(future_predictions[1]),
            'three_time_data': str(future_predictions[2]),
            'station': str(group_name)
        }

        predict_data.append(pds)

    for d in predict_data:
        # 插入数据的SQL语句
        insert_query = "INSERT INTO tb_predict_data(longiude, lastiude, current_time_data,second_time_data,three_time_data,station) VALUES (%s, %s, %s,%s,%s,%s)"
        # 插入的数据
        data = (
            str(d['longiude']), str(d['lastiude']), str(int(eval(d['current_time_data']))),
            str(int(eval(d['second_time_data']))), str(int(eval(d['three_time_data']))), str(d['station']))
        # 执行插入操作
        cursor.execute(insert_query, data)
        # 提交事务
        cnx.commit()
        time.sleep(2)
    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


# 定义一个任务，每隔30分钟执行
schedule.every(30).minutes.do(job)

# 不断地运行调度程序，直到程序结束
while True:
    schedule.run_pending()
    time.sleep(1)
