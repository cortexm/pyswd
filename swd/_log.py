"""logging module"""

import logging

DEBUG = logging.DEBUG
DEBUG1 = logging.DEBUG - 1
DEBUG2 = logging.DEBUG - 2
DEBUG3 = logging.DEBUG - 3
DEBUG4 = logging.DEBUG - 4
DEBUG5 = logging.DEBUG - 5

def configure():
    """configure logging levels"""
    logging.addLevelName(DEBUG1, 'DEBUG1')
    logging.addLevelName(DEBUG2, 'DEBUG2')
    logging.addLevelName(DEBUG3, 'DEBUG3')
    logging.addLevelName(DEBUG4, 'DEBUG4')
    logging.addLevelName(DEBUG5, 'DEBUG5')


def log(level):
    """Decorator for logging function call with parameters"""
    def log_decorator(func):
        """Real decorator"""
        def wrapper(*args, **kwargs):
            """wrapper for decorated function"""
            ret = func(*args, **kwargs)
            func_varnames = func.__code__.co_varnames
            func_name = func.__name__
            if 'self' in func_varnames:
                func_name = '%s.%s' % (args[0].__class__.__name__, func_name)
                func_varnames = func_varnames[1:]
                args = args[1:]
            str_args = []
            for name, arg in zip(func_varnames, args):
                if name == 'address':
                    str_args.append('0x%08x' % arg)
                else:
                    str_args.append(str(arg))
            logging.log(
                level, '%s.%s(%s)',
                func.__module__,
                func_name,
                ', '.join(str_args))
            return ret
        return wrapper
    return log_decorator
