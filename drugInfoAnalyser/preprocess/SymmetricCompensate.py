import numpy as np
import pymysql as mdb

from preprocess import pick_data

data_matrix = np.loadtxt('NotSymmetric.txt', dtype=np.str, delimiter=",")

conn = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='drugbank', charset='utf8')
conn.autocommit(1)
conn.ping(True)
cursor = conn.cursor()

try:
    for data in data_matrix:
        cursor.execute('SELECT * FROM drug_interaction_info where drug_a_id = \'%s\' and drug_b_id = \'%s\''
                       % (data[0], data[1]))
        result = cursor.fetchall()
        for index in range(len(result)):
            if pick_data.judge(result[index][4]):
                cursor.execute("insert into drug_info values(null,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" %
                               (result[index][2], result[index][3], result[index][0], result[index][1],
                                result[index][4].replace("drugB","drugC").replace("drugA", "drugB").replace("drugC", "drugA")))




except:
    import traceback
    traceback.print_exc()
    # 发生错误时会滚
    conn.rollback()
finally:
    # 关闭游标连接
    cursor.close()
    # 关闭数据库连接
    conn.close()
