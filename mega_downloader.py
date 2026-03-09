
import os
import subprocess
from uploader import upload_file

DOWNLOAD_DIR = "downloads"

async def start_mega_task(client, link, channel):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    command = [
        "megatools",
        "dl",
        link,
        "--path",
        DOWNLOAD_DIR
    ]

    subprocess.run(command)

    for file in os.listdir(DOWNLOAD_DIR):

        path = os.path.join(DOWNLOAD_DIR, file)

        await upload_file(client, path, channel)

        os.remove(path)
