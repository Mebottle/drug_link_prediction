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


def count_event(sent, counts):
    events = e_analyser.find_event(sent)
    sentiment = e_analyser.sentiment_extraction(sent)
    if "metabolism" in events:
        process_count("metabolism", sentiment, counts)
    elif "serum concentration" in events:
        process_count("serum concentration", sentiment, counts)
    elif "bioavailability" in events:
        process_count("bioavailability", sentiment, counts)
    elif "absorption" in events:
        process_count("absorption", sentiment, counts)
    elif "protein binding" in events:
        process_count("protein binding", sentiment, counts)
    elif "therapeutic efficacy" in events:
        process_count("therapeutic efficacy", sentiment, counts)
    elif "diagnostic agent" in events:
        process_count("diagnostic agent", sentiment, counts)
    elif "excretion rate" in events:
        process_count("excretion rate", sentiment, counts)
    elif ("risk" in events) or ("severity" in events):
        process_count("adverse effects", sentiment, counts)
    else:
        for e in events:
            if fuzz.partial_ratio(e, "activities") > 80:
                process_count("activities", sentiment, counts)
                return
        counts["other"] += 1


dic = {}
for topic in open("topics_crude"):
    if topic == "other":
        dic["other"] = 0
    else:
        dic[re.sub('\\n', '', topic)] = [0, 0]

data = pd.read_csv("drug_info.csv")
start = time.clock()
for i in range(len(data.index)):
    if i % 5000 == 0:
        print("process %d : %fs" % (i, time.clock() - start))
    count_event(str(data.loc[i]["interaction"]), dic)

print(dic)
data = []
labels = []
for topic in dic:
    if topic != "other":
        data.append(dic[topic][0])
        data.append(dic[topic][1])
        labels.append(topic+"\nasc")
        labels.append(topic+"\ndes")
    else:
        data.append(dic[topic])
        labels.append(topic)

width = 0.5
x_bar = np.arange(21) + 1
rect = plt.bar(left=x_bar, height=data, tick_label=labels, width=width, color="lightblue")
for rec in rect:
    x = rec.get_x()
    height = rec.get_height()
    plt.text(x-0.05, 1.02*height, str(height))
plt.xticks(x_bar, size="medium", rotation=60)
plt.xlabel("events")
plt.ylabel("numbers")
plt.title("topic distribution")
plt.grid(True)
plt.subplots_adjust(left=0.045, right=0.99, top=0.96, bottom=0.21)
plt.show()
