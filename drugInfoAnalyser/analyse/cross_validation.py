import pymysql as mdb
import pandas as pd


def get_data_set():
    conn = mdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='drugbank', charset='utf8')
    conn.autocommit(1)
    conn.ping(True)
    cursor = conn.cursor()

    # 22831
    sql_1 = "select link_feature,event " \
            "from drug_link_feature_0122_k10 " \
            "where event=\'1.0\'"
    cursor.execute(sql_1)
    re_1 = cursor.fetchall()
    # 16654
    sql_2 = "select link_feature,event " \
            "from drug_link_feature_0122_k10 " \
            "where event=\'2.0\'"
    cursor.execute(sql_2)
    re_2 = cursor.fetchall()
    # 25177
    sql_3 = "select link_feature,event " \
            "from drug_link_feature_0122_k10 " \
            "where event=\'3.0\'"
    cursor.execute(sql_3)
    re_3 = cursor.fetchall()
    # 15948
    sql_4 = "select link_feature,event " \
            "from drug_link_feature_0122_k10 " \
            "where event=\'4.0\'"
    cursor.execute(sql_4)
    re_4 = cursor.fetchall()
    # 2249
    sql_5 = "select link_feature,event " \
            "from drug_link_feature_0122_k10 " \
            "where event=\'5.0\'"
    cursor.execute(sql_5)
    re_5 = cursor.fetchall()

    res = [re_1, re_2, re_3, re_4, re_5]
    times = [2283, 1665, 2517, 1594, 224]
    dataset = [[], [], [], [], [], [], [], [], [], []]
    labelset = [[], [], [], [], [], [], [], [], [], []]
    for a in range(5):
        j = 0
        for i in range(10):
            set_i = []
            label_i = []
            if i == 9:
                for j in range(j, len(res[a])):
                    s = res[a][j][0].split(" ")
                    set_i.append([float(n) for n in s])
                    label_i.append(int(float(res[a][j][1])))
            else:
                for k in range(times[a]):
                    s = res[a][j][0].split(" ")
                    set_i.append([float(n) for n in s])
                    e = int(float(res[a][j][1]))
                    label_i.append(e)
                    j += 1
            dataset[i].extend(set_i)
            labelset[i].extend(label_i)

    return dataset, labelset


if __name__ == '__main__':
    datasets, labelsets = get_data_set()
    for i in range(10):
        data_test = [" ".join([str(s) for s in vec]) for vec in datasets[i]]
        label_test = labelsets[i]
        df_test = pd.DataFrame({'feature': data_test, 'tag': label_test})

        data_train = []
        label_train = []
        for j in range(10):
            if j != i:
                data_train.extend([" ".join([str(s) for s in vec]) for vec in datasets[j]])
                label_train.extend(labelsets[j])
        df_train = pd.DataFrame({'feature': data_train, 'tag': label_train})

        df_test.to_csv("data/train_test/test_%d.csv" % i, index=False, sep=',')
        df_train.to_csv("data/train_test/train_%d.csv" % i, index=False, sep=',')
