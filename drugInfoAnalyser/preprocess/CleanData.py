import time

import pymysql as mdb

conn = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='drugbank', charset='utf8')

conn.autocommit(1)
conn.ping(True)
cursor = conn.cursor()

# d_file = open('811', 'rb')
# data = d_file.read()
# l = eval(data)

# drug clean
# try:
#     sqli = "insert into drug_interaction_info values(%s,%s,%s,%s,%s)"
#     info_data = []
#     cursor.execute('SELECT DISTINCT * FROM drug_interaction')
#     results = cursor.fetchall()
#     for r in results:
#         if r[0] in l and r[2] in l:
#             info_data.append(r)
#     cursor.executemany(sqli, info_data)

# valid interaction clean
# try:
#     s = time.clock()
#     sqli = "select drug_a_id,drug_a_name,drug_b_id,drug_b_name,interaction from drug_info_201801"
#     sqin = "insert into drug_info_20180120 values(null,%s,%s,%s,%s,%s)"
#     info_data = []
#     cursor.execute(sqli)
#     result = cursor.fetchall()
#     for index in range(len(result)):
#         if index % 5000 == 0:
#             print("process %d: %fs" % (index, time.clock() - s))
#         if pick_data.judge(result[index][4]):
#             info_data.append(result[index])
#     cursor.executemany(sqin, info_data)

# eliminate duplicate
try:
    start = time.clock()
    sqli = "select drug_a_id,drug_a_name,drug_b_id,drug_b_name,interaction from drug_info_20180120"
    sqin = "insert into drug_info_20180120_2 values(null,%s,%s,%s,%s,%s)"
    info_data = []
    cursor.execute(sqli)
    results = cursor.fetchall()

    hash_map = {}
    for ind in range(len(results)):
        if ind % 5000 == 0:
            print("process %d : %fs" % (ind, time.clock() - start))
        if not "%s%s" % (results[ind][2], results[ind][0]) in hash_map.keys():
            hash_map["%s%s" % (results[ind][0], results[ind][2])] = 1
            info_data.append(results[ind])

    cursor.executemany(sqin, info_data)

# introduce data
# try:
#     df = pd.read_csv("ffinal.csv")
#     print(len(df))
#     sql = "insert into drug_info_201801 values(null,%s,%s,%s,%s,%s)"
#     info_data = []
#     for i in range(len(df)):
#         info_data.append([str(df.loc[i]["drug_a_id"]), str(df.loc[i]["drug_a_name"]),
#                           str(df.loc[i]["drug_b_id"]), str(df.loc[i]["drug_b_name"]),
#                           str(df.loc[i]["interaction"])])
#     cursor.executemany(sql, info_data)

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
