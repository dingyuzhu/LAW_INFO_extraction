# -*- coding: UTF-8 -*-

'''
tb_wenshu_*_*_paragraph表更新，
更新方式：
1.全字段更新
2.单字段更新
该表中的字段：
id,wenshu_id,ajlx,wslx,spcx_id,ssqq,ss-ssqq,party_info,ssjl,pjjg,update_time,create_time
'''


import time

import config
import Extract_2
import Extract_3
import Extract_4
import Extract_other
import common_
import pjjg_extract
import pandas as pd



if __name__ == "__main__":

    # 开始时间
    start = time.time()
    days = common_.day_range('2019/07/23', '2019/07/31',1)

    for i in range(len(days)):
        t1 = time.time()
        sql = config.Input_sql["sql1"].format(str(days[i])[:10])

        # 读出的数据
        if config.swither == "prod":
            all_data = common_.db_connection(common_.db_connection_prod, sql)
        else:
            all_data = common_.db_connection(common_.db_connection_test, sql)

        e1 = time.time()
        print('今天是：', str(days[i])[:10], '，是时间轴中的第', str(i), '天，还剩下' , str(len(days) - i) ,'天')
        print('sql读取时间:', e1-t1)

        t2 = time.time()

        # 刑事
        p = pjjg_extract.PJJG_Abstract()
        a2 = Extract_2.Fields_abstract()
        dict_party_info2, dict_ssqq2, dict_ss_ssqq2, dict_top2, extra_dict2 = a2.fields_dict_extract(all_data)
        dict_data2 = p.get_data2(all_data)
        dict_pjjg2 = p.run(dict_data2)
        # for k, v in dict_pjjg2.items():
        #     print(k, v)


        # 民事
        a3 = Extract_3.Fields_abstract()
        dict_party_info3, dict_ssqq3, dict_ss_ssqq3, dict_top3, extra_dict3 = a3.fields_dict_extract(all_data)
        dict_data3 = p.get_data3(all_data)
        dict_pjjg3 = p.run(dict_data3)
        # for k, v in dict_party_info3.items():
        #     print(k, v)


        # 行政
        a4 = Extract_4.Fields_abstract()
        dict_party_info4, dict_ssqq4, dict_ss_ssqq4, dict_top4, extra_dict4 = a4.fields_dict_extract(all_data)
        dict_data4 = p.get_data4(all_data)
        dict_pjjg4 = p.run(dict_data4)
        # for k, v in dict_pjjg4.items():
        #     print(k, v)

        # 其他
        a5 = Extract_other.Fields_abstract()
        dict_party_info_other, dict_ssqq_other, dict_ss_ssqq_other, dict_top_other, extra_dict_other = a5.fields_dict_extract(all_data)
        dict_data_other = p.get_data_other(all_data)
        dict_pjjg_other = p.run(dict_data_other)
        # for k, v in dict_pjjg_other.items():
        #     print(k, v)



        df2 = common_.dict_to_df(dict_party_info2, dict_ssqq2, dict_ss_ssqq2, dict_top2, dict_pjjg2, extra_dict2 )
        df3 = common_.dict_to_df(dict_party_info3, dict_ssqq3, dict_ss_ssqq3, dict_top3, dict_pjjg3, extra_dict3)
        df4 = common_.dict_to_df(dict_party_info4, dict_ssqq4, dict_ss_ssqq4, dict_top4, dict_pjjg4, extra_dict4)
        df_other = common_.dict_to_df(dict_party_info_other, dict_ssqq_other, dict_ss_ssqq_other, dict_top_other, dict_pjjg_other, extra_dict_other)

        df_arr = [df2, df3, df4, df_other]
        print(len(df2), len(df3), len(df4),len(df_other))
        valid_df_arr = [i for i in df_arr if len(i) > 0]
        e2 = time.time()
        print('处理时间：', e2 - t2)
        if valid_df_arr:
            df = pd.concat(valid_df_arr, axis=0)
            t3 = time.time()

            # common_.update(df)
            common_.df_to_sql(df)
            e3 = time.time()
            print('入库时间：', e3 - t3)
        else:
            print('入库时间：0.0000000')



    # 结束时间
    end = time.time() - start
    print(end)
