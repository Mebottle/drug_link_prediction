import pandas as pd
import numpy as np
import nltk
import re
from io import StringIO
from fuzzywuzzy import fuzz


def find_event(sentence):
    sent = nltk.word_tokenize(re.sub('( drugA| drugB|drugA |drugB )', '', sentence))
    sent = [token.lower() for token in sent]
    sent.remove(".")
    # todo 暂时不需要清除停用词
    # stopwords = nltk.corpus.stopwords.words('english')
    # for t in sent:
    #     if t in stopwords:
    #         sent.remove(t)
    sent = nltk.pos_tag(sent)
    grammar = "NP: {<JJ>*(<NN>|<NNS>)+}"
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(sent)

    sent_np = []
    for s in tree.subtrees(lambda t: t.label() == "NP"):
        np = [word for (word, pos) in s.leaves()]
        file_str = StringIO()
        for num in range(len(np)):
            if num == (len(np)-1):
                file_str.write(np[num])
                break
            file_str.write(np[num]+" ")
        sent_np.append(file_str.getvalue())

    return sent_np


def process_events(events, topics):
    new_events = []
    for e in events:
        if e in topics:
            new_events.append(e)
        else:
            for t in topics:
                if fuzz.partial_ratio(e, t) > 50:
                    new_events.append(e)
                    break

    return new_events


def sentiment_extraction(sent):
    increase_vector = np.loadtxt("increase.txt", dtype=np.str)
    decrease_vector = np.loadtxt("decrease.txt", dtype=np.str)
    increase_weight = 0  # the weight represents for "increase sentiment"
    decrease_weight = 0

    # each "increase sentiment" word contained in interaction string will increase the weight by 1
    for i_word in increase_vector:
        if str(sent).find(i_word) > -1:
            increase_weight += 1
    for d_word in decrease_vector:
        if str(sent).find(d_word) > -1:
            decrease_weight += 1

    # compare two weights and add the result into the sentiment vector
    if increase_weight > decrease_weight:
        return 1
    elif decrease_weight > increase_weight:
        return -1
    else:
        return 0


def analyse(df_record, topics, num):
    drug_a = str(df_record["drug_a_name"])
    drug_b = str(df_record["drug_b_name"])
    events = find_event(str(df_record["interaction"]))
    events = process_events(events, topics)
    sentiment = sentiment_extraction(str(df_record["interaction"]))
    if sentiment == 1:
        sentiment = "increase"
    elif sentiment == -1:
        sentiment = "decrease"
    else:
        sentiment = "not sure"

    print("--------------- record %d --------------" % num)
    print("drugA: " + drug_a)
    print("drugB: " + drug_b)
    print("event: ")
    print(events)
    print("sentiment: " + sentiment)
    print("---------------------------------------")


# todo for debug
def analyse_test(num):
    #drugA = str(df_record["drug_a_name"])
    #drugB = str(df_record["drug_b_name"])
    event = find_event("drugA may increase the atrioventricular blocking (AV block) activities of drugB.")
    print("--------------- record %d --------------" % num)
    #print("drugA: " + drugA)
    #print("drugB: " + drugB)
    print("event: ")
    print(event)
    print("---------------------------------------")

if __name__ == '__main__':
    topics = []
    for topic in open("topics.txt"):
        topics.append(re.sub('\\n', '', topic))

    data = pd.read_csv("drug_info_part10.csv")
    for i in range(100):
        analyse(data.loc[i], topics, i)
        print()

    analyse_test(1)
