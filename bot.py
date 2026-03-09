
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from mega_downloader import start_mega_task

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client("mega-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

user_channel = {}
pending_link = {}

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Send /setchannel <channel_id>")

@app.on_message(filters.command("setchannel"))
async def set_channel(client, message: Message):

    channel_id = int(message.command[1])

    try:
        member = await client.get_chat_member(channel_id, "me")
    except:
        await message.reply("Bot is not in that channel.")
        return

    if member.status not in ["administrator", "creator"]:
        await message.reply("Bot must be admin.")
        return

    user_channel[message.from_user.id] = channel_id

    await message.reply("Channel saved. Now send /mega")

@app.on_message(filters.command("mega"))
async def mega(client, message):

    if message.from_user.id not in user_channel:
        await message.reply("Set channel first.")
        return

    await message.reply("Send MEGA link.")

@app.on_message(filters.text & ~filters.command(["start","setchannel","mega"]))
async def receive_link(client, message):

    if "mega.nz" in message.text:

        pending_link[message.from_user.id] = message.text

        await message.reply("Start process? Reply YES")

@app.on_message(filters.text & filters.regex("YES"))
async def start_process(client, message):

    user = message.from_user.id

    if user not in pending_link:
        return

    link = pending_link[user]
    channel = user_channel[user]

    await message.reply("Starting task...")

    await start_mega_task(client, link, channel)
