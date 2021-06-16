
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
    "tb_wenshu_paragraph": "tb_wenshu_201907_paragraph",
    "tb_wenshu_check_pjjg_detail_fee_pct": "tb_wenshu_check_pjjg_detail_fee_pct_201907_0507",
    "tb_wenshu_check": "tb_wenshu_201907_check",

}

Output_table = {
    "tb_wenshu_pjjg_result":"tb_wenshu_201907_pjjg_result"
}

# ====================================入口sql配置===========================================
Input_sql = {
    "sql1":'select a.id,b.ajlx, b.wslx, b.spcx_id,c.yg_pct, c.bg_pct, c.pjjg_cost_bear,a.pjjg,a.party_info ' 
               'from '
               '%s a '
               'left join ' 
               '%s b '
               'on a.id = b.wenshu_id '
               'left join ' 
               '%s c '
               'on a.id=c.wenshu_id '
               'left join '
               '%s d '
               'on a.id = d.id '
               'where d.cprq="{}" '% (Input_table["tb_wenshu_paragraph"],Input_table["tb_wenshu_check"],Input_table["tb_wenshu_check_pjjg_detail_fee_pct"],Input_table["tb_wenshu"]),

    "sql2": 'SELECT a.id,a.pjjg,b.ajlx,b.wslx,b.spcx_id,a.sb,a.ssqq, c.pjjg as orin_pjjg ' 
            'FROM %s a '
            'LEFT JOIN '
            '%s b '
            'ON a.id=b.wenshu_id ' 
            'LEFT JOIN '
            '%s c '
            'ON a.id = c.id ' 
            'WHERE c.cprq="{}" '%(Input_table["tb_wenshu_paragraph"],Input_table["tb_wenshu_check"],Input_table["tb_wenshu"]),

    "sql3": 'SELECT a.id, c.ajmc, a.pjjg, b.wslx, c.pjjg as orin_pjjg ' 
            'FROM %s a '
            'left join ' 
            '%s b '
            'on a.id=b.wenshu_id '
            'left join ' 
            '%s c '
            'on a.id=c.id ' 
            'where b.spcx_id=30300000000000000 and b.ajlx=3 and a.pjjg is not null and c.cprq="{}" '%(Input_table["tb_wenshu_paragraph"],Input_table["tb_wenshu_check"],Input_table["tb_wenshu"])
}


# ====================================生产与测试切换===========================================
swither = "test"






