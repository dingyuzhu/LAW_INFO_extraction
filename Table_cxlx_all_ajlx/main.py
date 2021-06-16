

import time
import cxlx
import common_


if __name__ == "__main__":
    # 开始时间
    start = time.time()

    days = common_.day_range('1998/01/01', '2021/03/01',1)

    for i in range(len(days)):
        t1 = time.time()

        #
        sql = 'select a.id, b.party_info, a.ssjl, b.ss_ssqq,c.spcx_id ' \
              'from tb_wenshu a left join tb_wenshu_paragraph b on a.id = b.id left join tb_wenshu_check c on a.id=c.wenshu_id ' \
              'where a.cprq="{}"'.format(str(days[i])[:10])

        # 单测
        sql1 = 'select a.id, b.party_info, a.ssjl, b.ss_ssqq,c.spcx_id ' \
              'from tb_wenshu a left join tb_wenshu_paragraph b on a.id = b.id left join tb_wenshu_check c on a.id=c.wenshu_id ' \
              'where a.id = 123456789'

        all_data = common_.db_connection(common_.db_connection_prod, sql)
        e1 = time.time()

        print('今天是：', str(days[i])[:10], '，是时间轴中的第', str(i), '天，还剩下', str(len(days) - i), '天')
        print('SQL执行时间：', e1 -t1)

        t2 = time.time()
        a = cxlx.CXLX_CLASSIFICATION()
        df = a.run(all_data)

        e2 = time.time()
        print('数据处理时间：', e2 - t2)

        t3 = time.time()
        common_.df_to_sql(df)
        e3 = time.time()
        print('数据入库时间：', e3 - t3)





    # 结束时间
    end = time.time( ) -start
    print(end)