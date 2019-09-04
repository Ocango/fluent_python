import sys,asyncio

from charfinder import UnicodeNameIndex

CRLF = b'\r\n'
PROMPT = b'?>'

index = UnicodeNameIndex()

async def handle_queries(reader,writer):
    while True:
        writer.write(PROMPT)#StreamWriter.write向流中写入数据
        await writer.drain()#StreamWriter.drain等到适当时再恢复对流的写入
        data = await reader.readline()#StreamReader.readline读一行，其中“line”是以\n。结尾的字节序列。如果收到EOF \n但未找到，则该方法返回部分读取的数据。如果收到EOF且内部缓冲区为空，则返回一个空bytes对象。
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:#处理telnet客户端decode异常，设定为传空字符
            query = '\x00'
        client = writer.get_extra_info('peername')#返回与套接字连接的远程地址
        print('Received from {}: {!r}'.format(client,query))
        if query:
            if ord(query[:1]) < 32:#收到控制字符，退出
                break
            lines = list(index.find_description_strs(query))
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines)#将一个列表（或任何可迭代的）字节写入流。
            writer.write(index.status(query,len(lines)).encode() + CRLF)

            await writer.drain()#刷新输出缓冲
            print('Sent {} results'.format(len(lines)))
        
    print('Close the client socket')
    writer.close()

def main(address = '127.0.0.1',port = 2323):
    port = int(port)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(handle_queries,address,port,loop=loop)#返回一个TCP套接字服务器
    server = loop.run_until_complete(server_coro)#启动服务器
    host = server.sockets[0].getsockname()
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:#有个小问题，win下面捕获不到，捕捉不到KeyboardInterrupt
        pass
    print('Server shutting down.')
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main(*sys.argv[1:]) 