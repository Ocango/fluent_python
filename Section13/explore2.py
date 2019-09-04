from collections import abc
from keyword import iskeyword

class FrozenJSON:
    '''一个只读接口，使用属性访问JSON类对象
    '''
    def __new__(cls,arg):
        if isinstance(arg,abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg,abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg


    def __init__(self, mapping):
        self.__data = {}#构建字典，创建副本
        for key,value in mapping.items():
            if iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self,name):
        if hasattr(self.__data,name):#检查本身是否有此属性
            return getattr(self.__data,name)#如果是那就返回此属性
        else:
            return FrozenJSON(self.__data[name])

from osconfeed import load
some_thing = load()
feed_item = FrozenJSON(some_thing)
a = feed_item.Schedule.venues[0].name
print(a)