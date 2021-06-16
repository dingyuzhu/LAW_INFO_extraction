
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
    "tb_wenshu": "tb_wenshu_201907",
    "tb_wenshu_check": "tb_wenshu_201907_check"
}

Output_table = {
    "tb_wenshu_paragraph":"tb_wenshu_201907_paragraph"
}

# ====================================入口sql配置===========================================
Input_sql = {
    "sql1": 'SELECT a.id, a.qw, a.wb ' \
            'FROM '
            '%s a left join '
            '%s b on a.id=b.wenshu_id ' \
            'where a.cprq="{}" '% (Input_table["tb_wenshu"],Input_table["tb_wenshu_check"]),
}


# ====================================生产与测试切换===========================================
swither = "test"






