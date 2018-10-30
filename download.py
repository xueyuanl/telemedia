import asyncio
import functools
import logging
import time

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl import types

DOWNLOAD_PATH = '/mnt/telephotos/'


def run_till_success(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except FloodWaitError as e:
                logging.log(logging.INFO, '%s: flood wait for %s seconds.' % func.__name__, e.seconds)
                time.sleep(e.seconds)
            except ValueError:
                logging.log(logging.INFO, '%s: connecting again' % func.__name__)
                self.client.connect()
            except TimeoutError:
                logging.log(logging.INFO, '%s: timeout' % func.__name__)
                time.sleep(2)
                self.client.connect()

    return wrapper


# Create a global variable to hold the loop we will be using
loop = asyncio.get_event_loop()


class Teleclient:
    """Download media(photos, videos) in chart
    """

    def __init__(self, client=None):
        self.client = client
        self.api_id = 423258
        self.api_hash = '60c3795f40aefe47806113cfc4b65409'
        self.dialogs = None

    async def creat_client(self):
        self.client = TelegramClient(None, self.api_id, self.api_hash)
        await self.client.start()
        return self.client

    async def get_dialogs(self):
        self.dialogs = await self.client.get_dialogs()
        return self.dialogs

    @run_till_success
    def get_photos(self, entity):
        for message in self.client.iter_messages(entity):
            if isinstance(message.media, types.MessageMediaPhoto):
                self.client.download_media(message, file=DOWNLOAD_PATH)
                print(message.id)


if __name__ == '__main__':
    teleclient = Teleclient()
    loop.run_until_complete(teleclient.creat_client())


while True:
    try:
        for message in client.iter_messages(dialogs[3]):
            teleclient.client.download_media(message, file='/mnt/telephotos')
            print(message.id)
    except FloodWaitError as e:
        logging.log(logging.INFO, '%s: flood wait for %s seconds.' % func.__name__, e.seconds)
        time.sleep(e.seconds)