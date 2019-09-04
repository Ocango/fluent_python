from array import array
import math
class Vector2d():
    __slots__ = ('__x','__y')#表示slots实例只有一个含有__x,__y的元组
    #__weakref__默认会有，但是定义__slots__要记得把__weakref__加上去
    #所以说__slots__最好用在数据集处理上
    typecode = 'd'
    def __init__(self, x=0, y=0):
        self.__x = float(x)
        self.__y = float(y)
    
    @property#将读值属性标记为特性
    def x(self):#读值属性与公开属性同名
        return self.__x#直接返回__x
    
    @property
    def y(self):
        return self.__y
    
    def __iter__(self):#为了__repr__()拆包,将其变成可迭代对象
        return (i for i in (self.x,self.y))
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        class_name = type(self).__name__
        #%r就是调用对象的__repr__
        return '{}({!r},{!r})'.format(class_name,*self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)])) + bytes(array(self.typecode,self))

    def __eq__(self, value):
        return tuple(self) == tuple(value)

    def __abs__(self):
        #平方根
        return math.hypot(self.x,self.y)
    
    def __bool__(self):
        # return bool(abs(self))
        return bool(self.x or self.y)

    def angle(self):
        return math.atan2(self.y,self.x)
    
    @classmethod#类方法
    def frombytes(cls,octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
    
    def __format__(self, format_spec = ''):
        #优化下：可以解析以p结尾的格式化语句，以转化为极坐标系
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self),self.angle())
            outer_fmt = '<{},{}>'
        else:
            coords = self
            outer_fmt = '({},{})'
        components = (format(c,format_spec) for c in coords)
        return outer_fmt.format(*components)
print(format(Vector2d(1,1),'0.5fp'))
vector1 = Vector2d(3,4)
vector2 = Vector2d(11,13)
vector1._Vector2d__x = 5
print(set([vector1,vector2]))