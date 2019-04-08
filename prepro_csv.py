import pandas as pd
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

import bisect
import re

def find_nearest(a, target, test_func=lambda x: True):
    idx = bisect.bisect_left(a, target)
    if (0 <= idx < len(a)) and a[idx] == target:
        return target, 0
    elif idx == 0:
        return a[0], abs(a[0] - target)
    elif idx == len(a):
        return a[-1], abs(a[-1] - target)
    else:
        d1 = abs(a[idx] - target) if test_func(a[idx]) else 1e200
        d2 = abs(a[idx-1] - target) if test_func(a[idx-1]) else 1e200
        if d1 > d2:
            return a[idx-1], d2
        else:
            return a[idx], d1

def fix_span(para, offsets, span):
    span = span.strip()
    parastr = "".join(para)
    assert span in parastr, '{}\t{}'.format(span, parastr)
    begins, ends = map(list, zip(*[y for x in offsets for y in x]))

    best_dist = 1e200
    best_indices = None

    if span == parastr:
        return parastr, (0, len(parastr)), 0

    for m in re.finditer(re.escape(span), parastr):
        begin_offset, end_offset = m.span()

        fixed_begin, d1 = find_nearest(begins, begin_offset, lambda x: x < end_offset)
        fixed_end, d2 = find_nearest(ends, end_offset, lambda x: x > begin_offset)

        if d1 + d2 < best_dist:
            best_dist = d1 + d2
            best_indices = (fixed_begin, fixed_end)
            if best_dist == 0:
                break

    assert best_indices is not None
    return parastr[best_indices[0]:best_indices[1]], best_indices, best_dist

def word_tokenize(sent):
    doc = nlp(sent)
    return [token.text for token in doc]


def convert_idx(text, tokens):
    current = 0
    spans = []
    for token in tokens:
        pre = current
        current = text.find(token, current)
        if current < 0:
            raise Exception()
        spans.append((current, current + len(token)))
        current += len(token)
    return spans

def prepro_sent(sent):
    return sent
    # return sent.replace("''", '" ').replace("``", '" ')

def _process_article(article, config):
#     一篇文章包含 各种段落+ answer+ question+，每个段落
#     article： 一个dictionary: 
#               key context   由paragraph list 构成 每个paragraph 由para[0]:title para[1]: cur_para构成
#               key question
#               key supporting
    #     一个由段落组成的list
    paragraphs = article['context']
    # some articles in the fullwiki dev/test sets have zero paragraphs
    if len(paragraphs) == 0:
        paragraphs = [['some random title', 'some random stuff']]
        
    text_context, context_tokens, context_chars = '', [], []
    offsets = []
    flat_offsets = []
    start_end_facts = [] # (start_token_id, end_token_id, is_sup_fact=True/False)
    sent2title_ids = []

    def _process(sent, is_sup_fact, is_title=False):
#         主函数中的变量
        nonlocal text_context, context_tokens, context_chars, offsets, start_end_facts, flat_offsets
        N_chars = len(text_context)

        sent = sent
#         将一句话 string 转为token 的数组 Doc
        sent_tokens = word_tokenize(sent)
        if is_title:
#             更新title 的格式： string 和Doc(token 数组)
            sent = '<t> {} </t>'.format(sent)
            sent_tokens = ['<t>'] + sent_tokens + ['</t>']
#         将token 转为字母的list
        sent_chars = [list(token) for token in sent_tokens]
#         返回范围数组: list of range of position index : (current,current+len)
        sent_spans = convert_idx(sent, sent_tokens)
#         更新全局范围
        sent_spans = [[N_chars+e[0], N_chars+e[1]] for e in sent_spans]
        N_tokens, my_N_tokens = len(context_tokens), len(sent_tokens)
#        text_context为一个string 
        text_context += sent
#         context_tokens: list of tokens
        context_tokens.extend(sent_tokens)
#         context_chars: list of list of list of chars
        context_chars.extend(sent_chars)
#         start_end_facts: 范围+ is_sup_fact的数组
        start_end_facts.append((N_tokens, N_tokens+my_N_tokens, is_sup_fact))
#         offsets: 范围数组 :区分paragraph
        offsets.append(sent_spans)
#         flat_offsets： 范围数组： 不分paragraph
        flat_offsets.extend(sent_spans)
#    ？？ 这是什么？ article 中有没有Key ’supporting_facts‘ 
    if 'supporting_facts' in article:
        sp_set = set(list(map(tuple, article['supporting_facts'])))
#         sp_set的Key 为(title, idx) pair
    else:
        sp_set = set()
#   记录总共有几个support factor count
    sp_fact_cnt = 0
    for para in paragraphs:
        cur_title, cur_para = para[0], para[1]
#         prepro_sent 是啥都不干
        _process(prepro_sent(cur_title), False, is_title=True)
        sent2title_ids.append((cur_title, -1))
#         cur_para是由句子组成的list
        for sent_id, sent in enumerate(cur_para):
#             判断 （title, id）是否在这个数组中
            is_sup_fact = (cur_title, sent_id) in sp_set
            if is_sup_fact:
                sp_fact_cnt += 1
#                 sent 为句子
            _process(prepro_sent(sent), is_sup_fact)
#                （cur_title, sent_id）
            sent2title_ids.append((cur_title, sent_id))

    if 'answer' in article:
#         删去头尾string的空白
        answer = article['answer'].strip()
        if answer.lower() == 'yes':
            best_indices = [-1, -1]
        elif answer.lower() == 'no':
            best_indices = [-2, -2]
        else:
            if article['answer'].strip() not in ''.join(text_context):
                # in the fullwiki setting, the answer might not have been retrieved
                # use (0, 1) so that we can proceed
                best_indices = (0, 1)
            else:
                _, best_indices, _ = fix_span(text_context, offsets, article['answer'])
                answer_span = []
                for idx, span in enumerate(flat_offsets):
                    if not (best_indices[1] <= span[0] or best_indices[0] >= span[1]):
                        answer_span.append(idx)
                best_indices = (answer_span[0], answer_span[-1])
    else:
        # some random stuff
        answer = 'random'
        best_indices = (0, 1)

    ques_tokens = word_tokenize(prepro_sent(article['question']))
    ques_chars = [list(token) for token in ques_tokens]
    #         context_tokens: list of list of tokens. article中句子的集合
    #         context_chars: list of list of list of chars
#          y1s 为答案的起始点
#          y2s 为答案的终点
    example = {'context_tokens': context_tokens,'context_chars': context_chars, 
               'ques_tokens': ques_tokens, 'ques_chars': ques_chars, 'y1s': [best_indices[0]], 
               'y2s': [best_indices[1]], 'id': article['_id'], 'start_end_facts': start_end_facts}
#       answer为具体的answer
#       text_context 为一个token 流
    eval_example = {'context': text_context, 'spans': flat_offsets, 'answer': [answer], 'id': article['_id'],
            'sent2title_ids': sent2title_ids}
    return example, eval_example

def process_file(filename, config, word_counter=None, char_counter=None):
# filename = data_file: hotpot_train_v1.1.json  暂时不知道这里面是什么东西
    data = json.load(open(filename, 'r'))
#     list
    examples = []
#     set
    eval_examples = {}
#   多进程处理各个: _process_article(article,config)  
#   output是个什么东西？
    outputs = Parallel(n_jobs=12, verbose=10)(delayed(_process_article)(article, config) for article in data)
    # outputs = [_process_article(article, config) for article in data]
    examples = [e[0] for e in outputs]
    for _, e in outputs:
        if e is not None:
            eval_examples[e['id']] = e

    # only count during training
    if word_counter is not None and char_counter is not None:
        for example in examples:
            for token in example['ques_tokens'] + example['context_tokens']:
                word_counter[token] += 1
                for char in token:
                    char_counter[char] += 1

    random.shuffle(examples)
    print("{} questions in total".format(len(examples)))
#    examples 和eval_examples就是各article 输出的list
    return examples, eval_examples


def build_features(config, examples, data_type, out_file, word2idx_dict, char2idx_dict):
    length_vector=[]
    for example in tqdm(examples):
        length_vector+=[len(example["context_tokens"])]
    dataframe = pd.DataFrame({'length_in_words':length_vector})
    dataframe.to_csv("length_vector.csv",index=False,sep=',')
    


def prepro(config):
    random.seed(13)
    if config.data_split == 'train':
#         如果是train的话就要使用counter
#       word_counter train/ validation 中每个词出现的次数
#       char_counter train/ validation 中每个char 出现的次数
        word_counter, char_counter = Counter(), Counter()
        examples, eval_examples = process_file(config.data_file, config, word_counter, char_counter)
    else:
#         如果是dev,test的话就不用counter
        examples, eval_examples = process_file(config.data_file, config)
    build_features(config, examples, config.data_split)
