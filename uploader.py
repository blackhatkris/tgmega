
async def upload_file(client, path, channel):

    if path.endswith(".mp4"):
        await client.send_video(channel, path)

    elif path.endswith(".jpg") or path.endswith(".png"):
        await client.send_photo(channel, path)

    else:
        await client.send_document(channel, path)
