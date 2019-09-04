from concurrent import futures#启动并行任务
from flags import main
from flags_threadpool import download_one

def download_many(cc_list):
    # cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers = 3) as executor:
        to_do = []
        #创建并排定future
        for cc in sorted(cc_list):
            future = executor.submit(download_one,cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc,future))
        #获取future的结果
        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future,res))
            results.append(res)

    return len(results)

if __name__ == '__main__':
    main(download_many)