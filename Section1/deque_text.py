from collections import deque
dq = deque(range(10),maxlen = 10)
dq.rotate(-4)
print(dq)
dq.pop()
print(dq)
dq.extend([11,12,13])
print(dq)

import queue
#用以同步线程安全，满员时会等待销毁后再执行
import multiprocessing
#用以同步进程管理，同queue
import asyncio
#是用来编写 并发 代码的库，使用 async/await 语法
import heapq
#将可变序列当做堆队列处理