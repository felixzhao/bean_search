#!/usr/bin/env python

#from __future__ import print_function
import sys
import string, gzip
import math
import pickle
from collections import defaultdict
from multiprocessing import Pool
from heapq import *

trainfile = gzip.open(sys.argv[1], "rb")
testfile = gzip.open(sys.argv[2], "rb")

fout_matrix = open('C:/Users/zhaoqua/Documents/GitHub/bean_search/res/matrix.pkl', 'w')
fout_test = open('C:/Users/zhaoqua/Documents/GitHub/bean_search/res/test_match.words.txt','w')
fout_train = open('C:/Users/zhaoqua/Documents/GitHub/bean_search/res/train_match.words.txt','w')
fout = open('C:/Users/zhaoqua/Documents/GitHub/bean_search/res/out.txt', 'w')

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
    return res

#Read files
for l in trainfile:
    toks = string.split(l)
    if toks[0] == '*UNKNOWN*':
        continue
    trainwords.add(toks[0])
    trainvectors[toks[0]] = [float(f) for f in toks[1:]]
for l in testfile:
    toks = string.split(l)
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

print >>sys.stderr, 'Generating Matrix'
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

    row = []
    results = []
    #pool = Pool(processes = 8)
    for w in matchwords_train:
        print >>sys.stderr, 'Generating match scores for:', w, 'and', word
        results.append(calcMatchScore(word, w, knn))
        #results.append(pool.apply_async(calcMatchScore, (word, w, knn)))
        #row.append(calcMatchScore(word, w, knn))
    #pool.close()
    #pool.join()
    for res in results:
        #row.append(res.get())
        row.append(res)
    matrix.append(row)

print >>sys.stderr, 'Dumping Matrix'
pickle.dump(matrix, fout_matrix)


#print >>sys.stderr, 'Generating Matrix'
#matrix = []
#for word2 in matchwords_test:
#    pool = Pool(processes = 8)
#    row = []
#    results = []
#    for word in matchwords_train:
#        print >>sys.stderr, 'Generating match scores for:', word2, 'and', word
#        results.append(pool.apply_async(calcMatchScore, (word, word2)))
#    pool.close()
#    pool.join()
#    for res in results:
#        row.append(res.get())
#    matrix.append(row)
#
#print >>sys.stderr, 'Dumping Matrix'
#pickle.dump(matrix, fout_matrix)
#
#print >>sys.stderr, 'Beginning Computing Matching'
#munkres = Munkres()
#print >>sys.stderr, 'Computing Matching'
#indexes = munkres.compute(matrix)
#print >>sys.stderr, 'Computation Finished'
#
#for row, column in indexes:
#    value = matrix[row][column]
#    print >>fout, '(%s, %s) -> %d' % (matchwords_test[row], matchwords_train[column], value)
