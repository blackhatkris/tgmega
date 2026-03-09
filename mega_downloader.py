
import os
import subprocess
from uploader import upload_file

DOWNLOAD_DIR = "downloads"
MAX_SIZE_MB = 200


async def start_mega_task(client, link, channel, progress_msg):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    await progress_msg.edit_text("📥 Downloading from MEGA...")

    subprocess.run([
        "megatools",
        "dl",
        link,
        "--path",
        DOWNLOAD_DIR
    ])

    files_to_upload = []

    for root, dirs, files in os.walk(DOWNLOAD_DIR):

        dirs.sort()
        files.sort()

        for file in files:

            path = os.path.join(root, file)

            size_mb = os.path.getsize(path) / (1024*1024)

            if size_mb > MAX_SIZE_MB:
                continue

            files_to_upload.append(path)

    total = len(files_to_upload)

    done = 0

    for file in files_to_upload:

        done += 1

        await progress_msg.edit_text(
            f"⬆ Uploading\n\n"
            f"{done}/{total}\n"
            f"{os.path.basename(file)}"
        )

        await upload_file(client, file, channel)

        os.remove(file)

    await progress_msg.edit_text("✅ Upload complete")
