    
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
# text_context, offsets, article['answer']
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
#                 sent 为句子
# ***********************important modification: only if it is supportfactor will we feed it into the dataset
                _process(prepro_sent(sent), is_sup_fact)
#                （cur_title, sent_id）
# ***********************important 
                sent2title_ids.append((cur_title, sp_fact_cnt))
                sp_fact_cnt += 1

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
#                 这里面是找包含best_indices的句子idex范围
#                 如：best_indices word span 在句idx 3,4,5 中
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

def get_embedding(counter, data_type, limit=-1, emb_file=None, size=None, vec_size=None, token2idx_dict=None):
    print("Generating {} embedding...".format(data_type))
#     data_type 为word
    embedding_dict = {}
#     dictionary
    filtered_elements = [k for k, v in counter.items() if v > limit]
    if emb_file is not None:
#         emb_file 应该为生成字典的文件
        assert size is not None
        assert vec_size is not None
        with open(emb_file, "r", encoding="utf-8") as fh:
            for line in tqdm(fh, total=size):
                array = line.split()
                word = "".join(array[0:-vec_size])
                vector = list(map(float, array[-vec_size:]))
                if word in counter and counter[word] > limit:
                    embedding_dict[word] = vector
        print("{} / {} tokens have corresponding {} embedding vector".format(
            len(embedding_dict), len(filtered_elements), data_type))
    else:
#         若没有生成字典的文件 字典由filtered_elementes 中的元素构建
        assert vec_size is not None
        for token in filtered_elements:
#             每个element map到的的embedding vector 是一个vec_size长度的 normal distributed的vector
            embedding_dict[token] = [np.random.normal(
                scale=0.01) for _ in range(vec_size)]
        print("{} tokens have corresponding embedding vector".format(
            len(filtered_elements)))

    NULL = "--NULL--"
    OOV = "--OOV--"
#     enumerate 产生的一个是一个 index+ 元素的组合的list
#     token2idx_dict 是一个从token 至index的dictionary 其中 index从2开始
#     如果函数输入值有token2idx_dict的话就使用输入
    token2idx_dict = {token: idx for idx, token in enumerate(
        embedding_dict.keys(), 2)} if token2idx_dict is None else token2idx_dict
    token2idx_dict[NULL] = 0
#     设置index 0
    token2idx_dict[OOV] = 1
#     设置index 1
    embedding_dict[NULL] = [0. for _ in range(vec_size)]
#     设置0 的embedding_dict: 全零
    embedding_dict[OOV] = [0. for _ in range(vec_size)]
#     设置1 的embedding: 全0
#     由index至embedding的Mapping
    idx2emb_dict = {idx: embedding_dict[token]
                    for token, idx in token2idx_dict.items()}
#     所有embedding的list： 包含了index 为0 与为1
    emb_mat = [idx2emb_dict[idx] for idx in range(len(idx2emb_dict))]
#    idx-> token 的dict 是token2idx_dict的反向
    idx2token_dict = {idx: token for token, idx in token2idx_dict.items()}

    return emb_mat, token2idx_dict, idx2token_dict


def build_features(config, examples, data_type, out_file, word2idx_dict, char2idx_dict):
#     大致为word数组转idx
    if data_type == 'test':
        para_limit, ques_limit = 0, 0
        for example in tqdm(examples):
#             context_tokens是词的集合（句子结构以及paragraph结构已经被break了）
            para_limit = max(para_limit, len(example['context_tokens']))
#             para_limit 为 所有句子个数的最大值
            ques_limit = max(ques_limit, len(example['ques_tokens']))
    else:
        para_limit = config.para_limit
        ques_limit = config.ques_limit

    char_limit = config.char_limit
#  判断词数超越设定值（设定值在train模式下是pre规定的）
    def filter_func(example):
        return len(example["context_tokens"]) > para_limit or len(example["ques_tokens"]) > ques_limit

    print("Processing {} examples...".format(data_type))
    datapoints = []
#     句数合适的article
    total = 0
#     所有的article
    total_ = 0
    for example in tqdm(examples):
        total_ += 1
#       保证article的词数合适
        if filter_func(example):
            continue

        total += 1

        context_idxs = np.zeros(para_limit, dtype=np.int64)
        context_char_idxs = np.zeros((para_limit, char_limit), dtype=np.int64)
        ques_idxs = np.zeros(ques_limit, dtype=np.int64)
        ques_char_idxs = np.zeros((ques_limit, char_limit), dtype=np.int64)

        def _get_word(word):
            for each in (word, word.lower(), word.capitalize(), word.upper()):
                if each in word2idx_dict:
                    return word2idx_dict[each]
            return 1

        def _get_char(char):
            if char in char2idx_dict:
                return char2idx_dict[char]
            return 1
#       token 是一个单词 输出的context_idxs是一个vector 其中小于para_limit的部分为0
        context_idxs[:len(example['context_tokens'])] = [_get_word(token) for token in example['context_tokens']]
        ques_idxs[:len(example['ques_tokens'])] = [_get_word(token) for token in example['ques_tokens']]

        for i, token in enumerate(example["context_chars"]):
            l = min(len(token), char_limit)
            context_char_idxs[i, :l] = [_get_char(char) for char in token[:l]]

        for i, token in enumerate(example["ques_chars"]):
            l = min(len(token), char_limit)
            ques_char_idxs[i, :l] = [_get_char(char) for char in token[:l]]

        start, end = example["y1s"][-1], example["y2s"][-1]
        y1, y2 = start, end
#         example 是examples 中的一行
#         这个append的是一个vector
        datapoints.append({'context_idxs': torch.from_numpy(context_idxs),
            'context_char_idxs': torch.from_numpy(context_char_idxs),
            'ques_idxs': torch.from_numpy(ques_idxs),
            'ques_char_idxs': torch.from_numpy(ques_char_idxs),
            'y1': y1,
            'y2': y2,
            'id': example['id'],
            'start_end_facts': example['start_end_facts']})
    print("Build {} / {} instances of features in total".format(total, total_))
    # pickle.dump(datapoints, open(out_file, 'wb'), protocol=-1)
    torch.save(datapoints, out_file)

def save(filename, obj, message=None):
    if message is not None:
        print("Saving {}...".format(message))
    with open(filename, "w") as fh:
        json.dump(obj, fh)

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
# word ***************
    word2idx_dict = None
    if os.path.isfile(config.word2idx_file):
        with open(config.word2idx_file, "r") as fh:
#             如果之前已经处理过的话： 直接load word2idx_dict
            word2idx_dict = json.load(fh)
    else:
#             如果之前没有处理过的话： get_embedding
#       从词到embatting_vector/ dict 的映射关系 （dictionary）
        word_emb_mat, word2idx_dict, idx2word_dict = get_embedding(word_counter, "word", emb_file=config.glove_word_file,
                                                size=config.glove_word_size, vec_size=config.glove_dim, token2idx_dict=word2idx_dict)
# char **************
    char2idx_dict = None
    if os.path.isfile(config.char2idx_file):
        with open(config.char2idx_file, "r") as fh:
            char2idx_dict = json.load(fh)
    else:
        char_emb_mat, char2idx_dict, idx2char_dict = get_embedding(
            char_counter, "char", emb_file=None, size=None, vec_size=config.char_dim, token2idx_dict=char2idx_dict)

    if config.data_split == 'train':
        record_file = config.train_record_file
        eval_file = config.train_eval_file
    elif config.data_split == 'dev':
        record_file = config.dev_record_file
        eval_file = config.dev_eval_file
    elif config.data_split == 'test':
        record_file = config.test_record_file
        eval_file = config.test_eval_file
# 存储matrix  ******
    build_features(config, examples, config.data_split, record_file, word2idx_dict, char2idx_dict)
    save(eval_file, eval_examples, message='{} eval'.format(config.data_split))
# 存储字典     ******
    if not os.path.isfile(config.word2idx_file):
        save(config.word_emb_file, word_emb_mat, message="word embedding")
        save(config.char_emb_file, char_emb_mat, message="char embedding")
        save(config.word2idx_file, word2idx_dict, message="word2idx")
        save(config.char2idx_file, char2idx_dict, message="char2idx")
        save(config.idx2word_file, idx2word_dict, message='idx2word')
        save(config.idx2char_file, idx2char_dict, message='idx2char')
