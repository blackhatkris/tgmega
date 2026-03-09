
from pyrogram import Client, filters
from mega_downloader import process_mega_link
from config import API_ID, API_HASH, BOT_TOKEN, TARGET_CHANNEL

app = Client(
    "mega-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Bot ready. Send /mega <link>")

@app.on_message(filters.command("mega"))
async def mega(client, message):

    if len(message.command) < 2:
        await message.reply_text("Send /mega <mega_link>")
        return

    link = message.command[1]

    msg = await message.reply_text("Scanning MEGA link...")

    await process_mega_link(client, link, TARGET_CHANNEL, msg)

app.run()
