import sys
import pymongo
from utility.logger_decor import exception


class Config(object):
    host = "192.168.60.35"
    port = 27017
    db_name = "mldb"
    account = "mlusr"
    password = "123456"


class MongoDBManager(object):
    """
    MongoDB
    """

    @exception
    def __init__(self):
        try:
            config = Config()
            self.conn = pymongo.MongoClient(config.host, config.port)
            self.db = self.conn[config.db_name]
            self.username = config.account
            self.password = config.password
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            print('Connect Statics Database Fail.')
            sys.exit(1)

    def save(self, table, value):
        """
        一次操作一条记录，根据‘_id’是否存在，决定插入或更新记录
        :param table:
        :param value:
        :return:
        """
        self.db[table].save(value)

    def insert(self, table, value):
        """
        可以使用insert直接一次性向mongoDB插入整个列表，也可以插入单条记录，但是'_id'重复会报错
        :param table:
        :param value:
        :return:
        """
        self.db[table].insert(value, continue_on_error=True)

    def update(self, table, conditions, value, s_upsert=False, s_multi=False):
        """
        更新一条记录
        :param table:
        :param conditions:
        :param value:
        :param s_upsert:
        :param s_multi:
        :return:
        """
        self.db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)

    def upsert_mary(self, table, datas):
        """
        批量更新插入，根据‘_id’更新或插入多条记录。
        把'_id'值不存在的记录，插入数据库。'_id'值存在，则更新记录。
        如果更新的字段在mongo中不存在，则直接新增一个字段
        :param table:
        :param datas:
        :return:
        """
        bulk = self.db[table].initialize_ordered_bulk_op()
        for data in datas:
            _id = data['_id']
            bulk.find({'_id': _id}).upsert().update({'$set': data})
        bulk.execute()

    def upsert_one(self, table, data):
        """
        更新插入，根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
        :param table:
        :param data:
        :return:
        """
        query = {'_id': data.get('_id', '')}
        if not self.db[table].find_one(query):
            self.db[table].insert(data)
        else:
            data.pop('_id')  # 删除'_id'键
            self.db[table].update(query, {'$set': data})

    def find_one(self, table, value):
        """
        根据条件进行查询，返回一条记录
        :param table:
        :param value:
        :return:
        """
        return self.db[table].find_one(value)

    def find(self, table, value):
        """
        根据条件进行查询，返回所有记录
        :param table:
        :param value:
        :return:
        """
        return self.db[table].find(value)

    def remove(self, table, value):
        """
        根据条件进行查询，返回所有记录
        :param table:
        :param value:
        :return:
        """
        return self.db[table].remove(value)
