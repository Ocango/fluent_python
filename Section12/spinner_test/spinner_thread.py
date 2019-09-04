# import threading
# import itertools
# import time
# import sys

# class Signal:
#     go = True

# def spin(msg,signal):
#     write,flush = sys.stdout.write,sys.stdout.flush
#     for char in itertools.cycle('|/-\\'):
#         status = char + ' ' + msg
#         write(status)
#         flush()
#         write('\x08' * len(status))#退格符
#         time.sleep(.1)
#         if not signal.go:
#             break
#     write(' ' * len(status) + '\x08' * len(status))

# def slow_function():
#     #假装等待的样子
#     for i in range(100):
#         time.sleep(0.1)
#     return 42

# def superisor():
#     signal = Signal()
#     spinner  =threading.Thread(target = spin,args = ('thinking!',signal))
#     print('spinner object:',spinner)
#     spinner.start()#激活线程
#     result = slow_function()
#     signal.go = False
#     spinner.join()#等待线程终止
#     return result

# def main():
#     result = superisor()
#     print('Answer:',result)

# if __name__ == '__main__':
#     main()


#!/usr/bin/env python3

# spinner_thread.py

# credits: Adapted from Michele Simionato's
# multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_THREAD
import threading
import itertools
import time


def spin(msg, done):  # <1>
    for char in itertools.cycle('|/-\\'):  # <3>
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        '''
        wait(timeout=None)
        阻塞线程直到内部变量为true。如果调用时内部标志为true，将立即返回。否则将阻塞线程，直到调用 set() 方法将标志设置为true或者发生可选的超时。

        当提供了timeout参数且不是 None 时，它应该是一个浮点数，代表操作的超时时间，以秒为单位（可以为小数）。

        当内部标志在调用wait进入阻塞后被设置为true，或者调用wait时已经被设置为true时，方法返回true。 也就是说，除非设定了超时且发生了超时的情况下将会返回false，其他情况该方法都将返回 True 。
        '''
        if done.wait(.1):  # <5>

            break
    print(' ' * len(status), end='\r')

def slow_function():  # <7>
    # pretend waiting a long time for I/O
    time.sleep(3)  # <8>
    return 42


def supervisor():  # <9>
    done = threading.Event()
    '''
    事件对象
    这是线程之间通信的最简单机制之一：一个线程发出事件信号，而其他线程等待该信号。

    一个事件对象管理一个内部标志，调用 set() 方法可将其设置为true，调用 clear() 方法可将其设置为false，调用 wait() 方法将进入阻塞直到标志为true。

    class threading.Event
    实现事件对象的类。事件对象管理一个内部标志，调用 set() 方法可将其设置为true。调用 clear() 方法可将其设置为false。调用 wait() 方法将进入阻塞直到标志为true。这个标志初始时为false。
    '''
    spinner = threading.Thread(target=spin,
                               args=('thinking!', done))
    '''
    class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)¶
    调用这个构造函数时，必需带有关键字参数。参数如下：

    group 应该为 None；为了日后扩展 ThreadGroup 类实现而保留。

    target 是用于 run() 方法调用的可调用对象。默认是 None，表示不需要调用任何方法。

    name 是线程名称。默认情况下，由 "Thread-N" 格式构成一个唯一的名称，其中 N 是小的十进制数。

    args 是用于调用目标函数的参数元组。默认是 ()。

    kwargs 是用于调用目标函数的关键字参数字典。默认是 {}。

    如果 daemon 不是 None，线程将被显式的设置为 守护模式，不管该线程是否是守护模式。如果是 None (默认值)，线程将继承当前线程的守护模式属性。
    '''
    print('spinner object:', spinner)  # <10>
    spinner.start()  # <11>
    '''
    start()
    开始线程活动。

    它在一个线程里最多只能被调用一次。它安排对象的 run() 方法在一个独立的控制进程中调用。

    如果同一个线程对象中调用这个方法的次数大于一次，会抛出 RuntimeError 。
    '''
    result = slow_function()  # <12>
    done.set()  # <13>
    '''
    set()
    将内部标志设置为true。所有正在等待这个事件的线程将被唤醒。当标志为true时，调用 wait() 方法的线程不会被被阻塞。
    '''
    spinner.join()  # <14>
    '''
    > join(timeout=None)
    等待，直到线程终结。这会阻塞调用这个方法的线程，直到被调用 join() 的线程终结 -- 不管是正常终结还是抛出未处理异常 -- 或者直到发生超时，超时选项是可选的。
    '''
    return result


def main():
    result = supervisor()  # <15>
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_THREAD