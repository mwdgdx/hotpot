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

def prepro_sent(sent):
    return sent
    # return sent.replace("''", '" ').replace("``", '" ')

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
    def _process(sent, is_sup_fact, is_title=False):
        nonlocal  context_tokens,  offsets, sent_map,sent_idx, para_map, para_idx
        sent_tokens = sent
        
#         if is_title:
#             sent = '<t> {} </t>'.format(sent)
#             sent_tokens = ['<t>'] + sent_tokens + ['</t>']
        my_N_tokens = len(sent_tokens)
        context_tokens.extend(sent_tokens)
        sent_map += [(sent_idx,para_idx,is_sup_fact,sent_tokens[i]) for i in range(my_N_tokens)]
        sent_idx+=1 

    if 'supporting_facts' in article:
        sp_set = set(list(map(tuple, article['supporting_facts'])))
    else:
        sp_set = set()

    st = StanfordNERTagger('/home/mwdgdx/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz','/home/mwdgdx/stanford-ner-2018-10-16/stanford-ner.jar',encoding='utf-8')
    for para_idx , para in enumerate(paragraphs):
        cur_title, cur_para = para[0], para[1]
        _process(st.tag(word_tokenize(cur_title)), False, is_title=True)
        c_p= st.tag_sents([word_tokenize(sent) for sent in cur_para])
        for sent_id, sent in enumerate(c_p):
            is_sup_fact = (cur_title, sent_id) in sp_set
            if is_sup_fact:
                sup_list +=[sent_idx]
            _process(prepro_sent(sent), is_sup_fact)
#    想办法identify paragraph
    ques_tokens = word_tokenize(prepro_sent(article['question']))
    # start_end_facts 指的是每句句子的起始和终点
    example = {'context_tokens': context_tokens, 'ques_tokens': ques_tokens,  'id': article['_id'], 'sent_map': sent_map, 'sup': sup_list}
    return example

def process_file(filename, config, word_counter=None, char_counter=None):
    data = json.load(open(filename, 'r'))

    examples = []
    data=data[:30]
#     先看10篇
    outputs = Parallel(n_jobs=12, verbose=10)(delayed(_process_article)(article, config) for article in data)
    # outputs = [_process_article(article, config) for article in data]
    examples = [e for e in outputs]

    print("{} questions in total".format(len(examples)))

    return examples




# 记录：
#      node is_support degree type
def graph_process(text, ques, sent_map,sup_list):
    sup_set=set()
    nodes=set()
    q_s=set()
    for e in ques:
        if e[1]!='O':
            q_s.add(e[0])
    w_m={}
    s_m={}
    qp_m={}
    tp_m={}
#   nodes is the index of each entity
#   first filled with entities in question
    for i,e in enumerate(text):
        if e[1]!='O' and  e[0] in q_s:
#             check index validation
            nodes.add(i)
            if e[0] in w_m:
                w_m[e[0]].add(i)
            else:
                w_m[e[0]]={i}
            if sent_map[i][0] in s_m:
                s_m[sent_map[i][0]].add(i)
            else:
                s_m[sent_map[i][0]]={i}
            if sent_map[i][1] in qp_m:
                qp_m[sent_map[i][1]].add(i)
            else:
                qp_m[sent_map[i][1]]={i}
    is_changed=True
    while is_changed:
        is_changed =False
        for i, e  in enumerate(text):
            if (e[1]!='O')and ((e[0] in w_m) or (sent_map[i][0] in s_m))and (i not in nodes):
                nodes.add(i)
                is_changed = True
                if e[0] in w_m:
                    w_m[e[0]].add(i)
                else:
                    w_m[e[0]]={i}
                if sent_map[i][0] in s_m:
                    s_m[sent_map[i][0]].add(i)
                else:
                    s_m[sent_map[i][0]]={i}
                if sent_map[i][1] in qp_m:
                    if sent_map[i][1] in tp_m:
                        tp_m[sent_map[i][1]]+=1
                    else:
                        tp_m[sent_map[i][1]]= 1
    n_info={}
    for node in nodes: 
        n_info[node]=[0,int(sent_map[node][2] == True)]
        if sent_map[node][2] == True:
            sup_set.add(sent_map[node][0])
    print(len(sup_set),len(sup_list))
    print(int(len(sup_set) == len(sup_list)))
    for w_s in w_m.values():
        for w in w_s:
            n_info[w][0]+=len(w_s)
    
    for s_s in s_m.values():
        for w in s_s:
            n_info[w][0]+=len(s_s)
    
    for key, value in qp_m.items():
        for w in value:
            if key in tp_m:
                n_info[w][0]+=tp_m[key]
    edge= [value[0] for value in n_info.values()]
    is_sup = [value[1] for value in n_info.values()]
    gi = pd.DataFrame({'edges':edge, 'is_sup': is_sup})
#     gi.to_csv("graph_info.csv",index=False,sep=',')
    gi.to_csv('graph_info.csv', mode='a', header=False,index=False, sep=',')

def prepro(config):
    random.seed(13)
    word_counter, char_counter = Counter(), Counter()
    examples = process_file(config.data_file, config, word_counter, char_counter)
    st = StanfordNERTagger('/home/mwdgdx/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz','/home/mwdgdx/stanford-ner-2018-10-16/stanford-ner.jar',encoding='utf-8')
#     需要修改

    for example in examples:
#             example = {'context_tokens': context_tokens,'context_chars': context_chars, 'ques_tokens': ques_tokens, 'ques_chars': ques_chars, 'y1s': [best_indices[0]], 'y2s': [best_indices[1]], 'id': article['_id'], 'start_end_facts': start_end_facts}
        text = example['context_tokens']
        ques = st.tag(example['ques_tokens'])
        sent_map = example['sent_map']
        sup_list = example['sup']
        graph_process(text, ques,sent_map,sup_list)
