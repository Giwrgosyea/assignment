import time
from functools import wraps

from app.main.config import config
from app.main.log.logger import Logger
from mongoengine import connect, disconnect

my_logger = Logger(__name__)
logger = my_logger.get_logger()


def mongodb_access(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        connect(db=config.MONGO_DATABASE, host=config.MONGO_URI)
        res = f(*args, **kwargs)
        disconnect()
        return res

    return decorated


def timeit(method):
    @wraps(method)
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            logger.info("%r  %2.2f s" % (method.__name__, (te - ts)))
        return result

    return timed
