import re
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from preprocess import e_analyser


def process_count(event, sentiment, counts):
    if sentiment == 1:
        counts[event] += 1
    else:
        counts["other"] += 1


def count_ad_event(sent, counts):
    events = e_analyser.find_event(sent)
    sentiment = e_analyser.sentiment_extraction(sent)
    if ("risk" in events) or ("severity" in events):
        if "adverse effects" in events:
            process_count("adverse effects", sentiment, counts)
        elif "hypotension" in events:
            process_count("hypotension", sentiment, counts)
        elif "hypertension" in events:
            process_count("hypertension", sentiment, counts)
        elif "bleeding" in events:
            process_count("bleeding", sentiment, counts)
        elif "qtc prolongation" in events:
            process_count("qtc prolongation", sentiment, counts)
        elif "heart failure" in events:
            process_count("heart failure", sentiment, counts)
        elif "myelosuppression" in events:
            process_count("myelosuppression", sentiment, counts)
        elif "cytotoxicity" in events:
            process_count("cytotoxicity", sentiment, counts)
        else:
            counts["other"] += 1


dic = {}
for topic in open("adverse_effect"):
    dic[re.sub('\\n', '', topic)] = 0

data = pd.read_csv("drug_info.csv")
start = time.clock()
for i in range(len(data.index)):
    if i % 5000 == 0:
        print("process %d : %fs" % (i, time.clock() - start))
    count_ad_event(str(data.loc[i]["interaction"]), dic)
print(dic)

data = []
labels = []
for topic in dic:
    if topic != "other":
        data.append(dic[topic])
        labels.append(topic+"\nasc")
    else:
        data.append(dic[topic])
        labels.append(topic)

width = 0.5
x_bar = np.arange(9) + 1
rect = plt.bar(left=x_bar, height=data, tick_label=labels, width=width, color="lightblue")
for rec in rect:
    x = rec.get_x()
    height = rec.get_height()
    plt.text(x-0.05, 1.02*height, str(height))
plt.xticks(x_bar, size="medium", rotation=60)
plt.xlabel("events")
plt.ylabel("numbers")
plt.title("adverse effects distribution")
plt.grid(True)
plt.subplots_adjust(left=0.05, right=0.99, top=0.96, bottom=0.21)
plt.show()
