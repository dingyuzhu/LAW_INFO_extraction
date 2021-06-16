# -*- coding: UTF-8 -*-
import re




'''民事一审裁定书判决结果类'''
class MS_YS_CDS():

    def get_PJJG(self, all_data):  # a.id, a.pjjg, b.ajlx, b.wslx, b.spcx_id, a.sb, a.ssqq, c.pjjg as orin_pjjg
        dict_pjjg = {}
        dict_res = {}
        for data in all_data:
            if  data[2] == 3 and data[3] == 2 and data[4] == 30100000000000000:
                # 如果原判决不为空
                if data[7]:
                    dict_pjjg[data[0]] = data[7]
                # 如果原判决为空
                else:
                    dict_pjjg[data[0]] = data[1]

                dict_res[data[0]] = [data[2], data[3],data[4],data[6]]
        return dict_pjjg, dict_res


    '''对文书的判决结果进行分类'''
    def PJJG_classfication(self,dict_pjjg):
        result_dict_pjjg = {}
        a = CDS_CLASSFIER()
        for k, v in dict_pjjg.items():
            v_temp = a.classfication(v)
            result_dict_pjjg[k] = v_temp

        return result_dict_pjjg


    def run(self, all_data):
        dict_pjjg,dict_res = self.get_PJJG(all_data)
        result_dict_pjjg = self.PJJG_classfication(dict_pjjg)
        return result_dict_pjjg,dict_res


'''封装裁定书判定的一个功能'''
class CDS_CLASSFIER():
    def __init__(self):
        self.pjjg_type= {
        1: '是否受理类',
        2: '管辖权异议类',
        3: '驳回起诉类',
        4: '保全类',
        5: '准许与不准许撤诉类',
        6: '中止或终结诉讼类',
        7: '补正判决书笔误类',
        8: '中止或终结执行类',
        9: '撤销或不予执行仲裁裁决类',
        10: '不予执行公证机关赋予强制执行效力的债权文书',
        11: '先予执行类',
        12: '变更诉讼程序类',
        13: '案件移送类',
        14: '并案类',
        15: '驳回反诉类',
        16: '其他'

    }
    def classfication(self,txt):
            v_temp = {'判决结果类型': None, '判决结果': None}

            # 剔除干扰项1：如不服本裁定|如不服本判决后面的
            txt = re.sub('如不服(本裁定|本判决|\n案件受理费|\n诉讼费)[\S\s]+','',txt)


            # type5：准许与不准许撤诉类
            p_chesu ='撤[销回起上]{0,2}诉讼|撤[回销]{0,1}[\S\s]+?([起反告本]{0,1}诉|诉讼|申请)|' \
                     '准[许予]{0,1}[\S\S]+?(撤回[\S\s]+?(上诉|起诉)|撤诉)|[本案院]{0,2}[按作]{1}[\S\s]+?撤[回上起]{0,2}诉处理|撤诉处理|撤诉'
            if re.search(p_chesu, txt) and not re.search('驳回', txt):
                v_temp['判决结果类型'] = self.pjjg_type[5]
                p_allow = '准[许予]{0,1}[\S\s]+?(撤回[\S\s]+?(上诉|起诉)|撤诉)|[本案院]{0,2}[按作]{1}[\S\s]+?撤[回上起]{0,2}诉处理|' \
                          '撤[销回起上]{0,2}诉讼|撤[回销]{0,1}[\S\s]+?([起反告本]{0,1}诉|诉讼|申请)|' \
                          '[本案院]{0,2}[按作]{1}[\S\s]+?撤[回上起反]{0,2}[\S\s]+?诉处理|自动撤诉|自动撤回本诉|撤诉处理|撤诉'
                if re.search(p_allow, txt) != None:
                    v_temp['判决结果'] = '准许撤诉'
                if re.search('不准[许予]{0,1}.*?撤[回上起反]{0,2}诉', txt) != None:
                    v_temp['判决结果'] = '不准许撤诉'

            # type1  是否受理类
            elif re.search('不受理.*?的申请|不予受理|不予立案', txt) and not re.search('驳回', txt):
                v_temp['判决结果类型'] = self.pjjg_type[1]
                v_temp['判决结果'] = '不予受理'

            # type2  管辖权异议类
            elif re.search('管辖[权]{0,1}.*?(成立|不成立)|驳回.*?管[辖理]{1}[权]{0,1}.*?异议|异议成立', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[2]
                if re.search('管辖[权]{0,1}.*?(成立|不成立)|驳回.*?管[辖理]{1}[权]{0,1}.*?异议|异议成立', txt) != None:
                    v_temp['判决结果'] = '管辖权异议不成立'
                if re.search('管辖权.*?异议成立|管辖异议.*?成立', txt) != None:
                    v_temp['判决结果'] = '管辖权异议成立'

            # type3 驳回起诉类
            elif re.search('驳回.*?(起诉|申请|请求|诉讼|异议|上诉)|的(起诉|申请|请求|诉讼|异议|上诉).*?本院予以驳回|上诉不成立',txt):
                v_temp['判决结果类型'] = self.pjjg_type[3]
                v_temp['判决结果'] = '驳回起诉'


            # type15 驳回反诉类
            elif re.search('驳回.*?反诉|的反诉.*?本院予以驳回',txt):
                v_temp['判决结果类型'] = self.pjjg_type[15]
                v_temp['判决结果'] = '驳回反诉'


            # type4 保全类
            elif re.search('查封|冻结|解除|^((?!费)[\S\s])*保全((?!费)[\S\s])*$', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[4]
                if re.search('查封|冻结|解除|^((?!费)[\S\s])*保全((?!费)[\S\s])*$', txt) != None:
                    v_temp['判决结果'] = '保全'

            # type6 中止或终结诉讼
            elif re.search('(中止|终结).*?(诉讼|审理|审查)|(诉讼|审理|审查).{0,3}(中止|终结)', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[6]
                if re.search('中止.*?(诉讼|审理|审查)|(诉讼|审理|审查).{0,3}中止', txt) != None:
                    v_temp['判决结果'] = '中止诉讼'
                if re.search('终结.*?(诉讼|审理|审查)|(诉讼|审理|审查).{0,3}终结', txt) != None:
                    v_temp['判决结果'] = '终结诉讼'

            # type7  补正判决书笔误类
            elif re.search('笔误|补正|”应为“|更[正改]{1}为|改为|变更为|”应为：“|“.*?”修改成“.*?”', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[7]
                if re.search('^(?=.*笔误)(?=.*补正).*$|补正|[更补改]{1}[正改]{1}为|应为|改为|系笔误|变更为|“.*?”修改成“.*?”', txt) != None:
                    v_temp['判决结果'] = '补正判决书笔误'

            # type8 中止或终结执行
            elif re.search('(中止|终结).*?执行', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[8]
                if re.search('中止.*?执行', txt) != None:
                    v_temp['判决结果'] = '中止执行'
                if re.search('终结.*?执行', txt) != None:
                    v_temp['判决结果'] = '终结执行'

            # type9 撤销或不予执行仲裁裁决类
            elif re.search('仲裁裁决', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[9]
                if re.search('^撤销.*?仲裁裁决', txt) != None:
                    v_temp['判决结果'] = '撤销仲裁裁决'
                if re.search('^不予执行.*?仲裁裁决', txt) != None:
                    v_temp['判决结果'] = '不予执行仲裁裁决'


            # type10  不予执行公证机关赋予强制执行效力的债权文书
            # elif re.search('', v) != None:
            #     pass

            # type11  先予执行
            elif re.search('先予执行', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[11]
                if re.search('先予执行', txt) != None:
                    v_temp['判决结果'] = '先予执行'

            # type12  变更诉讼程序
            elif re.search('(转|适用|按照).*?(普通|简易)程序|不适宜使用.{0,2}程序', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[12]
                if re.search('(转|适用|按照).*?(普通|简易)程序|不适宜使用.{0,2}程序', txt) != None:
                    v_temp['判决结果'] = '变更诉讼程序'

            # type13  案件移送类
            elif re.search('^本案.{0,3}移送|移送', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[13]
                if re.search('^本案.{0,3}移送|该案.{0,2}移送|移送', txt) != None:
                    v_temp['判决结果'] = '案件移送'

            # type14 并案
            elif re.search('本案并入|并入', txt) != None:
                v_temp['判决结果类型'] = self.pjjg_type[14]
                v_temp['判决结果'] = '并案'

            # type16 其他需要裁定解决的事项类
            elif txt:
                v_temp['判决结果类型'] = self.pjjg_type[16]
                v_temp['判决结果'] = '其他'
            return v_temp



# import time
# if __name__=="__main__":
#
#
#     # 程序开始执行时间
#     start = time.time()
#
#
#     # 结束时间
#     end = time.time() - start
#     print(end)






