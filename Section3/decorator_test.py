#!/usr/bin/python
# -*- coding:utf-8 -*-
#示例
def deco(func):
    def inner():
        print('running inner()')
    return inner

@deco
def target():
    print('running target()')

target()
'''
此方法其实就是
def target():
    print('running target()')
target = deco(target)
仔细看区别
'''

# 计算移动平均值
## 使用类定义可调用对象
class Averager():
    def __init__(self):
        self.series = []
    def __call__(self,new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)

## 定义高阶函数
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)
    
    return averager

## 装饰器：输出函数运行时间

import time
def clock(func):
    print("start")
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed,name,arg_str,result))
        return result
    return clocked

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n<2 else n * factorial(n-1)

# print('*'*40 , 'Calling snooze(.123)')
# snooze(.123)
# print('*'*40 , 'Calling factorial(6)')
# print('6! = ',factorial(6))

import functools
def clock2(func):
    @functools.wraps(func)
    def clocked(*args,**kwargs):
        t0 = time.time()
        result = func(*args,**kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(','.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k,w) for k,w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.append(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed,name,arg_str,result))
    return clocked

# print('6! = ',factorial(6))
@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2 :
        return n
    return fibonacci(n-2) + fibonacci(n-1)

# print(fibonacci(30))


#单分派泛函数
from collections import abc
import numbers
import html
#作为默认实现
@functools.singledispatch
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)
#注册其他实现
@htmlize.register(str)
def _(text):
    content = html.escape(text).replace('\n','<br>\n')
    return '<p>{0}</p>'.format(content)
@htmlize.register(numbers.Integral)
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)
@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

print(htmlize([12,'江苏',['Single',1,72]]))

