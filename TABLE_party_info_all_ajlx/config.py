
import pymysql

# ====================================数据库配置===========================================
# 正式数据库连接信息
Prod_db_connect_info= pymysql.connect(host="120.78.145.144", user="root", passwd="dfkj2020", use_unicode=True,
                           db="db_extract_increment0",
                           port=3306, charset="utf8")
# 测试数据库连接信息
Test_db_connect_info = pymysql.connect(host="120.78.92.6", user="root", passwd="dfkj2020", use_unicode=True,
                           db="db_extract_increment0",
                           port=3306, charset="utf8")


# ====================================入口表配置===========================================


Input_table={
    "tb_wenshu":"tb_wenshu",
    "tb_wenshu_check": "tb_wenshu_check",
    "tb_wenshu_paragraph":"tb_wenshu_paragraph"
}

Output_table = {
    "tb_wenshu_party_info":"tb_wenshu_party_info"
}

# ====================================入口sql配置===========================================
Input_sql = {
    "sql1":   'select a.id,a.party_info,b.ajlx ' 
              'from '
              '%s a '
              'left join '
              '%s b '
              'on a.id = b.wenshu_id left join '
              '%s c '
              'on a.id = c.id ' 
              'where c.cprq="{}"'% (Input_table["tb_wenshu_paragraph"],Input_table["tb_wenshu_check"],Input_table["tb_wenshu"]),
}


# ====================================生产与测试切换===========================================
swither = "prod"






