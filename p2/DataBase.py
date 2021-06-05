import pymysql

host = '127.0.0.1'  # 数据库的ip地址
user = 'root'  # 数据库的账号
password = '123456'  # 数据库的密码
port = 3306  # mysql数据库通用端口号
mysql = pymysql.connect(host=host, user=user, password=password, port=port, database='student')


def get_id(sid, name):
    out = []
    cursor = mysql.cursor()
    sql = "select * from info where sid=" + sid + " and name=" + name
    cursor.execute(sql)
    results = cursor.fetchone()
    for row in results:
        out.append(row)
    cursor.close()
    return out


def get_info(id):
    out = []
    cursor = mysql.cursor()
    sql = "select * from info where id=" + str(id)
    cursor.execute(sql)
    results = cursor.fetchone()
    for row in results:
        out.append(row)
    cursor.close()
    return out


def update(sql, args):
    cursor = mysql.cursor()
    cursor.execute(sql, args)
    mysql.commit()
    cursor.close()


def sub(id, cost):
    out = get_info(id)
    old_money = out[3]
    money = old_money - cost
    if money >= 0:
        sql = 'UPDATE info SET money=%s WHERE id = %s;'
        args = (str(money), str(id))
        update(sql, args)
        out[3] = money
        return True, out
    else:
        out[3] = old_money
        return False, out


def add_one(sid, myname, money):
    cursor = mysql.cursor()
    sql = 'insert into info(sid,name,money) values(' + sid + ',' + myname + ',' + money + ');'
    print(cursor.execute(sql))
    mysql.commit()
    cursor.close()
