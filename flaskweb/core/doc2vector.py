# -*- coding: UTF-8 -*-
import sys

sys.path.append("./")
import pandas as pd
import gensim
from utility.mongodb import MongoDBManager
from utility.sentence import segment, sent2vec


class Doc2Vector(object):
    """
    文本转向量
    """

    def __init__(self):
        """
        :param keep_val: 设定的阈值
        """
        self.mongo_db = MongoDBManager()

    def doc2vect(self):
        """
        所有文档转成向量存储到数据库
        :return:
        """
        model = gensim.models.Doc2Vec.load('./models/doc2vec_v1.model')

        df_data = pd.read_excel("./data/new_prd.xlsx", names=["SysNo", "Title", "Content"])
        content = []
        title = []
        for idx, row in df_data.iterrows():
            seg_title = segment(row.Title)
            seg_content = segment(row.Content)
            # 转向量
            content_vect = sent2vec(model, ' '.join(seg_content))
            title_vect = sent2vec(model, ' '.join(seg_title))
            content_vect = map(str, content_vect.tolist())
            title_vect = map(str, title_vect.tolist())
            content.append({"_id": int(idx) + 1, "data": list(content_vect)})
            title.append({"_id": int(idx) + 1, "data": list(title_vect)})

        self.mongo_db.insert("content_vector", content)
        self.mongo_db.insert("title_vector", title)
        
        print("finished")


if __name__ == '__main__':
    doc2vect = Doc2Vector()
    doc2vect.doc2vect()
