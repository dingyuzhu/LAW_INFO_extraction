# -*- coding: UTF-8 -*-
# author：dingyuzhu
# date: 2021-04-02

import re
import datetime
import pymysql
import pandas as pd
# from ZS_PJJG import common_method



'''民事再审裁定书判决结果类'''
class MS_ZS_TZS():
    def get_PJJG(self, all_data):
        dict_pjjg = {}

        for data in all_data:  # a.id, c.ajmc, a.pjjg, b.wslx , c.pjjg as orin_pjjg
            if data[3] ==5:
                if data[4]:
                    dict_pjjg[data[0]] = data[4] + '\n' + data[1]
                else:
                    dict_pjjg[data[0]] = data[2] + '\n' + data[1]

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
                    v_temp['判决结果'] = '同意提审申请'

                # else:
                #     v_temp['判决结果类型'] = '提审'
                #     v_temp['判决结果'] = '提审-其他'

                    # dict_ts_res['id'].append(k)
                    # dict_ts_res['pjjg'].append(v)
            # 申诉
            elif re.search('申诉', v):
                # 驳回
                s1 = '驳回.{0,3}申诉|' \
                     '申诉.{0,3}应予驳回|' \
                     '申诉.{0,15}不能成立|' \
                     '申诉不符合'
                if re.search(s1, v):
                    v_temp['判决结果类型'] = '申诉'
                    v_temp['判决结果'] = '驳回再审申请'

                # 撤回
                elif re.search('撤回申诉.{0,15}本院予以准许', v):
                    v_temp['判决结果类型'] = '申诉'
                    v_temp['判决结果'] = '撤回再审申请'

                # 终结
                elif re.search('终结|申诉不再审查', v):
                    v_temp['判决结果类型'] = '申诉'
                    v_temp['判决结果'] = '终结再审申请'
                # 没有同意申诉这一说

            # 再审
            elif re.search('再审', v):

                # 同意再审申请
                s1 = "同意.*?的再审申请"
                # 驳回再审申请
                s2 = '驳回|不予采纳|不予支持|不符合|驳.*?再审[\n]{0,1}申请'

                if re.search(s1, v):
                    v_temp['判决结果类型'] = '再审'
                    v_temp['判决结果'] = '同意再审申请'
                elif re.search(s2, v):

                    v_temp['判决结果类型'] = '再审'
                    v_temp['判决结果'] = '驳回再审申请'
                elif re.search('终结审查', v):
                    v_temp['判决结果类型'] = '再审'
                    v_temp['判决结果'] = '终结再审申请'
                #
                # 其他再审类型
                # else:
                #     v_temp['判决结果类型'] = '再审'
                #     v_temp['判决结果'] = '再审-其他'



            # 其他（既不是再审，也不是提审，也不是申诉）
            elif v:

                v_temp['判决结果类型'] = '其他'
                v_temp['判决结果'] = '其他'

                # dict_res['id'].append(k)
                # dict_res['pjjg'].append(v)

            result_dict_pjjg[k] = v_temp
        return result_dict_pjjg


    def run(self, all_data):
        dict_pjjg = self.get_PJJG(all_data)
        result_dict_pjjg = self.PJJG_classfication(dict_pjjg)
        return result_dict_pjjg


# if __name__ == "__main__":

    # big_arr_ts_res_id = []
    # big_arr_ts_res_pjjg = []
    # big_dict_ts_res = {'id':'', 'pjjg':''}
    #
    # big_arr_zs_res_id = []
    # big_arr_zs_res_pjjg = []
    # big_dict_zs_res = {'id':'', 'pjjg':''}
    #
    # big_arr_res_id = []
    # big_arr_res_pjjg = []
    # big_dict_res = {'id': '', 'pjjg':''}

    # days = day_range('1998/01/01', '2019/07/01')
    #
    # for i in range(len(days)):
    #     # 民事再审裁定书
    #     sql = 'SELECT a.id, a.ajmc, a.pjjg  ' \
    #           'FROM tb_wenshu_201907 a left join 201907_01_tb_wenshu_check b on a.id=b.wenshu_id ' \
    #           'where  b.ajlx=3 and b.wslx = 5 and b.spcx_id=30300000000000000  and a.pjjg is not null ' \
    #           'and cprq="{}"'.format(str(days[i]))
    #
    #     sql_ = 'SELECT id, ajmc, pjjg  ' \
    #            'FROM tb_wenshu ' \
    #            'where  ajlx=3 and wslx = 5 and spcx_id=30300000000000000 and pjjg is not null ' \
    #            'and cprq="{}"'.format(str(days[i]))
    #     # 单测
    #     sql1 = 'SELECT id, ajmc, pjjg  ' \
    #            'FROM tb_wenshu_zs ' \
    #            'where  ajlx=3 and wslx = 5 and pjjg is not null ' \
    #            'and id=123456789'.format(str(days[i]))
    #
    #     conn_extract = db_connection_prod
    #     try:
    #         conn_extract.ping(reconnect=True)
    #     except:
    #         print("数据库连接失败")
    #
    #     cur_extract = conn_extract.cursor()
    #     cur_extract.execute(sql_)
    #     all_data = cur_extract.fetchall()
    #     cur_extract.close()
    #     conn_extract.close()
    #
    #     # 打印日期
    #     print('today is :', str(days[i]))
    #
    #
    #     a = MS_ZS_TZS()
    #     dict_pjjg = a.get_PJJG(all_data)
    #     result_dict_pjjg = a.PJJG_classfication(dict_pjjg)
    #     # for k, v in result_dict_pjjg.items():
    #     #     print(k)
    #     #     print(v)
    #
    #
    #     df = dict_to_df(result_dict_pjjg)
    #     df_to_sql(df)
    #
    #     print('OK')




