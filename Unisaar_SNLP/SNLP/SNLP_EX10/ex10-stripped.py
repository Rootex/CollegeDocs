#! /usr/bin/env python3
'''
Created on July 11, 2015

@author: janis
'''

from collections import Counter
from matplotlib import pyplot as plt
import os

DATA_PATH = os.path.realpath(__file__)
print(DATA_PATH)

def count_ngrams_hierarchical(text, n):
    from nltk import ngrams
    counts = {n: Counter(ngrams(text, n, pad_left=True, ))}
    if n == 1:
        counts.update({0: sum(counts[1].values())})
    else:
        counts.update(count_ngrams_hierarchical(text, n-1))
    return counts  

def compute_conditional_entropy_of_ngram(n, ngramCounts):
    from math import log2 as log
    allWords = ngramCounts[0]
    H = 0
    if n == 1:
        ''' TODO: Compute the entropy of the distribution '''
        for count in ngramCounts[1].values():
            H += (count/float(allWords)) * log((count/float(allWords)))
    else:
        ''' TODO: Compute the conditional entropy of the distribution '''
        pAll = 0
        pCond = 0
        for ngram, count in ngramCounts[n].items():
            history = ngram[:-1]
            countHistory = len(history)
            if countHistory == 0 : # Fix for the case of ngram padding
                countHistory = 1 

            nProb = 1
            hProb = 1
            for i in ngram:
                nProb *= ngram.count(i)/float(len(ngram))
            for i in history:
                hProb *= history.count(i)/float(countHistory)

            H += nProb * log(nProb/hProb)
    return H * -1

def measure_conditional_entropy_hierarchical(text, maxNumGrams = 5):
    ngramCounts = count_ngrams_hierarchical(text, maxNumGrams)
    return tuple(compute_conditional_entropy_of_ngram(n, ngramCounts)
                 for n in range(1,maxNumGrams+1))

def compute_perplexity(jointProbabilityTest,distributionModel):
    from math import log
    base = 2
    loglikelihood = -sum(testNgramCount*log(distributionModel[testNgram],base)
                         for testNgram,testNgramCount in jointProbabilityTest.items())
    perp = base**loglikelihood
    return perp

class discounting_model:
    def __init__(self, testTokens, d, unigramCounts, bigramCounts):
        self._bigramCounts = bigramCounts
        self._unigramCounts = unigramCounts
        self._d = d
        trainTokens = set(bigram[-1] for bigram in bigramCounts.keys())
        self._V = len(set(testTokens) | set(trainTokens) )
        ''' 
        TODO: Complete this part to return the R values, as in slide 18 of chapter 5.
        This must be a dict with histories as keys (these are tuples of 1 word); the value of each
        entry should amount to the number of words following that history with non-zero count in the training set. 
        '''
        self._R = ()

    def __getitem__(self, bigram):
        bigramCount = self._bigramCounts[bigram]
        history = bigram[0:1]
        historyCount = self._unigramCounts[history]
        V, d = self._V, self._d
        nPlus = self.R[history]
        '''
        TODO: copute the discounted probability.
        
        For your convenience the following values are pre-computed:
            V:            the size of the vocabulary (test tokens and training tokens)
            nPlus:        the number of tokens following the crrent history with non-zero counts.
            d:            discounting parameter
            historyCount: occurrence count of the bigram history (the first bigram token)
            bigramCount:  occurrence count of the bigram itself
        '''
        prob = 0
        # verify that prob is > 0
        assert(prob > 0)
        return prob

def get_bigram_probability(text):
    ngramCounts = count_ngrams_hierarchical(text, 2)
    bigramProbability = dict()
    for bigram,bigramCount in ngramCounts[2].items():
        history = bigram[0:1]
        historyCount = ngramCounts[1].get(history,1)
        bigramProbability[bigram] = bigramCount/historyCount
    return bigramProbability
    
def plot_entropy(H, title, fileName = None):
    x = range(1, len(H)+1)
    plt.clf()
    plt.plot(x, H)
    plt.xlabel('NGram history level')
    plt.ylabel('Entropy (bits)')
    plt.title(title)
    if fileName is not None:
        plt.savefig(fileName)
    # plt.show()

if __name__ == "__main__":
    import re

    textA = open(DATA_PATH+'textA.txt').read().split(' ')
    entropyA = measure_conditional_entropy_hierarchical(textA, 9)

    plot_entropy(entropyA, 'Text A conditional entropy (tokens)', 'textA-entropy.pdf')

    textB = open(DATA_PATH+'textB.txt').read().split(' ')

    entropyB = measure_conditional_entropy_hierarchical(textB, 9)
    plot_entropy(entropyB, 'Text B conditional entropy (tokens)', 'textB-entropy.pdf')

    textC = open(DATA_PATH+'textC.txt').read().lower()
    entropyC = measure_conditional_entropy_hierarchical(textC, 20)
    plot_entropy(entropyC, 'Text C conditional entropy (characters)', 'textC-entropy-chars.pdf')

    wordsC = re.findall("(?:\w+[-\'])+\w+|\w+", textC)

    entropyC = measure_conditional_entropy_hierarchical(wordsC, 9)
    plot_entropy(entropyC, 'Text C conditional entropy (tokens)', 'textC-entropy-words.pdf')
    
    trainSize = int(0.6 * len(wordsC)) 
    trainWordsC = wordsC[0:trainSize]
    testWordsC = wordsC[trainSize:]
    
    ngramCountsTrainC = count_ngrams_hierarchical(trainWordsC, 2)
    d = 0.7
    mdl = discounting_model(testWordsC, d, ngramCountsTrainC[1], ngramCountsTrainC[2])
    ngramCountsTestC = count_ngrams_hierarchical(testWordsC, 2)
    allWordsTestC = ngramCountsTestC[0]
    jointProbabilityTestC = dict((bigram,bigramCount/allWordsTestC)
                                 for bigram,bigramCount in ngramCountsTestC[2].items())
    # Verify that the joint probability sums to one
    assert(abs(sum(jointProbabilityTestC.values())-1) < 1e-4)
    # Verify that the discounted conditional probability for P(w|'the') sums to one 
    assert(abs(sum(mdl[('the',token)] for token in set(wordsC))-1) < 1e-4)
    
    H = compute_perplexity(jointProbabilityTestC, mdl)
    
    shouldPlot = True
    if shouldPlot:
        perplexity_of_d = lambda d: compute_perplexity(jointProbabilityTestC, discounting_model(testWordsC, d, ngramCountsTrainC[1], ngramCountsTrainC[2]))
        x=tuple(x/100 for x in range(1,100))
        y=tuple(perplexity_of_d(d) for d in x)
        plt.clf()
        plt.xlabel('d parameter')
        plt.ylabel('Perplexity')
        plt.plot(x, y)
    plt.savefig('perplexityC.pdf')
