def updatevector(match_word_test, match_word_train, train_vecotrs, test_vectors):
  updated_vectors = test_vectors.copy()
  updated_vectors[match_word_train] = train_vecotrs[match_word_train]
  del updated_vectors[match_word_test]
  return updated_vectors

if __name__ == '__main__':
  # define
  org_word = 'org'
  rpl_word = 'rpl'
  org_vec = {}
  org_vec['org'] = [1.1,1.2,1.3]
  org_vec['word'] = [2.1,2.2,2.3]
  rpl_vec = {}
  rpl_vec['rpl'] = [3.1,3.2,3.3]
  exp_vec = {}
  exp_vec['rpl'] = [3.1,3.2,3.3]
  exp_vec['word'] = [2.1,2.2,2.3]
  # call function
  act_vec = updatevector(org_word, rpl_word, org_vec, rpl_vec)
  # validation
  print( act_vec == exp_vec)
  for k in act_vec.keys():
    print( k + str(act_vec[k]))