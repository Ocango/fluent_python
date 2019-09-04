def record_factory(cls_name,field_names):
    try:
        field_names = field_names.replace(',',' ').split()#贯彻鸭子类型，针对不同情况，最终实现结果
    except AttributeError:
        pass
    field_names = tuple(field_names)#使用属性名构建元组

    def __init__(self,*args,**kwargs):
        attrs = dict(zip(self.__slots__,args))
        attrs.update(kwargs)
        for name,value in attrs.items():
            setattr(self,name,value)
    
    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self,name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__,self))
        return '{}({})'.format(self.__class__.__name__,values)

    cls_attrs = dict(__slots__ = field_names,#组建类的属性字典
                    __init__ = __init__,
                    __iter__ = __iter__,
                    __repr__ = __repr__)

    return type(cls_name,(object,),cls_attrs)#用type构造方法构造新类

My_store = record_factory('Book','name reader text price')
rex = My_store('develop','JX','书记',12)

print(rex)