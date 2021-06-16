# -*- coding: UTF-8 -*-
# author：dingyuzhu
# date: 2021-04-01

import re
import datetime
import pymysql
import pandas as pd
from MS_ES import ms_es_cds



'''民事再审裁定书判决结果类'''
class MS_ZS_CDS():
    def get_PJJG(self, all_data):
        dict_pjjg = {}
        for data in all_data:  # a.id, c.ajmc, a.pjjg, b.wslx, c.pjjg as orin_pjjg
            if data[3] == 2:
                if data[4]:
                    dict_pjjg[data[0]] = data[4]
                else:
                    dict_pjjg[data[0]] = data[2]

        return dict_pjjg


    '''对文书的判决结果进行分类'''
    def PJJG_classfication(self, dict_pjjg):
        result_dict_pjjg = {}


        for k, v in dict_pjjg.items():
            v_temp = {'判决结果类型': None, '判决结果': None}


            # 提审

            if re.search('提审', v):
                if re.search('本案由.*?提审', v):
                    v_temp['判决结果类型'] = '提审'
                    v_temp['判决结果'] = '同意再审申请'
                elif re.search('终结', v):
                    v_temp['判决结果类型'] = '提审'
                    v_temp['判决结果'] = '终结再审申请'
                elif re.search('驳回', v):
                    v_temp['判决结果类型'] = '提审'
                    v_temp['判决结果'] = '驳回再审申请'
                else:
                    # v_temp['判决结果类型'] = '提审'
                    # v_temp['判决结果'] = '提审-其他'
                    a = ms_es_cds.MS_ES_CDS()
                    v_temp = a.PJJG_classfication_(v)

            # 再审
            elif re.search('再审', v):

                # 同意再审申请
                s1 = "本案由本院.*?再审|" \
                     "指令.*?再审|" \
                     "本案由.*?院再审|" \
                     "同意.*?的再审申请|" \
                     "本案.*?由本案再审|" \
                     "另行组成合议庭.*?再审"

                # 驳回再审申请
                s2 = '驳回.*?再审[\n]{0,1}(申请|请求)|再审.*?(不予受理|不予支持)|不予受理.*?再审申请|不予再审|驳.*?再审申请'

                # 撤回再审申请
                s3 = '撤回.*?再审申请'

                # 终结再审申请
                s4 = '终结.*?再审'

                if re.search(s1, v):
                    v_temp['判决结果类型'] = '再审'
                    v_temp['判决结果'] = '同意再审申请'

                elif re.search(s2, v):
                    v_temp['判决结果类型'] = '再审'
                    v_temp['判决结果'] = '驳回再审申请'

                elif re.search(s3, v):
                    v_temp['判决结果类型'] = '再审'
                    v_temp['判决结果'] = '撤回再审申请'

                elif re.search(s4, v):
                    v_temp['判决结果类型'] = '再审'
                    v_temp['判决结果'] = '终结再审申请'

                # 其他再审类型
                else:
                    a = ms_es_cds.MS_ES_CDS()
                    v_temp = a.PJJG_classfication_(v)
                    # v_temp['判决结果类型'] = '再审'
                    # v_temp['判决结果'] = '再审-其他'


            # 申诉
            elif re.search('申诉', v):
                # 驳回
                if re.search('驳回|申诉不符合', v):
                    v_temp['判决结果类型'] = '申诉'
                    v_temp['判决结果'] = '驳回再审申请'

                # 撤回
                elif re.search('准许.*?(撤回|撤诉)', v):
                    v_temp['判决结果类型'] = '申诉'
                    v_temp['判决结果'] = '撤回再审申请'

                # 终结
                elif re.search('终结', v):
                    v_temp['判决结果类型'] = '申诉'
                    v_temp['判决结果'] = '终结再审申请'

                # 同意
                elif re.search('同意', v):
                    v_temp['判决结果类型'] = '申诉'
                    v_temp['判决结果'] = '同意再审申请'
                else:
                    a = ms_es_cds.MS_ES_CDS()
                    v_temp = a.PJJG_classfication_(v)
                    # v_temp['判决结果类型'] = '申诉'
                    # v_temp['判决结果'] = '申诉-其他'


            # 其他（既不是再审，也不是提审，也不是申诉）
            elif v:
                a = ms_es_cds.MS_ES_CDS()
                v_temp = a.PJJG_classfication_(v)


            result_dict_pjjg[k] = v_temp
        return result_dict_pjjg

    def run(self, all_data):
        dict_pjjg = self.get_PJJG(all_data)
        result_dict_pjjg = self.PJJG_classfication(dict_pjjg)
        return result_dict_pjjg










# if __name__ == "__main__":
#
#     # big_arr_ts_res_id = []
#     # big_arr_ts_res_pjjg = []
#     # big_dict_ts_res = {'id':'', 'pjjg':''}
#     #
#     # big_arr_zs_res_id = []
#     # big_arr_zs_res_pjjg = []
#     # big_dict_zs_res = {'id':'', 'pjjg':''}
#     #
#     # big_arr_res_id = []
#     # big_arr_res_pjjg = []
#     # big_dict_res = {'id':'', 'pjjg':''}
#
#     days = day_range('2000/08/04', '2020/02/01')
#
#     for i in range(len(days)):
#         # 民事再审裁定书
#         sql = 'SELECT a.id, a.ajmc, a.pjjg  ' \
#               'FROM tb_wenshu_201907 a left join 201907_01_tb_wenshu_check b on a.id=b.wenshu_id ' \
#               'where  b.ajlx=3 and b.wslx = 2 and b.spcx_id=30300000000000000 and a.pjjg is not null ' \
#               'and a.cprq="{}"'.format(str(days[i]))
#
#         sql_ = 'SELECT id, ajmc, pjjg  ' \
#                'FROM tb_wenshu ' \
#                'where  ajlx=3 and wslx = 2 and spcx_id=30300000000000000 and pjjg is not null ' \
#                'and cprq="{}"'.format(str(days[i]))
#         # 单测
#         sql1 = 'SELECT a.id, a.wslx, a.pjjg  ' \
#               'FROM tb_wenshu a ' \
#               'where a.spcx_id=30300000000000000 and a.ajlx=3 and a.wslx = 2 and a.pjjg is not null ' \
#               'and a.id=12345678910'
#
#         conn_extract = db_connection_prod
#         try:
#             conn_extract.ping(reconnect=True)
#         except:
#             print("数据库连接失败")
#
#         cur_extract = conn_extract.cursor()
#         cur_extract.execute(sql_)
#         all_data = cur_extract.fetchall()
#         cur_extract.close()
#         conn_extract.close()
#
#         # 打印日期
#         print('today is :', str(days[i]))
#
#
#         a = MS_ZS_CDS()
#         dict_pjjg = a.get_PJJG(all_data)
#         result_dict_pjjg = a.PJJG_classfication(dict_pjjg)
#
#         # for k, v in result_dict_pjjg.items():
#         #     print(k, v)
#
#         df = dict_to_df(result_dict_pjjg)
#         df_to_sql(df)
#         print('OK')



    #     big_arr_ts_res_id  += dict_ts_res['id']
    #     big_arr_ts_res_pjjg += dict_ts_res['pjjg']
    #
    #     big_arr_zs_res_id += dict_zs_res['id']
    #     big_arr_zs_res_pjjg += dict_zs_res['pjjg']
    #
    #     big_arr_res_id += dict_res['id']
    #     big_arr_res_pjjg += dict_res['pjjg']
    #
    # big_dict_ts_res['id'] = big_arr_ts_res_id
    # big_dict_ts_res['pjjg'] = big_arr_ts_res_pjjg
    #
    # big_dict_zs_res['id'] = big_arr_zs_res_id
    # big_dict_zs_res['pjjg'] = big_arr_zs_res_pjjg
    #
    # big_dict_res['id'] = big_arr_res_id
    # big_dict_res['pjjg'] = big_arr_res_pjjg
    #
    # df1 = pd.DataFrame(big_dict_ts_res)
    # df1.to_csv('其余未知pjjg_result的提审.csv', encoding='utf-8',index=False)
    #
    # df2 = pd.DataFrame(big_dict_zs_res)
    # df2.to_csv('其余未知pjjg_result的再审.csv', encoding='utf-8', index=False)
    #
    # df3 = pd.DataFrame(big_dict_res)
    # df3.to_csv('既不是提审也不是再审.csv', encoding='utf-8', index=False)
