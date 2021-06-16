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


# 字典转数据框
def dict_to_df(dict_party_info, dict_ssqq, dict_ss_ssqq, dict_top, dict_pjjg, extra_dict ):
    v_tmp = {'id': [], 'wenshu_id': [], 'party_info': [], 'ssqq': [], 'ss_ssqq': [], 'sb': [], 'pjjg': []}

    for k, v in extra_dict.items():

        if k not in dict_party_info.keys():
            v_tmp['party_info'].append('')
        else:
            v_tmp['party_info'].append(dict_party_info[k])

        if k not in dict_ssqq.keys():
            v_tmp['ssqq'].append('')
        else:
            v_tmp['ssqq'].append(dict_ssqq[k])

        if k not in dict_ss_ssqq.keys():
            v_tmp['ss_ssqq'].append('')
        else:
            v_tmp['ss_ssqq'].append(dict_ss_ssqq[k])

        if k not in dict_top.keys():
            v_tmp['sb'].append('')
        else:
            v_tmp['sb'].append(dict_top[k])

        if k not in dict_pjjg.keys() :
            v_tmp['pjjg'].append('')
        else:
            v_tmp['pjjg'].append(dict_pjjg[k])

        v_tmp['id'].append(k)
        v_tmp['wenshu_id'].append(k)


    df = pd.DataFrame(v_tmp)

    return df

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
    engine = con_create_engine('%s'%config.swither)
    pd.io.sql.to_sql(name='%s'%config.Output_table["tb_wenshu_paragraph"],
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



# 单条插入
def insert_into(success_pjjg):
    for k, v in success_pjjg.items():

        sql = 'insert into %s (id,wenshu_id,pjjg) VALUES (%d,%d,"%s")' % (config.Output_table["tb_wenshu_paragraph"],k, k, v)
        print(sql)
        con= db_connection_prod        # 创建游标对象
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
            print('插入成功')
        except Exception as e:
            print(e)
            con.rollback()
            print('插入失败')




# 更新操作

def update(df):
    for i in range(len(df)):

       # df的遍历是用iloc
        sql = 'update %s set  wenshu_id = %d,party_info="%s", ssqq="%s", ss_ssqq="%s", sb= "%s", pjjg = "%s"  where id = %d'\
              % (config.Output_table["tb_wenshu_paragraph"],df['id'].iloc[i],df['party_info'].iloc[i],
                 df['ssqq'].iloc[i],df['ss_ssqq'].iloc[i],df['sb'].iloc[i],df['pjjg'].iloc[i],df['id'].iloc[i])
        print(df['id'].iloc[i])
        print(sql)

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