import matchswithscore
import updatevec
import gzip
import sys

def nwindow(word_list, trainvectors, testvectors):
  result_tuple = (sys.float_info.max, '')

  word = word_list[0]
  topnum = 10
  match_list = matchswithscore.getmatchswithscore(word, trainvectors, testvectors, topnum)
  
  print('word : ' + word + ' ; match_list : ')
  print(match_list)
  
  round_min_con_score = sys.float_info.max
  for match_word in match_list:
    con_score = match_word[0]
    if len(word_list) > 1:
      updated_vec = updatevec.updatevector(word, match_word[1], trainvectors, testvectors)
      candidate_tuple = nwindow(word_list[1:], trainvectors, updated_vec) 
      candidate_score = candidate_tuple[0]
      con_score += candidate_score # calculate combination score
    if con_score < round_min_con_score :
      round_min_con_score = con_score
      result_tuple = (round_min_con_score,match_word[1])
  print('match word : ' + result_tuple[1] + ' ; score : ' + str(result_tuple[0]))
      
  return result_tuple

if __name__ == '__main__':
  ## init data
  trainvectors = {'a':[5,5], 'b':[2,2], 'c':[3,3], 'k':[1,1]}
  testvectors = {'<unk>1':[9,9], '<unk>2':[8,8], '<unk>3':[7,7], 'k':[1,1]}
  word_list = ['<unk>1', '<unk>2', '<unk>3']
  ## expected 
  expected = (3,'b')
  ## get result
  actual = nwindow(word_list, trainvectors, testvectors)
  ## pirnt out result
  print(expected == actual)
  print('best_match word : ' + actual[1] + ' ; score : ' + str(actual[0]))