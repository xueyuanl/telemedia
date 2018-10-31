from telethon import TelegramClient
from telethon.tl import types


class Teleclient:
    """Download media(photos, videos) in chart
    """

    def __init__(self, client=None):
        self.client = client
        self.api_id = 423258
        self.api_hash = '60c3795f40aefe47806113cfc4b65409'
        self.dialogs = None

        self.DOWNLOAD_PATH = '/mnt/telephotos/'

    async def creat_client(self):
        self.client = TelegramClient(None, self.api_id, self.api_hash)
        await self.client.start()
        return self.client

    async def get_dialogs(self):
        self.dialogs = await self.client.get_dialogs()
        return self.dialogs

    def get_photos(self, entity):
        for message in self.client.iter_messages(entity):
            if isinstance(message.media, types.MessageMediaPhoto):
                self.client.download_media(message, file=self.DOWNLOAD_PATH)
                print(message.id)
