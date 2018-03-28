import re, math
from collections import Counter
import nltk
from nltk.corpus import wordnet
from textblob import TextBlob


adje = re.compile("JJ.*") 
noun = re.compile("NN.*")
verb = re.compile("VB.*")
WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     print intersection
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

    
def text_to_vector(text): 
    #words = WORD.findall(text)
    synonyms=[]
    blob = TextBlob(text)           #tokenize the question
    q_tagged = blob.tags
    for i in q_tagged:
        if adje.match(i[1]):
            tag_variable = 'a'
        elif noun.match(i[1]):
            tag_variable = 'n'
        elif verb.match(i[1]):
            tag_variable = 'v'
        else:
            continue
        k=[]
        for syn in wordnet.synsets(i[0]):
            syn_name = syn.name()
            syn_name_split = syn_name.split('.')

            if syn_name_split[1]==tag_variable:
                if syn_name_split[0] not in k:
                    print syn_name_split[0]
                    k.append(syn_name_split[0])
                    print syn_name
                    for l in syn.lemmas():
                        print l
                        for final_name in l.name().split('_'):
                            synonyms.append(final_name)
    return Counter(synonyms)

def text_to_vector2(text):
     words = WORD.findall(text)
     return Counter(words)

text1 = 'Programming'
text2 = 'Software'
#maincat exactly same row[1]
#subcat similarity greater than 0.9
#check similarity of both preprocessed question and topics found out

vector1 = text_to_vector(text1)
vector2 = text_to_vector(text2)
#print vector1
#print vector2
cosine = get_cosine(vector1, vector2)

print 'Cosine:', cosine
