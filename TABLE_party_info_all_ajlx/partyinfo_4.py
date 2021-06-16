# -*- coding:utf-8 -*-

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import re
import time
import datetime
import pandas as pd
from sqlalchemy import create_engine
import rule_4
import common_

class Party_extract4():

    '''获取party_info'''
    def get_party_info(self,all_data):  #id,party_info,ajlx
        dict_party_info = {}
        for data in all_data:  # id,party_info,ajlx
            if data[1] and data[2] == 4:
                dict_party_info[data[0]] = data[1]

        return dict_party_info

    '''清洗party_info'''
    def clean_party_info(self,dict_party_info):
        dict_clean_party_info = {}
        #剔除没有换行的
        for k,v in dict_party_info.items():
            if v:
                if re.search('不公开', v):  # 33/240000
                    dict_clean_party_info[k] = ''
                else:
                    dict_clean_party_info[k] = v
            else:
                dict_clean_party_info[k] = v
        return dict_clean_party_info

    '''获取头部中的原告'''
    def get_yg_bg_dsr(self,dict_clean_party_info):

        dict_yg_bg_dsr = {}
        for k,v in dict_clean_party_info.items():
            if v:
                v = v.replace('(', '（').replace(')', '）').replace(':', '：').replace(' ', '')

                temp_arr = []
                if '\n' in v:
                    segments = v.split('\n')
                    for seg in segments:
                        if re.search('[事服]{1}务所|法律援助中心|法律服务', seg):
                            seg = seg
                        else:
                            seg = re.sub(
                                '（.*?）|（.*?人）|【.*?】：|（系.*?）|（.*?(告|机关|号)）|(\\[).*?(\\])：|(\\[).*?告(\\])|暨.*?人[：]{0,1}',
                                '：', seg)
                        temp_arr.append(seg)
                    v = '\n'.join(temp_arr)
                elif '。' in v:
                    segments = v.split('。')
                    for seg in segments:
                        if re.search('[事服]{1}务所|法律援助中心|法律服务', seg):
                            seg = seg
                        else:
                            seg = re.sub(
                                '（.*?）|（.*?人）|【.*?】：|（系.*?）|（.*?(告|机关|号)）|(\\[).*?(\\])：|(\\[).*?告(\\])|暨.*?人[：]{0,1}',
                                '：', seg)
                        temp_arr.append(seg)
                    v = '。'.join(temp_arr)

                v = re.sub('一审.*?(、|，).*?人', '被告', v)
                v = re.sub('代理人[0-9a-zA-Z一二三四五六七八九十`][：]{0,1}','代理人：',v)
                v = re.sub('（.*?(指派|委托)）', '', v)

                # 解决通知书的情况
                if re.search('：$', v):

                    v = v.replace('：', '').replace('\n','')
                    v = '原告：' + v


                v_tmp = {'原告信息': '', '被告信息': '', '第三人信息': ''}

                for i in range(len(rule_4.yg_pattern_1)):
                    if re.search(rule_4.yg_pattern_1[i], v) :

                        v_tmp['原告信息'] = re.search(rule_4.yg_pattern_1[i], v).group()
                        break
                if not v_tmp['原告信息']:
                    for i in range(len(rule_4.yg_pattern_2)):
                        if re.search(rule_4.yg_pattern_2[i], v) :
                            v_tmp['原告信息'] = re.search(rule_4.yg_pattern_2[i], v).group()
                            break



                for j in range(len(rule_4.bg_pattern_2)):  #不带第三人
                    if re.search(rule_4.bg_pattern_2[j], v) :
                        v_tmp['被告信息'] = re.search(rule_4.bg_pattern_2[j], v).group()
                        break
                if not v_tmp['被告信息']:
                    for j in range(len(rule_4.bg_pattern_1)):
                        if re.search(rule_4.bg_pattern_1[j], v) :
                            tail = 3
                            v_tmp['被告信息'] = re.search(rule_4.bg_pattern_1[j], v).group()[:-tail]
                            break

                for q in range(len(rule_4.dsr_pattern)):
                    try:
                        v_tmp['第三人信息'] = re.search(rule_4.dsr_pattern[q], v).group()
                    except:
                        v_tmp['第三人信息'] = ''


                dict_yg_bg_dsr[k] = v_tmp

        return dict_yg_bg_dsr

    def one_(self,role_dict):
        role_dict_arr = {}
        for k, v in role_dict.items():
            if v:
                role_arr = v.split('\n')
                role_arr_ = []
                for i in range(len(role_arr)):
                    if len(role_arr[i]) > 0:
                        x = re.split('：|:|,|，|。|/.|;|；', role_arr[i])
                        x = [_ for _ in x if len(_) > 0]
                        if x:
                            role_arr_.append(x)

                role_dict_arr[k] = role_arr_
            else:
                role_dict_arr[k] = ''
        return role_dict_arr

    #清理cognitor有问题的
    def clean_cognitor(self,cognitor):
        new_cognitor = ''
        p = '天津|黑龙江|辽宁|吉林|河北|河南|湖北|湖南|山东|山西|陕西|安徽|浙江|江苏|福建|广东|海南|四川|云南|贵州|青海|甘肃|江西|台湾省|上海|北京|重庆|新疆|香港|澳门|内蒙古|宁夏|西藏'
        if re.search('[事服]{1}务所|法律援助中心|法律服务|该|系', cognitor):
            if not re.search('^({})'.format(p), cognitor):
                if re.search('({})'.format(p), cognitor):
                    x_ = re.split('({})'.format(p), cognitor)[0]
                    new_cognitor = x_
            else:
                new_cognitor = '空'
        elif re.search('代理人.+', cognitor):
            x_ = re.search('代理人.+',cognitor).group()[3:]
            new_cognitor = x_
        else:
            new_cognitor = cognitor

        if re.search('[\u4e00-\u9fa5]', new_cognitor):
            if '、' in new_cognitor:
                if len(new_cognitor.split('、')) > 2:
                    new_cognitor = re.search('[\u4e00-\u9fa5]+', new_cognitor).group()
                # 内部清洗  乌兰、-聂爱珍----->乌兰、聂爱珍
                else:
                    temp_arr = new_cognitor.split('、')
                    temp_s = []
                    # 解决： 2、聂爱珍---> 聂爱珍
                    for i in temp_arr:
                        if re.search('[\u4e00-\u9fa5]+', i):
                            temp_s.append(re.search('[\u4e00-\u9fa5]+', i).group())
                    if len(temp_s) == 2:
                        new_cognitor = '、'.join(temp_s)
                    elif len(temp_s) == 1:
                        new_cognitor = temp_s[0]
                    else:
                        new_cognitor = '空'
            else:
                new_cognitor = re.search('[\u4e00-\u9fa5]+', new_cognitor).group()
        else:
            new_cognitor = '空'

        if len(new_cognitor) == 1:
            if new_cognitor == '年':
                new_cognitor = '空'

        return new_cognitor

    #清理name有问题的
    def clean_name(self,name):
        # 解决出现特殊符号的：张万民（曾用名、宁海县自然资源和规划局（统一社会信用代码、（一审原告××谢信光^（一审原告××谢信光
        name = name.replace('(', '（').replace(')', '）')
        new_name = name
        if re.search('（', name) and not re.search('）', name):
            if re.search('^（', name):
                new_name = name[1:]
            else:
                new_name = re.search('^.*?（', name).group()[0:-1]
        elif re.search('）', name) and not re.search('（', name):

            # 括号出现在句子首部：）杭州市萧山区浦阳镇人民政府
            if name.index('）') == 0:
                new_name = name[1:]
            # 括号出现在句子中间：暨复议机关）浙江省人民政府
            elif name.index('）')>0 and name.index('）')<len(name)-1:
                index_ = name.index('）')
                new_name = name[index_+1:]
            # 括号出现在句子尾部：广州市番禺区环境保护局已整合划入广州市生态环境局）~广州佳旺餐具消毒有限公司
            elif re.search('）$', name):
                new_name = name[0:-1]
        else:
            new_name = name

        if re.search('[\u4e00-\u9fa5]', new_name):
            if '、' in new_name:
                if len(new_name.split('、')) > 2:
                    new_cognitor = re.search('[\u4e00-\u9fa5]+', new_name).group()
                # 内部清洗  乌兰、-聂爱珍----->乌兰、聂爱珍
                else:
                    temp_arr = new_name.split('、')
                    temp_s = []
                    # 解决： 2、聂爱珍---> 聂爱珍
                    for i in temp_arr:
                        if re.search('[\u4e00-\u9fa5]+', i):
                            temp_s.append(re.search('[\u4e00-\u9fa5]+', i).group())
                    if len(temp_s) == 2:
                        new_name = '、'.join(temp_s)
                    elif len(temp_s) == 1:
                        new_name = temp_s[0]
                    else:
                        new_name = '空'
            else:
                new_name = re.search('[\u4e00-\u9fa5]+', new_name).group()
        else:
            new_name = '空'

        return new_name

    # 清理律所
    def clean_lawyer_address(self, address):
        p = '天津|黑龙江|辽宁|吉林|河北|河南|湖北|湖南|山东|山西|陕西|安徽|浙江|江苏|福建|广东|海南|四川|云南|贵州|青海|甘肃|江西|台湾省|上海|北京|重庆|新疆|香港|澳门|内蒙古|宁夏|西藏'
        # 清理xx符号
        if re.search('X', address):
            address = re.sub('X', '', address)

        # 处理是|为|均系|均为|均是|分别(是|系|为)
        elif re.search('^(是|为|均系|均为|均是|分别(是|系|为))', address):
            address = re.sub('^(是|为|均系|均为|均是|分别)', '', address)

        # 处理二人均系|(委托|诉讼|委托诉讼)代理人xxx|丁南鹏(一般代理)贵州xxx律师事务所
        elif re.search('^[二三四五六七八九十]人(系|均系|均是|均为)', address):
            address = re.sub('^[二三四五六七八九十]人(系|均系|均是|均为)', '', address)
        elif re.search('(委托|诉讼|委托诉讼)代理人', address):
            if re.search(p, address):
                address = re.sub('^(委托|诉讼|委托诉讼)代理人.*?(?={})'.format(p), '', address)
            else:
                if re.search('(委托|诉讼|委托诉讼)代理人系', address):
                    address = re.sub('(委托|诉讼|委托诉讼)代理人系', '', address)
                else:
                    address = re.sub('(委托|诉讼|委托诉讼)代理人.{3}', '', address)
        elif re.search(p, address) and not re.search('^({})'.format(p), address):
            address = re.sub('^.*?(?={})'.format(p), '', address)

        # 解决指派:郑州市法律援助中心指派河南舒展律师事务所律师
        elif re.search('指派.*?律师事务所', address):
            arr = re.split('指派', address)
            address = arr[-1]
        return address

    def two_(self,role_dict_arr, role_title_arr):
        detailed_dict = {}
        for k, v in role_dict_arr.items():
            name_arr = []
            address_arr = []
            lawyer_arr = []
            lawyer_address_arr = []
            representive_arr=[]
            if v:
                # print(k)
                # print(v)
                for i in range(len(v)):
                    if v[i][0] in role_title_arr:
                        if len(v[i]) > 1:
                            x_ = self.clean_name(v[i][1])
                            name_arr.append(x_)
                            address_arr.append('空')

                        elif len(v[i])<2 and len(v)>2:
                            x_ = self.clean_name(v[i+1][0])
                            name_arr.append(x_)
                            address_arr.append('空')

                        if len(v[i])>2:
                            for r in v[i][2:]:
                                if re.search('住', r) and len(r)>3:
                                    address_arr[-1] = r
                                    break
                                else:
                                    if re.search('省|市|区|县|路|道', r) and not re.search('[事服]{1}务所|法律援助中心|法律服务', r):
                                        address_arr[-1] = r
                                        break
                        elif len(v[i])<2 and len(v)>2:

                            for r in v[i+1][1:]:
                                if re.search('住', r) and len(r) > 3:
                                    address_arr[-1] = r
                                    break
                                else:
                                    if re.search('省|市|区|县|路|道', r) and not re.search('[事服]{1}务所|法律援助中心|法律服务', r):
                                        address_arr[-1] = r
                                        break

                    else:
                        for title in role_title_arr:
                            p = '^{}'.format(title)
                            if re.search(p, v[i][0]) and re.search('代理人|代表人',v[i][0]) == None:
                                x_ = self.clean_name(v[i][0][len(title):])
                                name_arr.append(x_)
                                address_arr.append('空')
                                if len(v[i]) >2 :
                                    for r in v[i]:
                                        if re.search('住', r) and len(r) > 3:
                                            address_arr[-1] = r
                                            break
                                        else:
                                            if re.search('省|市|区|县|路|道', r) and not re.search('[事服]{1}务所|法律援助中心|法律服务', r):
                                                address_arr[-1] = r
                                                break
                            elif re.search(title, v[i][0]) and v[i][0][-len(title):]==title and len(v[i])>1:
                                x_ = self.clean_name(v[i][1])
                                name_arr.append(x_)
                                address_arr.append('空')
                                if len(v[i]) >2:
                                    for r in v[i]:
                                        if re.search('住', r) and len(r) > 3:
                                            address_arr[-1] = r
                                            break
                                        else:
                                            if re.search('省|市|区|县|路|道', r) and not re.search('[事服]{1}务所|法律援助中心|法律服务', r):
                                                address_arr[-1] = r
                                                break

                    if re.search('诉讼代理人|委托代理人',v[i][0]):
                        lawyer_address_arr.append('空')
                        if v[i][0][-3:]=='代理人' and len(v[i])>1:
                            tmp = v[i][1]
                            if re.search('（|/\(',tmp):
                                tmp = re.sub('（.*?）|/\(.*?/\)|（.*','',tmp)
                            if re.search('、.*?[事服]{1}务所|法律援助中心|法律服务|该',tmp):
                                tmp = re.split('、', tmp)[0]

                        else:
                            tmp = re.search('代理人.*',v[i][0]).group()[3:]
                            if re.search('（|/\(',tmp):
                                tmp = re.sub('（.*?）|/\(.*?/\)|（.*','',tmp)
                                if len(tmp)>0:
                                    tmp = tmp

                        tmp = self.clean_cognitor(tmp)

                        lawyer_arr.append(tmp)

                        for x in v[i]:
                            if re.search('[事服]{1}务所|法律援助中心|法律服务|该', x):
                                if not re.search('（实习.*?）', x):
                                    if re.search('、', x):
                                        if not re.search('律师、实习律师', x):
                                            x_split_1 = re.split('、', x)[0]
                                            x_split_2 = re.split('、', x)[1]
                                            if not re.search('[事服]{1}务所|法律援助中心|法律服务|该', x_split_1):
                                                lawyer_address_arr[-1] = self.clean_lawyer_address(x_split_2)
                                                break
                                            else:
                                                lawyer_address_arr[-1] = self.clean_lawyer_address(x_split_1)
                                                break
                                        else:
                                            lawyer_address_arr[-1] = self.clean_lawyer_address(x)
                                            break
                                    else:
                                        lawyer_address_arr[-1] = self.clean_lawyer_address(x)
                                        break
                                else:
                                    tmp_x = re.split('（实习.*?）',x)
                                    lawyer_address_arr[-1] = self.clean_lawyer_address(tmp_x[1])

                    if re.search('法定代理人', v[i][0]):
                        if v[i][0][-3:]=='代理人' and len(v[i])>1:
                            representive_arr.append(v[i][1])
                        else:
                            tmp = re.search('代理人.*', v[i][0]).group()[3:]
                            representive_arr.append(tmp)

            detailed_dict[k] = [name_arr, address_arr, lawyer_arr, lawyer_address_arr, representive_arr]
        return detailed_dict


    #根据截距缩短数组
    def shorten_arr(self,old_arr, idx, intercept_):
        begin_idx = idx - intercept_ + 1
        new_arr = [old_arr[i] for i in range(0, begin_idx)]
        tmp_txt = ''.join(old_arr[begin_idx:idx+1])
        new_arr.append(tmp_txt)

        for i in range(idx + 1, len(old_arr)):
            new_arr.append(old_arr[i])

        return new_arr


    # 相同key值的字典合并
    def merge_(self,dict_arr):
        '''

        :param dict_arr: [{531474287685534398: [['清远市贝克新材料有限公司'], ['住所地广东省清远市清城区****************#厂房'], ['钟玉婷'], ['北京德和衡（广州）律师事务所律师'], []]}, {531474287685534398: [['董青'], ['住江苏省常州市金坛区**************'], ['钟玉婷'], ['北京德和衡（广州）律师事务所律师'], []]}, {531474287685534398: [['李秋霞'], ['住江苏省常州市金坛区**************'], ['钟玉婷'], ['北京德和衡（广州）律师事务所律师'], []]}, {531474287685534398: [['董春荣'], ['住江苏省常州市金坛区**************'], ['钟玉婷'], ['北京德和衡（广州）律师事务所律师'], []]}, {531474287685534398: [['郭祥'], ['住湖南省新宁县**********'], [], [], []]}]

                        [{531475900600943064: [['肇庆市高要区金利祥力五金制品厂', '唐某1', '唐锐强', '区素琴', '陈**'], ['住所地广东省肇庆市高要区金利镇西围江边煤地红珠岗侧', '住广东省高要市************队548号', '住广东省高要市************队280号', '住广东省高要市************队548号', '住广东省高要市************队280号'], ['朱祥宝', '梁楚雯'], ['广东天舜律师事务所律师', '广东天舜律师事务所律师'], []]}]

                        [{531627123845105247: [['林家鹏'], ['福建省大田县人'], [], [], []]}, {531627123845105247: [['紫金财产保险股份有限公司云南分公司'], ['空'], ['李东'], ['该公司员工'], []]}]


        :return: new_dict_arr: [{531474287685534398: ['清远市贝克新材料有限公司~董青~李秋霞~董春荣~郭祥', '住所地广东省清远市清城区****************#厂房~住江苏省常州市金坛区**************~住江苏省常州市金坛区**************~住江苏省常州市金坛区**************~住湖南省新宁县**********', '钟玉婷~钟玉婷~钟玉婷~钟玉婷~空', '北京德和衡（广州）律师事务所律师~北京德和衡（广州）律师事务所律师~北京德和衡（广州）律师事务所律师~北京德和衡（广州）律师事务所律师~空', '空~空~空~空~空']}]

                                [{531475900600943064: ['肇庆市高要区金利祥力五金制品厂^唐某1^唐锐强^区素琴^陈**', '住所地广东省肇庆市高要区金利镇西围江边煤地红珠岗侧^住广东省高要市************队548号^住广东省高要市************队280号^住广东省高要市************队548号^住广东省高要市************队280号', '朱祥宝^梁楚雯', '广东天舜律师事务所律师^广东天舜律师事务所律师', '空']}]

                                [{531627123845105247: ['林家鹏~紫金财产保险股份有限公司云南分公司', '福建省大田县人~空', '空~李东', '空~该公司员工', '空~空']}]

        '''
        new_dict_arr = []
        for dict_ in dict_arr:
            for k, v in dict_.items():
                for x in range(len(v)):
                    if len(v[x]) == 0:
                        v[x] = ['空']
                    v[x] = '^'.join(v[x])
                dict_[k] = v
            new_dict_arr.append(dict_)



        if len(new_dict_arr)>1:
            s0,s1,s2,s3,s4 = '','','','',''
            k__ = list(new_dict_arr[0].keys())[0]
            dict__ = {}
            for dict_ in new_dict_arr:
                for k, v in dict_.items():
                    s0 += (dict_[k][0]+'~')
                    s1 += (dict_[k][1]+'~')
                    s2 += (dict_[k][2] + '~')
                    s3 += (dict_[k][3] + '~')
                    s4 += (dict_[k][4] + '~')
            dict__[k__] = [s0[:-1],s1[:-1],s2[:-1],s3[:-1],s4[:-1]]
            new_dict_arr = [dict__]


        return new_dict_arr




    #将原被告与诉讼代理人、法定代理人对应
    def correspond(self,role_dict_arr, role_title):

        role_title_ = ['\n'+i for i in role_title]

        p = '|'.join(role_title_)

        role_merged_dict_arr = []
        for i in range(len(role_dict_arr)):
            k = list(role_dict_arr[i][0].keys())[0]
            v = list(role_dict_arr[i][0].values())[0]
            if re.search(p, v):
                title = re.search(p, v).group()
                tmp_arr = re.split(p, v)
                tmp_arr_ = [tmp_arr[0]]
                for i in range(1, len(tmp_arr)):
                    tmp_arr_.append(title+tmp_arr[i])
            else:
                tmp_arr_ = [v]



            def get_id_intercept(tmp_arr_):
                idx_arr = []  # 索引
                intercept_arr = []  # 截距

                for i in range(len(tmp_arr_)):
                    if re.search('\n(以上|上列|上述|众).*?代理人|\n.*?共同.*?代理人|\n[一二两三四五六七八九零十百千]+.*?代理人', tmp_arr_[i]):
                        s = re.search('\n(以上|上列|上述|众).*?代理人|\n.*?共同.*?代理人|\n[一二两三四五六七八九零十百千]+.*?代理人', tmp_arr_[i]).group()
                        pattern = re.compile(u'[一二两三四五六七八九零十]+')

                        # 如果带数字
                        if re.search(pattern, s):
                            num_ch = re.findall(pattern, s)[-1]
                            num = common_.t(num_ch)
                            idx_arr.append(i)
                            intercept_arr.append(num)

                        #不带数字:默认全连
                        else:
                            idx_arr.append(i)
                            intercept_arr.append(i+1)

                return idx_arr, intercept_arr

            idx_arr = get_id_intercept(tmp_arr_)[0]
            intercept_arr =get_id_intercept(tmp_arr_)[1]

            #融合tmp_arr_变成新的new_tmp_arr_
            new_tmp_arr_ = tmp_arr_
            if idx_arr and intercept_arr:
                new_tmp_arr_ = self.shorten_arr(tmp_arr_, idx_arr[0], intercept_arr[0])




            new_tmp_arr_process = []
            for j in range(len(new_tmp_arr_)):
                tmp_dict = {}
                tmp_dict[k] = new_tmp_arr_[j]
                role_dict_arr_ = self.one_(tmp_dict)
                detailed_dict_ = self.two_(role_dict_arr_, role_title)

                new_tmp_arr_process.append(detailed_dict_)

            # 打印这个new_tmp_arr_process可以看见没有合并之前的一对一关系

            #将id相同的进行内部外部的分割以及合并
            merged_dict_arr = self.merge_(new_tmp_arr_process)
            role_merged_dict_arr.append(merged_dict_arr)

        return role_merged_dict_arr


    def  move_duplicate(self,txt):
        new_txt = txt
        if '~' in txt:
            txt_Arr = txt.split('~')
            if len(set(txt_Arr)) == 1:
                new_txt = txt_Arr[0]
        return new_txt



    # 原被告、第三人组合成字典
    def combine_(self,yg_merged_dict_arr,bg_merged_dict_arr,dsr_merged_dict_arr):

        detailed_dict = {}
        for i in range(len(yg_merged_dict_arr)):
            v_temp = {'原告信息':'','被告信息':'','第三人信息':''}
            k = list(yg_merged_dict_arr[i][0].keys())[0]
            v_temp['原告信息'] = list(yg_merged_dict_arr[i][0].values())[0]
            v_temp['被告信息'] = list(bg_merged_dict_arr[i][0].values())[0]
            v_temp['第三人信息'] = list(dsr_merged_dict_arr[i][0].values())[0]
            detailed_dict[k] = v_temp



        v_temp = {'id': [], 'wenshu_id': [],
                   'yg_name': [], 'yg_address': [], 'yg_cognitor': [], 'yg_cognitor_address': [], 'yg_representive': [],
                   'bg_name': [], 'bg_address': [], 'bg_cognitor': [], 'bg_cognitor_address': [], 'bg_representive': [],
                   '_3rd_name': [], '_3rd_address': [], '_3rd_cognitor': [], '_3rd_cognitor_address': [],
                   '_3rd_representive': []
                   }


        for k, v in detailed_dict.items():
            v_temp['id'].append(k)
            v_temp['wenshu_id'].append(k)
            v_temp['yg_name'].append(v['原告信息'][0])
            v_temp['yg_address'].append(v['原告信息'][1])
            # v['原告信息'][2] = move_duplicate(v['原告信息'][2])
            v_temp['yg_cognitor'].append(v['原告信息'][2])
            # v['原告信息'][3] = move_duplicate(v['原告信息'][3])
            v_temp['yg_cognitor_address'].append(v['原告信息'][3])
            v_temp['yg_representive'].append(v['原告信息'][4])

            v_temp['bg_name'].append(v['被告信息'][0])
            v_temp['bg_address'].append(v['被告信息'][1])
            # v['被告信息'][2] = move_duplicate(v['被告信息'][2])
            v_temp['bg_cognitor'].append(v['被告信息'][2])
            # v['被告信息'][3] = move_duplicate(v['被告信息'][3])
            v_temp['bg_cognitor_address'].append(v['被告信息'][3])
            v_temp['bg_representive'].append(v['被告信息'][4])

            v_temp['_3rd_name'].append(v['第三人信息'][0])
            v_temp['_3rd_address'].append(v['第三人信息'][1])
            # v['第三人信息'][2] = move_duplicate(v['第三人信息'][2])
            v_temp['_3rd_cognitor'].append(v['第三人信息'][2])
            # v['第三人信息'][3] = move_duplicate(v['第三人信息'][3])
            v_temp['_3rd_cognitor_address'].append(v['第三人信息'][3])
            v_temp['_3rd_representive'].append(v['第三人信息'][4])

        df_ = pd.DataFrame(v_temp)

        return df_, detailed_dict




    def run(self,dict_party_info):

        dict_clean_party_info = self.clean_party_info(dict_party_info)
        # for k,v in dict_clean_party_info.items():
        #     print(k)
        #     print(v)

        dict_yg_bg_dsr = self.get_yg_bg_dsr(dict_clean_party_info)

        # for k,v in dict_yg_bg_dsr.items():
        #     print(k)
        #     print(v)

        dict_yg = {}
        dict_bg = {}
        dict_dsr = {}
        for k, v in dict_yg_bg_dsr.items():
            dict_yg[k] = dict_yg_bg_dsr[k]['原告信息']
            dict_bg[k] = dict_yg_bg_dsr[k]['被告信息']
            dict_dsr[k] = dict_yg_bg_dsr[k]['第三人信息']

        dict_yg_arr = []
        dict_bg_arr = []
        dict_dsr_arr = []
        for k, v in dict_yg.items():
            inn_dict = {}
            inn_dict[k] = v
            dict_yg_arr.append([inn_dict])

        for k, v in dict_bg.items():
            inn_dict = {}
            inn_dict[k] = v
            dict_bg_arr.append([inn_dict])

        for k, v in dict_dsr.items():
            inn_dict = {}
            inn_dict[k] = v
            dict_dsr_arr.append([inn_dict])

        bg_merged_dict_arr = self.correspond(dict_bg_arr, rule_4.bg_title)
        yg_merged_dict_arr = self.correspond(dict_yg_arr, rule_4.yg_title)
        dsr_merged_dict_arr = self.correspond(dict_dsr_arr, rule_4.dsr_title)

        df_ = self.combine_(yg_merged_dict_arr, bg_merged_dict_arr, dsr_merged_dict_arr)[0]
        detailed_dict = self.combine_(yg_merged_dict_arr, bg_merged_dict_arr, dsr_merged_dict_arr)[1]

        return df_, detailed_dict

