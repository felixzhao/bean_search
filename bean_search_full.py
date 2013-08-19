# merge functions

import sys
import math
from heapq import *

def calcdist(x, y):
    res = 0.0
    for i in range(len(x)):
        res += (x[i]-y[i]) ** 2
    return math.sqrt(res)

def calcMatchScore(w1, w2, knn, trainvectors, testvectors):
    res = 0.0
    i = 0
    for w in knn:
        d1 = calcdist(trainvectors[w2],trainvectors[w])
        d2 = calcdist(testvectors[w1],testvectors[w])
        i+=1
        res += (d1-d2)**2 / i
    return res
    
# get match word & match_score in train_words to test_word
# which size based on topnum
# "knn", "test_vectors" could be change in bean_search
def getmatchswithscore(match_word_test, trainvectors, testvectors, topnum):
  matchs = []
  
  trainwords = set(trainvectors.keys())
  testwords = set(testvectors.keys())
  knownwords = trainwords & testwords
  matchwords_train = list(trainwords - knownwords)
  
# Get knn
# calculate clostest known_words in test_vectors which count is topnum
# The test_vectors could be change in bean search
  heap = []
  knn = []
  for known_word in knownwords:
    dist = calcdist(testvectors[match_word_test],testvectors[known_word])
    heappush(heap, (dist,known_word))
  for item in nsmallest(topnum, heap):
    knn.append(item[1])
# End of Get knn  

# Get match words 
# get match word & match_score in train_words to test_word
# which size based on topnum
# "knn", "test_vectors" could be change in bean_search 
  heap = []
  for match_word_train in matchwords_train:
    print >>sys.stderr, 'Generating match scores for: ', match_word_train, ' and ', match_word_test
    match_score = calcMatchScore(match_word_test, match_word_train, knn, trainvectors, testvectors)
    heappush(heap, (match_score,match_word_train))
  for item in nsmallest(topnum, heap):
    matchs.append(item)
# end for Get match words
  return matchs

def updatevector(match_word_test, match_word_train, train_vecotrs, test_vectors):
  updated_vectors = test_vectors.copy()
  updated_vectors[match_word_train] = train_vecotrs[match_word_train]
  del updated_vectors[match_word_test]
  return updated_vectors

def nwindow(word_list, trainvectors, testvectors):
  result = (sys.float_info.max, [])
  word = word_list[0]
  topnum = 10
  match_list = getmatchswithscore(word, trainvectors, testvectors, topnum)
#  print('word : ' + word + ' ; match_list : ')
#  print(match_list)
  round_min_con_score = sys.float_info.max
  for match_word in match_list:
    con_score = match_word[0]
    candidate_word_list = []
    candidate_word_list.append(match_word[1])
    if len(word_list) > 1:
      updated_vec = updatevector(word, match_word[1], trainvectors, testvectors)
      candidate = nwindow(word_list[1:], trainvectors, updated_vec) 
      con_score += candidate[0] # calculate combination score
      candidate_word_list += candidate[1]
    if con_score < round_min_con_score :
      round_min_con_score = con_score
      result = (round_min_con_score, candidate_word_list)
#  print('*** match word : ')
#  print(result[1])
#  print( '*** score : ' + str(result[0]))
#  print(' ========================= ')
  return result

def bean_search(trainvectors, testvectors, window_size):
  result = []
  ## define
  trainwords = set(trainvectors.keys())
  testwords = set(testvectors.keys())
  knownwords = trainwords & testwords
  matchwords_train = list(trainwords - knownwords)
  matchwords_test = []
  for w in testwords:
    if w.startswith('<unk>'):
        matchwords_test.append(w)

# get ngram list
  ngram_list = []
  for i in range(len(word_list)):
      ngram_list.append(word_list[i:window_size+i])
# end of get ngram list
  
  updated_vec = testvectors.copy()
  for ngram in ngram_list:
    match_item = nwindow(ngram, trainvectors, updated_vec)
    org_word = ngram[0]
    rpl_word = match_item[1][0]
    print(org_word + ' ; ' + rpl_word)
    updated_vec = updatevector(org_word, rpl_word, trainvectors, updated_vec)
    result.append((org_word, rpl_word))
  return result
    
if __name__ == '__main__':
  ## init data
  trainvectors = {'a':[2,5], 'b':[4,4], 'c':[5,2], 'k':[2,4]}
  testvectors = {'<unk>1':[2,1], '<unk>2':[1,3], '<unk>3':[3,2], 'k':[2,4]}
  word_list = ['<unk>1', '<unk>2', '<unk>3']
  ## expected 
  expected = [('<unk>1','c'), ('<unk>2','a'), ('<unk>3','b')]
  ## get result
  actual = bean_search(trainvectors, testvectors,2)
  ## pirnt out result
  print(expected == actual)
  print(' ************ ')
  print('best match : ')
  for item in actual:
    print(str(item[0]) + ' => match to => ' + str(item[1]))
  