__author__ = 'plaix'
import os
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import matplotlib.pyplot as plt
import numpy as np

# path to the data folder
DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/')

#procedure for removing punctuation from the data except for
#'#' and '%' which are useful in identifying data
def punctuation_strip(path):
    f = open(path, 'r')
    data = f.read()
    for c in string.punctuation:
        if c not in ['#', '%']:
            data = data.replace(c, "")
    data = data.lower()
    f.close()
    f = open(path, 'w')
    f.write(data)
    f.close()


#procedure for the removal of stopwords
def stopwords_removal(path):
    stop = stopwords.words('english')
    f = open(path, 'r')
    data = f.read().splitlines()
    newdata = []
    for line in data:
        for l in line.split():
            newdata.append(l)
    newdata2 = [x for x in newdata if x not in stop and not x.isdigit()]
    data2 = " ".join(newdata2)
    f.close()

    f = open(path, 'w')
    f.write(data2)
    f.close()


#stemming procedure, we stem all words except for those we use as identifiers
#e.g #definition #label and the ''%'' words
def stemming(path):
    stemmer = PorterStemmer()
    f = open(path, 'r')
    data = f.read().split()
    newdata = []
    for x in data:
        if '%' not in x:
            newdata.append(stemmer.stem(x))
        else:
            newdata.append(x)
    data = " ".join(newdata)
    f.close()
    f = open(path, 'w')
    f.write(str(data))
    f.close()


#get all the words and their definitions.
def get_definitions(path):
    with open(path) as f:
        data = f.read()
        definit = data.split("#definit")
        definit = list(filter(None, definit))
        return definit


#get all the contexts
def get_contexts(path):
    with open(path) as f:
        data = f.read()
        context = data.split("#label")
        context = list(filter(None, context))
        return context


#overlap(A, B)
def overlap(a, b):
    overlapCoef = (2 * len(set.intersection(a, b))) / float((len(a) + len(b)))
    return overlapCoef


#lsk wsd algorithm
#passing the senses and the contexts, for each sense we calculate
#the overlap between the sense and its context using the overlap
#function above and then returns the word sense with the most overlap
def wsd(senses, contexts):
    sen = dict()
    overlap_dict = dict()
    #for each of the sense of word, we calculate the overlap with all the contexts
    #putting our result in a key value dictionary with the key as the word, value
    #the list of all the overlaps with the context. Then we select the sense
    for key in senses:
        for keys, values in contexts.items():
            if key.split('%')[0] == keys.split('%')[0]:
                for i in values:
                    u = overlap(set(senses[key]), set(i))
                    if key in sen:
                        sen[key].append(u)
                    else:
                        sen[key] = [u]

    for key, value in sen.items():
        overlap_dict[key] = max(value)
    overlap_dict2 = overlap_dict

    best_sense = []

    for key in overlap_dict:
        for keys in overlap_dict2:
            if key.split("%")[0] == keys.split("%")[0] and key.split("%")[1] != keys.split("%")[1]:
                if overlap_dict[key] > overlap_dict[keys]:
                    a = (key, overlap_dict[key])
                    best_sense.append(a)
                else:
                    a = (keys,  overlap_dict[keys])
                    best_sense.append(a)
    best_sense = set(best_sense)
    best_sense = list(best_sense)
    return best_sense

#We loop through all files and apply the puntuation_strip funtion
for filename in os.listdir(DATA_PATH):
    if filename not in ['README']:
        punctuation_strip(DATA_PATH + filename)

#removing all stopwords and numbers in all files
for filename in os.listdir(DATA_PATH):
    if filename not in ['README']:
        stopwords_removal(DATA_PATH + filename)

#stemming each word in each file
for filename in os.listdir(DATA_PATH):
    if filename not in ['README']:
        stemming(DATA_PATH + filename)

#dictionary that reads all definitions of each word uning
# the file name as key and definition list as value
definition_dict = dict()
for filename in os.listdir(DATA_PATH):
    if filename not in ['README']:
        if filename.split(".")[1] != 'test':
            definition_dict[filename] = get_definitions(DATA_PATH + filename)

#reading all the contexts and their description into a dictionary with
#file name as key
context_dict = dict()
for filename in os.listdir(DATA_PATH):
    if filename not in ['README']:
        if filename.split(".")[1] != 'definition':
            context_dict[filename] = get_contexts(DATA_PATH + filename)

#for each key pair value in definitions dictionary
#we create a new dictionary called table that contains the words ''%''
#as key and their various tokenized definitoin.
table = []

definition_table = dict()
for key in definition_dict:
    table.append(definition_dict[key][0].split())
    table.append(definition_dict[key][1].split())
for i in table:
    definition_table[i[0]] = i[1:len(i)]

#for each key pair value in contexts dictionary, we create a new
#dictionary table containing each word ''%'' as key and their various
#contexts as lists. This way we can easily check for overlap using the key.
table = []
contexts_table = dict()


for key in context_dict:
    for i in range(len(context_dict[key])):
        table.append(context_dict[key][i].split())
for i in table:
    if i[0] in contexts_table:
        contexts_table[i[0]].append(i[1:len(i)])
    else:
        contexts_table[i[0]] = [i[1:len(i)]]


best_sense = wsd(definition_table, contexts_table)

#displaying the best sense of each word
for i in best_sense:
    print(i[0], i[1])

