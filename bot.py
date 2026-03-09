
import os
from pyrogram import Client, filters
from mega_downloader import start_mega_task

print("🚀 Bot starting...")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

app = Client(
    "mega-bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

user_channel = {}
pending_link = {}


@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Welcome\n\n"
        "1️⃣ /setchannel -100xxxx\n"
        "2️⃣ /mega"
    )


@app.on_message(filters.command("setchannel"))
async def setchannel(client, message):

    if len(message.command) < 2:
        await message.reply_text("Usage:\n/setchannel -100xxxx")
        return

    channel_id = int(message.command[1])

    try:
        await client.get_chat(channel_id)
    except:
        await message.reply_text("❌ Bot is not in that channel.")
        return

    user_channel[message.from_user.id] = channel_id

    await message.reply_text("✅ Channel saved. Now send /mega")


@app.on_message(filters.command("mega"))
async def mega(client, message):

    if message.from_user.id not in user_channel:
        await message.reply_text("⚠️ Set channel first")
        return

    await message.reply_text("📎 Send MEGA link")


@app.on_message(filters.text)
async def handle_text(client, message):

    if "mega.nz" in message.text:

        pending_link[message.from_user.id] = message.text

        await message.reply_text("⚠️ Reply YES to start upload")


@app.on_message(filters.regex("^YES$"))
async def confirm(client, message):

    user = message.from_user.id

    if user not in pending_link:
        return

    link = pending_link[user]
    channel = user_channel[user]

    await message.reply_text("⏳ Starting task...")

    await start_mega_task(client, link, channel)


print("✅ Bot running")

app.run()
