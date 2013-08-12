#!/usr/bin/env python

#from __future__ import print_function
import sys
import string, gzip
import math
import pickle
from collections import defaultdict
from multiprocessing import Pool
from heapq import *

trainfile = gzip.open(sys.argv[1], "rb").readlines()
testfile = gzip.open(sys.argv[2], "rb").readlines()

fout_matrix = open('res3/matrix.pkl', 'w')
fout_test = open('res3/test_match.words.txt','w')
fout_train = open('res3/train_match.words.txt','w')
fout = open('res3/out.txt', 'w')

trainwords = set()
testwords = set()
knownwords = set()
matchwords_train = []
matchwords_test = []
trainvectors = {}
testvectors = {}
traindist = defaultdict(dict)
testdist = defaultdict(dict)

def calcdist(x, y):
    res = 0.0
    for i in range(len(x)):
        res += (x[i]-y[i]) ** 2
    return math.sqrt(res)

def calcMatchScore(w1, w2, knn):
    res = 0.0
    i = 0
    for w in knn:
        d1 = calcdist(trainvectors[w2],trainvectors[w])
        d2 = calcdist(testvectors[w1],testvectors[w])
        i+=1
        res += (d1-d2)**2 / i
    print(str(res))
    return res

#Read files
for l in trainfile:
    toks = l.split()
    if toks[0] == '*UNKNOWN*':
        continue
    trainwords.add(toks[0])
    trainvectors[toks[0]] = [float(f) for f in toks[1:]]
for l in testfile:
    toks = l.split()
    if toks[0] == '*UNKNOWN*':
        continue
    testwords.add(toks[0])
    testvectors[toks[0]] = [float(f) for f in toks[1:]]

knownwords = trainwords & testwords
matchwords_train = list(trainwords - knownwords)
#Deal with the OOV words in test corpus
#matchwords_test = list(testwords - knownwords)
for w in testwords:
    if w.startswith('<unk>'):
        matchwords_test.append(w)


print >>sys.stderr, 'Dumping Matchwords'
for word in matchwords_test:
    print >>fout_test, word
for word in matchwords_train:
    print >>fout_train, word

#pickle.dump(matchwords_test, fout_matrix)
#pickle.dump(matchwords_train, fout_matrix)

matrix = []
topnum = 50
for word in matchwords_test:
    heap = []
    knn = []
    for w in knownwords:
        dist = calcdist(testvectors[word],testvectors[w])
        heappush(heap, (dist,w))
    for item in nsmallest(topnum, heap):
        knn.append(item[1])
        #print(word + item[1] + '' + str(item[0]))
    #print('\n')
    
    row = []
    results = []

    for w in matchwords_train:
        print >>sys.stderr, 'Generating match scores for:', w, 'and', word
        #results.append(calcMatchScore, (word, w, knn))
        #row.append(calcMatchScore(word, w, knn))
        num = calcMatchScore(word, w, knn)
        print(str(num))
