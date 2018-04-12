#!/usr/bin/python

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import graphlab
import numpy as np
import pandas as pd
import os
import glob
import re
import spell
import ab
import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords
path1='/home/dhrisya/Documents/mtech/csv_data/concat_data'


brown_train = brown.tagged_sents(categories='learned')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"

def remove_non_ascii_1(text):

    return ''.join(i for i in text if ord(i)<128)
def prepro(org_qstn):
    re.sub(r'[^\w]', ' ', org_qstn)
    #print "after first re",org_qstn
    org_qstn=remove_non_ascii_1(org_qstn)
    #print "after second r",org_qstn
    org_qstn= org_qstn.decode('utf8', 'ignore')
    return org_qstn
def preprocess1(org_qstn):
	qwords=('what','who','when','where','which','do','how', 'why','does',' ',"what's")
    #f=[w for w in word_t if not w in stopword]
	stop_word = set(stopwords.words('english'))
	orgqstn= org_qstn.split()
	k=""
	for word in orgqstn:
		if word in ('.',',','?','!',';',':'):
			orgqstn.remove(word)
		word =  word.rstrip('.,!?;:')
		word=ab.main(word)
		word=spell.main(word)
		k = k+word+" "
	orgqstn= k.split()
	for word in orgqstn:
		if word.isdigit():
			orgqstn.remove(word)
		elif word.lower() in qwords:
			orgqstn.remove(word)
		elif word.lower() in stop_word:
			orgqstn.remove(word)
	org_qstn=" ".join(orgqstn)
	return org_qstn
class NPExtractor(object):

    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI":
            #if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches
def topicmod(sentence):

    #sentence = "I know it not right to hack but Tiger in Scania lvl 160 hacks so that kinda got me going.  Im in Bera lvl 44 cleric and I want vac hack, item duplication hack, or other sweet hacks.  can u tell me a siie THAT is FReE? All the sites I went on suc.Plz im poor too; only 26k.T_T I know u probabaly want to stick the middle finger at me but I want hacks, Tiger and others make me jealous.  Thnx for even looking at this question."
    np_extractor = NPExtractor(sentence)
    result = np_extractor.extract()
    return result
def writeDict(Dict, filename, sep) :
    with open(filename, 'w') as f:
        for key,value in sorted( Dict.items() ) :
            f.write( str(key) + sep + str(value) + '\n')
for file_name in sorted(glob.glob(os.path.join(path1,'newdata1.csv'))):
# Use graphlab to read question_content
	question_content = graphlab.SFrame.read_csv(file_name)

	question_content['sim_check_content'] = question_content['question']+question_content['sub_category']+question_content['main_category']
		
	

	
	
	question_content['word_count'] = graphlab.text_analytics.count_words(question_content['sim_check_content'])
	tfidf = graphlab.text_analytics.tf_idf(question_content['word_count'])
	question_content['tfidf'] = tfidf

	knn_model = graphlab.nearest_neighbors.create(question_content, features=['tfidf'], label='question')





	"""Similar_Qid_List = {}
	# for i in range(10) :
	i=10
	#for i in range( len(question_content) ) :
	key = 'Q' + str(i) + '_Similar_List'
	Q_i = question_content[i:i+1]
	value = knn_model.query(Q_i, k=3)['reference_label']
	Similar_Qid_List[key] = value"""
	#question = 'How does human evolution happen'
	#q_edit = prepro(question)
	#q_edit = preprocess1(q_edit)

	p= graphlab.SFrame({'main_category':['Cars & Transportation'],
						'sub_category':['Buying & Selling'],
						'question':['looking for a new car']})
    #'pre_question':[q_edit],'topic':topicmod(q_edit),'content':['']})
p['word_count'] = graphlab.text_analytics.count_words(p['question'])
tfidf = graphlab.text_analytics.tf_idf(p['word_count'])
p['tfidf'] = tfidf
q={}
val = knn_model.query(p,k=10)['reference_label']
q['1'] = val
writeDict(q, 'Similar_Question_ed.csv', ':')
