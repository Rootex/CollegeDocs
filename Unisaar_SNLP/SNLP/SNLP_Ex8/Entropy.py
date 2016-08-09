__author__ = 'plaix'
import os
import string
import math
import codecs
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/')

def parseText(file):
    data  = ""
    with codecs.open(DATA_PATH + file, "r",encoding='utf-8', errors='ignore') as f:
        data = f.read()

    for c in string.punctuation:
        data = data.replace(c, "")
    data = data.lower().split()

    # stop = stopwords.words('english')
    # data = [token for token in data if token not in stop]

    lemmatizer = WordNetLemmatizer()
    data = [str(lemmatizer.lemmatize(token)) for token in data]

    prob_dist = dict()
    data_size = len(data)
    for token in data:
        if token not in prob_dist:
            prob_dist[token] = data.count(token) / float(data_size)

    return prob_dist

def entropy(prob_dist):
    calc = dict()
    for key in prob_dist:
        calc[key] = prob_dist[key] * math.log2(prob_dist[key])
    entrop = -1 * sum(calc.values())
    return entrop

for f in os.listdir(DATA_PATH):
    if os.path.isfile(os.path.join(DATA_PATH, f)):
        prob = parseText(f)
        print(f.split(".")[0], entropy(prob))
