import re
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

from preprocess import e_analyser


def process_count(event, sentiment, counts):
    if sentiment == 1:
        counts[event][0] += 1
    elif sentiment == -1:
        counts[event][1] += 1
    else:
        counts["other"] += 1


def count_ac_event(sent, counts, topics):
    events = e_analyser.find_event(sent)
    sentiment = e_analyser.sentiment_extraction(sent)
    for e in events:
        if e in topics:
            process_count(e, sentiment, counts)
            return
        if fuzz.partial_ratio(e, "activities") >= 80:
            print(e)
            counts["other"] += 1
            return


dic = {}
topics = []
for topic in open("activities"):
    if topic == "other":
        dic["other"] = 0
    else:
        dic[re.sub('\\n', '', topic)] = [0, 0]
        topics.append(re.sub('\\n', '', topic))

data = pd.read_csv("drug_info.csv")
start = time.clock()
for i in range(len(data.index)):
    if i % 5000 == 0:
        print("process %d : %fs" % (i, time.clock() - start))
    count_ac_event(str(data.loc[i]["interaction"]), dic, topics)
print(dic)

data = []
labels = []
for topic in dic:
    if topic != "other":
        data.append(dic[topic][0]+dic[topic][1])
        #data.append(dic[topic][1])
        #labels.append(topic+"\nasc")
        #labels.append(topic+"\ndes")
        labels.append(topic)
    else:
        data.append(dic[topic])
        labels.append(topic)

width = 0.4
x_bar = np.arange(56) + 1
rect = plt.bar(left=x_bar, height=data, tick_label=labels, width=width, color="lightblue")
for rec in rect:
    x = rec.get_x()
    height = rec.get_height()
    plt.text(x-0.65, 1.02*height, str(height))
plt.xticks(x_bar, size="medium", rotation=90)
plt.xlabel("events")
plt.ylabel("numbers")
plt.title("activities distribution")
plt.grid(True)
plt.subplots_adjust(left=0.04, right=0.99, top=0.97, bottom=0.35)
plt.show()
