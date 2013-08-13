import sys
import common
import string, gzip
from heapq import *
import knn

# get match word in train_words to test_word
# which size based on topnum
# "knn", "test_vectors" could be change in bean_search
def getmatchs(match_word_test, matchwords_train, knn, trainvectors, testvectors, topnum):
  heap = []
  matchs = []
  for match_word_train in matchwords_train:
    print >>sys.stderr, 'Generating match scores for: ', match_word_train, ' and ', match_word_test
    match_score = common.calcMatchScore(match_word_test, match_word_train, knn, trainvectors, testvectors)
    heappush(heap, (match_score,match_word_train))
  for item in nsmallest(topnum, heap):
    matchs.append(item[1])
  return matchs

# get match word list
# simplified parameters
def getmatchs(match_word_test, trainvectors, testvectors, topnum):
  matchs = []
  
  trainwords = set(trainvectors.keys())
  testwords = set(testvectors.keys())
  knownwords = trainwords & testwords
  matchwords_train = list(trainwords - knownwords)
  
  knn_topnum = 50 
  knn_res = knn.getknn(match_word_test, knownwords, testvectors, topnum)
  matchs = getmatchs(match_word_test, matchwords_train, knn_res,trainvectors, testvectors, topnum)
  return matchs

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
  knn_res = []
  match_word_test = matchwords_test[0]
  topnum = 50 
  knn_res = knn.getknn(match_word_test, knownwords, testvectors, topnum)
  
  # get match list
  topnum = 10 # this is the size of math words
  match_list = getmatchs(match_word_test, matchwords_train, knn_res,trainvectors, testvectors, topnum)
  
  #pirnt knn
  print('knn :')
  for word in knn_res:
    print(word)
  # pirnt out result
  print('match list : ')
  print(match_list)
  for word in match_list:
    print(word)