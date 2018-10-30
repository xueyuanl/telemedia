import logging
import time
from telethon.errors import FloodWaitError


class Decorator:

    def run_till_success(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except FloodWaitError as e:
                    logging.log(logging.INFO, '%s: flood wait for %s seconds.' % func.__name__, e.seconds)
                    time.sleep(e.seconds)
                except ValueError:
                    logging.log(logging.INFO, '%s: connecting again' % func.__name__)
                    client.connect()
                except TimeoutError:
                    logging.log(logging.INFO, '%s: timeout' % func.__name__)
                    time.sleep(2)
                    client.connect()
        return wrapper

