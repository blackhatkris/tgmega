
import os
from mega import Mega
from uploader import upload_file
from config import MAX_FILE_SIZE_MB, DOWNLOAD_DIR

mega = Mega()

async def process_mega_link(client, link, target_channel, progress_msg):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    m = mega.login()

    files = m.get_files()

    uploaded = 0
    skipped = 0

    for file in files:

        info = files[file]

        if info['t'] != 0:
            continue

        size = int(info['s']) / (1024 * 1024)

        if size > MAX_FILE_SIZE_MB:
            skipped += 1
            continue

        name = info['a']['n']

        await progress_msg.edit_text(f"Downloading {name}")

        path = m.download(file, DOWNLOAD_DIR)

        await progress_msg.edit_text(f"Uploading {name}")

        await upload_file(client, path, target_channel)

        os.remove(path)

        uploaded += 1

        await progress_msg.edit_text(
            f"Uploaded: {uploaded}\nSkipped: {skipped}"
        )
