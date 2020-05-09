import os


def create_path(dirs, chats):
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    for chat in chats:
        path = os.path.join(dirs, chat)
        if not os.path.exists(path):
            os.makedirs(path)


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
