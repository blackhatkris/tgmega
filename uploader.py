
import os

async def upload_file(client, path, channel):

    name = os.path.basename(path).lower()

    if name.endswith((".mp4", ".mkv", ".mov", ".webm")):

        await client.send_video(
            channel,
            path,
            supports_streaming=True
        )

    elif name.endswith((".jpg", ".jpeg", ".png")):

        await client.send_photo(channel, path)

    else:

        await client.send_document(channel, path)
