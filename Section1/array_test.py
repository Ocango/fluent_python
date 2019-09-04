from array import array
from random import random
# floats = array('d',(random()*100 for i in range(10**7)))
# print(floats[-1])
# #注意哦，数组里面存的是数字的字节表达
# fp = open('floats.bin','wb')
# floats.tofile(fp)
# fp.close()

# #内存视图memoryview
# '''
# 泛化和去数学化的NumPy数组，实现在数据结构之间共享内存。用以处理大型数据集合
# 注意共享内存的意思是对memoryview的操作不会产生新的对象！！！这也是其高效的原因
# '''
# numbers = array('h',[-2,-1,0,1,2])
# memv = memoryview(numbers)
# numbers[2] = 5
# memv[1] = 2
# memv_oct = memv.cast('B')
# memv_oct[7] = 4

# #NumPy 与 SciPy
# '''
# 高阶数组与矩阵操作
# NumPy实现了多维同质数组和矩阵
# SciPy为线性代数、数值积分、统计学而生
# '''
import numpy
# a = numpy.arange(12)
# a.shape = 3,4
# print(a)
# print(a[1,2])
# #矩阵翻转
# a = a.transpose()
# print(a)

# # 只是为了生成文件
# floatss = array('d',(random()*1000 for i in range(10**7)))
# file=open('data.txt','w')
# for floats in floatss :
#     file.write(str(floats) + '\n')
# file.close()

from time import perf_counter as pc
t0 = pc()
floats = numpy.loadtxt('data.txt')
t1 = pc()
floats /= 3
t2 = pc()
numpy.save('floats-10M',floats)
t3 = pc()
floats2 = numpy.load('floats-10M.npy','r+')
t4 = pc()
floats2 *=363
t5 = pc()
print(floats2[-9:])
print({ 't0':t0,
        't1':t1,
        't2':t2,
        't3':t3,
        't4':t4,
        't5':t5})