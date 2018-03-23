import re, math
from collections import Counter
import nltk
from nltk.corpus import wordnet
synonyms = []

 


WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     #print intersection
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
	words = WORD.findall(text)
	for i in words:
		for syn in wordnet.synsets(i):
			for l in syn.lemmas():
				synonyms.append(l.name())
	return Counter(synonyms)

def text_to_vector2(text):
     words = WORD.findall(text)
     return Counter(words)

#text1 = 'Primary Secondary Education'
#text2 = 'Other - Education'
#maincat exactly same row[1]
#subcat similarity greater than 0.9
#check similarity of both preprocessed question and topics found out

def main(text1,text2):
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    #print vector1
    #print vector2
    cosine = get_cosine(vector1, vector2)

    print 'Cosine:', cosine
    return cosine