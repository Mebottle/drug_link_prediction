import pandas as pd
import gensim
import nltk
import re
from io import StringIO


def get_doc_event(topic_dis, lda):
    max_pro = 0
    topic_id = 0
    for tup in topic_dis:
        if tup[1] > max_pro:
            max_pro = tup[1]
            topic_id = tup[0]
    return lda.show_topic(topic_id)

sentences = []
path = ["drug_info.csv"
        #"drug_info_part3.csv",
        #"drug_info_part4.csv",
        #"drug_info_part5.csv",
        #"drug_info_part6.csv",
        #"drug_info_part7.csv",
        #"drug_info_part8.csv",
        #"drug_info_part9.csv",
        #"drug_info_part10.csv"
]

for p in path:
    data = pd.read_csv(p)
    for i in data.index:
        sentences.append(nltk.word_tokenize(re.sub('( drugA| drugB|drugA |drugB )', '', str(data["interaction"][i]))))

# todo 将全部token转为小写

# todo 消除停用词,暂不需要
# stopwords = nltk.corpus.stopwords.words('english')
for tokens in sentences:
    tokens.remove(".")
#     for t in tokens:
#         if t in stopwords:
#             tokens.remove(t)

# todo 可选 词形还原 词干提取
# wnl = nltk.WordNetLemmatizer()
# porter = nltk.PorterStemmer()
# lancaster = nltk.LancasterStemmer()

# 提取NP
sentences = [nltk.pos_tag(sent) for sent in sentences]
grammar = "NP: {<JJ>*(<NN>|<NNS>)+}"
cp = nltk.RegexpParser(grammar)
np_sentences = []
for sent in sentences:
    tree = cp.parse(sent)
    sentence = []
    for s in tree.subtrees(lambda t: t.label() == "NP"):
        np = [word for (word, pos) in s.leaves()]
        file_str = StringIO()
        for num in range(len(np)):
            if num == (len(np)-1):
                file_str.write(np[num])
                break
            file_str.write(np[num]+" ")
        sentence.append(file_str.getvalue())
    np_sentences.append(sentence)

# 训练lda模型
dic = gensim.corpora.Dictionary(np_sentences)
corpus = [dic.doc2bow(text) for text in np_sentences]
ldamodel = gensim.models.LdaModel(corpus, num_topics=25, id2word=dic, passes=20)
ldamodel.save("/Users/mebottle/Desktop/new_lda/lda.gensim")
topics = ldamodel.show_topics(num_topics=25, num_words=4)
for t in topics:
    print(t)

# print(ldamodel.print_topics(num_topics=10, num_words=3))
#print(ldamodel.get_topics())
# doc_topic_dis = ldamodel[dic.doc2bow(nltk.word_tokenize("The metabolism of can be decreased when combined with."))]
# print(get_doc_event(doc_topic_dis, ldamodel))
