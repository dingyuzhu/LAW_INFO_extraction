
import re
import Rule_3
class PJJG_Abstract():

    # 获取data
    def get_data2(self, all_data): #  a.id, a.qw, a.ssjl, b.sb, a.is_table, b.wslx, b.spcx_id, a.pjjg,b.ajlx,a.ss
        dict_data = {}
        for data in all_data:
            # 分流
            if data[8] == 2 and data[1]:
                qw = data[1].replace(':', '：').replace(' ', '').replace(' ', '').replace('　', '')
                qw = re.sub('审\n判\n(员|长)', '审判员', qw)
                pjjg = data[7]
                wslx = data[5]
                dict_data[data[0]] = [qw, pjjg, wslx]
        return dict_data

    def get_data3(self, all_data): #  a.id, a.qw, a.ssjl, b.sb, a.is_table, b.wslx, b.spcx_id, a.pjjg,b.ajlx,a.ss
        dict_data = {}
        for data in all_data:
            # 分流
            if data[8] == 3 and data[1]:
                qw = data[1].replace(':', '：').replace(' ', '').replace(' ', '').replace('　', '')
                qw = re.sub('审\n判\n(员|长)', '审判员', qw)
                pjjg = data[7]
                wslx = data[5]
                dict_data[data[0]] = [qw, pjjg, wslx]
        return dict_data

    def get_data4(self, all_data): #  a.id, a.qw, a.ssjl, b.sb, a.is_table, b.wslx, b.spcx_id, a.pjjg,b.ajlx,a.ss
        dict_data = {}
        for data in all_data:
            # 分流
            if data[8] == 4 and data[1]:
                qw = data[1].replace(':', '：').replace(' ', '').replace(' ', '').replace('　', '')
                qw = re.sub('审\n判\n(员|长)', '审判员', qw)
                pjjg = data[7]
                wslx = data[5]
                dict_data[data[0]] = [qw, pjjg, wslx]
        return dict_data

    def get_data_other(self, all_data): #  a.id, a.qw, a.ssjl, b.sb, a.is_table, b.wslx, b.spcx_id, a.pjjg,b.ajlx,a.ss
        dict_data = {}
        for data in all_data:
            # 分流
            if data[8] not in (2,3,4) and data[1]:
                qw = data[1].replace(':', '：').replace(' ', '').replace(' ', '').replace('　', '')
                qw = re.sub('审\n判\n(员|长)', '审判员', qw)
                pjjg = data[7]
                wslx = data[5]
                dict_data[data[0]] = [qw, pjjg, wslx]
        return dict_data

    def pjs_pjjg_abstract(self, qw):
        # 特征1：判决主文
        p1 = '判[\n]{0,2}决[\n]{0,2}主[\n]{0,2}文[\n]{0,2}'
        qw = re.sub(p1, '判决主文', qw)

        # 特征2：
        p2 = '裁[\n]{0,2}判[\n]{0,2}主[\n]{0,2}文[\n]{0,2}'
        qw = re.sub(p2, '裁判主文', qw)

        # 特征3：
        p3 = '判[\n]{0,2}(决|定|处)[\n]{0,2}如[\n]{0,2}下[\n]{0,2}|裁[\n]{0,2}定[\n]{0,2}如[\n]{0,2}下[\n]{0,2}|裁[\n]{0,2}判[\n]{0,2}如[\n]{0,2}下[\n]{0,2}'
        qw = re.sub(p3, '判决如下', qw)

        # 特征4：
        p4 = '判[\n]{0,2}决[\n]{0,2}结[\n]{0,2}果[\n]{0,2}'  # 563002158320979126
        qw = re.sub(p4, '判决结果', qw)

        # 特征5：
        p5 = '裁[\n]{0,2}判[\n]{0,2}结[\n]{0,2}果[\n]{0,2}'
        qw = re.sub(p5, '裁判结果', qw)

        # 特征6
        p6 = '判[\n]{0,2}令[\n]{0,2}如[\n]{0,2}下[\n]{0,2}|本[\n]{0,2}院[\n]{0,2}判[\n]{0,2}决[\n]{0,2}'
        qw = re.sub(p6, '裁判结果', qw)

        # 特征7：判决
        p7 = '\n判决\n|[，。；,/\.;]判决：'

        # 特征8：
        p8 = '(参照《|依照《|依据《|根据《).*?：\n|' \
             '(参照《|依照《|依据《|根据《).*[之的]{0,1}规定(，|。|：|,)(\n|一、)|' \
             '(参照《|依照《|依据《|根据《).*[一二三四五六七八九十]条(，|。|：|,|、)(\n|一、)|' \
             '(参照《|依照《|依据《|根据《).*[之的]规定\n|' \
             '(参照《|依照《|依据《|根据《).*[一二三四五六七八九十]条(\n|，|,|、)|' \
             '(参照《|依照《|依据《|根据《).*[之的]{0,1}规定(，|。|：|,|、)|' \
             '之规定(：\n|\n)'

        p9 = '\n判决被告人'

        p10 = '如下协议：'

        # 如果案件不公开：
        if re.search('不.{0,5}公开|不予公开|不予.{0,5}公开|不.{0,5}公布', qw):
            pjjg = '文书内容不公开'

        # 如果满足特征3：
        elif re.search('判决如下', qw):
            arr = [i for i in re.split('判决如下', qw) if i]
            content = arr[-1]
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判长|审判员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()


        # 如果满足特征1：
        elif re.search('判决主文', qw):
            arr = [i for i in re.split('判决主文', qw) if i]
            content = arr[-1]
            if re.search('基本事实|案件基本事实|案\n件\n基\n本\n事\n实|诉\n讼\n请\n求|案件\n基本\n事实|诉讼\n请求', content):
                pjjg = re.search('[\S\s]+?(?=([案件]{0,2}基本事实|案\n件\n基\n本\n事\n实|诉\n讼\n请\n求|案件\n基本\n事实|诉讼\n请求))',
                                 content).group()
                # 此种情况考虑诉讼费被截掉的可能
                if re.search('\n案件受理费|\n诉讼费', content):
                    tail = re.search('(\n案件受理费|\n诉讼费).*?(\n|。)', content).group()
                else:
                    tail = ''
                pjjg = pjjg + tail
            else:
                if re.search('\n审判员|\n审判长', content):
                    pjjg = re.search('[\S\s]+?(?=(审判长|审判员|书记员))', content).group()
                else:
                    pjjg = re.search('[\S\s]+', content).group()

        # 如果满足特征2：
        elif re.search('裁判主文', qw):
            arr = [i for i in re.split('裁判主文', qw) if i]
            content = arr[-1]
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判长|审判员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()

        # 如满足特征7：\n判决\n
        elif re.search(p7, qw):
            arr = re.split(p7, qw)
            content = arr[-1]
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判员|审判长|书记员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()

        # 如果满足特征4：
        elif re.search('判决结果', qw):
            arr = [i for i in re.split('判决结果', qw) if i]
            content = arr[-1]

            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判员|审判长|书记员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()
            pjjg = re.sub('\n判决理由[\S\s]+', '', pjjg)

        # 如果满足特征5：
        elif re.search('裁判结果', qw):
            content = re.search('裁判结果[\S\s]+', qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(?<=裁判结果)[\S\s]+?(?=(审判员|审判长|书记员))', content).group()
            else:
                pjjg = re.search('(?<=裁判结果)[\S\s]+', content).group()

        # 如果满足特征6：判令如下
        elif re.search('判令如下', qw):
            if re.search('\n审判员|\n审判长', qw):
                pjjg = re.search('(?<=判令如下)[\S\s]+?(?=(审判员|审判长|书记员))', qw).group()
            else:
                pjjg = re.search('(?<=判令如下)[\S\s]+', qw).group()


        # 如果满足特征8：根据|依照|依据.*?:
        elif re.search(p8, qw):
            arr = re.split(p8, qw)
            content = arr[-1]
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判员|审判长|书记员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()


        # 如果满足特征9：判决被告人
        elif re.search(p9, qw):
            if re.search('\n审判员|\n审判长', qw):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p9, qw).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p9, qw).group()

        # 如果满足特征10：如下协议
        elif re.search(p10, qw):
            if re.search('\n审判员|\n审判长', qw):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p10, qw).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p10, qw).group()
            pjjg = re.sub(p10, '', pjjg)


        else:

            pjjg = ""

        # 去除开头的冒号
        if pjjg and re.search('^：', pjjg):
            pjjg = re.sub('^：', '', pjjg)

        return pjjg

    '''裁定书pjjg抽取(纯国产)'''

    def cds_pjjg_abstract(self, qw):
        # 特征1：裁定如下
        p1 = '裁[\n]{0,2}定[\n]{0,2}如[\n]{0,2}下[\n]{0,2}|判[\n]{0,2}决[\n]{0,2}如[\n]{0,2}下[\n]{0,2}'
        qw = re.sub(p1, '裁定如下', qw)

        # 特征2：如下裁定
        p2 = '如[\n]{0,2}下[\n]{0,2}裁[\n]{0,2}定[\n]{0,2}'
        qw = re.sub(p2, '如下裁定', qw)

        # 特征3：裁定结果
        p3 = '裁[\n]{0,2}定[\n]{0,2}结[\n]{0,2}果[\n]{0,2}'
        qw = re.sub(p3, '裁定结果', qw)

        # 特征4：裁定事项
        p4 = '裁[\n]{0,2}定[\n]{0,2}事[\n]{0,2}项[\n]{0,2}'  # 563002158320979126
        qw = re.sub(p4, '裁定事项', qw)

        # 特征5：裁定主文
        p5 = '裁[\n]{0,2}(定|判)[\n]{0,2}主[\n]{0,2}文[\n]{0,2}'
        qw = re.sub(p5, '裁定主文', qw)

        # 特征6：调解协议：|如下协议：|协议如下：
        p6 = '调解协议：|如下协议：|协议如下：|补正如下：|变更如下：|予以补正：|更正如下：|裁定：'

        # 特征7：
        p7 = '(参照《|依照《|依据《|根据《).*?：\n|' \
             '(参照《|依照《|依据《|根据《).*[之的]{0,1}规定(，|。|：|,)(\n|一、)|' \
             '(参照《|依照《|依据《|根据《).*[一二三四五六七八九十]条(，|。|：|,|、)(\n|一、)|' \
             '(参照《|依照《|依据《|根据《).*[之的]规定\n|' \
             '(参照《|依照《|依据《|根据《).*[一二三四五六七八九十]{0,1}条(\n|，|,|、)|' \
             '(参照《|依照《|依据《|根据《).*[之的]规定{0,1}(，|。|：|,)|' \
             '之规定(：\n|\n)'

        # 特征8：本院口头裁定
        p8 = '本院口头裁定|本院依法口头裁定|口头裁定'

        # 特征9：裁判结果\n
        p9 = '\n裁判结果\n'

        # 特征10:\n准许撤诉
        p10 = '\n准(许|予).*?(撤回上诉|撤回起诉|撤诉)'

        # 特征11:按.*?处理
        p11 = '\n本案按.*?处理'

        # 特征12:本案终止|中止
        p12 = '\n本案(终止|中止|中结束)'

        # 特征13：综上所述
        p13 = '\n综上所述，|\n综上，'

        # 特征14；
        p14 = '裁定补正如下:\n'

        # 特征16:笔误类单独处理
        p16 = "改为“|应改为“|更正为“|补正为“|应为“|变更为“"

        # 特征17:转为普通或者简易程序
        p17 = "(转为.{0,1}|转入|适用|按照)(普通程序|简易程序)"

        # 特征18:撤诉
        p18 = "撤诉申请|撤诉处理|撤诉.*?符合.*?准许|撤诉"

        # 特征19:保全
        p19 = "准予保全|不予保全"

        # 如果案件不公开：
        if re.search('不.{0,5}公开|不予公开|不予.{0,5}公开|不.{0,5}公布', qw):
            pjjg = '文书内容不公开'

        # 如果满足特征1和2：裁定如下|如下裁定
        elif re.search('裁定如下|如下裁定', qw):
            arr = re.split('裁定如下|如下裁定', qw)
            content = arr[-1]
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判长|审判员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()

        # 如果满足特征3：裁定结果
        elif re.search('裁定结果', qw):
            content = re.search('裁定结果[\S\s]+', qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判长|审判员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()


        # 如果满足特征4：裁定事项
        elif re.search('裁定事项', qw):
            content = re.search('裁定事项[\S\s]+', qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(?<=裁定事项)[\S\s]+?(?=(审判员|审判长|书记员))', content).group()
            else:
                pjjg = re.search('(?<=裁定事项)[\S\s]+', content).group()

        # 如果满足特征5：裁定主文
        elif re.search('裁定主文', qw):
            content = re.search('裁定主文[\S\s]+', qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(?<=裁定主文)[\S\s]+?(?=(审判员|审判长|书记员))', content).group()
            else:
                pjjg = re.search('(?<=裁定主文)[\S\s]+', content).group()

        # 如果满足特征5：调解协议：|如下协议：|协议如下
        elif re.search(p6, qw):
            arr = re.split(p6, qw)
            content = arr[-1]
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判员|审判长|书记员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()


        # 特征8：本院口头裁定
        elif re.search(p8, qw):
            content = re.search('(%s)[\S\s]+' % p8, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p8, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p8, content).group()

        # 特征9：裁判结果
        elif re.search(p9, qw):
            content = re.search('(%s)[\S\s]+' % p9, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p9, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p9, content).group()
            pjjg = re.sub(p9, '', pjjg)

        # 特征10:
        elif re.search(p10, qw):
            content = re.search('(%s)[\S\s]+' % p10, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p10, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p10, content).group()

        # 特征11:
        elif re.search(p11, qw):
            content = re.search('(%s)[\S\s]+' % p11, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p11, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p11, content).group()

        # 特征12:
        elif re.search(p12, qw):
            content = re.search('(%s)[\S\s]+' % p12, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p12, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p12, content).group()

        # 特征13：综上所述
        elif re.search(p13, qw):
            content = re.search('(%s)[\S\s]+' % p13, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p13, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+?(。|\n)' % p13, content).group()

        # 特征13：裁定补正如下:\n
        elif re.search(p14, qw):
            content = re.search('(%s)[\S\s]+' % p14, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p14, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+?(。|\n)' % p14, content).group()
            pjjg = re.sub(p14, '', pjjg)

        # 如果满足特征7：根据|依照|依据.*?:
        elif re.search(p7, qw):
            arr = re.split(p7, qw)
            content = arr[-1]
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('[\S\s]+?(?=(审判员|审判长|书记员))', content).group()
            else:
                pjjg = re.search('[\S\s]+', content).group()

        # 特征16:如果是笔误补正
        elif re.search(p16, qw):
            segments = re.split('。', qw)
            for seg in segments:
                if re.search(p16, seg):
                    pjjg = seg
                    break

        # 特征17:转普通或者简易程序
        elif re.search(p17, qw):
            segments = re.split('。', qw)
            for seg in segments:
                if re.search(p17, seg):
                    pjjg = seg
                    break

        # 特征18:撤诉处理
        elif re.search(p18, qw):
            segments = re.split('。', qw)
            for seg in segments:
                if re.search(p18, seg):
                    pjjg = seg
                    break


        # 特征19:保全
        elif re.search(p19, qw):
            segments = re.split('。', qw)
            for seg in segments:
                if re.search(p19, seg):
                    pjjg = seg
                    break

        # 否则
        else:
            pjjg = ""

        # 去除开头的冒号
        if pjjg and re.search('^：', pjjg):
            pjjg = re.sub('^：', '', pjjg)
        return pjjg

    '''调解书pjjg提取(国产+进口)'''

    def tjs_pjjg_abstract(self, qw):
        # 如果案件不公开：
        if re.search('不.{0,5}公开|不予公开|不予.{0,5}公开|不.{0,5}公布|不上网原因', qw):
            pjjg = '文书内容不公开'
        else:
            pjjg = "当事人自愿达成调解"
        return pjjg

    '''决定书pjjg提取(纯国产)'''

    def jds_pjjg_abstract(self, qw):

        # 特征1：决定如下
        p1 = '决[\n]{0,2}定[\n]{0,2}如[\n]{0,2}下[\n]{0,2}'

        # 特征2：决定：|本院决定：
        p2 = '决定：\n'

        # 特征3：裁定如下
        p3 = '裁[\n]{0,2}定[\n]{0,2}如[\n]{0,2}下[\n]{0,2}'

        # 特征4：
        p4 = '如下协议：\n|协议如下：\n'

        # 特征5：(依照《|依据《|根据《).*规定，决定
        p5 = '(依照《|依据《|根据《).*规定，'

        # 特征6：本院决定
        p6 = '本[\n]{0,2}院[\n]{0,2}决[\n]{0,2}定'

        # 特征7：决定
        p7 = '决定.*?。'

        # 如果案件不公开：
        if re.search('不.{0,5}公开|不予公开|不予.{0,5}公开|不.{0,5}公布|不上网原因', qw):
            pjjg = '文书内容不公开'

        # 特征1：决定如下
        elif re.search(p1, qw):
            content = re.search('(%s)[\S\s]+' % p1, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p1, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p1, content).group()
            pjjg = re.sub(p1, '', pjjg)

        # 特征2：决定：|本院决定：
        elif re.search(p2, qw):
            content = re.search('(%s)[\S\s]+' % p2, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p2, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p2, content).group()
            pjjg = re.sub(p2, '', pjjg)

        # 特征3：裁定如下
        elif re.search(p3, qw):
            content = re.search('(%s)[\S\s]+' % p3, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p3, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p3, content).group()
            pjjg = re.sub(p3, '', pjjg)

        # 特征4：如下协议|协议如下
        elif re.search(p4, qw):
            content = re.search('(%s)[\S\s]+' % p4, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p4, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p4, content).group()
            pjjg = re.sub(p4, '', pjjg)

        # 特征5：(依照《|依据《|根据《).*规定，
        elif re.search(p5, qw):
            content = re.search('(%s)[\S\s]+' % p5, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p5, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+?(。|\n)' % p5, content).group()
            pjjg = '决定' + re.sub(p5, '', pjjg)

        # 特征6：本院决定
        elif re.search(p6, qw):
            content = re.search('(%s)[\S\s]+' % p6, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p6, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p6, content).group()
            pjjg = re.sub(p6, '', pjjg)

        # 特征7：决定
        elif re.search(p7, qw):
            content = re.search('(%s)[\S\s]+' % p7, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p7, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p7, content).group()


        # 否则
        else:
            pjjg = ""

        # 去除开头的冒号和决定书结尾的二〇一九年七月十日
        if pjjg:
            pjjg = re.sub('^：', '', pjjg)
            pjjg = re.sub('\n.{0,4}年.{0,3}月.{0,3}日[\S\s]*', '', pjjg)
            pjjg = re.sub('\n(书记员|执行员)[\S\s]+', '', pjjg)
            pjjg = re.sub('\n.*法院$', '', pjjg)
            pjjg = re.sub('\n附[\S\s]+', '', pjjg)

        return pjjg

    '''通知书pjjg抽取（纯国产）'''

    def tzs_pjjg_abstract(self, qw):

        # 特征1：通知如下
        p1 = '通知如下：|如下通知：|告知你们：|告知如下：|通知你如下：|裁定如下：|判决如下：'

        # 特征2：综上
        p2 = '\n综上，.*?(。|\n)'

        # 特征3：特此通知
        p3 = '特此通知|特此告知'

        # 特征4：根据.*？规定,
        p4 = '(依照.*?《|依据.*?《|根据.*?《).*规定，'

        # 特征5:综上 综上所述
        p5 = '(综上，|综上所述，|\n本院决定)'

        # 如果案件不公开：
        if re.search('不.{0,5}公开|不予公开|不予.{0,5}公开|不.{0,5}公布|不上网原因', qw):
            pjjg = '文书内容不公开'

        # 特征1：通知如下
        elif re.search(p1, qw):
            content = re.search('(%s)[\S\s]+' % p1, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p1, content).group()
            else:
                pjjg = re.search('(%s)[\S\s]+' % p1, content).group()
            pjjg = re.sub(p1, '', pjjg)

        # 特征2：综上
        elif re.search(p2, qw):

            content = re.search(p2, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('(%s)[\S\s]+?(?=(审判员|审判长|书记员))' % p2, content).group()
            else:
                pjjg = re.search(p2, content).group()

        # 特征3：特此通知
        elif re.search(p3, qw):
            content = re.search('^[\S\s]+?(?=%s)' % p3, qw).group()
            content_arr = [i for i in re.split('\n|。', content) if i]
            pjjg = content_arr[-1]

        # 特征4：根据.*规定
        elif re.search(p4, qw):
            content = re.search('(%s)[\S\s]+' % p4, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('%s[\S\s]+?(?=(审判员|审判长|书记员))' % p4, content).group()
            else:

                pjjg = re.search('%s[\S\s]+' % p4, content).group()
            pjjg = '决定' + re.sub(p4, '', pjjg)

        # 特征5:综上所述
        elif re.search(p5, qw):
            content = re.search('(%s)[\S\s]+' % p5, qw).group()
            if re.search('\n审判员|\n审判长', content):
                pjjg = re.search('%s[\S\s]+?(?=(审判员|审判长|书记员))' % p5, content).group()
            else:

                pjjg = re.search('%s[\S\s]+' % p5, content).group()



        # 否则
        else:
            pjjg = ""

        # 去除开头的冒号和决定书结尾的二〇一九年七月十日
        if pjjg:
            pjjg = re.sub('^：', '', pjjg)
            pjjg = re.sub('\n.{0,4}年.{0,3}月.{0,3}日[\S\s]*', '', pjjg)
            pjjg = re.sub('\n(书记员|执行员)[\S\s]+', '', pjjg)
            pjjg = re.sub('\n.*法院$', '', pjjg)
            pjjg = re.sub('\n附[\S\s]+', '', pjjg)

        return pjjg

    def abstract_pjjg(self, dict_data):  # qw,pjjg,wslx
        pjjg = ""
        dict_pjjg = {}
        for k, v in dict_data.items():

            # 如果是判决书
            if v[2] == 1:
                pjjg = self.pjs_pjjg_abstract(v[0])
                if re.search('\n本院查明|\n本院认为', pjjg):
                    pjjg = self.pjs_pjjg_abstract(pjjg)



            # 如果是裁定书
            elif v[2] == 2:
                pjjg = self.cds_pjjg_abstract(v[0])
                if re.search('\n本院查明|\n综上，|\n综上所述，', pjjg):
                    pjjg = self.cds_pjjg_abstract(pjjg)



            # 如果是调解书
            elif v[2] == 3:
                if v[1]:
                    pjjg = v[1]
                else:
                    pjjg = self.tjs_pjjg_abstract(v[0])
                    if re.search('\n本院查明|\n本院认为|\n综上，|\n综上所述，', pjjg):
                        pjjg = self.tjs_pjjg_abstract(pjjg)


            # 如果是决定书
            elif v[2] == 4:
                pjjg = self.jds_pjjg_abstract(v[0])
                if re.search('\n本院查明|\n本院认为|\n综上，|\n综上所述，', pjjg):
                    pjjg = self.jds_pjjg_abstract(pjjg)


            # 如果是通知书
            elif v[2] == 5:
                pjjg = self.tzs_pjjg_abstract(v[0])
                if re.search('\n本院查明|\n本院认为|\n综上，|\n综上所述，', pjjg):
                    pjjg = self.tzs_pjjg_abstract(pjjg)


            # 如果是支付令
            elif v[2] == 6:
                if v[1]:
                    pjjg = v[1]

            # 如果是其他
            elif v[2] == 7:
                if v[1]:
                    pjjg = v[1]
            # 否则
            else:
                pjjg = v[1]

            dict_pjjg[k] = pjjg

        return dict_pjjg

    def run(self, dict_data):
        dict_pjjg = self.abstract_pjjg(dict_data)
        return dict_pjjg