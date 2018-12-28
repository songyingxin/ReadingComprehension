# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import argparse
import os
import json

from collections import Counter
from tqdm import tqdm
import nltk

from utils import get_word_span, get_word_idx, process_tokens


""" Settings """
source_dir = "E:\dataset\squad"
target_dir = "E:\dataset\squad"
glove_dir = "E:\dataset\glove"

def get_args():
    """命令行参数解析, 用于与shell进行交互, 提高灵活性"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', "--source_dir", default=source_dir)
    parser.add_argument('-t', "--target_dir", default=target_dir)
    parser.add_argument("--glove_dir", default=glove_dir)
    parser.add_argument('-d', "--debug", action='store_true')  # 是否调试
    parser.add_argument("--mode", default="full", type=str)    # 模式

    return parser.parse_args()

def create_all(args):
    """ 将所有数据写入到all-v1.1.json文件中"""
    out_path = os.path.join(args.source_dir, "all-v1.1.json")
    if os.path.exists(out_path):
        print("the file already exit")
        return
    print("load all data(train data and dev data) in all-v1.1.json")
    train_path = os.path.join(args.source_dir, "train-v1.1.json")
    train_data = json.load(open(train_path, 'r'))
    dev_path = os.path.join(args.source_dir, "dev-v1.1.json")
    dev_data = json.load(open(dev_path, 'r'))
    train_data['data'].extend(dev_data['data'])
    json.dump(train_data, open(out_path, 'w'))


def prepro(args):
    if not os.path.exists(args.target_dir):
        os.makedirs(args.target_dir)

    if args.mode == 'full':
        prepro_each(args, 'train', out_name='train')
        prepro_each(args, 'dev', out_name='dev')
        prepro_each(args, 'dev', out_name='test')

def sent_tokenize(data):
    """句子分割"""
    return nltk.sent_tokenize(data)

def word_tokenize(tokens):
    """ 句子分词 """
    return nltk.word_tokenize(tokens)


def prepro_each(args, data_type, start_ratio=0.0, stop_ratio=1.0, out_name='default', in_path=None):
    """对数据进行处理
    Args:
        data_type: train , dev , all
        start_ratio: 数据起点
        stop_ratio: 数据终点

    """
    data_path = in_path or os.path.join(args.source_dir, "{}-v1.1.json".format(data_type))
    data = json.load(open(data_path, 'r'))

    word_counter, char_counter, lower_word_counter = Counter(), Counter(), Counter()

    start_num = int(round(len(source_data['data']) * start_ratio))
    stop_num = int(round(len(source_data['data']) * stop_ratio))

    """ data file 元素 """
    q = []   # word-level question
    cq = []   # char-level question
    y = []   # 未知
    rx = []
    rcx = []
    cy = []
    idxs = []    # 0-n，表示数据未知
    ids = []    # 真实id
    answerss = []  # 未分词的答案片段：['Saint Bernadette Soubirous']

    """share file 元素 """
    x = []   # context_words
    cx = []  # context_chars
    p = []   # contexts
    word_counter = []
    char_counter = []
    lower_word_counter = []
    word2vec_dict = []
    lower_word2vec_dict = []

    """ 一个title下的内容"""
    for article_num, article in enumerate(tqdm(data['data'][start_num:stop:num])):
        # 一个title下的contexts
        context_words = []
        context_chars = []
        contexts = []

        x.append(context_words)
        cx.append(context_chars)
        p.append(contexts)

        """ 一个context下的内容 """
        for para_num, para in enumerate(article['paragraphs']):
            context = para['context']
            """ 清洗数据context """
            context = context.replace("''", '"' )
            context = context.replace("``", '" ')
            context_word = list(map(word_tokenize, sent_tokenize(context))) # 分词
            context_char = [[list(word) for word in sentence] for sentence in context_word]

            contexts.append(context)
            context_words.append(context_word)
            context_chars.append(context_char)

            for sentence_word in context_word:
                for word in sentence_word:
                    word_counter[word] += len(para['qas']) # 5? why not 1
                    lower_word_counter[word.lower()] += len(para['qas'])
                    for char in word:
                        char_counter[char] += len(para['qas'])

            para_id = [article_num, para_num]   # 第?个title下的第?个paragraph

            """ 一个context下的5个问题， 答案对 """
            for qa in para['qas']:
                question_word = word_tokenize(qa['question'])
                question_char = [list(word) for word in question_word]

                """ answers ： answer_start, text """
                answers = []   # 问题的答案文本
                for answer in qa[answerss]:
                    answer_text = answer['text']
                    answers.append(answer_text)
                    answer_start = answer['answer_start']
                    answer_stop = answer_start + len(answer_text)
                    answer_word_start, answer_word_stop = get_word_span(context, context_word, answer_start, answer_stop)

                    answer_start_word = context_word[answer_word_start[0]][answer_word_start[1]]
                    answer_stop_word = context_word[answer_word_stop[0]][answer_word_stop[1] - 1]

                    start_word_id = get_word_idx(context, context_word, answer_word_start)
                    stop_word_id = get_word_idx(context, context_word, answer_word_stop)





















def main():
    args = get_args()
    prepro(args)

if __name__ == "__main__":
    main()
