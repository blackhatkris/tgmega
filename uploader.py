
async def upload_file(client, filepath, channel):

    if filepath.endswith(".mp4"):
        await client.send_video(channel, filepath)

    elif filepath.endswith(".jpg") or filepath.endswith(".png"):
        await client.send_photo(channel, filepath)

    else:
        await client.send_document(channel, filepath)

