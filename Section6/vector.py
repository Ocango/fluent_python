from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools

class Vector():
    typecode = 'd'
    shortname_names = 'xyzt'

    def __init__(self,components):
        self._components = array(self.typecode,components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)#获取其有限长度表示
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __eq__(self, value):
        if len(self) != len(value):
            return False
        for a,b in zip(self,value):
            if a!= b :
                return False
        return True

    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __abs__(self):
        return math.sqrt(sum(x*x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def angle(self,n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r,self[n-1])
        if (n==len(self) - 1) and (self[-1] < 0):
            return math.pi *2 -a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1,len(self)))

    def __format__(self, format_spec = ''):
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self)],self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c,format_spec) for c in coords)
        return outer_fmt.format(', '.join(components))


#实现序列的特性
    def __getitem__(self,index):
        '''
        这个内容审查可以参阅：
        class Myseq:
            def __getitem__(self,index):
                return index
        从而查看index的行为
        '''
        cls = type(self)
        if isinstance(index,slice):
            return cls(self._components[index])#切片是返回slice
        elif isinstance(index,numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    def  __len__(self):
        return len(self._components)

    @classmethod
    def frombytes(cls,octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:].cast(typecode))
        return cls(memv)
    
    #动态存取属性
    def __getattr__(self,name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortname_names.find(name)
            if 0<= pos <len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls,name)) 
    
    def __setattr__(self,name,value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortname_names:
                error = 'Readonly attribute {attr_name!r}'
            elif name.islower():
                error = "Can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name = cls.__name__,attr_name = name)
                raise AttributeError(msg)
        super().__setattr__(name,value)
    
    def __hash__(self):
        hashed = (hash(x) for x in self._components)
        return functools.reduce(operator.xor,hashed,0)


vector = Vector([3,4,0,0])
print(format(vector,'0.5fh'))
