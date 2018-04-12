

import csv
import nltk
def main(word):
	#sentence=raw_input('enter the sentence:')

	#tokens = nltk.word_tokenize(sentence)
	#for word in tokens:
	with open('acrynom.csv', 'rb') as f:
		reader = csv.reader(f)
		
		for row in reader:
			if word == row[0]:
				#print  word,'->', row[1]
				word=row[1]
				break
	return word
        

