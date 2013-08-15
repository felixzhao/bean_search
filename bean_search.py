import ngrams
import nwindow_beansearch
import updatevec

def bean_search(trainvectors, testvectors):
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
  window_size = 3
  
  ngram_list = ngrams.getngrams(matchwords_test, window_size)

  updated_vec = testvectors.copy()
  for ngram in ngram_list:
    match_item = nwindow_beansearch.nwindow(ngram, trainvectors, updated_vec)
    org_word = ngram[0]
    rpl_word = match_item[1][0]
    print(org_word + ' ; ' + rpl_word)
    updated_vec = updatevec.updatevector(org_word, rpl_word, trainvectors, updated_vec)
    result.append((org_word, rpl_word))
  return result
    
if __name__ == '__main__':
  ## init data
  trainvectors = {'a':[2,5], 'b':[4,4], 'c':[5,2], 'k':[2,4]}
  testvectors = {'<unk>1':[2,1], '<unk>2':[1,3], '<unk>3':[3,2], 'k':[2,4]}
  word_list = ['<unk>1', '<unk>2', '<unk>3']
  ## expected 
  expected = [('<unk>1','b'), ('<unk>2','a'), ('<unk>3','c')]
  ## get result
  actual = bean_search(trainvectors, testvectors)
  ## pirnt out result
  print(expected == actual)
  print(' ************ ')
  print('best match : ')
  for item in actual:
    print(str(item[0]) + ' => match to => ' + str(item[1]))
  