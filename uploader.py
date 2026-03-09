
import os

async def upload_file(client, path, channel):

    file_name = os.path.basename(path).lower()

    # VIDEO FILES
    if file_name.endswith((".mp4", ".mkv", ".mov", ".webm")):

        await client.send_video(
            chat_id=channel,
            video=path,
            supports_streaming=True
        )

    # IMAGE FILES
    elif file_name.endswith((".jpg", ".jpeg", ".png")):

        await client.send_photo(
            chat_id=channel,
            photo=path
        )

    # OTHER FILES
    else:

        await client.send_document(
            chat_id=channel,
            document=path
        )
