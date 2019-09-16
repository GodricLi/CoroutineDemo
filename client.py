import asyncio
import time
import requests

"""
要实现异步处理，我们得先要有挂起的操作，当一个任务需要等待 IO 结果的时候，
可以挂起当前任务，转而去执行其他任务，这样我们才能充分利用好资源，
要实现异步，接下来我们再了解一下 await 的用法，
使用 await 可以将耗时等待的操作挂起，让出控制权。当协程执行的时候遇到 await，
时间循环就会将本协程挂起，转而去执行别的协程，直到其他的协程挂起或执行完毕
"""

start = time.time()


async def get(url):
    """用 async 把请求的方法改成 coroutine 对象"""
    return requests.get(url)


async def request():
    """
    await 后面的对象必须是如下格式之一：
        一个原生 coroutine 对象
        可以返回 coroutine 对象decorated with types.coroutine()
        一个包含 __await 方法的对象返回的一个迭代器

    用 async 把请求的方法改成 coroutine 对象
    """
    url = "http://127.0.0.1:5000"
    print('Waiting for ', url)
    response = await get(url)
    print('Get response form ', url, 'Result:', response.text)


tasks = [asyncio.ensure_future(request()) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('Cost time:', end - start)

"""
仅仅将涉及 IO 操作的代码封装到 async 修饰的方法里面是不可行的！
我们必须要使用支持异步操作的请求方式才可以实现真正的异步，需要 aiohttp
"""