# -*- coding:utf-8 -*-

import time
import common_
import pandas as pd
from MS_ES import ms_es_pjs
from MS_ES import ms_es_cds
from MS_ES import ms_es_tjs
from MS_YS import ms_ys_cds
from MS_YS import ms_ys_tjs
from MS_YS import ms_ys_tzs
from MS_YS import ms_ys_pjs
from MS_ZS import ms_zs_cds
from MS_ZS import ms_zs_jds
from MS_ZS import ms_zs_tzs

import config


if __name__ == "__main__":

    start= time.time()
    days = common_.day_range('2019/07/01', '2019/07/01')
    for i in range(len(days)):
        t1 = time.time()
        # 民事一审判决书
        sql0 =  'select a.id,b.ajlx, b.wslx, b.spcx_id, c.yg_pct, c.bg_pct,c.pjjg_cost_bear,a.pjjg,a.party_info ' \
                'from ' \
                '%s a left join '\
                '%s b on a.id = b.wenshu_id left join ' \
                '%s c on a.id=c.wenshu_id  left join ' \
                '%s d on a.id = d.id '\
                'where a.id = 533531574033976319'% (config.Input_table["tb_wenshu_paragraph"],config.Input_table["tb_wenshu_check"],config.Input_table["tb_wenshu_check_pjjg_detail_fee_pct"],config.Input_table["tb_wenshu"])

        # 民事一审、二审的其他文书类型
        sql1 =  'SELECT a.id,a.pjjg,b.ajlx,b.wslx,b.spcx_id,a.sb,a.ssqq ' \
                'FROM ' \
                '%s a LEFT JOIN ' \
                '%s b ON a.id=b.wenshu_id LEFT JOIN ' \
                '%s c ON a.id = c.id ' \
                'WHERE a.id = 533531574033976319 '%(config.Input_table["tb_wenshu_paragraph"],config.Input_table["tb_wenshu_check"],config.Input_table["tb_wenshu"])


        # 民事再审245且只处理pjjg有的
        sql2 = 'SELECT a.id, c.ajmc, a.pjjg, b.wslx, c.pjjg as orin_pjjg ' \
               'FROM ' \
               '%s a left join ' \
               '%s b on a.id=b.wenshu_id left join ' \
               '%s c on a.id=c.id ' \
               'where a.id = 533531574033976319'%(config.Input_table["tb_wenshu_paragraph"],config.Input_table["tb_wenshu_check"],config.Input_table["tb_wenshu"])


        # 更新
        with open('update_list.txt',encoding='utf-8') as f:
            lines = f.readlines()
            lines = tuple([int(i.strip()) for i in lines])

        # 具体更新内容看上述三个sql
        sql_update = 'WHERE a.id in {}'.format(lines)


        print('今天是：', str(days[i])[:10], '，是时间轴中的第', str(i), '天，还剩下' , str(len(days) - i) ,'天')

        # 测试
        if config.swither == "test":
            # 民事一审判决书
            all_data0 = common_.db_connection(common_.db_connection_test, sql0)
            # 民事一审、二审
            all_data1 = common_.db_connection(common_.db_connection_test, sql1)
            # # 民事再审
            all_data2 = common_.db_connection(common_.db_connection_test, sql2)
        # 生产
        else:
            # 民事一审判决书
            all_data0 = common_.db_connection(common_.db_connection_prod, sql0)
            # 民事一审、二审
            all_data1 = common_.db_connection(common_.db_connection_prod, sql1)
            # # 民事再审
            all_data2 = common_.db_connection(common_.db_connection_prod, sql2)


        e1 = time.time()
        print('SQL执行时间：', e1-t1)


        t2 = time.time()

        # 民事一审判决书判决结果
        ms_ys_pjs_ = ms_ys_pjs.MS_YS_PJS()
        result_dict_pjjg_0, dict_res = ms_ys_pjs_.run(all_data0)
        df0 = common_.dict_to_df(result_dict_pjjg_0, dict_res)
        # common_.df_to_sql(df0)

        # 民事一审裁定书判决结果
        ms_ys_cds_ = ms_ys_cds.MS_YS_CDS()
        result_dict_pjjg_1,dict_res = ms_ys_cds_.run(all_data1)
        df1 = common_.dict_to_df(result_dict_pjjg_1,dict_res)
        ## common_.df_to_sql(df1)



        # 民事一审调解书判决结果
        ms_ys_tjs_ = ms_ys_tjs.MS_YS_TJS()
        result_dict_pjjg_2, dict_res = ms_ys_tjs_.run(all_data1)
        df2 = common_.dict_to_df(result_dict_pjjg_2, dict_res)
        # # common_.df_to_sql(df2)




        # 民事一审通知书判决结果
        ms_ys_tzs_ = ms_ys_tzs.MS_YS_TZS()
        result_dict_pjjg_3, dict_res = ms_ys_tzs_.run(all_data1)
        df3 = common_.dict_to_df(result_dict_pjjg_3,dict_res)
        # # common_.df_to_sql(df3)



        # 民事二审判决书判决结果
        ms_es_pjs_ = ms_es_pjs.MS_ES_PJS()
        result_dict_pjjg_4, dict_res = ms_es_pjs_.run(all_data1)
        df4 = common_.dict_to_df(result_dict_pjjg_4, dict_res)
        # # common_.df_to_sql(df4)



        # 民事二审裁定书判决结果
        ms_es_cds_ = ms_es_cds.MS_ES_CDS()
        result_dict_pjjg_5,dict_res = ms_es_cds_.run(all_data1)
        df5 = common_.dict_to_df(result_dict_pjjg_5,dict_res)
        # # common_.df_to_sql(df5)



        # 民事二审调解书
        ms_es_tjs_ = ms_es_tjs.MS_ES_TJS()
        result_dict_pjjg_6, dict_res = ms_es_tjs_.run(all_data1)
        df6 = common_.dict_to_df(result_dict_pjjg_6,dict_res)
        #common_.df_to_sql(df6)

        # 民事再审裁定书
        ms_zs_cds_ = ms_zs_cds.MS_ZS_CDS()
        result_dict_pjjg_7 = ms_zs_cds_.run(all_data2)
        df7 = common_.dict_to_df_zs(result_dict_pjjg_7)

        # 民事再审决定书
        ms_zs_jds_ = ms_zs_jds.MS_ZS_JDS()
        result_dict_pjjg_7 = ms_zs_jds_.run(all_data2)
        df8 = common_.dict_to_df_zs(result_dict_pjjg_7)

        # 民事再审通知书
        ms_zs_tzs_ = ms_zs_tzs.MS_ZS_TZS()
        result_dict_pjjg_7 = ms_zs_tzs_.run(all_data2)
        df9 = common_.dict_to_df_zs(result_dict_pjjg_7)



        # 多个df纵向拼接
        df_arr = [df0, df1, df2, df3, df4, df5, df6, df7, df8, df9]
        print(len(df0), len(df1), len(df2), len(df3), len(df4), len(df5), len(df6), len(df7), len(df8), len(df9))

        valid_df_arr = [i for i in df_arr if len(i) > 0]

        if valid_df_arr:
            df = pd.concat(valid_df_arr, axis=0)
            e2 = time.time()
            print('数据处理时间：', e2 - t2)

            if len(df) > 0:
                df = pd.concat(valid_df_arr, axis=0)
                t3 = time.time()
                # common_.df_to_sql(df)
                common_.update(df)
                e3 = time.time()
                print('入库时间：', e3 - t3)
            else:
                print('入库时间：0.0000000')
        else:
            print('入库时间：0.0000000')


    end = time.time()
    print(end-start)



