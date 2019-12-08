from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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

# def bm25(query, num_docs_contain, this_doc, total_docs, avg_len, b, k):
#     score = 0
#     for term in query:
#         contain=0
#         #total_docs=len(total_docs_file)
#         for i in num_docs_contain:
#             if term in i:
#                 contain+=1
#         idf = math.log((total_docs - contain + 0.5) / (contain + 0.5))# / math.log(1.0 + total_docs)
#         tf = term_frequency(this_doc,term)
#         score = score + ( tf* idf * (k + 1)) / (tf + k * (1 - b + (b * (len(this_doc)/avg_len))))
#     return score

def bm25(query, num_docs_contain, this_doc, total_docs, avg_len, b, k, k3, delta):
    score = 0
    k1 = k
    N = total_docs
    D = len(this_doc)
    for term in query:
        contain=0
        for i in num_docs_contain:
            if term in i:
                contain+=1
        df = contain
        ctd = term_frequency(this_doc,term)
        ctq = term_frequency(query,term)
        add = math.log((N+1)/(df)) * ((k1+1)*ctd/(k1*(1-b+b*D/avg_len)+ctd) + delta) * (k3+1)*ctq/(k3+ctq)
        score = score + add
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



@csrf_exempt
def index(request):
    if 'in' in request.POST:
        li = []
        query = str(request.POST['in'])
        print(query)
        que = word_tokenize(query)
        que = [ps.stem(word.lower()).strip('\n') for word in que if word not in english_punctuations]
        que = [word for word in que if word not in stopwords]
        num_docs_contain=[]
        for doc in des:
            num_docs_contain.append(set(doc))
        score = []
        for index,doc in enumerate(des):
            num=bm25(que, num_docs_contain, doc, len(des), avg_len, 0.2,1.2,500,1)
            score.append((index,num))
        sorted_score=sorted(score,key=lambda t:t[1], reverse=True)
        iter1=0
        for s in sorted_score:
            print(tit[s[0]])
            li.append(tit[s[0]])
            iter1+=1
            if iter1>4:
                break
    else:
        li = ['none']
    # print('into index')
    # if 'in' in request.POST:
    #     print('into search')
    #     li = []
    #     # query_input = str(request.POST['in'])
    #     query_input = 'jack and rose'
    #     print(query_input)
    #     ranker = BM25()
    #     query_in = query_input
    #     query = metapy.index.Document()
    #     print('get query')
    #     query.content(query_in)
    #     top_docs = ranker.score(inv_idx, query, num_results=1)  
    #     print('get doc')
    #     for num, (d_id, _) in enumerate(top_docs):
    #         content = inv_idx.metadata(d_id).get('content')
    #         li.append("{}. {}\n".format(num + 1, content))
    #     print('finish search')
    # else:
    #     li = ['none']
    print('return')
    return render(request, 'list.html', {'li': li})
