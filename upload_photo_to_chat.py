import logging
import time
import os
from random import randint

from telethon import TelegramClient
from utils import create_folder
from config import api_id, api_hash
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.INFO)
logging.getLogger('telethon').setLevel(level=logging.WARNING)


client = TelegramClient('telemedia', api_id, api_hash)
client.start()


def time_wait():
    minutes = randint(10, 60)
    logging.info('get random minutes {}'.format(minutes))
    time.sleep(minutes * 60)
    logging.info('slept for {} minutes.'.format(minutes))


def pick_up_photo(path):
    files = os.listdir(path)
    file_number = len(files)
    logging.info('the number of files is {}.'.format(file_number))
    index = randint(0, file_number - 1)
    return files[index]


def back_up_photo(file, folder):
    logging.info('move {} to {}'.format(file, folder))
    os.system('mv {} {}'.format(file, folder))

async def main():
    # Now you can use all client methods listed below, like for example...
    path = '/Users/tutu/workspace/telegram-photos/streetshoot'
    create_folder(os.path.join(path, 'sent'))
    entity = 'tuhuatianxia'
    while True:
        photo_name = pick_up_photo(path)
        logging.info('get file {}'.format(photo_name))
        await client.send_file(entity, os.path.join(path, photo_name))
        back_up_photo(os.path.join(path, photo_name), os.path.join(path, 'sent'))
        time_wait()

with client:
    client.loop.run_until_complete(main())
