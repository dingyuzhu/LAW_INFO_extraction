# -*- coding: UTF-8 -*-
import re
import pandas as pd
import rule_3





'''民事一审、二审诉讼记录分类'''
class CXLX_CLASSIFICATION():
    def get_cxlx_data(self, all_data):
        dict_cxlx_data = {}
        for data in all_data:   # id, party_info, ssjl, ss_ssqq,spcx_id
            dict_cxlx_data[data[0]] = [data[1], data[2], data[3],data[4]]

        return dict_cxlx_data



    def absence(self,ssjl):
        # 0：缺席  1：出席
        yg_absence_ = 0
        bg_absence_ = 0
        _3rd_absence_ = None
        absence_pattern = '([未不]{1}[到出]{1}庭|不履行到庭义务|拒绝到庭|传唤未到|未能到庭|未按[时期]{1}[到出]{1}庭|未参加|离开法庭|缺席|传唤|传票)'
        if re.search(absence_pattern, ssjl):
            ssjl = re.sub('（.*?）', '', ssjl)
            ssjl_arr = re.split('，|。|,|/\.', ssjl)
            for j in range(len(ssjl_arr)):
                for i in range(len(rule_3.yg_title)):

                    if re.search(absence_pattern, ssjl_arr[j]):
                        if re.search('^{yg}'.format(yg=rule_3.yg_title[i]), ssjl_arr[j]):
                            yg_absence_ = 1
                        else:
                            if re.search('^{yg}'.format(yg=rule_3.yg_title[i]), ssjl_arr[j - 1]):
                                if not re.search(absence_pattern, ssjl_arr[j - 1]) and not re.search('到庭参加|出庭',ssjl_arr[j - 1]):
                                    yg_absence_ = 1

                        if re.search('{bg}'.format(bg=rule_3.bg_title[i]), ssjl_arr[j]):
                            bg_absence_ = 1
                        else:
                            if re.search('{bg}'.format(bg=rule_3.bg_title[i]), ssjl_arr[j - 1]):
                                if not re.search(absence_pattern, ssjl_arr[j - 1]) and not re.search('到庭参加|出庭',ssjl_arr[j - 1]):
                                    bg_absence_ = 1

                        if re.search('第三人', ssjl_arr[j]):
                            _3rd_absence_ = 1
                        else:
                            if re.search('第三人', ssjl_arr[j - 1]) and not re.search('到庭参加|出庭',ssjl_arr[j - 1]):
                                _3rd_absence_ = 1

        return [yg_absence_, bg_absence_, _3rd_absence_]



    def file_trial_time(self,ssjl):
        file_time = ''
        trial_time = ''
        ssjl_arr = re.split('，|。|,|/\.|、', ssjl)
        for i in range(len(ssjl_arr)):
            if re.search('[\d]{0,4}年[\d]{0,2}月[\d]{0,2}日.*?立案', ssjl_arr[i]):
                file_time = re.search('[\d]{0,4}年[\d]{0,2}月[\d]{0,2}日', ssjl_arr[i]).group()

            elif re.search('[\d]{0,4}年[\d]{0,2}月[\d]{0,2}日.*?审理', ssjl_arr[i]):
                trial_time = re.search('[\d]{0,4}年[\d]{0,2}月[\d]{0,2}日', ssjl_arr[i]).group()

        return file_time, trial_time





    '''根据诉讼记录进行分类'''
    def cxlx_process(self, dict_cxlx_data):
        #案件是否是再审案件
        dict_cxlx_result = {}   #v=[ party_info, ssjl, ss_ssqq, spcx_id]
        for k, v in dict_cxlx_data.items():
            v_temp = {'是否再审案件': None, '是否重审案件': None, '是否反诉案件': None, '案件所处程序': None,'原告缺席情况':None,'被告缺席情况':None,'第三人缺席情况':None,'庭审时间':None,'立案时间':None,'审判程序':None}

            #是否再审：先用ssjl，若无再用ss_ssqq （party_info, ssjl, ss_ssqq, spcx_id）
            if v[1] and v[2]:
                if re.search('(/\(|（)[\d]+(/\)|）)[\D]{1}[\d]+民(再|申|抗|监).{0,3}[\d]+.{0,3}号.{0,3}',v[1]) or re.search('(/\(|（)[\d]+(/\)|）)[\D]{1}[\d]+民(再|申|抗|监).{0,3}[\d]+.{0,3}号.{0,3}',v[2]):
                    v_temp['是否再审案件'] = 1
                else:
                    v_temp['是否再审案件'] = 0
            elif v[1] and not v[2]:
                if re.search('(/\(|（)[\d]+(/\)|）)[\D]{1}[\d]+民(再|申|抗|监).{0,3}[\d]+.{0,3}号.{0,3}',v[1]):
                    v_temp['是否再审案件'] = 1
                else:
                    v_temp['是否再审案件'] = 0
            elif not v[1] and v[2]:
                if re.search('(/\(|（)[\d]+(/\)|）)[\D]{1}[\d]+民(再|申|抗|监).{0,3}[\d]+.{0,3}号.{0,3}',v[2]):
                    v_temp['是否再审案件'] = 1
                else:
                    v_temp['是否再审案件'] = 0
            else:
                v_temp['是否再审案件'] = None

            #新版本：是否重审案件：只看ssjl
            if v[1]:
                if re.search('重审|重新审', v[1]):
                    v_temp['是否重审案件'] = 1
                else:
                    v_temp['是否重审案件'] = 0
            else:
                v_temp['是否重审案件'] = None

            #老版本：是否重审案件：先用ssjl，若无，再用ss_ssqq(party_info, ssjl, ss_ssqq, pjjg)
            # if v[1]:
            #     if re.search('重审|重新审', v[1]):
            #         v_temp['是否重审案件'] = 1
                # else:
                #     if v[2]:
                #         if re.search('(请|请求)(:|：)[\S\s]+?。',v[2]):
                #             pre_ssqq = re.search('(请|请求)(:|：)[\S\s]+?。', v[2]).group()
                #             pre_ssqq = pre_ssqq.replace('\\','-')
                #             rest = ''.join(re.split(pre_ssqq,v[2]))
                #             if re.search('重审|重新审',rest):
                #                 v_temp['是否重审案件'] = 1
                #             else:
                #                 v_temp['是否重审案件'] = 0
                #         else:
                #             if re.search('重审|重新审',v[2]):
                #                 v_temp['是否重审案件'] = 1
                #             else:
                #                 v_temp['是否重审案件'] = 0
                #     else:
                #         v_temp['是否重审案件'] = 0
            # else:
            #     if v[2]:
            #         if re.search('(请|请求)(:|：)[\S\s]+?。', v[2]):
            #             pre_ssqq = re.search('(请|请求)(:|：)[\S\s]+?。', v[2]).group()
            #             rest = ''.join(re.split(pre_ssqq, v[2]))
            #             if re.search('重审|重新审', rest):
            #                 v_temp['是否重审案件'] = 1
            #             else:
            #                 v_temp['是否重审案件'] = 0
            #         else:
            #             if re.search('重审|重新审', v[2]):
            #                 v_temp['是否重审案件'] = 1
            #             else:
            #                 v_temp['是否重审案件'] = 0
            #     else:
            #         v_temp['是否重审案件'] = None



            #是否反诉案件：只用party_info(反诉只做一审的)v=[ party_info, ssjl, ss_ssqq, spcx_id]
            if v[3] == 30100000000000000:
                if v[0]:
                    if re.search('反诉原告|反诉被告|反诉人|原告（被告）|被告（原告）',v[0]):
                        v_temp['是反诉审案件'] = 1
                    else:
                        v_temp['是否反诉案件'] = 0
                else:
                    v_temp['是否反诉案件'] = None
            else:
                if not v[0]:
                    v_temp['是反诉审案件'] = None
                else:
                    v_temp['是否反诉案件'] = 0


            #案件所处程序:只用ssjl
            if v[1]!=None and re.search('^((?!(普通[诉讼]{0,2}程序|小额[诉讼]{0,2}))[\S\s])*(简易[诉讼]{0,2}程序)((?!(普通[诉讼]{0,2}程序|小额[诉讼]{0,2}))[\S\s])*$', v[1]) != None:
                v_temp['案件所处程序'] = 1
            elif v[1] != None and re.search('^((?!(简易[诉讼]{0,2}程序|小额[诉讼]{0,2}))[\S\s])*(普通[诉讼]{0,2}程序)((?!(简易[诉讼]{0,2}程序|小额[诉讼]{0,2}))[\S\s])*$',v[1]):
                v_temp['案件所处程序'] = 2
            elif v[1] != None and re.search('^((?!(简易[诉讼]{0,2}程序|普通[诉讼]{0,2}程序))[\S\s])*(小额[诉讼]{0,2})((?!(简易[诉讼]{0,2}程序|普通[诉讼]{0,2}程序))[\S\s])*$', v[1]):
                v_temp['案件所处程序'] = 3
            elif v[1] != None and re.search('(转[为入换成]{0,1}|变更为)普通[诉讼]{0,2}程序', v[1]):
                v_temp['案件所处程序'] = 2
            elif v[1] != None and re.search('(转[为入换成]{0,1}|变更为)小额[诉讼]{0,2}程序', v[1]):
                v_temp['案件所处程序'] = 3
            elif v[1] != None and re.search('(转[为入换成]{0,1}|变更为)简易[诉讼]{0,2}程序', v[1]):
                v_temp['案件所处程序'] = 1
            elif v[1] != None and re.search('普通程序（√）', v[1]) != None:
                v_temp['案件所处程序'] = 2
            elif v[1] != None and re.search('简易程序（√）', v[1]) != None:
                v_temp['案件所处程序'] = 1
            elif v[1] != None and re.search('简易[诉讼]{0,2}程序.*?普通[诉讼]{0,2}程序', v[1]) != None:
                v_temp['案件所处程序'] = 2
            elif v[1] != None and re.search('普通[诉讼]{0,2}程序.*?简易[诉讼]{0,2}程序', v[1]) != None:
                v_temp['案件所处程序'] = 1
            elif v[1] != None and re.search('简易[诉讼]{0,2}程序.*?小额[诉讼]{0,2}程序|适用简易.*?（小额诉讼）|小额诉讼简易程序|简易程序.*?小额诉讼', v[1]) != None:
                v_temp['案件所处程序'] = 3
            elif v[1] != None and re.search('小额[诉讼]{0,2}程序.*?简易[诉讼]{0,2}程序|依法适用简易.*?审理|小额(贷款|借款).*?适用简易程序', v[1]) != None:
                v_temp['案件所处程序'] = 1
            elif v[1] != None and re.search('小额[诉讼]{0,2}程序.*?普通[诉讼]{0,2}程序|小额(贷款|借款).*?适用普通程序', v[1]) != None:
                v_temp['案件所处程序'] = 2
            elif v[1] != None and re.search('简易[诉讼]{0,2}程序|普通[诉讼]{0,2}程序|小额[诉讼]{0,2}程序', v[1]) == None:
                v_temp['案件所处程序'] = 4
            elif v[1] == None:
                v_temp['案件所处程序'] = None

            #当事人缺席情况
            if v[1]:
                v_temp['原告缺席情况'] = self.absence(v[1])[0]
                v_temp['被告缺席情况'] = self.absence(v[1])[1]
                v_temp['第三人缺席情况'] = self.absence(v[1])[2]
                v_temp['立案时间'] = self.file_trial_time(v[1])[0]
                v_temp['庭审时间'] =self.file_trial_time(v[1])[1]


            else:
                v_temp['原告缺席情况'] = None
                v_temp['被告缺席情况'] = None
                v_temp['第三人缺席情况'] = None
                v_temp['立案时间'] = None
                v_temp['庭审时间'] = None
            dict_cxlx_result[k] = v_temp

        return dict_cxlx_result



    def dict_to_df(self,dict_cxlx_result):

        v_temp = {'id':[], 'wenshu_id':[], 'is_zs': [], 'is_cs':[],'is_fs':[],'procedure_':[],'yg_absence':[],'bg_absence':[],'_3rd_absence':[],'trial_time':[],'file_time':[]}
        for k, v in dict_cxlx_result.items():
            if k :
                v_temp['id'].append(k)
                v_temp['wenshu_id'].append(k)
                v_temp['is_zs'].append(v['是否再审案件'])
                v_temp['is_cs'].append(v['是否重审案件'])
                v_temp['is_fs'].append(v['是否反诉案件'])
                v_temp['procedure_'].append(v['案件所处程序'])
                v_temp['yg_absence'].append(v['原告缺席情况'])
                v_temp['bg_absence'].append(v['被告缺席情况'])
                v_temp['_3rd_absence'].append(v['第三人缺席情况'])
                v_temp['trial_time'].append(v['庭审时间'])
                v_temp['file_time'].append(v['立案时间'])

        df = pd.DataFrame(v_temp)

        return df



    def run(self,all_data):

        dict_cxlx_data = self.get_cxlx_data(all_data)

        dict_cxlx_result = self.cxlx_process(dict_cxlx_data)

        df = self.dict_to_df(dict_cxlx_result)

        return df






