import asyncio
import collections

import aiohttp
from aiohttp import web
import tqdm

from flags_commen import main,HTTPStatus,Result,save_flags

#默认设置为较小的值
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception):#包装网络异常，捕获城市代号
    def __init__(self,country_code):
        self.country_code = country_code

async def get_flag(session,base_url,cc):
    url = "{}/{cc}/{cc}.gif".format(base_url,cc=cc.lower())
    async with session.get(url) as resp:
        if resp.status ==200:
            return await resp.read()
        elif resp.status == 404:
            raise web.HTTPNotFound()
        else:
            raise aiohttp.HttpProcessingError(
                code = resp.status,message = resp.reason,
                headers = resp.headers
            )
        
async def download_one(session,cc,base_url,semaphore,verbose):
    try:
        async with semaphore:#限制并发量
            image = await get_flag(session,base_url,cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc#这个主要是为了在异常捕获加上国家代号,并链接原异常
    else:
        save_flags(image,cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'
    
    if verbose and msg:
        print(cc,msg)
    
    return Result(status,cc)

async def downloader_coro(cc_list,base_url,verbose,concur_req):
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)#限制并发量的同步装置
    async with aiohttp.ClientSession() as session:
        to_do = [download_one(session,cc,base_url,semaphore,verbose) for cc in sorted(cc_list)]#协程对象列表

        to_do_iter = asyncio.as_completed(to_do)#获取一个迭代器，在运行结束后返回future
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter,total = len(cc_list))
        for future in to_do_iter:
            try:
                res = await future#获取asyncio.Future对象的结果
            except FetchError as exc:
                country_code = exc.country_code#错误的国家代码
                try:
                    error_msg = exc.__cause__.args[0]#原错误讯息
                except IndexError:
                    error_msg = exc.__cause__.__class__.__name__#将连接的异常作为错误
                if verbose and error_msg:
                    msg = '*** Error for {}:{}'
                    print(msg.format(country_code,error_msg))
                status = HTTPStatus.error
            else:
                status = res.status
            
            counter[status] += 1

    return counter

def download_many(cc_list,base_url,verbose,concur_req):#实例化downloader_coro协程再通过run_until_complete传给事件循环
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list,base_url,verbose,concur_req)
    counts = loop.run_until_complete(coro)
    loop.close()

    return counts

if __name__ == '__main__':
    main(download_many,DEFAULT_CONCUR_REQ,MAX_CONCUR_REQ)


