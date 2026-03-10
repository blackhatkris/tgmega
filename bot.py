
import os
import sys
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from mega_downloader import start_mega_task

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

app = Client("mega-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

user_channel = {}
pending_link = {}

task_queue = []
running_task = False

saved_state = {}


async def process_queue(client):

    global running_task

    if running_task:
        return

    running_task = True

    while task_queue:

        user, link = task_queue.pop(0)
        channel = user_channel[user]

        msg = await client.send_message(user, "⏳ Starting task...")

        try:

            saved_state["user"] = user
            saved_state["link"] = link
            saved_state["channel"] = channel

            await start_mega_task(client, link, channel, msg)

        except Exception as e:

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("▶ Resume", callback_data="resume"),
                        InlineKeyboardButton("♻ Restart", callback_data="restart")
                    ]
                ]
            )

            await msg.edit_text(
                f"⚠ Task paused\n\n{str(e)}",
                reply_markup=keyboard
            )

            running_task = False
            return

    running_task = False


@app.on_message(filters.command("start"))
async def start(client, message):

    await message.reply_text(
        "Mega Bot\n\n"
        "/setchannel -100xxxx\n"
        "/mega"
    )


@app.on_message(filters.command("setchannel"))
async def setchannel(client, message):

    channel_id = int(message.command[1])

    try:
        await client.get_chat(channel_id)
    except:
        await message.reply_text("Bot not in channel")
        return

    user_channel[message.from_user.id] = channel_id

    await message.reply_text("Channel saved")


@app.on_message(filters.command("mega"))
async def mega(client, message):

    await message.reply_text("Send MEGA link")


@app.on_message(filters.text & ~filters.regex("^YES$"))
async def link(client, message):

    if "mega.nz" in message.text:

        pending_link[message.from_user.id] = message.text

        await message.reply_text("Reply YES to start")


@app.on_message(filters.regex("^YES$"))
async def confirm(client, message):

    user = message.from_user.id

    link = pending_link[user]

    task_queue.append((user, link))

    await message.reply_text(
        f"📥 Added to queue\nQueue size: {len(task_queue)}"
    )

    await process_queue(client)


@app.on_callback_query(filters.regex("resume"))
async def resume_task(client, callback):

    await callback.answer("Resuming")

    user = saved_state["user"]
    link = saved_state["link"]
    channel = saved_state["channel"]

    msg = callback.message

    await start_mega_task(client, link, channel, msg)


@app.on_callback_query(filters.regex("restart"))
async def restart_container(client, callback):

    await callback.answer("Restarting")

    await callback.message.edit_text("Restarting container...")

    sys.exit(0)


app.run()
