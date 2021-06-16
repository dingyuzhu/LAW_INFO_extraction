# -*- coding: UTF-8 -*-

import common_
import config
import judge_extraction

if __name__ == "__main__":
    days = common_.day_range('2019/07/01', '2019/07/31', 1)
    for i in range(len(days)):
        sql =config.Input_sql["sql1"].format(str(days[i])[:10])

        # 单测
        sql1 = 'select a.id,a.qw,a.wb from tb_wenshu_201907 a left join tb_wenshu_201907_check b on a.id = b.wenshu_id where id = 562362648058922579'

        all_data = common_.db_connection(common_.db_connection_test, sql)
        print('sql excute ok')
        dict_judge_extact = judge_extraction.run(all_data)
        # for k, v in dict_judge_extact.items():
        #     print(k, v)