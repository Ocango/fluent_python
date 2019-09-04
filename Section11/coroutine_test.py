# def simple_coroutine( a ):
#     print('-> coroutine started! ', a)
#     x = yield a
#     print('-> coroutine received :',x)

# #使用inspect.getgeneratorstate(...)确定协程的状态
# my_coro = simple_coroutine(12)#'GEN_CREATED'等待开始执行
# # my_coro.send(None)
# next(my_coro)#'GEN_RUNNING'解释器正在执行，也可以send(None)督促其执行
# #'GEN_SUSPENDED'在yield处暂停
# my_coro.send(42)#'GEN_RUNNING'解释器正在执行
#'GEN_CLOSED'执行结束

# from functools import wraps
# def coroutine(func):
#     """装饰器：向前执行到第一个yield表达式，预先激活'func'"""
#     @wraps(func)
#     def primer(*args,**kwargs):
#         gen = func(*args,**kwargs)
#         next(gen)
#         return gen
#     return primer

from collections import namedtuple
Results = namedtuple('Result','count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Results(count,average)

avg = averager()
next(avg)
avg.send(12)
avg.send(32)
avg.send(None)