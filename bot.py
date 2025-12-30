from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaPhoto
import asyncio
import time

# =======================
# CONFIG (HARDCODED)
# =======================
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8046672368:AAGx5yzAUwF-8voOqUu1xwBFuCBGa5-iCPc"

OWNER_ID = 7383046042
DESTINATION_CHANNEL_ID = -1003395725940

# =======================
# BOT INIT
# =======================
app = Client(
    "image_forward_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =======================
# ALBUM BUFFER
# =======================
album_buffer = {}
album_timer = {}

ALBUM_WAIT_TIME = 1.5  # seconds


async def process_album(media_group_id):
    await asyncio.sleep(ALBUM_WAIT_TIME)

    messages = album_buffer.get(media_group_id)
    if not messages:
        return

    media = []
    for msg in messages:
        if msg.photo:
            media.append(InputMediaPhoto(media=msg.photo.file_id))

    if media:
        while True:
            try:
                await app.send_media_group(
                    chat_id=DESTINATION_CHANNEL_ID,
                    media=media
                )
                break
            except FloodWait as e:
                await asyncio.sleep(e.value)

    album_buffer.pop(media_group_id, None)
    album_timer.pop(media_group_id, None)


# =======================
# MESSAGE HANDLER
# =======================
@app.on_message(filters.private)
async def handle_forwarded_media(client, message):

    # 1️⃣ Owner check
    if not message.from_user or message.from_user.id != OWNER_ID:
        return

    # 2️⃣ Must be forwarded
    if not message.forward_from_chat:
        return

    # =======================
    # ALBUM HANDLING
    # =======================
    if message.media_group_id:
        mgid = message.media_group_id

        if mgid not in album_buffer:
            album_buffer[mgid] = []

        album_buffer[mgid].append(message)

        if mgid not in album_timer:
            album_timer[mgid] = asyncio.create_task(process_album(mgid))

        return

    # =======================
    # SINGLE IMAGE
    # =======================
    if message.photo:
        while True:
            try:
                await client.send_photo(
                    chat_id=DESTINATION_CHANNEL_ID,
                    photo=message.photo.file_id
                )
                break
            except FloodWait as e:
                await asyncio.sleep(e.value)


# =======================
# RUN BOT
# =======================
print("Bot started successfully...")
app.run()
