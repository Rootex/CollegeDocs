__author__ = 'plaix'
import os
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cran/')

def fileParser(file):
    lines = tuple(open(DATA_PATH+file))
    lines = list(lines)
    data = dict()
    det = False
    id = ""
    for l in lines:
        l = l.strip("\n")
        if '.I' in l:
            id = l.split(" ")[1]
            data[id] = []
            det = False
        if '.W' in l:
            det = True
        if det:
            data[id] = data[id] + l.split(" ")

    for key in data:
        for c in string.punctuation:
            data[key] = list(filter(None, " ".join(data[key]).replace(c, "").lower().split(" ")))

    for i in data:
        data[i] = data[i][1:]

    stop = stopwords.words('english')
    for key in data:
        data[key] = [x for x in data[key] if x not in stop]

    lemmatizer = WordNetLemmatizer()
    data[key] = [str(lemmatizer.lemmatize(x)) for x in data[key]]

    return data

def createInvertedIndex(file):
    data = fileParser(file)

    invertedIndex = dict()
    for key in data:
        for token in data[key]:
            if token in invertedIndex:
                invertedIndex[token].append([key, data[key].count(token)])
            else:
                invertedIndex[token] = [[key, data[key].count(token)]]


    docSize = dict()
    for key in data:
        docSize[key] = len(data[key])

    return invertedIndex, docSize
queries = fileParser("cran.qry")

inI, docS = createInvertedIndex("cran.all.1400")

Pt_d = dict()
Pt_C = dict()
token_doc = dict()

collection_size = sum(docS.values())
lam_da = 0.7
epsilon = 0.5


for key in inI:
    counter = 0
    for i in inI[key]:
        counter += i[1]
    Pt_C[key] = counter/float(collection_size)

def lidstone(token):
        value = Pt_C[token]
        return (value + epsilon) / collection_size

# add tokens in query that are not in the document collection and set
# probability to 0
for key in queries:
    for token in queries[key]:
        if token not in Pt_C:
            Pt_C[token] = 0

# perform lidstone smoothing on all tokens
for key in Pt_C:
    Pt_C[key] = lidstone(key)

for key in inI:
    token_doc[key] = dict()
    Pt_d[key] = dict()

# in inverted index, key is the token, i[0] is the document ID and
# i[1] is the frequency of the token in the document ID i[0]
for key in inI:
    for i in inI[key]:
        token_doc[key][i[0]] = i[1]

# calculating P(t|d)
for token in token_doc:
    for docid in token_doc[token]:
        Pt_d[token][docid] = token_doc[token][docid]/float(docS[docid])

# calculating P(t|d) based on Jelinek Mercer Smoothing technic
for token in Pt_d:
    for docid in Pt_d[token]:
        Pt_d[token][docid] = ((1 - lam_da) * Pt_d[token][docid]) + (lam_da * Pt_C[token])

# fetch the cranqrel value mapping to be used in calculating Pq_d
cranqrel = dict()

with open(DATA_PATH+"cranqrel") as f:
    cnt = 1
    for line in f:
        l = line.split(" ")
        cranqrel[cnt] = l[1]
        cnt+=1

Pqi_d = dict()

# Pqi_d is the probability of a token in a query given a document
for key in queries:
    for token in queries[key]:
        Pqi_d[token] = dict()

# Pq_d calculation
Pq_d = dict()
for id in queries:
    Pq_d[int(id)] = dict()

for id in queries:
    prob = 1
    for token in queries[id]:
        if token in Pt_d:
            if cranqrel[int(id)] in Pt_d[token]:
                prob *= Pt_d[token][cranqrel[int(id)]]
    Pq_d[int(id)][cranqrel[int(id)]] = prob

AvgPQ = dict()
for qid in Pq_d:
    AvgPQ[qid] = sum(Pq_d[qid].values()) / float(len(Pq_d[qid]))

MAP = sum(AvgPQ.values()) / float(len(AvgPQ))
print(MAP)