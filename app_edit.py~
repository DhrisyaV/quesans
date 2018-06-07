#!/usr/bin/python

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
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
path1='/home/dhrisya/Documents/mtech/csv_data/'
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
        word = word.rstrip('.,!?;:')
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
		#question = raw_input('enter the question')
		category = raw_input('enter the category')
		sub_category = raw_input('enter the sub_category')
		print question
		q_edit = prepro(question)
		q_edit = preprocess1(q_edit)
        for file_name in sorted(glob.glob(os.path.join(path1,'data1.csv'))):
        	print file_name
        	with open(file_name, 'rb') as inp:
        		for row in csv.reader(inp):
					topic_text=""
					if row[1]==category:
						if cosine_sim_edit.main(row[2],sub_category)>0:
							val = cosine_sim_edit.main(row[4].lower(),q_edit)
							for i in row[5]:
								
								topic_text=topic_text+i
							if topic_text:
								
								val1 = cosine_sim_edit.main(topic_text.lower(),q_edit)
								if val>0.01 and val1>0.01:
									#print row[3], val, val1
									k=(row[3],val1)
									ans.append(k)
		ans=sorted(ans, key=lambda x:x[1], reverse=True)
		print ans[0:10]
	return render_template('index.html',page="home",history=history)

		





if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050)