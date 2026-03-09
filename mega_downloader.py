
import os
from mega import Mega
from uploader import upload_file

mega = Mega()

async def start_mega_task(client, link, channel):

    m = mega.login()

    files = m.get_files()

    for f in files:

        info = files[f]

        if info["t"] != 0:
            continue

        name = info["a"]["n"]

        path = m.download(f)

        await upload_file(client, path, channel)

        os.remove(path)
