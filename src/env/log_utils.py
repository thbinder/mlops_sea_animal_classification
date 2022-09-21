import logging
import time

logger = logging.getLogger(__name__)


def log_duration(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info("{} took {} seconds".format(func.__name__, round(end - start, 3)))
        return result

    return wrapper
