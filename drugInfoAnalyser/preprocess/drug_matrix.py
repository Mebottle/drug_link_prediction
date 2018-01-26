import time

import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

from preprocess import e_analyser


def get_event_index(sent):
    events = e_analyser.find_event(sent)
    if "metabolism" in events:
        return 3
    elif ("serum concentration" in events) or ("excretion rate" in events):
        return 4
    elif "therapeutic efficacy" in events:
        return 5
    elif ("risk" in events) or ("severity" in events):
        return 1
    else:
        for e in events:
            if fuzz.partial_ratio(e, "activities") > 80:
                return 2
    return -1


def build_matrix(df, drugs):
    start = time.clock()
    matrix = np.mat(np.zeros((len(drugs), len(drugs))), dtype=np.int32)
    for i in range(len(df.index)):
        if i % 5000 == 0:
            print("process %d : %fs" % (i, time.clock() - start))
        a_id_index = drugs.index(df.loc[i]["drug_a_id"])
        b_id_index = drugs.index(df.loc[i]["drug_b_id"])
        event_index = get_event_index(df.loc[i]["interaction"])
        if matrix[a_id_index, b_id_index] == 0:
            matrix[a_id_index, b_id_index] = event_index
        else:
            matrix[a_id_index, b_id_index] = -2
    matrix.tofile("matrix")
    np.savetxt("mat.txt", matrix, fmt="%d")
    print(matrix)

# produce matrix
file = open('811', 'rb')
drugs = eval(file.read())
df = pd.read_csv("drug_info_20180120.csv")
build_matrix(df, drugs)

# check the matrix
# np.set_printoptions(threshold=np.inf)
# mat = np.fromfile("matrix", dtype=np.int32)
# mat.shape = (811, 811)
# mat2 = np.mat(np.zeros((811, 811)), dtype=np.int32)
# for i in range(811):
#     for j in range(811):
#         mat2[i, j] = int(mat[i, j])
#
# result1 = np.sum(mat, axis=0)  # 列和
# result2 = np.sum(mat, axis=1)  # 行和
# inds1 = np.where(result1 == 0)
# inds2 = np.where(result2 == 0)
# for i in inds1[0]:
#     if i in inds2[0]:
#         print(i)
# for j in inds2[0]:
#     if j in inds1[0]:
#         print(j)
