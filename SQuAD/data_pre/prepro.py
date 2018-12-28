import tensorflow as tf
import random
from tqdm import tqdm
import spacy
import ujson as json
from collections import Counter
import numpy as np
from codecs import open
import os

from config import flags


nlp = spacy.blank("en")

def word_tokenize(sent):
    """ 对 sent 进行分词 """
    doc = nlp(sent)
    return [token.text for token in doc]

def convert_idx(text, tokens):
    """ 将 text 的 word 转化为相对位置，起点为0
    Args:
        text: 真实文本
        tokens： 分词后的文本
    Returns
        spans: token在文本中的相对位置：起点，终点
    """
    current = 0
    spans = []
    for token in tokens:
        current = text.find(token, current)
        if current < 0:
            print("Token {} cannot be found".format(token))
            raise Exception()
        spans.append((current, current + len(token)))
        current += len(token)
    return spans

def process_file(filename, data_type, word_counter, char_counter):
    """
    定义样本数据格式
    Args:
        filename: 文件名
        data_type: train,dev,test
        word_counter: 对 word 计数
        char_counter: 对 char 计数

    Returns:
        examples: [
            {
                "context_tokens": 分词后的上下文
                "context_chars": 分char后的上下文
                "ques_tokens": 分词后的question
                "ques_chars": 分char后的question
                "y1s": 答案的word level起始位置
                "y2s": 答案的word level终止位置
                "id": 表示问题对的id
            }
        ]
        eval_examples:{
            "id":{
                "context": 原始的上下文
                "spans": 上下文word起始位置，如： (0,15)
                "answers": 未处理的答案文本
                "uuid": question对应id

            }
        }
    """
    print("Generating {} examples...".format(data_type))
    examples = []  #  处理后的examples
    eval_examples = {}  # 未处理的examples
    total = 0  # 问题总数

    with open(filename, "r") as fh:
        source = json.load(fh)
        for article in tqdm(source['data']):
            for para in article['paragraphs']:

                """ 对 context 进行处理 """
                context = para["context"].replace(
                    "''", '" ').replace("``", '" ')

                context_tokens = word_tokenize(context) # 分词
                context_chars = [list(token) for token in context_tokens] # 分char
                spans = convert_idx(context, context_tokens)

                for token in context_tokens:
                    word_counter[token] += len(para["qas"])
                    for char in token:
                        char_counter[char] += len(para["qas"])

                """ 对 qas 进行处理 """
                for qa in para["qas"]:
                    total += 1
                    """ 对question进行处理 """
                    ques = qa["question"].replace(
                        "''", '" ').replace("``", '" ')
                    ques_tokens = word_tokenize(ques)  # 分词
                    ques_chars = [list(token) for token in ques_tokens] # 分char
                    for token in ques_tokens:
                        word_counter[token] += 1
                        for char in token:
                            char_counter[char] += 1

                    """ 对 answers 进行处理 """
                    y1s, y2s = [], []  # answer 的起始和终止位置
                    answer_texts = []   # answer 真实文本

                    for answer in qa["answers"]:
                        answer_text = answer["text"]
                        answer_start = answer['answer_start']
                        answer_end = answer_start + len(answer_text)
                        answer_texts.append(answer_text)
                        answer_span = []  # answer token 的位置
                        for idx, span in enumerate(spans):
                            if not (answer_end <= span[0] or answer_start >= span[1]):
                                answer_span.append(idx)
                        y1, y2 = answer_span[0], answer_span[-1] # answer token的起始位置，终止位置

                        y1s.append(y1)
                        y2s.append(y2)

                    example = {"context_tokens": context_tokens,"context_chars": context_chars, "ques_tokens": ques_tokens,"ques_chars": ques_chars, "y1s": y1s, "y2s": y2s, "id": total}
                    examples.append(example)

                    eval_examples[str(total)] = {
                        "context": context, "spans": spans, "answers": answer_texts, "uuid": qa["id"]}
        random.shuffle(examples)
        print("{} questions in total".format(len(examples)))

    return examples, eval_examples


def get_embedding(counter, data_type, emb_file, size, dim, limit=-1):
    """

    Args:
        counter: char_counter or word_counter
        data_type: word or char
        emb_file: word embedding 或 char embedding 文件
        size: word表或char表的大小
        dim： word 向量 或char 向量的维度
        limit: 对数据进行过滤，去掉低频词

    Returns:
        emb_mat: 向量矩阵 [vector1, ..., vector_n]
        token2idx_dict: {word: id}
    """

    print("Generating {} embedding ...".format(data_type))
    embedding_dict = {} # { word: vector}
    filtered_elements = [k for k, v in counter.items() if v > limit] # 过滤低频词

    """ 读取向量文件，将向量与词分开 """
    with open(emb_file, "r", encoding='utf-8') as f:
        for line in tqdm(f, total=size):
            """ 将词与向量分开 """
            array = line.split()
            word = "".join(array[0:-dim])  # 词
            vector = [float(vec) for vec in array[-dim:]] # 词对应的向量

            """ 将所有涉及到的word或char拿出来，其余的丢弃"""
            if word in counter and counter[word] > limit:
                embedding_dict[word] = vector

    NULL = "--NULL--"
    OOV = "--OOV--"

    embedding_dict[NULL] = [0. for _ in range(dim)]
    embedding_dictp[OOV] = [0. for _ in range(dim)]

    """ token2idx_dict: {word:id}, id 为0,1,2,3，...n """
    token2idx_dict = {token:idx for idx, token in
                     enumerate(embedding_dict.keys(), 2)}
    token2idx_dict[NULL] = 0
    token2idx_dict[OOV] = 1

    """ idx2emb_dict: {id: vector}, id is 0,2,...n"""
    idx2emb_dict = {idx:embedding_dict[token]
                    for token, idx in token2idx_dict.items()}

    emb_mat = [idx2emb_dict[idx] for idx in range(len(idx2emb_dict))]

    return emb_mat, token2idx_dict










def prepro(config):

    """ word 相关配置 """
    word_emb_file = config.glove_word_file
    word_emb_size = config.glove_word_size  # 词向量中词的个数
    word_emb_dim = config.glove_word_dim   # 词向量的维度

    """ char 相关配置 """
    char_emb_file = config.glove_char_file
    char_emb_size = config.glove_char_size # char 向量中char的个数
    char_emb_dim = config.glove_char_dim   # char-level 向量的维度

    word_counter, char_counter = Counter(), Counter()  # 计词频

    """ 分词，分char，对word, char计数"""
    train_examples, train_eval = process_file(
        config.train_file, "train", word_counter, char_counter)
    dev_examples, dev_eval = process_file(
        config.dev_file, "dev", word_counter, char_counter)
    test_examples, test_eval = process_file(
        config.test_file, "test", word_counter, char_counter)

    word_emb_mat, word2idx_dict = get_embedding(
        word_counter, "word", emb_file=word_emb_file,
        size=word_emb_size, dim=word_emb_dim)

    char_emb_mat, char2idx_dict = get_embedding(
        char_counter, 'char', emb_file=char_emb_file,
        size=char_emb_size, dim=char_emb_dim)




def main(_):
    config = flags.FLAGS
    prepro(config)

if __name__ == "__main__":
    tf.app.run()
