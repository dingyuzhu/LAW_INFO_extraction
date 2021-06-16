# -*- coding: UTF-8 -*-
import re
import Rule_3


'''当事人信息段提取类'''


class Fields_abstract():

    # 原则：（前提一定要排除qw为空的情况）
    # 1. 如果qw和ssjl都不为空，那么当事人段落就为qw-ssjl
    # 2. 如果qw不为空，ssjl为空，那么当事人段落按照我的规则提取

    def fields_dict_extract(self, all_data):

        dict_party_info = {}
        dict_ssqq = {}
        dict_ss_ssqq = {}
        extra_dict = {}
        dict_top = {}
        for data in all_data: #  a.id, a.qw, a.ssjl, b.sb, a.is_table, b.wslx, b.spcx_id, b.pjjg,b.ajlx,a.ss
            # 民事
            if data[8] == 3:
                dict_top[data[0]] = data[3]
                extra_dict[data[0]] = data[0]


                #dict_ssqq = {}和dict_ss_ssqq = {}的构造
                if data[9]:
                    if re.search(Rule_3.SSQQ_Rule, data[9]):
                        dict_ssqq[data[0]] = re.search(Rule_3.SSQQ_Rule, data[9]).group()
                    else:
                        if re.search(Rule_3.SSQQ_Rule_, data[9]):
                            dict_ssqq[data[0]] = re.search(Rule_3.SSQQ_Rule_, data[9]).group()
                        else:
                            dict_ssqq[data[0]] = ''

                    if dict_ssqq[data[0]]:
                        try:
                            dict_ss_ssqq[data[0]] = data[9].replace(dict_ssqq[data[0]], '')
                            dict_ssqq[data[0]] = re.search('(:|：|,)[\S\s]+(。|\n)', dict_ssqq[data[0]]).group()[1:]
                        except:
                            dict_ssqq[data[0]] = dict_ssqq[data[0]]
                    else:
                        dict_ss_ssqq[data[0]] = data[9]



                # dict_party_info = {}的构造  # id, qw,ssjl,ss,sb,is_table
                tmp_partyinfo = ''
                # qw 和 ssjl都不为空
                if data[1] and data[2]:

                    data_2 = data[2].replace('\\', '').replace('(', '（').replace(')','）').replace(' ','').replace('Ｘ','X')\
                        .replace('[', '［').replace(']', '］').replace('Ｃ', 'C').replace('Ｂ', 'B')
                    data_1 = data[1].replace('\\', '').replace('(', '（').replace(')','）').replace(' ','').replace('Ｘ','X')\
                        .replace('[', '［').replace(']', '］')

                    data_2 = re.sub('\*|\?|＃','', data_2)
                    data_1 = re.sub('\*|\?|#','', data_1)


                    if re.search(data_2, data_1):
                        try:
                            tmp_partyinfo = re.split(data_2, data_1)[0]


                        except:
                            pass
                    else:
                        try:
                            first_sen = re.search('^[\S\s]+?(，|,|。|/.|、|\n)',data_2).group()
                        except:
                            first_sen = data_2

                        if re.search(first_sen, data_1):

                            tmp_partyinfo = re.split(first_sen, data_1)[0]

                        elif re.search(data_2[:15], data_1):

                            tmp_partyinfo = re.split(data_2[:15], data_1)[0]

                        else:
                            # 通知书、决定书、通知书、支付令、支付令、其他通用
                            extra_rule = '\n.*?诉讼请求(：|:|\n)|' \
                                         '\n.*?(如下协议|协议如下).*?\n|' \
                                         '\n本院[\S\s]+?决定如下(:|：)|' \
                                         '\n你.*?起诉状已收到|' \
                                         '\n申请人[\S\s]+?特发出如下支付令|' \
                                         '\n申请人.*?向本院申请支付令|' \
                                         '\n.*?[与诉]{1}.*?纠纷.*?案|' \
                                         '\n本院[\S\s]+?裁定如下|' \
                                         '\n.*?向本院提出诉讼请求(：|:)|' \
                                         '\n根据《|' \
                                         '\n.*?一案'
                            r1 = Rule_3.ms_ys_pjs_HEAD_RULE
                            r2 = Rule_3.ms_ys_cds_HEAD_RULE
                            r3 = Rule_3.ms_ys_tjs_HEAD_RULE
                            r4 = Rule_3.ms_es_pjs_HEAD_RULE
                            r5 = Rule_3.ms_es_cds_HEAD_RULE
                            r6 = Rule_3.ms_zs_cds_HEAD_RULE

                            rule_arr = [extra_rule, r1, r2, r3, r4, r5, r6]
                            for i in rule_arr:
                                if re.search(i, data_1):
                                    tmp_partyinfo = re.split(i, data_1)[0]
                                    break

                # qw 不为空，ssjl为空
                elif data[1] and not data[2]:

                    data_1 = data[1].replace('\\', '').replace('(', '（').replace(')', '）').replace(' ', '').replace('Ｘ',
                                                                                                                    'X') \
                        .replace('[', '［').replace(']', '］').replace(' ','')
                    data_1 = re.sub('\*|\?|#', '', data_1)

                    # 通知书、决定书、通知书、支付令、支付令、其他通用
                    extra_rule = '\n.*?诉讼请求(：|:|\n)|'\
                                 '\n.*?(如下协议|协议如下).*?\n|' \
                                 '\n本院[\S\s]+?决定如下(:|：)|' \
                                 '\n你.*?起诉状已收到|' \
                                 '\n申请人[\S\s]+?特发出如下支付令|' \
                                 '\n申请人.*?向本院申请支付令|' \
                                 '\n.*?[与诉]{1}.*?纠纷.*?案|' \
                                 '\n本院[\S\s]+?裁定如下|' \
                                 '\n.*?向本院提出诉讼请求(：|:)|' \
                                 '\n根据《|' \
                                 '\n(原告诉求|基本案情|申请事项：|原告诉请)\n|' \
                                 '\n(经本院审查，|本案在审理过程中|经审查认为，|经本院主持调解，)|' \
                                 '\n诉[\n]{0,1}讼[\n]{0,1}请[\n]{0,1}求[\n]{0,1}|' \
                                 '\n.*?诉称：|' \
                                 '\n原告.*?一案|' \
                                 '\n申请事项：|' \
                                 '\n.*?根据.*?的申请|' \
                                 '\n复议申请人.*?不服.*?申请复议'
                    r1 = Rule_3.ms_ys_pjs_HEAD_RULE
                    r2 = Rule_3.ms_ys_cds_HEAD_RULE
                    r3 = Rule_3.ms_ys_tjs_HEAD_RULE
                    r4 = Rule_3.ms_es_pjs_HEAD_RULE
                    r5 = Rule_3.ms_es_cds_HEAD_RULE
                    r6 = Rule_3.ms_zs_cds_HEAD_RULE

                    rule_arr = [extra_rule, r1, r2, r3, r4, r5, r6]
                    for i in rule_arr:
                        if re.search(i, data_1):
                            tmp_partyinfo = re.split(i, data_1)[0]
                            break

                # 去除party_info表中的sb部分  # a.id, a.qw, a.ssjl, b.sb, a.is_table, b.wslx, b.spcx_id, a.pjjg
                tmp_partyinfo = tmp_partyinfo.replace('(', '（').replace(')', '）').\
                    replace('{', '（').replace('}', '）').replace(' ','').replace('\\','').replace('?','').replace('*','').replace('+','').replace('.','')
                tmp_partyinfo = re.sub('ｘ|Ｘ', 'x', tmp_partyinfo)

                if data[3]:
                    slicer_ = data[3].replace('(', '（').replace(')', '）').\
                        replace('{', '（').replace('}', '）').replace(' ', '').replace('\\','').replace('?','').replace('*','').replace('+','').replace('.','')
                    slicer_ = re.sub('ｘ|Ｘ', 'x', slicer_)

                    if tmp_partyinfo:
                        # print(data[0])
                        # print(slicer_)
                        # print(tmp_partyinfo)
                        if re.search(slicer_, tmp_partyinfo):
                            tmp_partyinfo = re.split(slicer_, tmp_partyinfo)[1]

                        elif '\n' in tmp_partyinfo:
                            try:
                                tmp_partyinfo = re.sub('/\*', '', tmp_partyinfo)
                                tmp = re.split('[\D]{1}[\d]+[\D]{0,3}[\d]+.{0,3}号.{0,3}\n', tmp_partyinfo)
                                tmp = [i for i in tmp if i]
                                tmp_partyinfo = tmp[1]

                            except:
                                pass

                # qw 和 ssjl都为空
                else:
                    pass
                tmp_partyinfo = self.clean_party_info(tmp_partyinfo)
                dict_party_info[data[0]] = tmp_partyinfo

        return dict_party_info, dict_ssqq, dict_ss_ssqq,dict_top,extra_dict


    def clean_party_info(self,party_info):
        extra_rule = '诉讼请求：|\n原告[^。原告被告诉与]{0,300}(，|诉|与|和)被告[^。原告被告诉与纠纷一案]{0,300}(纠纷|一案)|' \
                     '\n.*?诉讼请求(：|:|\n)|' \
                     '\n本院[\S\s]+?决定如下(:|：)|' \
                     '\n你.*?起诉状已收到|' \
                     '\n申请人[\S\s]+?特发出如下支付令|' \
                     '\n申请人.*?向本院申请支付令|' \
                     '\n本院[\S\s]+?裁定如下|' \
                    '\n根据《|' \
                    '\n(原告诉求|基本案情|申请事项：|原告诉请)\n|' \
                     '\n(经本院审查，|本案在审理过程中|经审查认为，|经本院主持调解，)|' \
                    '\n诉[\n]{0,1}讼[\n]{0,1}请[\n]{0,1}求[\n]{0,1}|' \
                    '\n原告.*?一案|' \
                    '\n申请事项：' \

        tmp_partyinfo = party_info
        p = '（.*?案.*?）'
        if re.search(p, tmp_partyinfo):
            pass
        else:
            if re.search(extra_rule, party_info):
                tmp_partyinfo = re.split(extra_rule, party_info)[0]

        # 处理party_info中包含sb问题
        tmp_partyinfo = re.sub('　', '', tmp_partyinfo)
        rule_sb = '判决书\n|裁定书\n|通知书\n|调解书\n|决定书\n'
        ah = '（[\d]+?）[\D]{1}[\d]+[\D]{0,3}[\d]+.{0,3}号'

        if re.search(rule_sb, tmp_partyinfo):
            tmp_partyinfo = re.split(rule_sb, tmp_partyinfo)[1]

        if re.search(ah, tmp_partyinfo):
            tmp_partyinfo = re.split(ah, tmp_partyinfo)[1]

        return tmp_partyinfo




