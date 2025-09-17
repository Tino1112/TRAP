import functools
import logging
import functions
from datetime import datetime
from database.database import Database
from new_trap.tables import Logs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def now():
    return datetime.now()

class Log:
    def __init__(self, username):
        self.database = Database('pstg', logger)
        self.username = username

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            params = f'args={args}, kwargs={kwargs}'
            error_msg = None

            start_time = now()

            try:
                return_func = func(*args, **kwargs)
            except Exception as e:
                error_msg = str(e)
                raise
            finally:
                end_time = now()
                run_time = float((end_time - start_time).total_seconds())

                log_dict = {'username': self.username,
                            'func_name': func_name,
                            'params': params,
                            'start_time': start_time,
                            'end_time': end_time,
                            'runtime': run_time,
                            'error_msg': error_msg}

                with self.database.start_session() as pstg_session:
                    self.database.insert_data(log_dict, Logs)

            return return_func
        return wrapper
