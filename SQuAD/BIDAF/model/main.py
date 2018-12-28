import os
import shutil
import argparse
import datetime
from tqdm import tqdm

import torch
import torch.nn as nn
from torch.autograd import Variable

from input_data import save_pickle, load_pickle, load_task, load_processed_json, load_glove_weights, Dataset

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', type=int, default=20, help='input batch size')
parser.add_argument('--lr', type=float, default=0.5, help='learning rate, default=0.5')
parser.add_argument('--ngpu', type=int, default=1, help='number of GPUs to use')
parser.add_argument('--w_embd_size', type=int, default=100, help='word embedding size')
parser.add_argument('--c_embd_size', type=int, default=8, help='character embedding size')
parser.add_argument('--manualSeed', type=int, help='manual seed')
parser.add_argument('--start_epoch', type=int, default=0, help='resume epoch count, default=0')
parser.add_argument('--use_pickle', type=int, default=0, help='load dataset from pickles')
parser.add_argument('--test', type=int, default=0, help='1 for test, or for training')
parser.add_argument('--resume', default='./checkpoints/model_best.tar', type=str, metavar='PATH', help='path saved params')
parser.add_argument('--seed', type=int, default=1111, help='random seed')
args = parser.parse_args()

# Set the random seed manually for reproducibility.
torch.manual_seed(args.seed)

""" 数据路径, 随时更改 """
train_data_path = "E:\dataset\squad\out\data_train.json"
train_shared_path = "E:\dataset\squad\out\shared_train.json"
test_data_path = "E:\dataset\squad\out\data_test.json"
test_shared_path = "E:\dataset\squad\out\shared_test.json"

""" 读取json文件数据 """
train_data_json, train_shared_json = load_processed_json(train_data_path, train_shared_path)
test_data_json, test_shared_json = load_processed_json(test_data_path, test_shared_path)

""" 将数据转化为Dataset对象 """
train_data = Dataset(train_data_json, train_shared_json)
test_data = Dataset(test_data_json, test_shared_json)

char_context_maxlen = train_data.get_char_context_maxlen()
