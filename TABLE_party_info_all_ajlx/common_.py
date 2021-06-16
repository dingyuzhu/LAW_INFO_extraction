#-*- coding: UTF-8 -*-
#author：dingyuzhu
#date: 2021-04-08

import config
import pymysql
import datetime
import pandas as pd
from sqlalchemy import create_engine
#数据库连接
# 120.78.145.144
db_connection_prod = config.Prod_db_connect_info


# 120.78.92.6
db_connection_test = config.Test_db_connect_info

# 日期计算函数
def day_range(bgn, end, gap):
    fmt = '%Y/%m/%d'
    begin = datetime.datetime.strptime(bgn, fmt)
    end = datetime.datetime.strptime(end, fmt)
    delta = datetime.timedelta(days=1)

    interval = int((end - begin).days) + 1
    if interval % gap == 0:
        days = [begin + delta * i for i in range(0, interval, gap)]
    else:
        days = [begin + delta * i for i in range(0, interval, gap)]
        days.append(end)
    return days



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
    engine = con_create_engine('%s'%(config.swither))
    pd.io.sql.to_sql(name='%s'%config.Output_table["tb_wenshu_party_info"],
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


def t(str):
    zhong={'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'两':2}
    danwei={'十':10,'百':100,'千':1000,'万':10000}
    num=0
    if len(str)==0:
        return 0
    if len(str)==1:
        if str == '十':
            return 10
        num=zhong[str]
        return num
    temp=0
    if str[0] == '十':
        num=10
    for i in str:
        if i == '零':
            temp=zhong[i]
        elif i == '一':
            temp=zhong[i]
        elif i == '二':
            temp=zhong[i]
        elif i == '三':
            temp=zhong[i]
        elif i == '四':
            temp=zhong[i]
        elif i == '五':
            temp=zhong[i]
        elif i == '六':
            temp=zhong[i]
        elif i == '七':
            temp=zhong[i]
        elif i == '八':
            temp=zhong[i]
        elif i == '九':
            temp=zhong[i]
        if i == '十':
            temp=temp*danwei[i]
            num+=temp
        elif i == '百':
            temp=temp*danwei[i]
            num+=temp
        elif i == '千':
            temp=temp*danwei[i]
            num+=temp
        elif i == '万':
            temp=temp*danwei[i]
            num+=temp
    if str[len(str)-1] != '十'and str[len(str)-1] != '百'and str[len(str)-1] != '千'and str[len(str)-1] != '万':
        num+=temp
    return num



# 更新操作

def update(df):
    for i in range(len(df)):
       # df的遍历是用iloc
        sql = 'update %s set ' \
              'yg_name = "%s",yg_address= "%s",yg_cognitor="%s",yg_cognitor_address="%s",yg_representive="%s", ' \
              'bg_name = "%s",bg_address= "%s",bg_cognitor="%s",bg_cognitor_address="%s",bg_representive="%s", ' \
              '_3rd_name = "%s",_3rd_address= "%s",_3rd_cognitor="%s",_3rd_cognitor_address="%s",_3rd_representive="%s",wenshu_id=%d  where id = %d' \
              % (config.Output_table["tb_wenshu_party_info"],df['yg_name'].iloc[i],df['yg_address'].iloc[i],df['yg_cognitor'].iloc[i],df['yg_cognitor_address'].iloc[i],df['yg_representive'].iloc[i],
                 df['bg_name'].iloc[i], df['bg_address'].iloc[i], df['bg_cognitor'].iloc[i], df['bg_cognitor_address'].iloc[i], df['bg_representive'].iloc[i],
                 df['_3rd_name'].iloc[i], df['_3rd_address'].iloc[i], df['_3rd_cognitor'].iloc[i], df['_3rd_cognitor_address'].iloc[i], df['_3rd_representive'].iloc[i],
                 df['wenshu_id'].iloc[i],df['wenshu_id'].iloc[i]
                 )
        print(df['id'].iloc[i])
        print(sql)

        con = db_connection_prod  # 创建游标对象
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