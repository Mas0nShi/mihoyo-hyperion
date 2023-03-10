from functools import wraps
import logging
from loguru import logger
import os
import pathlib

PATH = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
LOG_PATH = os.path.join(PATH, 'logs')
logging.getLogger("urllib3").setLevel(logging.WARNING)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 3
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logger.add(f'{LOG_PATH}/{{time}}.log', rotation='1 day', retention='7 days', level='DEBUG', encoding='utf-8')
mlog = logging.getLogger('miyoushe')
mlog.setLevel(logging.DEBUG)
mlog.addHandler(InterceptHandler())

def new_logger(name: str) -> logging.Logger:
    _log = logging.getLogger(name)
    _log.setLevel(logging.DEBUG)
    _log.addHandler(InterceptHandler())
    return _log

def called(message: str, show_args: bool = False, show_return: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
                msg = message
                msg += f' args: {args}' if show_args else ''
                msg += f' return: {result}' if show_return else ''
                mlog.debug(msg)
            except Exception as e:
                mlog.error(e)

            return result

        return wrapper

    return decorator


if __name__ == '__main__':
    @called('test called')
    def test():
        print('test')
    test()

