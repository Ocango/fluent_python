from collections import abc

class FrozenJSON:
    '''一个只读接口，使用属性访问JSON类对象
    '''
    def __init__(self, mapping):
        self.__data = dict(mapping)#构建字典，创建副本

    def __getattr__(self,name):
        if hasattr(self.__data,name):#检查本身是否有此属性
            return getattr(self.__data,name)#如果是那就返回此属性
        else:
            return FrozenJSON.build(self.__data[name])
    
    @classmethod
    def build(cls,obj):#备选构造方案
        if isinstance(obj,abc.Mapping):#映射对象
            return cls(obj)
        elif isinstance(obj,abc.MutableSequence):#列表对象
            return [cls.build(item) for item in obj]
        else:
            return obj

