import logging

from telethon import TelegramClient, events
from telethon.tl import types

import config
from utils import create_path

logging.basicConfig(level=logging.INFO)
logging.getLogger('telethon').setLevel(level=logging.WARNING)

api_id = config.api_id
api_hash = config.api_hash
chats = config.chats  # string list of chat IDs, user/channel/group
photo_dir = config.photo_dir
video_dir = config.video_dir
video_size_limit = config.video_size_limit  # type int. eg. 26214400 that is less than 25MB

client = TelegramClient('telemedia', api_id, api_hash)

create_path(photo_dir, chats)
create_path(video_dir, chats)


# # Either a single item or a list of them will work for the chats.
# # You can also use the IDs, Peers, or even User/Chat/Channel objects.
# @client.on(events.NewMessage(chats=('TelethonChat', 'TelethonOffTopic')))
# async def normal_handler(event):
#     if 'roll' in event.raw_text:
#         await event.reply(str(random.randint(1, 6)))
#
#
# # Similarly, you can use incoming=True for messages that you receive
# @client.on(events.NewMessage(chats='TelethonOffTopic', outgoing=True,
#                              pattern='eval (.+)'))
# async def admin_handler(event):
#     expression = event.pattern_match.group(1)
#     await event.reply(str(ast.literal_eval(expression)))


@client.on(events.NewMessage(chats=chats))
async def my_event_handler(event):
    if isinstance(event.message.media, types.MessageMediaPhoto):
        download_path = photo_dir + event.chat.username
        logging.info("downloading a new photo from " + event.chat.username)
        await client.download_media(message=event.message, file=download_path)
    if isinstance(event.message.media, types.MessageMediaDocument):
        if event.message.video and event.message.video.size <= video_size_limit:  # gif and video
            download_path = video_dir + event.chat.username
            logging.info("downloading a new video/gif from " + event.chat.username)
            await client.download_media(message=event.message, file=download_path)


client.start()
client.run_until_disconnected()
