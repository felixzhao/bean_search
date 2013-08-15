import matchswithscore
import updatevec
import gzip
import sys

def nwindow(word_list, trainvectors, testvectors):
  result = (sys.float_info.max, [])
  word = word_list[0]
  topnum = 10
  match_list = matchswithscore.getmatchswithscore(word, trainvectors, testvectors, topnum)
#  print('word : ' + word + ' ; match_list : ')
#  print(match_list)
  round_min_con_score = sys.float_info.max
  for match_word in match_list:
    con_score = match_word[0]
    candidate_word_list = []
#    candidate_word_list.append(match_word[1])
    candidate_word_list.append(match_word[1])
    if len(word_list) > 1:
      updated_vec = updatevec.updatevector(word, match_word[1], trainvectors, testvectors)
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

if __name__ == '__main__':
  ## init data
  trainvectors = {'a':[5,5], 'b':[2,2], 'c':[3,3], 'k':[1,1]}
  testvectors = {'<unk>1':[9,9], '<unk>2':[8,8], '<unk>3':[7,7], 'k':[1,1]}
  word_list = ['<unk>1', '<unk>2', '<unk>3']
  ## expected 
  expected = 'a'
  ## get result
  actual = nwindow(word_list, trainvectors, testvectors)
  ## pirnt out result
  print(expected == actual[1][0])
  print('best_match is the first word in list : ')
  print(actual[1])
  print(' ; score : ' + str(actual[0]))