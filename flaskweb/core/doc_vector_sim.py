# -*- coding: UTF-8 -*-
import sys

sys.path.append("./")
import gensim
import numpy as np
from scipy.spatial.distance import pdist
from utility.logger_decor import exception
from utility.mongodb import MongoDBManager
from utility.sentence import segment, sent2vec


class DocVectSim(object):
    """
    文本相似度
    """

    def __init__(self, keep_val: float = 0.8):
        """
        :param keep_val: 设定的阈值
        """
        self.keep_val = keep_val
        self.mongo_db = MongoDBManager()

    @exception
    def similarity(self, prefix: str, sysno: int, text: str):
        """计算相似度
        返回索引和余弦值

        Arguments:
            text {str} -- 文本数据
            value {float} -- 设定的阈值，返回大于这个值的数据
        """
        # 加载训练的模型
        model = gensim.models.Doc2Vec.load('./models/doc2vec_v1.model')
        # 分词
        sent = segment(text)
        # 转成句子向量
        doc_vect = sent2vec(model, sent)
        vectors = self.mongo_db.find("{}_vector".format(prefix), {})
        result_dict = dict()
        for item in vectors:
            idx = item["_id"]
            data = item["data"]
            item_vector = list(map(float, data))
            x = np.vstack([item_vector, doc_vect])
            cosine = 1 - pdist(x, 'cosine')
            if cosine[0] > self.keep_val and idx != sysno:
                result_dict[idx] = [cosine[0]]

        similar_id = 0
        if len(result_dict) >= 1:
            items = result_dict.items()
            # 获取编号
            backitems = [v[0] for v in items]
            backitems.sort()
            similar_id = backitems[0]
        # 保存到数据库
        if similar_id == 0:
            data = {"_id": sysno, "data": list(map(str, doc_vect.tolist()))}
            self.mongo_db.upsert_one("{}_vector".format(prefix), data)

        return [similar_id]


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            try:
                yield gensim.models.doc2vec.LabeledSentence(words=doc.split(), tags=[self.labels_list[idx]])
            except:
                print(doc)


if __name__ == '__main__':
    doc = DocVectSim()
