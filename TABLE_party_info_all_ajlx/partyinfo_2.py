# -*- coding:utf-8 -*-
import re
import time
import datetime
import pandas as pd
import common_
from sqlalchemy import create_engine
import rule_2



class Party_extract2():
    '''获取party_info'''
    def get_party_info(self,all_data):  #id,party_info,ajlx
        dict_party_info = {}
        # 剔除为table的
        for data in all_data:  # id,party_info,ajlx
            if data[1] and data[2] == 2:
                dict_party_info[data[0]] = data[1]

        return dict_party_info

    '''清洗party_info'''
    def clean_party_info(self,dict_party_info):
        dict_clean_party_info = {}
        for k,v in dict_party_info.items():
            if v:
                if re.search('不公开', v):  # 33/240000
                    dict_clean_party_info[k] = ''
                else:
                    # 将英文括号替换
                    v_tmp = v.replace('(', '（').replace(')', '）')
                    # 将英文冒号、空格替换
                    v_tmp = v_tmp.replace(':', '：').replace(' ','')
                    # 将斜杠替换
                    v_tmp = v_tmp.replace('\\', '')
                    # 将括号中的内容替换为空
                    temp_arr = []
                    if '\n' in v_tmp:
                        segments = v_tmp.split('\n')
                        for seg in segments:
                            if re.search('[事服]{1}务所|法律援助中心|法律服务', seg):
                                seg = seg
                            else:
                                seg = re.sub('（.*?）|（.*?人）|【.*?】：|（系.*?）|（.*?(告|机关|号)）|(\\[).*?(\\])：|(\\[).*?告(\\])|暨.*?人[：]{0,1}','：', seg)
                            temp_arr.append(seg)
                        v_tmp = '\n'.join(temp_arr)
                    elif '。' in v_tmp:
                        segments = v_tmp.split('。')
                        for seg in segments:
                            if re.search('[事服]{1}务所|法律援助中心|法律服务', seg):
                                seg = seg
                            else:
                                seg = re.sub('（.*?）|（.*?人）|【.*?】：|（系.*?）|（.*?(告|机关|号)）|(\\[).*?(\\])：|(\\[).*?告(\\])|暨.*?人[：]{0,1}','：', seg)
                            temp_arr.append(seg)
                        v_tmp = '。'.join(temp_arr)



                    # 解决通知书的情况
                    if re.search('附带民事诉讼原告人|原告人|起诉人', v_tmp):
                        v_tmp = re.sub('附带民事诉讼原告人|原告人|起诉人','\n自诉人',v_tmp)



                    v_tmp = v_tmp.replace('\n被申请人','\n被告人')
                    v_tmp = v_tmp.replace('申请人', '自诉人')

                    # 将原审被告人替换为被告人
                    p1 = '^[\S\s]+?(信息|情况)|辩护人\n无|姓名\n'
                    p2 = '(原审被告人|被告人|一审被告人)'
                    p3 = '原审被告人|一审被告人|被申请人'
                    p4 = '\n辩护人\n辩护人'

                    v_tmp = re.sub(p1, '', v_tmp)
                    v_tmp = re.sub(p2, '上诉人', v_tmp)
                    v_tmp = re.sub(p3, '被告人', v_tmp)
                    v_tmp = re.sub(p4,'\n辩护人',v_tmp)
                    v_tmp = re.sub('（.*?(指派|委托)）', '', v_tmp)



                    dict_clean_party_info[k] = v_tmp
            else:
                dict_clean_party_info[k] = v
        return dict_clean_party_info

    '''获取原告信息、被告信息'''
    def get_yg_bg(self,dict_clean_party_info):

        dict_yg_bg = {}
        for k, v in dict_clean_party_info.items():
            v_tmp = {'原告信息': '', '被告信息': ''}
            if v:
                # 1.自诉人做原告
                if re.search('自诉人', v):
                    # 原告
                    # 1.1自诉人、被告人同时存在
                    for i in range(len(rule_2.yg_bg_rule)):
                        if re.search(rule_2.yg_bg_rule[i],v):

                            v_tmp['原告信息'] = re.search(rule_2.yg_bg_rule[i], v).group()
                            break

                    # 1.2只存在自诉人
                    if not v_tmp['原告信息']:
                        for i in range(len(rule_2.yg_rule)):
                            if re.search(rule_2.yg_rule[i], v):
                                v_tmp['原告信息'] = re.search(rule_2.yg_rule[i], v).group()
                                break

                    # 被告
                    for j in range(len(rule_2.bg_rule)):
                        if re.search(rule_2.bg_rule[j], v):
                            v_tmp['被告信息'] = re.search(rule_2.bg_rule[j], v).group()
                            break

                # 2.检察院做原告
                elif re.search('检察院|检院|法院', v):
                    v_arr = v.split('\n')
                    for v_ in v_arr:
                        if re.search('检察院|检院|法院', v_) and len(v_) < 50:
                            if '公诉机关' in v_:
                                v_ = re.search('机关.*?(检察院|法院|检院)', v_).group()[2:]
                            else:
                                v_ = re.search('^.*?院', v_).group()
                            v_ = v_.replace('：', '')
                            v_tmp['原告信息'] = v_
                            break

                    # 被告
                    for j in range(len(rule_2.bg_rule)):
                        if re.search(rule_2.bg_rule[j], v):
                            v_tmp['被告信息'] = re.search(rule_2.bg_rule[j], v).group()
                            break
                        else:
                            v_tmp['被告信息'] = v

                # 3.原告不明确
                else:
                    # 原告
                    v_tmp['原告信息'] = ''

                    # 被告
                    for j in range(len(rule_2.bg_rule)):
                        if re.search(rule_2.bg_rule[j], v):
                            v_tmp['被告信息'] = re.search(rule_2.bg_rule[j], v).group()
                            break
                        else:
                            v_tmp['被告信息'] = v

            dict_yg_bg[k] = v_tmp

        return dict_yg_bg



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
        #针对行事：清理出现辩护人出现诉讼代理人的情况:暨委托诉讼代理人代莉^郭凤林^李行^刘雪梅^任小蓉
        elif re.search('(兼|暨|及|、).*?(代理人|被告人|原告人|上诉人|被上诉人)', cognitor):
            x_ = re.search('(代理人|被告人|原告人|上诉人|被上诉人).*', cognitor).group()[3:]
            new_cognitor = x_

        #针对刑事：被告人宝东林未委托辩护人
        elif re.search('未委托辩护人', cognitor):
            new_cognitor = '空'
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
        elif re.search('人',name):
            id_ = name.index('人')
            new_name = name[id_+1:]
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
                # 针对刑事案件：
                # 四川省泸州市中级人民法院
                # 驳 回 申 诉 通 知 书
                # （2020）川05刑申6号
                # 刘某：
                # 你因刘定才被判故意伤害罪一案,

                if len(v[0]) == 1 and re.search('被告人|嫌疑人|上诉人|原审被告人|罪犯|被罚款人|被拘留人|被申请人',v[0][0]) == None:
                    x_ = self.clean_name(v[0][0])
                    name_arr.append(x_)
                    address_arr.append('空')

                else:
                    for i in range(len(v)):
                        if v[i][0] in role_title_arr:
                            if len(v[i])>1:
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



                        if re.search('诉讼代理人|委托代理人|辩护人|辨护人', v[i][0]):

                            lawyer_address_arr.append('空')
                            if v[i][0][-3:] in ('代理人', '辩护人') and len(v[i])>1:
                                tmp = v[i][1]

                                if re.search('（|/\(',tmp):
                                    tmp = re.sub('（.*?）|/\(.*?/\)|（.*','',tmp)
                                if re.search('、.*?[事服]{1}务所|法律援助中心|法律服务|该',tmp):
                                    tmp = re.split('、', tmp)[0]

                            else:

                                tmp = re.search('(代理人|辩护人|辨护人).*',v[i][0]).group()[3:]
                                if re.search('（|/\(',tmp):
                                    tmp = re.sub('（.*?）|/\(.*?/\)|（.*','',tmp)
                                    if len(tmp)>0:
                                        tmp = tmp
                                    else:
                                        try:
                                            if not re.search('[事服]{1}务所|法律援助中心|法律服务|该',v[i][1]):
                                                tmp = v[i][1]
                                        except:
                                            pass

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

                        if re.search('法定代理人',v[i][0]):
                            if v[i][0][-3:]=='代理人' and len(v[i])>1:
                                representive_arr.append(v[i][1])
                            else:
                                tmp = re.search('代理人.*',v[i][0]).group()[3:]
                                representive_arr.append(tmp)

            detailed_dict[k] = [name_arr,address_arr,lawyer_arr,lawyer_address_arr,representive_arr]
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

    # 原告被告第三人组合的具体字典
    def combine_(self,yg_merged_dict_arr,bg_merged_dict_arr):

        detailed_dict = {}
        for i in range(len(yg_merged_dict_arr)):
            v_temp = {'原告信息':'','被告信息':'','第三人信息':''}
            k = list(yg_merged_dict_arr[i][0].keys())[0]
            v_temp['原告信息'] = list(yg_merged_dict_arr[i][0].values())[0]
            v_temp['被告信息'] = list(bg_merged_dict_arr[i][0].values())[0]

            detailed_dict[k] = v_temp


        return detailed_dict

    # 将刑事的原告检察院加入原告信息
    def add_office(self,dict_yg,detailed_dict):
        for k, v in detailed_dict.items():
            if re.search('检察院|检院|法院',dict_yg[k]):
                detailed_dict[k]['原告信息'][0] = dict_yg[k]

        return detailed_dict

    def detailed_dict_to_df(self,detailed_dict):
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

            v_temp['_3rd_name'].append('空')
            v_temp['_3rd_address'].append('空')
            # v['第三人信息'][2] = move_duplicate(v['第三人信息'][2])
            v_temp['_3rd_cognitor'].append('空')
            # v['第三人信息'][3] = move_duplicate(v['第三人信息'][3])
            v_temp['_3rd_cognitor_address'].append('空')
            v_temp['_3rd_representive'].append('空')

        df_ = pd.DataFrame(v_temp)

        return df_, detailed_dict

    # 刑事party_info入口
    def run(self,dict_party_info):

        # 清洗当事人头部信息
        dict_clean_party_info = self.clean_party_info(dict_party_info)

        # 获取原被告信息
        dict_yg_bg = self.get_yg_bg(dict_clean_party_info)

        dict_yg = {}
        dict_bg = {}
        for k, v in dict_yg_bg.items():
            dict_yg[k] = dict_yg_bg[k]['原告信息']
            dict_bg[k] = dict_yg_bg[k]['被告信息']

        dict_yg_arr = []
        dict_bg_arr = []
        for k, v in dict_yg.items():
            inn_dict = {}
            inn_dict[k] = v
            dict_yg_arr.append([inn_dict])
        for k, v in dict_bg.items():
            inn_dict = {}
            inn_dict[k] = v
            dict_bg_arr.append([inn_dict])

        bg_merged_dict_arr = self.correspond(dict_bg_arr, rule_2.bg_title)
        yg_merged_dict_arr = self.correspond(dict_yg_arr, rule_2.yg_title)

        detailed_dict_ = self.combine_(yg_merged_dict_arr, bg_merged_dict_arr)
        detailed_dict__ = self.add_office(dict_yg, detailed_dict_)
        df_ = self.detailed_dict_to_df(detailed_dict__)[0]
        detailed_dict = self.detailed_dict_to_df(detailed_dict__)[1]
        # for k,v in detailed_dict_.items():
        #     print(k)
        #     print(v)

        return df_,detailed_dict





