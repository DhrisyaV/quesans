#!/usr/bin/python

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xml.etree.ElementTree as ET
from xmlutils.xml2csv import xml2csv
import csv
import os
import glob
import nltk
import re
import spell
import ab
#import cosine_sim
from nltk.corpus import brown
#import graphlab as gl
from nltk.corpus import stopwords


def remove_non_ascii_2(text):
    return re.sub(r'[^\x0-\x7F]',' ', text)
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
#############################################################################
def remove_non_ascii_1(text):

    return ''.join(i for i in text if ord(i)<128)


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


# Main method, just run "python np_extractor.py"
def topicmod(sentence):

    #sentence = "I know it not right to hack but Tiger in Scania lvl 160 hacks so that kinda got me going.  Im in Bera lvl 44 cleric and I want vac hack, item duplication hack, or other sweet hacks.  can u tell me a siie THAT is FReE? All the sites I went on suc.Plz im poor too; only 26k.T_T I know u probabaly want to stick the middle finger at me but I want hacks, Tiger and others make me jealous.  Thnx for even looking at this question."
    np_extractor = NPExtractor(sentence)
    result = np_extractor.extract()
    return result
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

    


path1='/home/cse/Documents/xml/200_600'
i=201
stat={}
qwords=('what','who','when','where','which','do','how', 'why','does',' ',"what's")
#f=[w for w in word_t if not w in stopword]
stop_word = set(stopwords.words('english'))
for file_name in sorted(glob.glob(os.path.join(path1,'*.xml'))):
    print file_name
    tree = ET.parse(file_name)
    root = tree.getroot()
    Final_data = open('/tmp/data%s.csv' %i, 'w')

# create the csv writer object

    csvwriter = csv.writer(Final_data)

    count = 0
    for doc in root.findall('vespaadd'):
        
        member = doc.find('document')
        if member.find('qlang').text == 'en':
            firstrow = []
            if member.find('cat') is not None:
                cat = member.find('cat').text
                firstrow.append(cat)
            else:
                firstrow.append(' ')
            if member.find('maincat') is not None:
                maincat = member.find('maincat').text
                firstrow.append(maincat)
                """if maincat in stat:
                    stat[maincat]+=1
                else:
                    stat[maincat]=1"""
            else:
                firstrow.append(' ')
          
            if member.find('subcat') is not None:
                subcat = member.find('subcat').text
                firstrow.append(subcat)
            else:
                firstrow.append(' ')
        
            q = member.find('subject').text
            q=remove_non_ascii_1(q)
            firstrow.append(q)
            q_ed = prepro(q)
            q_ed=preprocess1(q_ed)
            firstrow.append(q_ed)
            rs = topicmod(q_ed)
            firstrow.append(rs)

            if member.find('content') is not None:
                q_content = member.find('content').text
                q_content = remove_non_ascii_1(q_content)
                q_content.encode('utf-8')
                q_content = prepro(q_content)
                firstrow.append(q_content)
            else: 
                firstrow.append(' ')
        
            if member.find('bestanswer') is not None:
                BestAns = member.find('bestanswer').text
                BestAns=remove_non_ascii_1(BestAns)
                BestAns = prepro(BestAns)
                firstrow.append(BestAns)
            else: 
                firstrow.append(' ')
            if member.find('nbestanswers') is not None:
                answers = member.find('nbestanswers')
                for j in answers.findall('answer_item'):
                    k=remove_non_ascii_1(j.text)
                    k = prepro(k)
                    firstrow.append(k)

        
        
            print firstrow
            csvwriter.writerow(firstrow)
    i+=1
    Final_data.close()
"""data=[]
statistics=open('/tmp/statis.csv','w')
csvwriter=csv.writer(statistics)
for iter in stat:
    data.append(iter)
    data.append(stat[iter])
    converter = xml2csv(file_name, "data%s.csv" %i, encoding="utf-8")
    converter.convert(tag="vespaadd")
    with open('data%s.csv' %i, 'rb') as inp, open('data_edit%s.csv' %i, 'wb') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            #print row
            flag=0
            for i in range(12,14):
                if row[i] in ("en", "us", "en-us", "document_qlang"):
                    flag=1
            if flag == 1:
                #print "question after",row[1]
                org_qstn=row[1]


                re.sub(r'[^\w]', ' ', org_qstn)
                #print "after first re",org_qstn
                org_qstn=remove_non_ascii_1(org_qstn)
                #print "after second r",org_qstn
                org_qstn= org_qstn.decode('utf8', 'ignore')
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
                print k
                orgqstn= k.split()
                for word in orgqstn:
                    
                    if word.isdigit():
                        orgqstn.remove(word)
                    elif word.lower() in qwords:
                        orgqstn.remove(word)
                        
                    
                    elif word.lower() in stop_word:
                        orgqstn.remove(word)
                        

                org_qstn=" ".join(orgqstn)
                
                
                    

                rs = topicmod(org_qstn)
                writer.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[13], rs, org_qstn))
	i+=1
    	


# This is a fast and simple noun phrase extractor (based on NLTK)
# Feel free to use it, just keep a link back to this post
# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
# Create by Shlomi Babluki
# May, 2013


# This is our fast Part of Speech tagger
#############################################################################

"""
