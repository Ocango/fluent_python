
import abc
class Tombola(abc.ABC):
    '''取值抽象基类'''
    @abc.abstractmethod
    def load(self,iterable):
        """
        从可迭代对象中添加元素
        """
    
    @abc.abstractmethod
    def pick(self):
        """
        随机删除元素，并返回
        如果实例为空，则返回‘LookupError’
        """
    
    def loaded(self):
        """检查是否有元素"""
        return bool(self.inspect())
    
    def inspect(self):
        """返回一个有序数组，由当前元素组成"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        
        self.load(items)
        return tuple(sorted(items))

    