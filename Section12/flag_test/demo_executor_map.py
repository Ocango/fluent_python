from time import sleep,strftime
from concurrent import futures

def display(*args):
    print(strftime('[%H:%M:%S]'),end = ' ')
    print(*args)

def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n,n,n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n,n))
    return n*10

def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers = 4)
    results = executor.map(loiter,[10,2,15,4])
    display('results:',results)
    display('Waiting for individual results:')
    for i,result in enumerate(results):#通过__next__迭代器的方式返回一个元祖
        display('result {}: {}'.format(i,result))

main()