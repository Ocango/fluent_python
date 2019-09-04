# def gen_123():
#     print('start')
#     yield f1
#     print('end f1')
#     yield f2
#     print('end f2')
#     yield f3
#     print('end f3')

# def f1():
#     return 1
# def f2():
#     return 2
# def f3():
#     return 3


# g = gen_123()

# print(next(g)())
# print(next(g)())
# print(next(g)())

#调用当前对象的生成器
# def chain(quen):
#     yield from quen
# for a in chain([1,2,3,4,5]):
#     print(a)

# from random import randint
# def d6():
#     return randint(1,6)

# #类似截止符的操作。有一个比较有趣的用法
# d6_iter = iter(d6,1)
# for item in d6_iter:
#     print(item)

import asyncio
async def time_lose(a):
    print('start:',a)
    await asyncio.sleep(a)
    print(a)


loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(time_lose(my_list)) for my_list in [4,5,2,5,7]
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()