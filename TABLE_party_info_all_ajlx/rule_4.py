# -*- coding:utf-8 -*-

#暗示原告、被告、第三人的标志
yg_title = ['起诉人','原告', '反诉人', '上诉人', '处罚人', '询问人', '解除保全申请人', '解除保全申请人','申请解除人', '执行人', '罚款人', '申请人', '申诉人', '申告人', '再审申请人', '保全人', '拘留人', '申请执行人', '上诉人','原审原告']
bg_title = ['被起诉人','被告', '被反诉人', '被诉人', '被处罚人', '被询问人', '被解除保全申请人', '被申请人','被申请解除人', '被执行人', '被罚款人', '被申请人', '被申诉人', '被申告人', '再被审申请人', '被保全人', '被拘留人', '被申请执行人', '被上诉人','原审被告']
dsr_title = ['第三人']

#原告、被告同时存在时原告的正则
yg_pattern_1 = ['原审原告[\\S\\s]+?(?=\n.*?原审被告)', '上诉人[\\S\\s]+?(?=\n.*?被上诉人)','反诉人[\\S\\s]+?(?=\n被反诉人)', '上诉人[\\S\\s]+?(?=\n被诉人)', '处罚人[\\S\\s]+?(?=\n被处罚人)', '原告[\\S\\s]+?(?=\n被告)', '询问人[\\S\\s]+?(?=\n被询问人)', '解除保全申请人[\\S\\s]+?(?=\n被申请人)','解除保全申请人[\\S\\s]+?(?=\n被解除保全申请人)', '申请解除人[\\S\\s]+?(?=\n被申请解除人)', '执行人[\\S\\s]+?(?=\n被执行人)', '罚款人[\\S\\s]+?(?=\n被罚款人)', '申请人[\\S\\s]+?(?=\n被申请人)', '申诉人[\\S\\s]+?(?=\n被申诉人)', '申告人[\\S\\s]+?(?=\n被申告人)', '再审申请人[\\S\\s]+?(?=\n[再审]{0,2}被申请人)', '起诉人[\\S\\s]+?(?=\n被起诉人)', '保全人[\\S\\s]+?(?=\n被保全人)', '拘留人[\\S\\s]+?(?=\n被拘留人)', '申请执行人[\\S\\s]+?(?=\n被申请执行人)']


#只存在原告时原告的正则
yg_pattern_2 = ['原审原告[\\S\\s]+','反诉人[\\S\\s]+', '上诉人[\\S\\s]+', '处罚人[\\S\\s]+', '原告[\\S\\s]+', '询问人[\\S\\s]+', '解除保全申请人[\\S\\s]+', '申请解除人[\\S\\s]+?', '执行人[\\S\\s]+', '罚款人[\\S\\s]+', '申请人[\\S\\s]+', '申诉人[\\S\\s]+', '申告人[\\S\\s]+', '^再审申请人[\\S\\s]+', '起诉人[\\S\\s]+', '^保全人[\\S\\s]+', '拘留人[\\S\\s]+', '申请执行人[\\S\\s]+', '上诉人[\\S\\s]+']


#被告第三人同时存在时，被告的正则
bg_pattern_1 = ['原审被告[\\S\\s]+?(?=\n.*?第三人)','被反诉人[\\S\\s]+?(?=\n.*?第三人)', '被诉人[\\S\\s]+?(?=\n.*?第三人)', '被处罚人[\\S\\s]+?(?=\n.*?第三人)', '被告[\\S\\s]+?(?=\n.*?第三人)', '被询问人[\\S\\s]+?(?=\n.*?第三人)', '被解除保全申请人[\\S\\s]+?(?=\n.*?第三人)', '被申请解除人[\\S\\s]+?(?=\n.*?第三人)', '被执行人[\\S\\s]+?(?=\n.*?第三人)', '被罚款人[\\S\\s]+?(?=\n.*?第三人)', '被申请人[\\S\\s]+?(?=\n.*?第三人)', '被申诉人[\\S\\s]+?(?=\n.*?第三人)', '被申告人[\\S\\s]+?(?=\n.*?第三人)', '再审被申请人[\\S\\s]+?(?=\n.*?第三人)', '被起诉人[\\S\\s]+?(?=\n.*?第三人)', '被保全人[\\S\\s]+?(?=\n.*?第三人)', '被拘留人[\\S\\s]+?(?=\n.*?第三人)', '被申请执行人[\\S\\s]+?(?=\n.*?第三人)', '被上诉人[\\S\\s]+?(?=\n.*?第三人)']

#不存在第三人时，被告的正则
bg_pattern_2 = ['原审被告[\\S\\s]+','被反诉人[\\S\\s]+', '被诉人[\\S\\s]+', '被处罚人[\\S\\s]+', '被告[\\S\\s]+', '被询问人[\\S\\s]+', '被解除保全申请人[\\S\\s]+', '被申请解除人[\\S\\s]+', '被执行人[\\S\\s]+', '被罚款人[\\S\\s]+', '被申请人[\\S\\s]+', '被申诉人[\\S\\s]+', '被申告人[\\S\\s]+', '再审被申请人[\\S\\s]+', '被起诉人[\\S\\s]+', '被保全人[\\S\\s]+', '被拘留人[\\S\\s]+', '被申请执行人[\\S\\s]+', '被上诉人[\\S\\s]+']

#第三人的正则
dsr_pattern = ['\n.*?第三人[\S\s]+']



#插入、更新语句
sql_person_party_info_insert = 'insert into `tb_wenshu_one_month_party_info_test_2` ' \
                  '(yg_name,yg_address,yg_cognitor,yg_cognitor_address,yg_representive,bg_name,bg_address,bg_cognitor,bg_cognitor_address,bg_representive,_3rd_name,_3rd_address,_3rd_cognitor,_3rd_cognitor_address,_3rd_representive,id,wenshu_id) ' \
                  'values ' \
                  '("{yg_name}","{yg_address}","{yg_cognitor}","{yg_cognitor_address}","{yg_representive}","{bg_name}","{bg_address}","{bg_cognitor}","{bg_cognitor_address}","{bg_representive}","{_3rd_name}","{_3rd_address}","{_3rd_cognitor}","{_3rd_cognitor_address}","{_3rd_representive}",{id},{wenshu_id})' \


sql_person_party_info_update = 'update tb_wenshu_one_month_party_info_test_3 set yg_name="{yg_name}",yg_address="{yg_address}",yg_cognitor="{yg_cognitor}",yg_cognitor_address="{yg_cognitor_address}",yg_representive="{yg_representive}",' \
                               'bg_name="{bg_name}",bg_address = "{bg_address}",bg_cognitor= "{bg_cognitor}",bg_cognitor_address= "{bg_cognitor_address}",bg_representive="{bg_representive}",' \
                               '_3rd_name="{_3rd_name}",_3rd_address="{_3rd_address}",_3rd_cognitor="{_3rd_cognitor}",_3rd_cognitor_address = "{_3rd_cognitor_address}",_3rd_representive="{_3rd_representive}" where id = {id}'



# for i in range(len(bg_title)):
#     p = '{}[\S\s]+'.format(bg_title[i])
#     bg_pattern_2.append(p)
#
# print(bg_pattern_2)