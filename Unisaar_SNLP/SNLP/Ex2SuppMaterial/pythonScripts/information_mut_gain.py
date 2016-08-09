__author__ = 'plaix'
from collections import Counter
import matplotlib.pyplot as plt
import wordCounting
import os
import math
import numpy as np

#data paths
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'dataset/')
SPAM_TRAIN_PATH = DATA_PATH + "spam-train"
NSPAM_TRAIN_PATH = DATA_PATH + "nonspam-train"

#get data from wordcounting
dictionary=dict()
spam_dictionary = wordCounting.spamTrain(dictionary)
dictionary=dict()
nonSpam_dictionary = wordCounting.nonSpamTrain(dictionary)

#document frequency of terms
DF_S = dict()
for key in spam_dictionary:
    DF_S[key] = len(spam_dictionary[key])

DF_NS = dict()
for key in nonSpam_dictionary:
    DF_NS[key] = len(nonSpam_dictionary[key])

A = Counter(DF_S)
B = Counter(DF_NS)
combined = A + B

spam_train_samples = len([name for name in os.listdir(SPAM_TRAIN_PATH)
                          if os.path.isfile(os.path.join(SPAM_TRAIN_PATH, name))])
nspam_train_samples = len([name for name in os.listdir(NSPAM_TRAIN_PATH)
                           if os.path.isfile(os.path.join(NSPAM_TRAIN_PATH, name))])

#probabilities
#P(term)
pTerm = dict()
for key in combined:
    pTerm[key] = combined[key] / float(spam_train_samples+nspam_train_samples)

#P(_term)
p_Term = dict()
for key in pTerm:
    p_Term[key] = 1 - pTerm[key]

#P(spam)
p_s = dict()
for key in DF_S:
    p_s[key] = DF_S[key] / float(spam_train_samples)

#P(non-spam)
p_ns = dict()
for key in DF_NS:
    p_ns[key] = DF_NS[key] / float(nspam_train_samples)

#P(spam|term)
pSpam_Term = dict()
for key in p_s:
    pSpam_Term[key] = p_s[key] / pTerm[key]

#P(spam|_term)
pSpam_NTerm = dict()
for key in p_s:
    pSpam_NTerm[key] = p_s[key] / p_Term[key]

#P(non-spam|term)
pNSpam_Term = dict()
for key in p_ns:
    pNSpam_Term[key] = p_ns[key] / pTerm[key]

#P(non-spam|_term)
pNSpam_NTerm = dict()
for key in p_ns:
    pNSpam_NTerm[key] = p_ns[key] / p_Term[key]


C = 0.0
for key in p_s:
    C += p_s[key] * math.log10(p_s[key])

D = 0.0
for key in pSpam_Term:
    D += pSpam_Term[key] * math.log10(pSpam_Term[key])

E = 0.0
for key in pSpam_NTerm:
    E += pSpam_NTerm[key] * math.log10(pSpam_NTerm[key])

#Information gain
def computeInfGain(p):
    IG = (-C) + (p * D) + (p * C)
    return IG

#Mutual Information
def computeMutGain(p1, p2):
    pc = 0.0
    for key in p_s:
        pc += p_s[key]
    MI = math.log10(p1 / float(p2 * pc))
    return MI

#words selection
words_p = dict()
words_sp = dict()
wanted_keys = ['latinoweb', 'yellow', 'four', 'unmask', 'lee', 'bandera', 'innocent']
for key in wanted_keys:
    words_p[key] = pTerm[key]

for key in wanted_keys:
    words_sp[key] = pSpam_Term[key]


#IG for each word selected
words_IG = dict()
for key in words_p:
    words_IG[key] = computeInfGain(words_p[key])

#MI for each word selected
words_MI = dict()
for key in words_p:
    words_MI[key] = computeMutGain(words_sp[key], words_p[key])

IG = []
MI = []
for key in words_IG:
    IG.append(words_IG[key])

for key in words_MI:
    MI.append(words_MI[key])
#IG = sorted(IG)
#MI = sorted(MI)
print words_MI
print MI
wanted_IG = ['latinoweb', 'unmask', 'bandera', 'yellow', 'innocent', 'lee', 'four']
wanted_MI = ['four', 'lee', 'yellow','innocent', 'latinoweb', 'unmask', 'bandera']
#plt.yscale('log', nonposy="clip")
#plt.xscale('log', nonposx="clip")
x = np.array([0,1,2,3, 4, 5, 6])
plt.xticks(x, wanted_IG)
plt.plot(x, IG, color='r', label='Words/IG')
plt.legend(loc='upper right')
plt.xlabel("Words")
plt.ylabel("IG")
plt.title("Word IG")
plt.show()

x = np.array([0,1,2,3, 4, 5, 6])
plt.xticks(x, wanted_MI)
plt.plot(x, MI, color='r', label='Words/MI')
plt.legend(loc='upper right')
plt.xlabel("Words")
plt.ylabel("MI")
plt.title("Word MI")
plt.show()
