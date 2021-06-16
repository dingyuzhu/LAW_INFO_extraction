# -*- coding: UTF-8 -*-

import re

'''民事一审通知书判决结果类'''
class MS_YS_TZS():
    def get_PJJG(self,all_data):

        dict_pjjg_result = {}
        dict_res = {}
        for data in all_data:  # a.id, a.pjjg, b.ajlx, b.wslx, b.spcx_id, a.sb, a.ssqq, c.pjjg as orin_pjjg

            if data[5] and data[2] == 3 and data[3] == 5 and data[4] == 30100000000000000:
                v_temp = {'判决结果类型': None, '判决结果': None}
                v_tmp_arr = data[5].split('\n')
                if len(v_tmp_arr) > 1:
                    for i in v_tmp_arr:
                        if re.search('书|告|函',i):
                            v_temp['判决结果类型'] = i.replace(' ','')
                            v_temp['判决结果'] = i.replace(' ','')
                else:
                    v_temp['判决结果类型'] = None
                    v_temp['判决结果'] = None

                dict_pjjg_result[data[0]] = v_temp
                dict_res[data[0]] = [data[2],data[3],data[4],data[6]]

        return dict_pjjg_result,dict_res


    def run(self, all_data):
        result_dict_pjjg,dict_res = self.get_PJJG(all_data)
        return result_dict_pjjg,dict_res



# import time
# if __name__ == "__main__":
#
#     # 程序开始执行时间
#     start = time.time()
#     ms_ys_tzs = MS_YS_TZS()
#     sql = 'select id, pjjg, ajlx, wslx, spcx_id, qw from tb_wenshu_one_month_check where id=531688414941021226'
#     conn = config.db_connection
#     try:
#         conn.ping(reconnect=True)
#     except:
#         print("数据库连接失败")
#     cur = conn.cursor()
#     cur.execute(sql)
#     all_data = cur.fetchall()
#     cur.close()
#     conn.close()
#     result_dict_pjjg=ms_ys_tzs.get_PJJG(all_data)
#     for k, v in result_dict_pjjg.items():
#         print(k)
#         print(v)
#     ms_ys_tzs.run(all_data)
#     # 结束时间
#     end = time.time() - start
#     print(end)
