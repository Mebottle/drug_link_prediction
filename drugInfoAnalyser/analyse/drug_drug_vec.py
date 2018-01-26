import matlab.engine
import pymysql as mdb
import scipy.io as scio
import time

#eng = matlab.engine.start_matlab()
# mat = np.fromfile("matrix", dtype=np.int32)
# mat.shape = (811, 811)
# mat = [[1,0,0],[0,1,0],[0,0,1]]
# scio.savemat("testmat.mat",{'A':mat})
# mat = scio.loadmat("testmat.mat")
# mat = eng.sparse(mat['A'])
# print("sparse:")
# print(mat)
# mat = eng.spones(mat)
# print("spones:")
# print(mat)

conn = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='drugbank', charset='utf8')

conn.autocommit(1)
conn.ping(True)
cursor = conn.cursor()

try:
    start = time.clock()
    sqin = "insert into drug_link_feature_0122_k10 values(%s,%s,%s,%s)"
    info_data = []
    data1 = (scio.loadmat("data/drug_link_event.mat"))['drug_matrix']
    data2 = (scio.loadmat("data/drug_link_features.mat"))['drug_link_vec']
    coo = data1.tocoo()
    for i in range(len(data2)):
        if i % 5000 == 0:
            print("process %d: %fs" % (i, time.clock() - start))
        str_l = [str(s) for s in data2[i]]
        del str_l[0]
        feature = " ".join(str_l)
        info_i = [str(coo.row[i]), str(coo.col[i]), feature, str(coo.data[i])]
        info_data.append(info_i)
    cursor.executemany(sqin, info_data)
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
