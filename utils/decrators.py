import time
from functools import wraps

from loguru import logger


def timer(func):
    """基础计时装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"函数 {func.__name__} 执行耗时: {end_time - start_time:.4f} 秒")
        return result

    return wrapper


def retry(times=3, excepts: tuple = None):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_times = times
            exceptions = excepts if excepts else ()
            exp = None
            while retry_times:
                retry_times -= 1
                try:
                    result = func(*args, **kwargs)
                except exceptions as e:
                    raise e
                except Exception as e:
                    logger.exception(e)
                    exp = e
                    continue
                if result is not None:
                    return result
                else:
                    logger.debug(f'retry {func.__name__},left times {retry_times}')
                    continue
            else:
                logger.debug(f'failed retry {func.__name__} after  {retry_times} times,exceptions {exp}')

        return wrapper

    return decorate


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
