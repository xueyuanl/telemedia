import asyncio
import logging
import time

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl import types

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

def run_untill_success(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except FloodWaitError as e:
                logging.info('%s: flood wait for %s seconds.' % func.__name__, e.seconds)
                time.sleep(e.seconds)
    return wrapper


@run_untill_success
def download_photos(client, entity, download_path='/mnt/telephotos/'):
    '''
    :param client: type TelegramClient
    :param entity: could be a person, chat or channel
    :param download_path: the path that photos would be saved in
    :return: 
    '''
    for message in client.iter_messages(entity):
        if isinstance(message.media, types.MessageMediaPhoto):
            client.download_media(message, file=download_path)
            logging.info('message %s ' % message.id, )
            logging.info(message.date)

def start_client(client):
    client.start()


if __name__ == '__main__':
    api_id = 423258
    api_hash = '60c3795f40aefe47806113cfc4b65409'
    client = TelegramClient(None, api_id, api_hash)



