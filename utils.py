import os


def mkdirs(dirs, chats):
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    for chat in chats:
        if not os.path.exists(dirs + chat):
            os.makedirs(dirs + chat)
