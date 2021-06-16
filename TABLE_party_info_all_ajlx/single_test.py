#-*- coding: UTF-8 -*-

import config
import common_
import partyinfo_2
import partyinfo_3
import partyinfo_4
import partyinfo_other
import rule_2
import rule_3
import rule_4
import pandas as pd

import time
if __name__ == "__main__":
    # 开始时间
    start = time.time()

    days = common_.day_range('1998/10/01', '1998/10/01',1)
    for i in range(len(days)):

        t1 = time.time()
        with open('update_list.txt',encoding='utf-8') as f:
            lines = f.readlines()
            lines = tuple([int(i.strip()) for i in lines])
        # 更新测试
        sql_update = 'select a.id,a.party_info,b.ajlx ' \
                     'from ' \
                     '{} a left join ' \
                     '{} b on a.id = b.wenshu_id left join ' \
                     '{} c on a.id = c.id ' \
                     'where a.id in {}'.format(config.Input_table["tb_wenshu_paragraph"],config.Input_table["tb_wenshu_check"],config.Input_table["tb_wenshu"],lines)

        # 单测
        sql1 = 'select a.id,a.party_info,b.ajlx ' \
                'from ' \
                '{} a left join ' \
                '{} b on a.id = b.wenshu_id left join ' \
                '{} c on a.id = c.id ' \
                'where a.id=531686903297082211'.format(config.Input_table["tb_wenshu_paragraph"],config.Input_table["tb_wenshu_check"],config.Input_table["tb_wenshu"])


        all_data = common_.db_connection(common_.db_connection_prod, sql1)

        print('今天是：' + str(days[i])[:10] + '是时间轴中的第' + str(i) + '天，还剩下' + str(len(days) - i) + '天')
        e1 = time.time()
        print('SQL执行时间：', e1 - t1)



        t2 = time.time()
        a2 = partyinfo_2.Party_extract2()
        a3 = partyinfo_3.Party_extract3()
        a4 = partyinfo_4.Party_extract4()
        a5 = partyinfo_other.Party_extract_other()
        dict_party_info2 = a2.get_party_info(all_data)
        dict_party_info3 = a3.get_party_info(all_data)
        dict_party_info4 = a4.get_party_info(all_data)
        dict_party_info_other = a5.get_party_info(all_data)

        df2,detailed_dict2 = a2.run(dict_party_info2)
        df3,detailed_dict3 = a3.run(dict_party_info3)
        # for k,v in detailed_dict3.items():
        #     print(k,v)
        df4,detailed_dict4 = a4.run(dict_party_info4)
        df_other,detailed_dict_other = a5.run(dict_party_info_other)
        # print(df2[df2['id'] == 536023366235066163])
        # print(df3[df3['id'] == 536023366235066163])

        e2 = time.time()
        print('数据处理时间：', e2 - t2)


        df_arr = [df2, df3, df4, df_other]
        print(len(df2), len(df3), len(df4), len(df_other))
        valid_df_arr = [i for i in df_arr if len(i) > 0]
        if valid_df_arr:
            df = pd.concat(valid_df_arr, axis=0)

            t3 = time.time()
            common_.update(df)
            # common_.df_to_sql(df)
            e3 = time.time()
            print('入库时间：', e3 - t3)
        else:
            print('入库时间：0.0000000')