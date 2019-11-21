# -*- coding: UTF-8 -*-
import re
import sys

sys.path.append("./")
import jieba
import numpy as np
import pandas as pd


def segment(doc: str):
    """中文分词

    Arguments:
        doc {str} -- 输入文本
    Returns:
        [type] -- [description]
    """
    # 停用词
    stop_words = pd.read_csv("./data/stopwords_TUH.txt", index_col=False, quoting=3,
                             names=['stopword'],
                             sep="\n",
                             encoding='utf-8')
    stop_words = list(stop_words.stopword)

    reg_html = re.compile(r'<[^>]+>', re.S)
    doc = reg_html.sub('', doc)
    doc = re.sub('[０-９]', '', doc)
    doc = re.sub('\s', '', doc)
    word_list = list(jieba.cut(doc))
    out_str = ''
    for word in word_list:
        if word not in stop_words:
            out_str += word
            out_str += ' '
    segments = out_str.split(sep=" ")

    return segments


def sent2vec(model, words):
    """文本转换成向量
    Arguments:
        model {[type]} -- Doc2Vec 模型
        words {[type]} -- 分词后的文本

    Returns:
        [type] -- 向量数组
    """
    vect_list = []
    for w in words:
        try:
            vect_list.append(model.wv[w])
        except:
            continue
    vect_list = np.array(vect_list)
    vect = vect_list.sum(axis=0)
    return vect / np.sqrt((vect ** 2).sum())
