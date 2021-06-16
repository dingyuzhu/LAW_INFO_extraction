# -*- coding: UTF-8 -*-
import re

'''获取数据'''
def get_data(all_data): # a.id, a.qw, a.wb
    dict_data = {}
    for data in all_data:
        if not data[2] and data[1]:
            dict_data[data[0]] = [data[1],"qw"]
        elif data[2]:
            dict_data[data[0]] = [data[2],"wb"]

    return dict_data


'''法官数据抽取'''
def judge_extact(dict_data):
    dict_judge_info = {}

    def wb_extract(wb):
        v_temp = {"审判长": [], "审判员": []}
        if re.search('\n', wb):
            wb_arr = [i for i in re.split('\n', wb) if i]
            for i in range(len(wb_arr)):
                if re.search('审判长', wb_arr[i]):
                    v_temp['审判长'].append(wb_arr[i][3:])
                elif re.search('审判员', wb_arr[i]):
                    v_temp['审判员'].append(wb_arr[i][3:])
                else:
                    v_temp = v_temp
        else:
            if not re.search('审判长|审判员',wb):
                v_temp = v_temp
            else:
                print(k, '没有换行但却有审判长,审判员')
        return v_temp

    for k,v in dict_data.items():

        # 如果是wb
        if v[1] == "wb":
            wb = v[0].replace(' ', '').replace(' ', '').replace('　', '')
            v_temp = wb_extract(wb)

        # 如果是qw
        elif v[1] == "qw":
            qw = v[0].replace(' ', '').replace(' ', '').replace('　', '')
            if re.search('\n(审判长|审判员)[\S\s]+?书记员',qw):
                self_wb = re.search('\n(审判长|审判员)[\S\s]+?书记员',qw).group()
                v_temp = wb_extract(self_wb)
            else:
                print(k, qw)

        # 否则
        else:
            v_temp = {"审判长": [], "审判员": []}

        dict_judge_info[k] = v_temp

    return dict_judge_info


def run(all_data):
    dict_data = get_data(all_data)
    dict_judge_info = judge_extact(dict_data)
    return dict_judge_info


