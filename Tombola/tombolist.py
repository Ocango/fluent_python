from random import randrange
from Tombola.tombola import Tombola

@Tombola.register
class TomboList(list):
    def pick(self):
        if self:
            position = randrange(len(self))
        else:
            raise LookupError('pop from empty TomboList')
    
    load = list.extend

    def loaded(self):
        return bool(self)
    
    def inspect(self):
        return tuple(sorted(self))

#注册的虚拟子类，可以用__mro验明真身
#其他issubclass，isinstance都是查不出来，被蒙骗，而且生成对象也不会报错
