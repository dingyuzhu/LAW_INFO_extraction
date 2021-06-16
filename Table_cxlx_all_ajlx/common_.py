#-*- coding: UTF-8 -*-
#author：dingyuzhu
#date: 2021-04-29


import pymysql
import datetime
import pandas as pd
from sqlalchemy import create_engine
#数据库连接
# 120.78.145.144
db_connection_prod = pymysql.connect(host="120.78.145.144", user="root", passwd="dfkj2020", use_unicode=True,
                               db="db_extract_increment0",
                               port=3306, charset="utf8")


# 120.78.92.6
db_connection_test = pymysql.connect(host="120.78.92.6", user="root", passwd="dfkj2020", use_unicode=True,
                               db="db_extract_increment0",
                               port=3306, charset="utf8")

# 日期计算函数
def day_range(bgn, end):
    fmt = '%Y/%m/%d'
    begin = datetime.datetime.strptime(bgn, fmt)
    end = datetime.datetime.strptime(end, fmt)
    delta = datetime.timedelta(days=1)
    interval = int((end - begin).days) + 1
    return [begin + delta * i for i in range(0, interval, 1)]



#引擎
def con_create_engine(env):
    if env == 'test':
        engine = create_engine(
            "mysql+pymysql://root:dfkj2020@120.78.92.6:3306/db_extract_increment0?charset=utf8mb4")
        return engine
    elif env == 'prod':
        engine = create_engine(
            "mysql+pymysql://root:dfkj2020@120.78.145.144:3306/db_extract_increment0?charset=utf8mb4")
        return engine
    else:
        return '请输入参数test或prod!'




# 数据框入库
def df_to_sql(df):
    engine = con_create_engine('prod')
    pd.io.sql.to_sql(name='temp_tb_wenshu_cxlx',
                     frame=df,
                     con=engine,
                     index=False,
                     if_exists='append',
                     chunksize=len(df))

# 查询data
def db_connection(db_connection,sql):
    conn_extract = db_connection
    try:
        conn_extract.ping(reconnect=True)
    except:
        print("数据库连接失败")
    cur_extract = conn_extract.cursor()
    cur_extract.execute(sql)
    all_data = cur_extract.fetchall()
    cur_extract.close()
    conn_extract.close()
    return all_data


# 更新操作
def update_Table(df):
    for i in range(len(df)):
        sql = '？？？？？？？？？？？'
        con = db_connection_test  # 创建游标对象
        try:
            con.ping(reconnect=True)
        except:
            print("数据库连接失败")
        cur = con.cursor()
        try:
            # 执行sql
            cur.execute(sql)
            # 提交事务
            con.commit()
            print('更新成功')
        except Exception as e:
            print(e)
            con.rollback()
            print('更新失败')