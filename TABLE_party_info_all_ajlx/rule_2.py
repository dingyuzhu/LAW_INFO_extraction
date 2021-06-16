# -*- coding:utf-8 -*-

'''刑事案件'''
# 暗示原告
yg_title = ['自诉人']

# 暗示被告
bg_title = ['被告人', '嫌疑人', '上诉人', '罪犯', '被罚款人', '被拘留人','被申请人']

#只有原告
yg_rule = ['自诉人[\\S\\s]+','原告人[\\S\\s]+']


#只有被告
bg_rule = [ '罪犯[\\S\\s]+','上诉人[\\S\\s]+','被告人[\\S\\s]+', '嫌疑人[\\S\\s]+','被申请人[\\S\\s]+']


#原被告都有
yg_bg_rule = ['自诉人[\\S\\s]+?(?=被告人)','自诉人[\\S\\s]+?(?=上诉人)']



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