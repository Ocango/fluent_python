from concurrent import futures#启动并行任务
from flags import save_flags,get_flag,show,main

MAX_WORKS = 20

def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flags(image,cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    workers = min(MAX_WORKS,len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:#创建执行器对象
        res = executor.map(download_one,sorted(cc_list))#异步并发，其他且同map(func, *iterables)
    
    return len(list(res))

if __name__ == '__main__':
    main(download_many)