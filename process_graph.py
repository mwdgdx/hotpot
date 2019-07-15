import random
from tqdm import tqdm
import spacy
import ujson as json
from collections import Counter
import numpy as np
import os.path
import argparse
import torch
# import pickle
import torch
import os
from joblib import Parallel, delayed

import torch

nlp = spacy.blank("en")
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import bisect
import re
import pandas as pd
import csv


def word_tokenize(sent):
    doc = nlp(sent)
    return [token.text for token in doc]

def find_tokenized_length(token_list):
    length = 0
    for token in token_list:
        if token not in [' ','   ','  ']:
            length+=1
    return length
def _process_article(article, config):
    paragraphs = article['context']
    # some articles in the fullwiki dev/test sets have zero paragraphs
    if len(paragraphs) == 0:
        paragraphs = [['some random title', 'some random stuff']]
#     st = StanfordNERTagger('/home/mwdgdx/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz','/home/mwdgdx/stanford-ner-2018-10-16/stanford-ner.jar',encoding='utf-8')

    context_tokens = []
    offsets = []
    sent_map = [] # (sent_idx, is_sup_fact=True/False)  
    sent_idx=0
    para_map = []   
    sup_list=[]
    def _process(sent_tokens, is_sup_fact, is_title=False):
        nonlocal  context_tokens,  offsets, sent_map,sent_idx, para_map, para_idx
        my_N_tokens = len(sent_tokens)
        context_tokens.extend(sent_tokens)
        sent_map += [(sent_idx,para_idx,is_sup_fact,sent_tokens[i]) for i in range(my_N_tokens) if sent_tokens[i] not in [' ','  ','   ']]
        sent_idx+=1 

    if 'supporting_facts' in article:
        sp_set = set(list(map(tuple, article['supporting_facts'])))
    else:
        sp_set = set()

    st = StanfordNERTagger('/home/mwdgdx/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz','/home/mwdgdx/stanford-ner-2018-10-16/stanford-ner.jar',encoding='utf-8')
    token_list  = word_tokenize(article['question'])
    ques_length = find_tokenized_length(token_list)
    for para_idx , para in enumerate(paragraphs):
        cur_title, cur_para = para[0], para[1]
        token_list += word_tokenize(cur_title)
        _process(word_tokenize(cur_title), False, is_title=True)
        c_p= [word_tokenize(sent) for sent in cur_para]
        for sent in cur_para:
            token_list +=word_tokenize(sent)
        for sent_id, sent in enumerate(c_p):
            is_sup_fact = (cur_title, sent_id) in sp_set
            if is_sup_fact:
                sup_list +=[sent_idx]
            _process(sent, is_sup_fact)
#     ori_list = token_list
    token_list = st.tag(token_list)
    ques_tokens= token_list[:ques_length]
    context_tokens = token_list[ques_length:]
#     print(len(sent_map), len(context_tokens))
#     testing NER Efficiency 
#     qi = pd.DataFrame({'q+c': [i for i in ori_list if i!=' ' and i !='  ' and i !='']})
#     qi.to_csv('NER seperate'+article['_id']+'.csv', header=True,index=False, sep=',')
#     qi = pd.DataFrame({'q+c': [e[0] for e in token_list ]})
#     qi.to_csv('NER token_list'+article['_id']+'.csv', header=True,index=False, sep=',')
    example = {'context_tokens': context_tokens, 'ques_tokens': ques_tokens,  'id': article['_id'], 'sent_map': sent_map, 'sup': sup_list}
    return example

def process_file(filename, config, word_counter=None, char_counter=None):
    data = json.load(open(filename, 'r'))

    examples = []
    data=data[:]
#     先看10篇
    outputs = Parallel(n_jobs=12, verbose=10)(delayed(_process_article)(article, config) for article in data)
    # outputs = [_process_article(article, config) for article in data]
    examples = [e for e in outputs]

    print("{} questions in total".format(len(examples)))

    return examples




# 记录：
#      node is_support degree type
def graph_process(text, ques, sent_map,sup_list,art_idx):
    print("length of text and sent_map",len(text), len(sent_map))
    if len(text)!=len(sent_map):
        print("error")
        return 1
    
    sup_set=set()
    nodes=set()
    q_s=set()
    for e in ques:
        if e[1]!='O':
            q_s.add(e[0].lower())
#             大小写
    w_m={}
    s_m={}
#     qp_m={}
#     tp_m={}
#   nodes is the index of each entity
#   first filled with entities in question
    for i in range(len(text)):
        if text[i][1]!='O':
            word=text[i][0].lower()
            for q_w in q_s:
                if (word in q_w) or (q_w in word):
                    nodes.add(i)
#                     add next sentence
                    nextSentIdx=i+1
                    while  nextSentIdx< len(sent_map) and sent_map[nextSentIdx][0]<=(sent_map[i][0]+1):
                       if text[nextSentIdx] in {"she","it","they","he","their","her","his","its","him","them"}:
                           s_m.add(sent_map[nextSentIdx][0])
                           break
                       nextSentIdx+=1
#                     add word  in word_map
                    if q_w in w_m:
                        w_m[q_w].add(i)
                    else:
                        w_m[q_w]={i}
#                     add sent in sent_map
                    if sent_map[i][0] in s_m:
                        s_m[sent_map[i][0]].add(i)
                    else:
                        s_m[sent_map[i][0]]={i}
#                     if sent_map[i][1] in qp_m:
#                         qp_m[sent_map[i][1]].add(i)
#                     else:
#                         qp_m[sent_map[i][1]]={i}
                    break
    is_changed=True
    while is_changed:
        is_changed =False
        for i in range(len(text)):
            if ((text[i][1]!='O') and (i not in nodes)):
                word=text[i][0].lower()
                for q_w in w_m:
                    if (word in q_w) or (q_w in word):
                        nodes.add(i)
                        nextSentIdx=i+1
                        while  nextSentIdx< len(sent_map) and sent_map[nextSentIdx][0]<=(sent_map[i][0]+1):
                            if text[nextSentIdx] in {"she","it","they","he","their","her","his","its","him","them"}:
                                s_m.add(sent_map[nextSentIdx][0])
                                break
                            nextSentIdx+=1
                        is_changed = True
                        if q_w in w_m:
                            w_m[q_w].add(i)
                        else:
                            w_m[q_w]={i}
                        if sent_map[i][0] in s_m:
                            s_m[sent_map[i][0]].add(i)
                        else:
                            s_m[sent_map[i][0]]={i} 
                        break
                if sent_map[i][0] in s_m:
                    nodes.add(i)
                    nextSentIdx=i+1
                    while  nextSentIdx< len(sent_map) and sent_map[nextSentIdx][0]<=(sent_map[i][0]+1):
                        if text[nextSentIdx] in {"she","it","they","he","their","her","his","its","him","them"}:
                            s_m.add(sent_map[nextSentIdx][0])
                            break
                        nextSentIdx+=1
                    is_changed = True
#                     这里有可能会列入不一样的列表
                    if word in w_m:
                        w_m[word].add(i)
                    else:
                        w_m[word]={i}
                    if sent_map[i][0] in s_m:
                        s_m[sent_map[i][0]].add(i)
                    else:
                        s_m[sent_map[i][0]]={i}  

    #                 if sent_map[i][1] in qp_m:
#                     if sent_map[i][1] in tp_m:
#                         tp_m[sent_map[i][1]]+=1
#                     else:
#                         tp_m[sent_map[i][1]]= 1
    n_info={}
    is_node = [0 for e in text]
    for node in nodes: 
        n_info[node]=[0,int(sent_map[node][2] == True)]
        is_node[node]=1
        if sent_map[node][2] == True:
            sup_set.add(sent_map[node][0])
    for w_s in w_m.values():
        for w in w_s:
            n_info[w][0]+=len(w_s)
    
    for s_s in s_m.values():
        for w in s_s:
            n_info[w][0]+=len(s_s)
    print(art_idx, len(sup_set),len(sup_list))
#     for key, value in qp_m.items():
#         for w in value:
#             if key in tp_m:
#                 n_info[w][0]+=tp_m[key]
#     edge= [value[0] for value in n_info.values()]
#     is_sup = [value[1] for value in n_info.values()]
#     gi = pd.DataFrame({'text':[e for e in text], 'is_sup': [i[2] for i in sent_map], 'is_node':is_node})
#     gi.to_csv('graph_info'+str(art_idx)+'.csv', header=False,index=False, sep=',')
#     qi = pd.DataFrame({'question': [e for e in ques]})
#     qi.to_csv('ques_info'+str(art_idx)+'.csv', header=False,index=False, sep=',')
    return int(len(sup_set) != len(sup_list))

def prepro(config):
#     word_counter, char_counter = Counter(), Counter()
#     examples = process_file(config.data_file, config, word_counter, char_counter)
#     torch.save(examples, '/scratch/qmei_fluxg/mwdgdx/graph_process_371.pkl') 
    examples = torch.load('/scratch/qmei_fluxg/mwdgdx/graph_process.pkl')
    missed =0
    for i, example in enumerate(examples):
        text = example['context_tokens']
        ques = example['ques_tokens']
        sent_map = example['sent_map']
        sup_list = example['sup']
        missed += graph_process(text, ques,sent_map,sup_list, i)
    print("missed" , missed, "from", len(examples))
    print ("percentile", missed/len(examples))

