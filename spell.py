import enchant
#import nltk
d = enchant.Dict("en_US")
from enchant.checker import SpellChecker
def main(g):
  chkr = SpellChecker("en_US")
  #g='It is really anoying. plaese dont buy'
  #lis=nltk.word_tokenize(g)
  #final=''
  #for i in lis:
  chkr.set_text(g)
  for err in chkr:
    print "ERROR:", err.word
    if d.suggest(err.word):
        sug=d.suggest(err.word)
        g=sug[0]
  return g
