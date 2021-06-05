import pymysql

# 根据流程
# 1.我们先建立数据库的连接信息
host = '127.0.0.1'  # 数据库的ip地址
user = 'root'  # 数据库的账号
password = '123456'  # 数据库的密码
port = 3306  # mysql数据库通用端口号
mysql = pymysql.connect(host=host, user=user, password=password, port=port, database='student')


def get_name(id):
    cursor = mysql.cursor()
    # 3编写sql
    # sql = 'SELECT * FROM future.member WHERE MobilePhone = 18876153542 '
    sql = "select * from info where id="+str(id)
    # 4.执行sql
    cursor.execute(sql)
    # 5.查看结果
    result = cursor.fetchone() #用于返回单条数据
    print(result)
    # 6.关闭查询
    cursor.close()
