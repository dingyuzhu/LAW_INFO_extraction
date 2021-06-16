# -*- coding: UTF-8 -*-
import re
import Rule_4

'''当事人信息段提取类'''


class Fields_abstract():

    # 原则：（前提一定要排除qw为空的情况）
    # 1. 如果qw和ssjl都不为空，那么当事人段落就为qw-ssjl
    # 2. 如果qw不为空，ssjl为空，那么当事人段落按照我的规则提取

    def fields_dict_extract(self, all_data):

        dict_top = {}
        dict_party_info = {}
        extra_dict = {}
        dict_ssqq = {}
        dict_ss_ssqq = {}
        for data in all_data:   # a.id, a.qw, a.ssjl, b.sb, a.is_table, b.wslx, b.spcx_id, a.pjjg

            # 行政
            if data[8] == 4:
                dict_ssqq[data[0]] = ''
                dict_ss_ssqq[data] = ''
                dict_top[data[0]] = data[3]
                extra_dict[data[0]] = data[0]



                # dict_party_info = {}的构造
                tmp_partyinfo = ''
                # qw 和 ssjl 都不为空时
                if data[1] and data[2]:
                    data_2 = data[2].replace('\\', '').replace('(', '（').replace(')', '）').replace(' ', '').replace('Ｘ',
                                                                                                                    'X') \
                        .replace('[', '［').replace(']', '］').replace('Ｃ', 'C').replace('Ｂ', 'B')
                    data_1 = data[1].replace('\\', '').replace('(', '（').replace(')', '）').replace(' ', '').replace('Ｘ',
                                                                                                                    'X') \
                        .replace('[', '［').replace(']', '］')

                    data_2 = re.sub('\*|\?|＃', '', data_2)
                    data_1 = re.sub('\*|\?|#', '', data_1)

                    if re.search(data_2, data_1):
                        try:
                            tmp_partyinfo = re.split(data_2, data_1)[0]
                        except:
                            pass
                    else:
                        if re.search('^[\S\s]+?(，|,|。|/.|、|\n)', data_2):
                            first_sen = re.search('^[\S\s]+?(，|,|。|/.|、|\n)', data_2).group()
                        else:
                            first_sen = data_2

                        if re.search(first_sen, data_1):
                            tmp_partyinfo = re.split(first_sen, data_1)[0]

                        elif re.search(data_2[:15], data_1):

                            tmp_partyinfo = re.split(data_2[:15], data_1)[0]

                        else:
                            r1 = Rule_4.ms_ys_pjs_HEAD_RULE
                            r2 = Rule_4.ms_ys_cds_HEAD_RULE
                            r3 = Rule_4.ms_ys_tjs_HEAD_RULE
                            r4 = Rule_4.ms_es_pjs_HEAD_RULE
                            r5 = Rule_4.ms_es_cds_HEAD_RULE
                            r6 = Rule_4.ms_zs_cds_HEAD_RULE
                            r7 = '\n申请执行人.*?[0-9]+?号|' \
                                 '\n(申请执行人|申请人).*?申请.*?执行|' \
                                 '\n.*?本院.*?收到.*?(诉状|诉讼)|' \
                                 '\n.*?诉称|' \
                                 '\n.*?向本院(提起|提交|递交).*?(诉讼|诉状)|' \
                                 '\n事实与理由:|' \
                                 '\n经审查查明|' \
                                 '\n被告以|\n申请人.*?以|' \
                                 '\n.*?一案(，|。)' \

                            rule_arr = [r7, r1, r2, r3, r4, r5, r6]
                            for i in rule_arr:
                                if re.search(i, data_1):
                                    tmp_partyinfo = re.split(i, data_1)[0]
                                    break

                elif data[1] and not data[2]:
                    data_1 = data[1].replace('\\', '').replace('(', '（').replace(')','）').replace(' ','').replace('[', '（').replace(']','）').replace('［','（')
                    data_1 = re.sub('\*|\?', '', data_1)

                    r7 ='\n.*?请求(:|：)|\n申请执行人.*?申请书|\n起诉人.*?诉状称'\
                        '\n[0-9]+?年[0-9]+?月[0-9]+?日|' \
                        '\n.*?本院.*?收到.*?起诉状|' \
                        '\n申请执行人.*?[0-9]+?号|' \
                         '\n(申请执行人|申请人).*?申请.*?执行|' \
                         '\n.*?向本院(提起|提交|递交).*?(诉讼|诉状)|' \
                         '\n.*?诉称|' \
                         '\n.*?向本院提起诉讼|' \
                         '\n事实与理由:|' \
                         '\n经审查查明|' \
                         '\n被告以|\n申请人.*?以|' \
                         '\n.*?一案(，|。)'
                    r1 = Rule_4.ms_ys_pjs_HEAD_RULE
                    r2 = Rule_4.ms_ys_cds_HEAD_RULE
                    r3 = Rule_4.ms_ys_tjs_HEAD_RULE
                    r4 = Rule_4.ms_es_pjs_HEAD_RULE
                    r5 = Rule_4.ms_es_cds_HEAD_RULE
                    r6 = Rule_4.ms_zs_cds_HEAD_RULE

                    rule_arr = [r7, r1, r2, r3, r4, r5, r6]

                    for i in rule_arr:
                        if re.search(i, data_1):
                            tmp_partyinfo = re.split(i, data_1)[0]
                            break

                # 去除party_info表中的sb部分  # id, qw,ssjl,sb,is_table
                tmp_partyinfo = tmp_partyinfo.replace('(', '（').replace(')', '）'). \
                                              replace('{', '（').replace('}', '）').replace(' ', '').\
                                              replace('\\', '').replace('?', '').replace('*', '').replace('　', '')
                tmp_partyinfo = re.sub('ｘ|Ｘ', 'x', tmp_partyinfo)

                if data[3]:
                    slicer_ = data[3].replace('(', '（').replace(')', '）'). \
                                      replace('{', '（').replace('}', '）').replace(' ', '').\
                                      replace('\\', '').replace('?', '').replace('*','').replace('　', '')
                    slicer_ = re.sub('ｘ|Ｘ', 'x', slicer_)

                    if tmp_partyinfo:
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

                else:
                    pass
                tmp_partyinfo = self.clean_party_info(tmp_partyinfo)
                dict_party_info[data[0]] = tmp_partyinfo


        return dict_party_info, dict_ssqq, dict_ss_ssqq,dict_top,extra_dict

    def clean_party_info(self, party_info):


        # 1.处理party_info中带有ssjl的问题
        extra_rule = '\n.*?诉讼请求(：|:|\n|，)|' \
                     '\n.*?(如下协议|协议如下).*?\n|' \
                     '\n本院[\S\s]+?决定如下(:|：)|' \
                     '\n你.*?起诉状已收到|' \
                     '\n申请人[\S\s]+?特发出如下支付令|' \
                     '\n申请人.*?向本院申请支付令|' \
                     '\n.*?[与诉]{1}.*?纠纷.*?案|' \
                     '\n本院[\S\s]+?(裁定如下|审理查明：)|' \
                     '\n.*?向本院提出诉讼请求(：|:)|' \
                     '\n根据《|' \
                     '\n(原告|起诉人).*?称(，|：|:)|' \
                     '\n[0-9]+?年[0-9]+?月[0-9]+?日|' \
                     '\n诉讼请求.*?，|' \
                     '\n申请执行人.*?申请书|' \
                     '\n诉请事由(:|：)|' \
                     '\n申请执行人.*?申请|' \
                     '\n本院收到.*?起诉材料'

        tmp_partyinfo = party_info

        # 排除案外人的干扰
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



