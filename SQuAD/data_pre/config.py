import tensorflow as tf
import os


""" related input directory and files """
source_dir = "/home/songyingxin/datasets"

train_file = os.path.join(source_dir, "squad", "train-v1.1.json")
dev_file = os.path.join(source_dir, "squad", "dev-v1.1.json")
test_file = os.path.join(source_dir, "squad", "dev-v1.1.json")
glove_word_file = os.path.join(source_dir, "glove", "glove.840B.300d.txt")
glove_char_file = os.path.join(source_dir, "glove", "glove.840B.300d-char.txt")

""" related output directory and files"""
target_dir = "/home/songyingxin/data"

train_record_file = os.path.join(target_dir, "train.tfrecords")
dev_record_file = os.path.join(target_dir, "dev.tfrecords")
test_record_file = os.path.join(target_dir, "test.tfrecords")

flags = tf.flags

flags.DEFINE_string("target_dir", target_dir, "Target directory for out data")
flags.DEFINE_string("train_file", train_file, "Train source file")
flags.DEFINE_string("dev_file", dev_file, "Dev source file")
flags.DEFINE_string("test_file", test_file, "Test source file")

flags.DEFINE_string("glove_word_file", glove_word_file, "Glove word embedding source file")
flags.DEFINE_integer("glove_word_size", int(2.2e6), "Corpus size for Glove")
flags.DEFINE_integer("glove_word_dim", 300, "Embedding dimension for Glove")

flags.DEFINE_string("glove_char_file", glove_char_file, "Glove character embedding source file")
flags.DEFINE_integer("glove_char_size", 94, "Corpus size for Glove")
flags.DEFINE_integer("glove_char_dim", 64, "Embedding dimension for char")
