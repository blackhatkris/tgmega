
import os
from pyrogram import Client, filters
from mega_downloader import start_mega_task

print("🚀 Bot container starting...")

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
        "👋 Hello!\n\n"
        "1️⃣ Use /setchannel <channel_id>\n"
        "2️⃣ Use /mega to send MEGA link"
    )


@app.on_message(filters.command("setchannel"))
async def setchannel(client, message):

    if len(message.command) < 2:
        await message.reply_text("Usage:\n/setchannel -100xxxx")
        return

    channel_id = int(message.command[1])

    try:
        member = await client.get_chat_member(channel_id, "me")
    except:
        await message.reply_text("❌ Bot is not in that channel.")
        return

    if member.status not in ["administrator", "creator"]:
        await message.reply_text("❌ Bot must be admin in that channel.")
        return

    user_channel[message.from_user.id] = channel_id

    await message.reply_text("✅ Channel saved.\nNow send /mega")


@app.on_message(filters.command("mega"))
async def mega(client, message):

    if message.from_user.id not in user_channel:
        await message.reply_text("⚠️ Set channel first using /setchannel")
        return

    await message.reply_text("📎 Send your MEGA link")


@app.on_message(filters.text & ~filters.command(["start", "setchannel", "mega"]))
async def receive_link(client, message):

    if "mega.nz" in message.text:

        pending_link[message.from_user.id] = message.text

        await message.reply_text(
            "⚠️ Start uploading?\n\nReply **YES** to confirm."
        )


@app.on_message(filters.regex("^YES$"))
async def start_process(client, message):

    user = message.from_user.id

    if user not in pending_link:
        return

    link = pending_link[user]
    channel = user_channel[user]

    await message.reply_text("⏳ Starting MEGA task...")

    await start_mega_task(client, link, channel)


print("✅ Bot is running...")

app.run()
