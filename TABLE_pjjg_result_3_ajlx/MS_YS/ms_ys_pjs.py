# -*- coding: UTF-8 -*-
import re

'''民事一审判决书判决结果类'''
class MS_YS_PJS():

    def get_PJJG(self, all_data):

        dict_pjjg = {}
        dict_res = {}
        for data in all_data:    # a.id, b.ajlx, b.wslx, b.spcx_id, c.yg_pct, c.bg_pct,c.pjjg_cost_bear,a.pjjg,a.party_info
            if data[1] == 3 and data[2] == 1 and data[3] == 30100000000000000:
                dict_pjjg[data[0]] = [data[4], data[5], data[6], data[7],data[8]]
                dict_res[data[0]] = [data[1], data[2], data[3]]

        return dict_pjjg, dict_res


    #使用pjjg_cost_bear来判断胜败诉
    def cost_bear_pjjg(self,pjjg_cost_bear,pjjg):
        # 部分胜诉(保留)
        win_half = '(原[告]{0,1}|[上起]{1}诉人|申请人).*?(被告|被上诉人|被申请人).*(各半|共同|各|均|每人|各自)(负担|承担|担负|缴纳|担)' \
                   '|(原告|被告|[被]{0,1}上诉人|[被]{0,1}申请人).*?(负担|承担|担负|缴纳)[\d]+?[元]{0,1}.*?(原告|被告|[被]{0,1}上诉人|[被]{0,1}申请人).*?(负担|承担|担负|缴纳)[\d]+?[元]{0,1}|' \
                   '(原[告]{0,1}|[上起]{1}诉人|申请人).{0,5}(被告|被上诉人|被申请人).*(负担|承担|担负|缴纳|担)'
        # 胜诉(保留)
        win = '(被告|被[上起]{1}诉人|被申请人).*?(负担|承担|担负|缴纳|交纳|交付)|由被告'
        # 败诉(保留)
        lose = '(原告|[上起]{1}诉人|申请人).*?(负担|承担|担负|缴纳|交纳|交付)'
        tmp_v0 = pjjg_cost_bear.replace('(', '（').replace(')', '）')
        tmp_v0_ = re.sub('（.*?）', '', tmp_v0)
        v_tmp = {'判决结果类型':None, '判决结果':None}
        if re.search(win_half, tmp_v0_) != None:
            v_tmp['判决结果类型'] = '部分胜诉'
            v_tmp['判决结果'] = '部分胜诉'

        elif re.search(win, tmp_v0_) != None:
            v_tmp['判决结果类型'] = '胜诉'
            v_tmp['判决结果'] = '胜诉'


        elif re.search(lose, tmp_v0_) != None:
            v_tmp['判决结果类型'] = '败诉'
            v_tmp['判决结果'] = '败诉'

        else:
            v_tmp = self.pjjg_pjjg(pjjg)

        return v_tmp

    # 使用yg_pct,bg_pct来判断胜败诉
    def yg_bg_pct_pjjg(self, yg_pct, bg_pct):
        v_tmp = {'判决结果类型': None, '判决结果': None}
        if yg_pct > 0 and yg_pct < 1 and bg_pct > 0 and bg_pct < 1:
            v_tmp['判决结果类型'] = '部分胜诉'
            v_tmp['判决结果'] = '部分胜诉'
        elif yg_pct == 1 and bg_pct == 0:
            v_tmp['判决结果类型'] = '败诉'
            v_tmp['判决结果'] = '败诉'
        elif yg_pct == 0 and bg_pct == 1:
            v_tmp['判决结果类型'] = '胜诉'
            v_tmp['判决结果'] = '胜诉'
        return v_tmp

    # 使用pjjg来判断胜败诉
    def pjjg_pjjg(self,pjjg):
        v_tmp = {'判决结果类型': None, '判决结果': None}
        if not re.search('驳回', pjjg):
                v_tmp['判决结果类型'] = '胜诉'
                v_tmp['判决结果'] = '胜诉'
        else:
            if re.search('驳回', pjjg)  and not re.search('(其余|其他|其它).{0,5}(诉求|诉讼请求|请求)', pjjg):
                v_tmp['判决结果类型'] = '败诉'
                v_tmp['判决结果'] = '败诉'
            elif re.search('驳回.*?(其余|其他|其它)', pjjg):
                v_tmp['判决结果类型'] = '部分胜诉'
                v_tmp['判决结果'] = '部分胜诉'



        return v_tmp




    '''对文书的判决结果进行分类'''
    def PJJG_classfication(self, dict_pjjg):
        result_dict_pjjg = {}

        for k, v in dict_pjjg.items():# v=[yg_pct, bg_pct, pjjg_cost_bear, pjjg, party_info]

            # 有原被告承担比例
            if v[0] or v[1]:
                # 出现自愿用pjjg
                p = '自愿[^，。\\n]{0,50}(负担|承担|支付)|负担（自愿）|减免|免交|免收|免(于|予)[^，；。\\n]{0,10}收取|免于交纳|免于缴纳|免予缴纳|免予交纳|予以免缴|予以免受|予以免取|免受|免缴|予以免除|免予征收'
                if re.search(p,v[2]):
                    v_tmp = self.pjjg_pjjg(pjjg=v[3])
                # 不出现自愿用pct
                else:
                    v_tmp = self.yg_bg_pct_pjjg(yg_pct=v[0],bg_pct=v[1])
            # 无原被告承担比例
            else:
                # 如果pjjg不为空,且party_info暗示不是反诉并案
                v4 = v[4].replace('(', '（').replace(')','）')
                if v[3] and not re.search('(反诉|并案)(原告|被告|人)|原告（被告）|被告（原告）',v4):
                    v_tmp = self.pjjg_pjjg(pjjg=v[3])
                # 如果pjjg为空
                else:
                    v_tmp = {'判决结果类型': None, '判决结果': None}
            result_dict_pjjg[k] = v_tmp

        return result_dict_pjjg


    def run(self, all_data):
        dict_pjjg,dict_res = self.get_PJJG(all_data)

        result_dict_pjjg = self.PJJG_classfication(dict_pjjg)

        return result_dict_pjjg,dict_res








