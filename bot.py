# file: bot.py
from pyrogram import Client, filters

# ===================== CONFIG =====================
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8046672368:AAGx5yzAUwF-8voOqUu1xwBFuCBGa5-iCPc"
OWNER_ID = 7383046042
# ==================================================

bot = Client(
    "mybot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# /start command handler
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("Bot is Alive✅")

# Run the bot
bot.run()
