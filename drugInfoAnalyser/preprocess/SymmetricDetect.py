import pymysql as mdb
import time


def check(cursor, conn):
    try:
        start = time.clock()
        hash_map = {}
        cursor.execute('SELECT * FROM drug_info_20180120')
        results = cursor.fetchall()

        for ind in range(len(results)):
            if ind % 5000 == 0:
                print("process hash %d : %fs" % (ind, time.clock() - start))
            hash_map["%s%s" % (results[ind][1], results[ind][3])] = results[ind][0]

        for ind in range(len(results)):
            if ind % 5000 == 0:
                print("process check %d : %fs" % (ind, time.clock() - start))
            if not ("%s%s" % (results[ind][3], results[ind][1]) in hash_map.keys()):
                print("%s %s %s %s %s" % (results[ind][1], results[ind][2],
                                        results[ind][3], results[ind][4], results[ind][5]))
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


def check2(cursor, conn):
    try:
        id_tuple = []
        start = time.clock()
        hashmap = {}
        cursor.execute('SELECT * FROM drug_info_20180120')
        results = cursor.fetchall()

        for ind in range(len(results)):
            if ind % 5000 == 0:
                print("process hash %d : %fs" % (ind, time.clock() - start))
            if "%s%s" % (results[ind][1], results[ind][3]) in hashmap.keys():
                tuple_i = [results[ind][1], results[ind][3]]
                id_tuple.append(tuple_i)
            hashmap["%s%s" % (results[ind][1], results[ind][3])] = results[ind][0]

        print(id_tuple)

        for ind in range(len(results)):
            if ind % 5000 == 0:
                print("process check %d : %fs" % (ind, time.clock() - start))
            if not ("%s%s" % (results[ind][3], results[ind][1]) in hashmap.keys()):
                print("%s %s %s %s %s" % (results[ind][1], results[ind][2],
                                        results[ind][3], results[ind][4], results[ind][5]))

        new_hashmap = {}
        for ind in range(len(id_tuple)):
            if "%s%s" % (id_tuple[ind][0], id_tuple[ind][1]) in new_hashmap.keys():
                print(id_tuple[ind])
            new_hashmap["%s%s" % (id_tuple[ind][0], id_tuple[ind][1])] = 1

        for ind in range(len(id_tuple)):
            if not ("%s%s" % (id_tuple[ind][1], id_tuple[ind][0]) in hashmap.keys()):
                print("%s %s" % (id_tuple[ind][0], id_tuple[ind][1]))

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


def check3(cursor, conn):
    try:
        cursor.execute('SELECT * FROM drug_info_201801 where drug_a_id=\'DB00541\'') #253
        results1 = cursor.fetchall()
        cursor.execute('SELECT * FROM drug_info_201801 where drug_b_id=\'DB00541\'') #248
        results2 = cursor.fetchall()

        print(results1)
        print(results2)
        for r1 in results1:
            flag = False
            for r2 in results2:
                if r2[3] == r1[1] and r2[1] == r1[3]:
                    flag = True
            if not flag:
                print(r1)

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


def check4(cursor, conn):
    try:
        drug_list = []
        d_file = open('811', 'rb')
        data = d_file.read()
        l = eval(data)
        num = 0
        for drug in l:
            cursor.execute('SELECT COUNT(*) FROM drug_info_201801 where drug_a_id=\'%s\' or drug_b_id=\'%s\'' % (drug, drug))
            count = cursor.fetchall()
            if count[0][0] % 2 == 1:
                drug_list.append([drug, count[0][0]])
            num += 1
            print(num)
        print(drug_list)

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

conn_ = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='drugbank', charset='utf8')

conn_.autocommit(1)
conn_.ping(True)
cursor_ = conn_.cursor()
check2(cursor_, conn_)
