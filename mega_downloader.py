
import os
import subprocess
from uploader import upload_file

DOWNLOAD_DIR = "downloads"
MAX_SIZE_MB = 200


async def start_mega_task(client, link, channel, progress_msg):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    await progress_msg.edit_text("📥 Listing files from MEGA...")

    # list files
    result = subprocess.run(
        ["megatools", "ls", link],
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()

    files = []

    for line in lines:

        if line.strip() == "":
            continue

        files.append(line.strip())

    files.sort()

    total = len(files)
    done = 0

    for file in files:

        try:

            await progress_msg.edit_text(
                f"📥 Downloading\n\n{done}/{total}\n{file}"
            )

            # download single file
            subprocess.run([
                "megatools",
                "dl",
                f"{link}/{file}",
                "--path",
                DOWNLOAD_DIR
            ])

            path = os.path.join(DOWNLOAD_DIR, file)

            if not os.path.exists(path):
                continue

            size_mb = os.path.getsize(path) / (1024 * 1024)

            if size_mb > MAX_SIZE_MB:

                os.remove(path)

                continue

            await progress_msg.edit_text(
                f"⬆ Uploading\n\n{done+1}/{total}\n{file}"
            )

            await upload_file(client, path, channel)

            os.remove(path)

            done += 1

        except Exception as e:

            await progress_msg.edit_text(
                f"⚠️ Stopped\n\nReason:\n{str(e)}"
            )

            break

    await progress_msg.edit_text(
        f"✅ Finished\nUploaded {done}/{total}"
    )
