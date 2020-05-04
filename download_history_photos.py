import logging
import time

from telethon import TelegramClient, sync
from telethon.errors import FloodWaitError
from telethon.tl import types

import config
from utils import mkdirs

photo_dir = config.photo_dir

logging.basicConfig(level=logging.INFO)
logging.getLogger('telethon').setLevel(level=logging.WARNING)

api_id = config.api_id
api_hash = config.api_hash
chat = config.chat  # string list of chat IDs, user/channel/group
video_size_limit = config.video_size_limit  # type int. eg. 26214400 that is less than 25MB

client = TelegramClient('telemedia', api_id, api_hash)

mkdirs(photo_dir, chat)


def pass_floodwait_error(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except FloodWaitError as e:
                logging.info('%s: flood wait for %s seconds.' % func.__name__, e.seconds)
                time.sleep(e.seconds)

    return wrapper


def download_photos(client, entity, download_path):
    '''
    :param client: type TelegramClient
    :param entity: could be a person, chat or channel
    :param download_path: the path that photos would be saved in
    :return:
    '''
    for message in client.iter_messages(entity):
        if isinstance(message.media, types.MessageMediaPhoto):
            logging.info("Downloading photo from message " + str(message.id) + '.')
            client.download_media(message, file=download_path)


client.start()

entity = client.get_entity(chat)

logging.info('Starting download photos...')
download_photos(client, entity[0], photo_dir + chat[0])
