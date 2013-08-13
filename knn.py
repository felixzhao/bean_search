import sys
import common
import string, gzip
from heapq import *

# calculate clostest known_words in test_vectors which count is topnum
# The test_vectors could be change in bean search
def getknn(match_word_test, knownwords, testvectors, topnum):
  heap = []
  knn = []
  for known_word in knownwords:
    dist = common.calcdist(testvectors[match_word_test],testvectors[known_word])
    heappush(heap, (dist,known_word))
  for item in nsmallest(topnum, heap):
    knn.append(item[1])
  return knn

if __name__ == '__main__':

  # load files
  trainfile = gzip.open(sys.argv[1], "rb")
  testfile = gzip.open(sys.argv[2], "rb")

  # define
  trainwords = set()
  testwords = set()
  knownwords = set()
  matchwords_train = []
  matchwords_test = []
  trainvectors = {}
  testvectors = {}
  # load data
  # load train data
  for l in trainfile.readlines():
    toks = l.split()
    if toks[0] == '*UNKNOWN*':
      continue
    trainwords.add(toks[0])
    trainvectors[toks[0]] = [float(f) for f in toks[1:]]
  # load test data
  for l in testfile.readlines():
    toks = l.split()
    if toks[0] == '*UNKNOWN*':
      continue
    testwords.add(toks[0])
    testvectors[toks[0]] = [float(f) for f in toks[1:]]
  # get known words
  knownwords = trainwords & testwords
  # get match words train
  matchwords_train = list(trainwords - knownwords)
  # get match words test
  for w in testwords:
    if w.startswith('<unk>'):
      matchwords_test.append(w)
  # get knn
  knn = []
  match_word_test = matchwords_test[0]
  topnum = 10
  knn = getknn(match_word_test, knownwords, testvectors, topnum)
  print(knn)
  for w in knn:
    print(w)