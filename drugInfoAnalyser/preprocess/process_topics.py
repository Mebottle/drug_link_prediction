import time
import pandas as pd
import numpy as np

# lda = gensim.models.LdaModel.load("/Users/mebottle/Desktop/lda3/lda.gensim")
# topics = lda.show_topics(num_topics=25, num_words=5)
# for t in topics:
#     print(t)

# topics = []
# for topic in open("topics.txt"):
#     topics.append(re.sub('\\n', '', topic))
# print(topics)

#print(fuzz.partial_ratio("s", "activities"))
#print(e_analyser.find_event("qtc-prolonging activities."))

# start = time.clock()
# hashmap = {}
# results = pd.read_csv("data.csv")
# for ind in range(len(results.index)):
#     if ind % 5000 == 0:
#         print("process hash %d : %fs" % (ind, time.clock() - start))
#     # if "%s%s" % (results[ind][1], results[ind][3]) in hashmap.keys():
#     # tuple_i = [results[ind][1], results[ind][3]]
#     # id_tuple.append(tuple_i)
#     hashmap["%s%s" % (results.loc[ind]["drug_a"], results.loc[ind]["drug_b"])] = 1
#     # print(len(hashmap))
#
# for ind in range(len(results.index)):
#     if ind % 5000 == 0:
#         print("process check %d : %fs" % (ind, time.clock() - start))
#     if not ("%s%s" % (results.loc[ind]["drug_b"], results.loc[ind]["drug_a"]) in hashmap.keys()):
#         print("%s %s %s" % (results.loc[ind]["drug_a"], results.loc[ind]["drug_b"], results.loc[ind]["interaction"]))

# DB01418 DB01163
# df = pd.read_csv("data.csv")
# for i in range(len(df)):
#     if str(df.loc[i]["drug_a"]) == "DB00589" and str(df.loc[i]["drug_b"]) == "DB00211":
#         print("%s %s %s" % (df.loc[i]["drug_a"], df.loc[i]["drug_b"], df.loc[i]["interaction"]))
print(np.random.choice(3,2))
