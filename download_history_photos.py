import logging
import os
import time

from telethon import TelegramClient, sync  # sync should to be keep, otherwise get error
from telethon.errors import FloodWaitError, RpcCallFailError, ServerError
from telethon.tl import types

import config
from utils import create_path

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.INFO)
logging.getLogger('telethon').setLevel(level=logging.WARNING)

photo_dir = os.path.join(os.environ['HOME'], 'workspace', 'telegram-photos')

api_id = config.api_id
api_hash = config.api_hash
chat = config.chat  # string list of chat IDs, user/channel/group
video_size_limit = config.video_size_limit  # type int. eg. 26214400 that is less than 25MB

client = TelegramClient('telemedia', api_id, api_hash)

create_path(photo_dir, chat)


def pass_floodwait_error(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except FloodWaitError as e:
                logging.info('flood wait for {} seconds.'.format(e.seconds))
                time.sleep(e.seconds)

    return wrapper


def join_photo_name(message):
    name = '{}_{}_{}_{}.jpg'.format(message.chat.id, message.id, message.sender_id, message.date.strftime('%Y%m%d%H%M'))
    logging.info('file name would be {}.'.format(name))
    return name


# @pass_floodwait_error
async def download_photos(entity, download_path):
    '''
    :param client: type TelegramClient
    :param entity: could be a person, chat or channel
    :param download_path: the path that photos would be saved in
    :return:
    '''
    async for message in client.iter_messages(entity, reverse=True):
        if isinstance(message.media, types.MessageMediaPhoto):
            logging.info("Downloading photo from message " + str(message.id) + '.')
            try:
                file_path = os.path.join(download_path, join_photo_name(message))
                await client.download_media(message, file=file_path)
            except FloodWaitError as e:
                logging.info('flood wait for {} seconds.'.format(e.seconds))
                time.sleep(e.seconds)
            except RpcCallFailError as e:
                logging.info('get RpcCallFailError: {}'.format(e))
                time.sleep(60)
            except ServerError as e:
                logging.info('get ServerError: {}'.format(e))
                time.sleep(120)


client.start()

entity = client.get_entity(chat)

logging.info('Starting download photos...')

with client:
    client.loop.run_until_complete(download_photos(entity[0], os.path.join(photo_dir, chat[0])))
