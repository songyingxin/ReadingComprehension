import tensorflow as tf
import random
from tqdm import tqdm
import spacy
import ujson as json
from collections import Counter
import numpy as np
from codecs import open

nlp = spacy.blank("en")

def word_tokenize(sent):
    """ segmentation for english word using spacy"""
    doc = nlp(sent)
    return [token.text for token in doc]

def convert_idx(text, tokens):
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

def process_file(dir_name, data_type, word_counter, char_counter):

    return examples, eval_examples



def main():

    cnn_dir = "/home/songyingxin/dataset/cnn/questions/"
    sub_dirs = ["training/", "validation/", "test/"]
    dirs = [cnn_dir + sub_name for sub_name in sub_dirs]

    train_files = [dirs[0] + file_name for file_name in os.listdir(dirs[0])]
    dev_files = [dirs[1] + file_name for file_name in os.listdir(dirs[1])]
    test_files = [dirs[2] + file_name for file_name in os.listdir(dirs[2])]








if __name__ == "__main__":
    sent = ["i was a"]
    doc = word_tokenize(sent)
    print(doc)
