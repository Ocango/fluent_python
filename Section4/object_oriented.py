lists = [1,2,3,4,5]
t1 = ('haha',lists)
lists.append(77)
# print(t1)

import copy
class Bus():
    def __init__(self, peoplelist = None):
        if peoplelist is None:
            self.peoplelist = []
        else:
            self.peoplelist = list(peoplelist)
    
    def pick(self,people):
        self.peoplelist.append(people)
    
    def drop(self,poeple):
        self.peoplelist.remove(poeple)
    
    def __repr__(self):
        return "<Bus>:{!r}".format(self.peoplelist)
    
# bus = Bus(['aa','bb','cc'])
# bus2 = copy.copy(bus)
# bus3 = copy.deepcopy(bus)
# bus2.pick('dd')
# bus3.drop('aa')
# print({1:bus,2:bus2,3:bus3})

# class Bus():
#     def __init__(self, peoplelist = []):
#         self.peoplelist = list(peoplelist)
    
#     def pick(self,people):
#         self.peoplelist.append(people)
    
#     def drop(self,poeple):
#         self.peoplelist.remove(poeple)
    
#     def __repr__(self):
#         return "<Bus>:{!r}".format(self.peoplelist)
# bus = Bus()
# bus.pick('qq')

# bus1 = Bus()
# bus1.pick('11')
# bus2 = Bus()
# bus2.pick('22')
# print({1:bus,2:bus1,3:bus2})

#演示一个回调函数
import weakref
# s1 = {1,2,3}
# s2 = s1
# def bye():
#     print('GOODBYE!')

# ender = weakref.finalize(s1,bye)
# print(ender.alive)
# del s1#不会删除对象
# print(ender.alive)
# s2 = 'spam'#重新绑定最后一个引用导致{1,2,3}无法获取，则对象被销毁
# print(ender.alive)
class Cheese():
    def __init__(self,kind):
        self.kind = kind
    def __repr__(self):
        return 'Cheese(%r)' % self.kind

stock = weakref.WeakValueDictionary()
catalog = [Cheese('aa'),Cheese('bb'),Cheese('cc'),Cheese('dd')]
for cheese in catalog:#cheese是一个全局变量影响了其回收
    stock[cheese.kind] = cheese
    print(cheese)
print(sorted(stock.keys()))
del catalog
print(sorted(stock.keys()))
del cheese
print(sorted(stock.keys()))

