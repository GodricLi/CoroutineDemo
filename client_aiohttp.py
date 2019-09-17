import asyncio
import aiohttp
import time

"""
aiohttp 是一个支持异步请求的库，利用它和 asyncio 配合我们可以非常方便地实现异步请求操作
    开始运行时，时间循环会运行第一个 task，针对第一个 task 来说，当执行到第一个 await 跟着的 get() 方法时，
它被挂起，但这个 get() 方法第一步的执行是非阻塞的，挂起之后立马被唤醒，所以立即又进入执行，创建了 ClientSession 对象，
接着遇到了第二个 await，调用了 session.get() 请求方法，然后就被挂起了，由于请求需要耗时很久，所以一直没有被唤醒。
第一个 task 被挂起了，事件循环会寻找当前未被挂起的协程继续执行，于是就转而执行第二个 task 了，
也是一样的流程操作，直到执行了第五个 task 的 session.get() 方法之后，全部的 task 都被挂起了。所有 task 都已经处于挂起状态，
那咋办？只好等待了。3 秒之后，几个请求几乎同时都有了响应，然后几个 task 也被唤醒接着执行，输出请求结果，最后耗时，3 秒！
"""

start = time.time()


# 阻塞操作都要用await手动挂起
async def get(url):
    session = aiohttp.ClientSession()               # 创建ClientSession对象
    response = await session.get(url)               # 发起异步请求，同样支持post()，headers,params/data,proxy等参数
    result = await response.text()                  # 获取响应文本,json()返回json类型,read()返回二进制
    await session.close()                           # 关闭连接资源
    return result


# 上面的代码可以使用with语句，不用关闭资源
async def get_page(url):
    async with aiohttp.ClientSession() as session:
        async with await  session.get(url) as response:
            result = await response.text()
            return result


async def request():
    url = 'http://127.0.0.1:5000'
    print('Waiting for', url)
    # result = await get(url)
    result = await  get_page(url)
    print('Get response from', url, 'Result:', result)


tasks = [asyncio.ensure_future(request()) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('Cost time:', end - start)
