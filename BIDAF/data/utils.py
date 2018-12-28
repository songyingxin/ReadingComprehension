import re


def process_tokens(tokens):
    """ 将单词列表中的细微部分 例如：'s 切分 """
    new_tokens = []

    for token in tokens:
        """
        需要查一下下面几个编码表示什么
        """
        l = ("-", "\u2212", "\u2014", "\u2013", "/", "~", '"', "'", "\u201C", "\u2019", "\u201D", "\u2018", "\u00B0")
        tokens.extend(re.split("([{}])".format("".join(l)), token))
    return tokens

def get_2d_spans(text, tokenss):
    """ 将text 转化为数字间隔表示， 如： (0, 15) """
    spanss = []
    cur_idx = 0
    for tokens in tokenss:
        spans = []
        for token in tokens:
            if text.find(token, cur_idx) < 0:
                print(tokens)
                print("{} {} {}".format(token, cur_idx, text))
                raise Exception()
            cur_idx = text.find(token, cur_idx)
            spans.append((cur_idx, cur_idx + len(token)))
            cur_idx += len(token)
        spanss.append(spans)
    return spanss


def get_word_span(context, wordss, start, stop):
    """ 将answer转化为在context中的位置 如： ((0, 108), (0, 111)) 表示答案在context中的第108个word 与第111(不包括111)个word之间 """
    spanss = get_2d_spans(context, wordss)
    idxs = []
    for sent_idx, spans in enumerate(spanss):
        for word_idx, span in enumerate(spans):
            if not (stop <= span[0] or start >= span[1]):
                idxs.append((sent_idx, word_idx))

    assert len(idxs) > 0, "{} {} {} {}".format(context, spanss, start, stop)
    return idxs[0], (idxs[-1][0], idxs[-1][1] + 1)


def get_word_idx(context, wordss, idx):
    spanss = get_2d_spans(context, wordss)
    return spanss[idx[0]][idx[1]][0]



if __name__ == "__main__":
    text = 'Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend "Venite Ad Me Omnes". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.'

    tokens = [['Architecturally', ',', 'the', 'school', 'has', 'a', 'Catholic', 'character', '.', 'Atop', 'the', 'Main', 'Building', '', "'", 's', 'gold', 'dome', 'is', 'a', 'golden', 'statue', 'of', 'the', 'Virgin', 'Mary', '.', 'Immediately', 'in', 'front', 'of', 'the', 'Main', 'Building', 'and', 'facing', 'it', ',', 'is', 'a', 'copper', 'statue', 'of', 'Christ', 'with', 'arms', 'upraised', 'with', 'the', 'legend', '', '"', '', 'Venite', 'Ad', 'Me', 'Omnes', '', '"', '', '.', 'Next', 'to', 'the', 'Main', 'Building', 'is', 'the', 'Basilica', 'of', 'the', 'Sacred', 'Heart', '.', 'Immediately', 'behind', 'the', 'basilica', 'is', 'the', 'Grotto', ',', 'a', 'Marian', 'place', 'of', 'prayer', 'and', 'reflection', '.', 'It', 'is', 'a', 'replica', 'of', 'the', 'grotto', 'at', 'Lourdes', ',', 'France', 'where', 'the', 'Virgin', 'Mary', 'reputedly', 'appeared', 'to', 'Saint', 'Bernadette', 'Soubirous', 'in', '1858', '.', 'At', 'the', 'end', 'of', 'the', 'main', 'drive', '(', 'and', 'in', 'a', 'direct', 'line', 'that', 'connects', 'through', '3', 'statues', 'and', 'the', 'Gold', 'Dome', ')', ',', 'is', 'a', 'simple', ',', 'modern', 'stone', 'statue', 'of', 'Mary', '.']]

    print(get_2d_spans(text, tokens))
    print(get_word_span(text, tokens, 515, 541))

    print(get_word_idx(text, tokens, (0, 108)))
