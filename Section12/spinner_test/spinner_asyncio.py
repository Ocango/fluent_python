import asyncio
import itertools
import sys
'''
@asyncio.coroutine
用来标记基于生成器的协程的装饰器。

此装饰器使得旧式的基于生成器的协程能与 async/await 代码相兼容:

@asyncio.coroutine
def old_style_coroutine():
    yield from asyncio.sleep(1)

async def main():
    await old_style_coroutine()
此装饰器 已弃用 并计划觉得 Python 3.10 中移除。

此装饰器不应该被用于 async def 协程。
'''
# @asyncio.coroutine
# def spin(msg):
#     write,flush = sys.stdout.write,sys.stdout.flush
#     for char in itertools.cycle('|/-\\'):
#         status = char + ' ' + msg
#         write(status)
#         flush()
#         write('\x08' * len(status))#退格符
#         try:
#             yield from asyncio.sleep(.1)#不阻塞事件循环
#         except asyncio.CancelledError:
#             break
#     write(' ' * len(status) + '\x08' * len(status))

# @asyncio.coroutine
# def slow_function():
#     #假装等待的样子
#     yield from asyncio.sleep(5)
#     return 42

# @asyncio.coroutine
# def superisor():
#     spinner = asyncio.async(spin('thinking!'))
#     print('spinner object:',spinner)
#     result = yield from slow_function()
#     spinner.cancel()
#     return result

# def main():
#     loop = asyncio.get_event_loop()
#     '''
#     获取当前事件循环。 如果当前 OS 线程没有设置当前事件循环并且 set_event_loop() 还没有被调用，asyncio 将创建一个新的事件循环并将其设置为当前循环。
#     由于此函数具有相当复杂的行为（特别是在使用了自定义事件循环策略的时候），更推荐在协程和回调中使用 get_running_loop() 函数而非 get_event_loop()。
#     应该考虑使用 asyncio.run() 函数而非使用低层级函数来手动创建和关闭事件循环。
#     '''
#     result = loop.run_until_complete(superisor())#运行loop直到结束或抛出异常
#     loop.close()
#     print('Answer:',result)

# if __name__ == '__main__':
#     main()

import asyncio
import itertools


async def spin(msg):  # <1>
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        try:
            await asyncio.sleep(.1)  # <2>
        except asyncio.CancelledError:  # <3>
            break
    print(' ' * len(status), end='\r')


async def slow_function():  # <4>
    # pretend waiting a long time for I/O
    await asyncio.sleep(3)  # <5>
    return 42


async def supervisor():  # <6>
    spinner = asyncio.create_task(spin('thinking!'))  # <7>
    print('spinner object:', spinner)  # <8>
    result = await slow_function()  # <9>
    spinner.cancel()  # <10>
    return result


def main():
    result = asyncio.run(supervisor())  # <11>
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO