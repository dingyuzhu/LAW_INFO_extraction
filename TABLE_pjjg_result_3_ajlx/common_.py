
#-*- coding: UTF-8 -*-
#author：dingyuzhu
#date: 2021-04-29

import re
import pymysql
import config
import datetime
import pandas as pd
from sqlalchemy import create_engine
#数据库连接
# 120.78.145.144
db_connection_prod = config.Prod_db_connect_info

# 120.78.92.6
db_connection_test = config.Test_db_connect_info

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





#字典转df
def dict_to_df(result_dict_pjjg,dict_res):

    v_temp = {'id': [], 'wenshu_id': [], 'pjjg_result': [], 'pjjg_lx': []}
    for k, v in result_dict_pjjg.items():
        if k:
            if result_dict_pjjg[k]:
                v_temp['id'].append(k)
                v_temp['wenshu_id'].append(k)
                v_temp['pjjg_result'].append(v['判决结果'])
                v_temp['pjjg_lx'].append(v['判决结果类型'])
                # v_temp['is_over'].append(0)
        #         if v['判决结果'] in is_over_pjjg():
        #             is_over = 1
        #             if dict_res[k][0] == 3 and dict_res[k][2] == 30200000000000000: # ajlx, wslx, spcx_id,ssqq
        #                 if dict_res[k][1] == 2 or dict_res[k][1] == 5:
        #                     if dict_res[k][3]:
        #                         if re.search('管辖', dict_res[k][3]):
        #                             is_over = 0
        #             v_temp['is_over'].append(is_over)
        #         else:
        #             v_temp['is_over'].append(0)
        # else:
        #     print(k, v)



    df = pd.DataFrame(v_temp)
    df['is_over'] = None
    return df

# 民事再审
def dict_to_df_zs(result_dict_pjjg):
    v_temp = {'id': [], 'wenshu_id': [], 'pjjg_lx': [], 'pjjg_result': []}
    for k, v in result_dict_pjjg.items():
            v_temp['id'].append(k)
            v_temp['wenshu_id'].append(k)
            v_temp['pjjg_lx'].append(v['判决结果类型'])
            v_temp['pjjg_result'].append(v['判决结果'])


    df = pd.DataFrame(v_temp)
    df['is_over'] = None
    return df


# 数据框入库
def df_to_sql(df):
    engine = con_create_engine('%s'%config.swither)
    pd.io.sql.to_sql(name='%s'%config.Output_table["tb_wenshu_pjjg_result"],
                     frame=df,
                     con=engine,
                     index=False,
                     if_exists='append',
                     chunksize=len(df))


# 更新操作
def update(df):

    for i in range(len(df)):
       # df的遍历是用iloc
        sql = 'update %s set ' \
              'pjjg_lx = "%s",pjjg_result= "%s",wenshu_id=%d  where id = %d' \
              % (config.Output_table["tb_wenshu_pjjg_result"],df['pjjg_lx'].iloc[i],df['pjjg_result'].iloc[i],df['wenshu_id'].iloc[i],df['id'].iloc[i])

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