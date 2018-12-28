import json

def load_processed_json(data_path, shared_path):
    data = json.load(open(data_path))
    shared = json.load(open(share))
    return data, shared


class Dataset(object):
    """ 对raw数据进行操作"""

    def __init__(self, data, shared):
        self.data = data
        self.shared = shared

    def get_char_context_maxlen(self):
        """ 获取所有context最长的char-level长度 """
        return max([len(p) for title_contexts in self.shared['p'] for context in title_contexts])

    def get_sent_maxlen(self):
        """ 获取句子中 word level amxlen """
        return 
