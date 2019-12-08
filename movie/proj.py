import os
import sys
import pickle
import nltk
import csv
import json
import math
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
ps=PorterStemmer()
import sklearn


########################################################################
### 

def term_frequency(doc,term):
    count=0
    for word in doc:
        if term==word:
            count+=1
    return count/len(doc)

def bm25(query, num_docs_contain, this_doc, total_docs, avg_len, b, k):
    score = 0
    for term in query:
        contain=0
        #total_docs=len(total_docs_file)
        for i in num_docs_contain:
            if term in i:
                contain+=1
        idf = math.log((total_docs - contain + 0.5) / (contain + 0.5))# / math.log(1.0 + total_docs)
        tf = term_frequency(this_doc,term)
        score = score + ( tf* idf * (k + 1)) / (tf + k * (1 - b + (b * (len(this_doc)/avg_len))))
    return score

count=0
title=[]
for line in open('title.dat', 'r',encoding="ISO-8859-1"):
    title.append(line)
    
count=0
description=[]
for line in open('description.dat', 'r',encoding="ISO-8859-1"):
    description.append(line)

data=pd.read_csv("movies_metadata.csv")
data=data.iloc[:,[3,8,9]]
data=data.dropna()
#description=list(data.iloc[:,9])
title_gen=list(data.iloc[:,1])
genre1=data.iloc[:,0]
genre=[]
for g in genre1:
    g=g.split(",")
    gen=[]
    for h in g:
        h=h.strip()
        if h[0:6]=="'name'":
            gen.append(h[7:-1].strip("}").strip().strip("'").lower())
    genre.append(gen)


english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%',"'"]
stopwords = stopwords.words("english")

tit = []
des=[]
length=[]
for index,line in enumerate(description):
    if len(line)==0:
        continue
    sent = word_tokenize(line)
    sent = [ps.stem(word.lower()).strip('\n') for word in sent if word not in english_punctuations]
    sent = [word for word in sent if word not in stopwords]
   
    this_title=title[index].strip('\n')
    for gen_ind,tt in enumerate(title_gen):
        if tt.strip().lower() == this_title.strip().lower():
            gens = genre[gen_ind]
            for gen in gens:
                sent.append(gen)
    length.append(len(sent))  
    des.append(sent)
    tit.append(this_title)
avg_len=sum(length)/len(length)



#query="many people fight for a ring of magic. a war happened"

query=""
while query != "exit":
    query = input("Please describe your movie:")
    if query=="exit":
        break
    que = word_tokenize(query)
    que = [ps.stem(word.lower()).strip('\n') for word in que if word not in english_punctuations]
    que = [word for word in que if word not in stopwords]
    
    num_docs_contain=[]
    for doc in des:
        num_docs_contain=set(doc)


    score=[]
    for index,doc in enumerate(des):
    #def bm25(query, num_docs_contain, this_doc, total_docs,  avg_len, b, k):
        b=0.75
        k=0.9
        num=bm25(que, num_docs_contain, doc, len(des), avg_len, b,k)
        score.append((index,num))
    
    sorted_score=sorted(score,key=lambda t:t[1], reverse=True)
    iter1=0
    for s in sorted_score:
        print(tit[s[0]])
        #print(description[s[0]])
        iter1+=1
        if iter1>4:
            break

#query = [word for word in query if word not in english_punctuations]

########################################################################
###
