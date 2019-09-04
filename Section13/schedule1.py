import warnings

import osconfeed


DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conferebce.115'

class Record():
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)#一个技巧:__dict__储存着对象的属性，直接update他，传入映射关系是一个及其方便的构建对象的方法

def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading '+DB_NAME)
    for collection,res_list in raw_data['Schedule'].items():
        record_type = collection[:-1]
        for record in res_list:
            key = '{}.{}'.format(record_type,record['serial'])#定义key值
            record['serial'] = key
            db[key] = Record(**record)

