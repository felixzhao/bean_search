def getngrams(word_list,n):
  ngrams = []
  for i in range(len(word_list)):
    if i != len(word_list) - 1: # exclude one node element
      ngrams.append(word_list[i:n+i])
  return ngrams

def unittest(word_list, n):
  ngram_list = getngrams(word_list,n)
  print(' n = ' + str(n) + ' :')
  print(' ********* ')
  for gram in ngram_list:
    print(gram)
  
if __name__ == '__main__':
  word_list = ['a','b','c','d','e']
  n = 3
  expected = [['a','b','c'],['b','c','d'],['c','d','e'],['d','e']]
  actual = getngrams(word_list, n)
  print(expected == actual)
  print(actual)