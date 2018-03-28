import graphlab
import numpy as np
import pandas as pd
import os
import glob
path1='/home/dhrisya/Documents/mtech/csv_data'
def writeDict(Dict, filename, sep) :
    with open(filename, 'w') as f:
        for key,value in sorted( Dict.items() ) :
            f.write( str(key) + sep + str(value) + '\n')
for file_name in sorted(glob.glob(os.path.join(path1,'newdata1.csv'))):
# Use graphlab to read question_content
	question_content = graphlab.SFrame.read_csv(file_name)

	#question_content['sim_check_content'] =question_content['question'] 
		
	

	
	
	question_content['word_count'] = graphlab.text_analytics.count_words(question_content['question'])
	tfidf = graphlab.text_analytics.tf_idf(question_content['word_count'])
	question_content['tfidf'] = tfidf

	knn_model = graphlab.nearest_neighbors.create(question_content, features=['tfidf'], label='question')





	Similar_Qid_List = {}
	# for i in range(10) :

	for i in range( len(question_content) ) :
		key = 'Q' + str(i) + '_Similar_List'
		Q_i = question_content[i:i+1]
		value = knn_model.query(Q_i, k=3)['reference_label']
		Similar_Qid_List[key] = value

	writeDict(Similar_Qid_List, 'Similar_Qid.csv', ':')
