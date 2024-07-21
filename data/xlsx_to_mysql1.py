import pandas as pd
import pymysql
import random

# 读取 Excel 文件到 pandas 数据框
df = pd.read_excel('深圳通刷卡数据.xlsx')

# 建立与 MySQL 数据库的连接
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='YJzj0610&',
    db='subway',
    charset='utf8mb4'
)

# 创建一个游标对象
cursor = conn.cursor()

sql = "DELETE from tb_data"
cursor.execute(sql)
conn.commit()

# 遍历数据框中的每一行，将数据插入数据库
for i, row in df.iterrows():
    # 获取每一列的值
    col1 = row['deal_date']
    col2 = row['close_date']
    col3 = row['card_no']
    col4 = row['deal_value']
    col5 = row['deal_type']
    col6 = row['company_name']
    col7 = row['car_no']
    col8 = row['station']
    col9 = row['conn_mark']
    col10 = row['deal_money']
    col11 = row['equ_no']

    max = random.randint(300, 400)
    min = random.randint(50, 100)

    data_period = col1[11:-6]
    if data_period[0] == '0':
        data_period = data_period[1:]
    data_period = eval(data_period)
    if data_period >= 6 and data_period <= 9:
        col4 = max
    elif data_period >= 18 and data_period <= 20:
        col4 = max
    else:
        col4 = min

    # 构建插入语句
    # sql = f"INSERT INTO tb_data (`deal_date`, `colse_date`, `deal_value`, `deal_type`, `company_name`,`card_no`, `car_no`, `station`, `conn_mark`, `deal_money`, `equ_no` ) VALUES ('{col1}', '{col2}', '{col3}','{col4}','{col5}','{col6}','{col7}','{col8}','{col9}','{col10}','{col11}')"

    sql = 'insert into tb_data(`deal_date`,`close_date`,`crad_no`,`deal_value`,`deal_type`,`company_name`,`car_no`,`station`,`conn_mark`,`deal_money`,`equ_no`) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")' % (
        str(col1), str(col2), str(col3), str(col4), str(col5), str(col6), str(col7), str(col8), str(col9), str(col10),
        str(col11))
    # 执行插入语句
    cursor.execute(sql)
    # print(i)

# 提交更改
conn.commit()
print("导入完毕，请查看~v~")
# 关闭游标和连接
cursor.close()
conn.close()
