# -*- coding:utf-8 -*-



'''民事二审调解书结果类'''
class MS_ES_TJS():
    def get_PJJG(self,all_data):
        result_dict_pjjg = {}
        dict_res = {}
        v_temp = {'判决结果类型': '达成调解', '判决结果': '达成调解'}
        for data in all_data:  # a.id, a.pjjg, b.ajlx, b.wslx, b.spcx_id, a.sb, a.ssqq, c.pjjg as orin_pjjg
            if data[2] == 3 and data[3] == 3 and data[4]==30200000000000000:
                result_dict_pjjg[data[0]] = v_temp
                dict_res[data[0]] = [data[2], data[3], data[4], data[6]]
        return result_dict_pjjg, dict_res



    def run(self, all_data):
        result_dict_pjjg,dict_res = self.get_PJJG(all_data)
        return result_dict_pjjg,dict_res


