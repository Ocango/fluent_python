#列表推导，只有一种作用：生成列表
colors = ['black','white']
sizes = ['S','M','L']
tshirts = [(color,size) for color in colors 
                        for size in sizes]
print(tshirts)

#生成器表达式，降低内存占用，因为列表推导会先生成列表，生成器表达式则是使用的迭代的方式
symbols = '$↺➸☠¼'
print(tuple(ord(symbol) for symbol in symbols))
import array
print(array.array('I',(ord(symbol) for symbol in symbols)))

for tshirt in ("%s %s" % (color,size) for color in colors 
                            for size in sizes):
    print(tshirt)

import os
#拆包
_,filename = os.path.split(r'E:\py_work\fluent_python')
print(filename)

