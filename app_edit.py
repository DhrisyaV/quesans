from flask import Flask, request, render_template, url_for, redirect, flash, session, g, send_file, abort

import gensim
from nltk.tokenize import word_tokenize
import csv
import os
import glob
import re
import ab
import spell
import cosine_sim_edit
from nltk.corpus import stopwords
path1='/home/dhrisya/Documents/mtech/csv_data'
#from sqlalchemy.exc import IntegrityError
#from textblob import TextBlob
#import json,nltk,urllib2,re,pattern.en,calendar,wikipedia
#from math import radians, cos, sin, asin, sqrt
#from datetime import date,datetime
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
    orgqstn= org_qstn.split()
    #row[1] = row[1].dict_trim_by_keys(gl.text_analytics.stopwords(), exclude=True)
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
app = Flask(__name__)

app.config.from_object('config')
#from models import Properties,History
#from models import db

#db.init_app(app)

question = ""
qwords=('what','who','when','where','which','do','how', 'why','does',' ',"what's")
#f=[w for w in word_t if not w in stopword]
stop_word = set(stopwords.words('english'))
@app.route('/', methods=['GET', 'POST'])

def index():
	global question
	if request.method == 'GET':
		#history = History.query.order_by(History.id.desc()).limit(9)
		return render_template('index.html',page="home")
	elif request.method == 'POST':
		history = [" U.S Invade Iraq",
                 "yawns contagious",
             " kid usually move sleeping crib bed",
             "juice from orange peel supposed good eyes",
            "coffee bad skin"]
		ans=[]
		app.logger.info(repr(request.form))
		question = request.form['question']

		#get category
		question = question.replace('?','')
		question = raw_input('enter the question')
		category = raw_input('enter the category')
		sub_category = raw_input('enter the sub_category')
		print question
		q_edit = prepro(question)
		q_edit = preprocess1(q_edit)
        for file_name in sorted(glob.glob(os.path.join(path1,'data1.csv'))):
        	with open(file_name, 'rb') as inp:
        		for row in csv.reader(inp):
					topic_text=""
					if row[1]==category:
						if cosine_sim_edit.main(row[2],sub_category)>0:
							val = cosine_sim_edit.main(row[4],q_edit)
							for i in row[5]:
								
								topic_text=topic_text+i
							if topic_text:
								
								val1=cosine_sim_edit.main(topic_text,q_edit)
								if val>0 and val1>0:
									#print row[3], val, val1
									k=(row[3],val1)
									ans.append(k)
		print ans
							#elif val>0:
								#print row[3], val





		"""raw_documents = [" U.S Invade Iraq",
                 "yawns contagious",
             " kid usually move sleeping crib bed",
             "juice from orange peel supposed good eyes",
            "coffee bad skin"]
		print("Number of documents:",len(raw_documents))


		gen_docs = [[w.lower() for w in word_tokenize(text)] 
        		    for text in raw_documents]
		print(gen_docs)

		dictionary = gensim.corpora.Dictionary(gen_docs)
		print(dictionary[5])
		#print(dictionary.token2id['Iraq'])
		print("Number of words in dictionary:",len(dictionary))
		for i in range(len(dictionary)):
			print(i, dictionary[i])

		corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
		print(corpus)

		tf_idf = gensim.models.TfidfModel(corpus)
		print(tf_idf)
		s = 0


		for i in corpus:
			s += len(i)
		print(s)

		sims = gensim.similarities.Similarity('/home/dhrisya/Documents/mtech/Review',tf_idf[corpus],
                                      num_features=len(dictionary))
		print(sims)
		print(type(sims))

		query_doc = [w.lower() for w in word_tokenize(question)]
		print(query_doc)
		query_doc_bow = dictionary.doc2bow(query_doc)
		print(query_doc_bow)
		query_doc_tf_idf = tf_idf[query_doc_bow]
#print(query_doc_tf_idf)

		print sims[query_doc_tf_idf]"""
		return render_template('index.html',page="home",history=history)



		"""blob = TextBlob(question)				#tags the question
		q_tagged = blob.tags
		app.logger.info(repr(q_tagged))

		parsed = parse(q_tagged)
		q_noun = parsed['q_noun']
		typ = parsed['type']
		noun_save = parsed['noun_save']

		ques = History.query.filter_by(q_noun = noun_save).first()
		if ques:
			if ques.content == "list":
				answer = []
				word=""
				for i in ques.answer:
					if i == ",":

						answer.append(word)
						word=""
					else:
						word = word+str(i)
				answer = [tuple(answer[i:i+3]) for i in range(0, len(answer), 3)]
				app.logger.info(repr(answer))
			else:
				answer = ques.answer


			value = {'question':question,'answer':answer, 'content' : ques.content}
			typ = "From history"


		if typ == "keyword":
			app.logger.info(repr("keyword"))
			quest = []
			quest.append(question)
			searched = wikidata_search(quest)
			qid = searched['qid']

			if qid == False:
				answer = searchwiki(question.replace(' ','+'))
				if answer == False:
					answer = "As of now, the System is unable to answer the question."

			else:
				app.logger.info(repr(qid))
				data = wikidata_get_entity(qid)
				if 'description' in data['entities'][qid]:
					answer = data['entities'][qid]['description']['en']['value']
				else:
					answer = data['entities'][qid]['descriptions']['en']['value']

			value = {'question':question,'answer':answer, 'content' : "string"}


		if typ == "list":
			app.logger.info(repr("list"))
			
			np_tree=parsed['np_tree']
			value = get_list(q_noun,np_tree)
			if value==True:
				value = "As of now, the System is unable to answer the question."
				value = {'question':question,'answer':answer, 'content' : "string"}
		if typ == "general":
			app.logger.info(repr("general"))
			result = get_property(q_noun)
			if result:
				pty = result['property']
				q_noun = result['q_noun']
				value = get_general(q_noun,pty)
			else:
				answer = "As of now, the System is unable to answer the question."
				value = {'question':question,'answer':answer, 'content' : "string"}
			
		if typ == "distance":
			app.logger.info(repr("distance"))
			value = get_distance(q_noun)
			if not value:
				answer = "As of now, the System is unable to answer the question."
				value = {'question':question,'answer':answer, 'content' : "string"}
		if typ == "time":
			app.logger.info(repr("time"))
			answer = get_date(q_noun)
			value = {'question':question,'answer':answer, 'content' : "string"}

		if typ == "description":
			app.logger.info(repr("description"))
			value = get_description(q_noun)
			if not value:
				value = {'question':question,'answer':"As of now, the System is unable to answer the question.", 'content' : "string"}

		if typ !="From history":
			answer = ""
			if value['content']=="list":
				for jdx,j in enumerate(value['answer']):
					for i in value['answer'][jdx]:
						answer += str(i) + ", "
				saveqa(question,noun_save,answer,value['content'])
			else:
				saveqa(question,noun_save,value['answer'],value['content'])
			
		flash(value,'success')
		app.logger.info(repr(value))"""
		





if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050)