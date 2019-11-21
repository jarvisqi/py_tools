import logging
import time


def create_logger():
    """
    创建日志
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    time_format = '%Y-%m-%d'
    filename = time.strftime(time_format, time.localtime(time.time()))
    handler = logging.FileHandler("./logs/{}.txt".format(filename))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def exception(func):
    """
    异常装饰器
    @param func: The function object
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger = create_logger()
            err = "There was an exception in  "
            err += func.__name__
            logger.exception(err)

            raise

    return wrapper
