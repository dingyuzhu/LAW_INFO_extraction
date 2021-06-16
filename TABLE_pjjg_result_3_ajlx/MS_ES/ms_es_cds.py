# -*- coding: UTF-8 -*-
import re
import pymysql
from MS_YS import ms_ys_cds


db_connection = pymysql.connect(host="120.78.92.6", user="root", passwd="dfkj2020", use_unicode=True,
                               db="db_extract_increment0",
                               port=3306, charset="utf8")

'''民事二审裁定书判决结果类'''
class MS_ES_CDS():
    def get_PJJG(self, all_data):
        dict_pjjg = {}
        dict_res = {}
        for data in all_data: # a.id, a.pjjg, b.ajlx, b.wslx, b.spcx_id, a.sb, a.ssqq, c.pjjg as orin_pjjg

            if data[2] == 3 and data[3] == 2 and data[4] == 30200000000000000:
                #如果原判决不为空
                if data[7]:
                    dict_pjjg[data[0]] = data[7]
                # 如果原判决为空
                else:
                    dict_pjjg[data[0]] = data[1]
                dict_res[data[0]] = [data[2],data[3],data[4],data[6]]
        return dict_pjjg, dict_res


    '''民事二审裁定书裁定结果分类'''
    def PJJG_classfication_(self, txt):
        v_temp = {'判决结果类型': None, '判决结果': None}

        # 驳回上诉，维持原判开头的
        if re.search('^驳回.*?维持', txt) != None:
            v_temp['判决结果类型'] = '一审裁定认定事实清楚，适用法律正确的'
            v_temp['判决结果'] = '裁定驳回上诉，维持原裁定'

        # 同时包含撤销、发回...重审, 或者只包含发回重审
        elif re.search('撤销',txt) and re.search('发回.*?(重审|重新审)',txt) or re.search('发回.*?(重审|重新审)',txt):
            v_temp['判决结果类型'] = '一审判决认定基本事实不清的'
            v_temp['判决结果'] = '裁定撤销原判决，发回原审人民法院重审'

        # 同时包含撤销、改判
        elif re.search('撤销',txt) and re.search('改判',txt):
            v_temp['判决结果类型'] = '一审判决认定基本事实不清的'
            v_temp['判决结果'] = '裁定撤销原判决，查清事实后改判'

        # 包含撤销、变更、依法改判但不包含维持
        elif re.search('撤销|变更|改判',txt) and not re.search('维持|变更为“',txt):
            v_temp['判决结果类型'] = '一审裁定认定事实错误或者适用法律错误的'
            v_temp['判决结果'] = '裁定依法改判、撤销或者变更'

        # 既包含维持又包含撤销、变更、改判
        elif re.search('维持',txt) :
            if re.search('撤销|变更|改判',txt) and not re.search('变更为“',txt):
                v_temp['判决结果类型'] = '一审裁定认定事实错误或者适用法律错误的'
                v_temp['判决结果'] = '裁定部分改判、撤销或者变更'
            # 只包含维持,但不包含撤销、变更、改判
            else:
                v_temp['判决结果类型'] = '一审裁定认定事实清楚，适用法律正确的'
                v_temp['判决结果'] = '裁定驳回上诉，维持原裁定'

        else:
            a = ms_ys_cds.CDS_CLASSFIER()
            v_temp = a.classfication(txt)

        return v_temp

    '''对文书的判决结果进行分类'''
    def PJJG_classfication(self, dict_pjjg):
        result_dict_pjjg = {}
        for k, v in dict_pjjg.items():
            v_temp = self.PJJG_classfication_(v)
            result_dict_pjjg[k] = v_temp
        return result_dict_pjjg


    def run(self, all_data):
        dict_pjjg, dict_res = self.get_PJJG(all_data)
        result_dict_pjjg = self.PJJG_classfication(dict_pjjg)
        return result_dict_pjjg, dict_res

# if __name__=="__main__":
#
#     # 程序开始执行时间
#     start = time.time()
#
#
#     end = time.time()
#     print(end)


