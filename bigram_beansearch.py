import matchswithscore
import updatevec
import gzip

def combinationscore(score_list):
  score = 0
  score = sum(score_list)
  return score

def bigram(word_1, word_2, trainvectors, testvectors):
  fixed_word = ''
  topnum = 10
  word_1_match_list = matchswithscore.getmatchswithscore(word_1, trainvectors, testvectors, topnum)
  max_combination_score = 0
  for word_1_match_tuple in word_1_match_list:
    match_word = word_1_match_tuple[1]
    word_1_match_word_score = word_1_match_tuple[0]
    updated_vec = updatevec.updatevector(word_1, match_word, trainvectors, testvectors)
    word_2_match_list = matchswithscore.getmatchswithscore(word_2, trainvectors, updated_vec, topnum)
    for word_2_match_tuple in word_2_match_list:
      word_2_match_word_score = word_2_match_tuple[0]
      combination_score = combinationscore([word_1_match_word_score, word_2_match_word_score])
      if combination_score > max_combination_score :
        max_combination_score = combination_score
        fixed_word = word_1_match_tuple[1]
  return fixed_word
  
if __name__ == '__main__':
  ## load files
  # trainfile = gzip.open(sys.argv[1], "rb")
  # testfile = gzip.open(sys.argv[2], "rb")
  train_path = 'C:\\Users\\zhaoqua\\Documents\\GitHub\\bean_search\\test2\\embed-train-full.txt.gz'
  test_path = 'C:\\Users\\zhaoqua\\Documents\\GitHub\\bean_search\\test2\\embed-test-full-33percent.txt.gz'
  trainfile = gzip.open(train_path, "rb")
  testfile = gzip.open(test_path, "rb")

  ## define
  trainwords = set()
  testwords = set()
  matchwords_train = []
  matchwords_test = []
  trainvectors = {}
  testvectors = {}
  ## load data
  ## load train data
  for l in trainfile.readlines():
    toks = l.split()
    if toks[0] == '*UNKNOWN*':
      continue
    #trainwords.add(toks[0])
    trainvectors[toks[0]] = [float(f) for f in toks[1:]]
  ## load test data
  for l in testfile.readlines():
    toks = l.split()
    if toks[0] == '*UNKNOWN*':
      continue
    testwords.add(toks[0])
    testvectors[toks[0]] = [float(f) for f in toks[1:]]
  ## get match words test
  for w in testwords:
    if w.startswith('<unk>'):
      matchwords_test.append(w)
  word_1 = matchwords_test[0]
  word_2 = matchwords_test[1]
  ## get result
  best_match = bigram(word_1, word_2, trainvectors, testvectors)
  ## pirnt out result
  print('best_match : ' + best_match)