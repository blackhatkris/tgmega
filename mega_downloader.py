
import os
import subprocess
from uploader import upload_file

# ensure megatools installed
os.system("apt update && apt install -y megatools")

DOWNLOAD_DIR = "downloads"

async def start_mega_task(client, link, channel):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    subprocess.run([
        "megatools",
        "dl",
        link,
        "--path",
        DOWNLOAD_DIR
    ])

    for file in os.listdir(DOWNLOAD_DIR):

        path = os.path.join(DOWNLOAD_DIR, file)

        await upload_file(client, path, channel)

        os.remove(path)
