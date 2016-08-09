__author__ = 'plaix'
import string
import os
import math
import numpy as np
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
    return data

def createInvertedIndex(file, stoprmv=False, lemmatize=False):
    data = fileParser(file)
    for key in data:
        for c in string.punctuation:
            data[key] = list(filter(None, " ".join(data[key]).replace(c, "").lower().split(" ")))

    for key in data:
        data[key] = data[key][1:]

    if stoprmv:
        stop = stopwords.words('english')
        for key in data:
            data[key] = [x for x in data[key] if x not in stop]
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        data[key] = [str(lemmatizer.lemmatize(x)) for x in data[key]]

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

def createDocWordMatrix(invertedi_docsize, tf_idfB = False):
    invertedI, docSize = invertedi_docsize
    tf_idf = dict()
    tf = dict()
    N = 1400
    for key in invertedI:
        for i in invertedI[key]:
            if key in tf:
                tf[key].append((int(i[0]), (i[1]/float(docSize[i[0]]))))
            else:
                tf[key] = [(int(i[0]), (i[1]/float(docSize[i[0]])))]
            if key in tf_idf:
                tf_idf[key].append((int(i[0]), (i[1]/float(docSize[i[0]])) * math.log(N/float(len(invertedI[key])))))
            else:
                #print(docSize)
                tf_idf[key] = [(int(i[0]), (i[1]/float(docSize[i[0]])) * math.log(N/float(len(invertedI[key]))))]


    docMatrix = dict()
    tf_new = dict()
    if tf_idfB:
        for key in tf:
            tf_new[key] = tf_idf[key]
    else:
        for key in tf:
            tf_new[key] = tf[key]
    for key in tf_new:
        docMatrix[key] = dict()

    for key in docMatrix:
        for key2 in tf_new:
            if key == key2:
                for i in tf_new[key2]:
                    if i[0] in docMatrix[key]:
                        docMatrix[key][i[0]].append(i[1])
                    else:
                        docMatrix[key][i[0]] = [i[1]]

    # docMatrix = np.zeros(shape=(8485, 1401))
    # np.set_printoptions(precision=5)
    # row = 0
    # for i in tf_new:
    #     for j in i:
    #         docMatrix[row, j[0]] = float(j[1])
    #     row += 1
    return docMatrix

def IR_challenge(file, file2, docmatrix):
    data = fileParser(file)
    data2 = dict()
    counter = 0
    with open(DATA_PATH+file2) as f:
        for line in f:
            line = line.split(" ")
            counter +=1
            data2[counter] = line[1]

    for key in data:
        for c in string.punctuation:
            data[key] = list(filter(None, " ".join(data[key]).replace(c, "").lower().split(" ")))

    for key in data:
        data[key] = data[key][1:]
    sim = dict()
    precision = dict()

    for id in data:
        counter = 0
        for token in data[id]:
            if token in docmatrix and int(id) in docmatrix[token]:
                counter += sum(docmatrix[token][int(id)])
        sim[id] = counter

    # for key in sim:
    #     if int(key) in data2:
    #         precision[key] = int(data2[int(key)])/float(sim[key])
    # for key in sim:
    #     print(key, sim[key])
    # avgPrec = sum(precision.values())/len(precision)
    # return avgPrec, precision
IR_challenge('cran.qry', 'cranqrel', createDocWordMatrix(createInvertedIndex('cran.all.1400')))
