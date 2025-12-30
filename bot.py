# file: bot.py
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# ===================== CONFIG =====================
API_ID = 22134923
API_HASH = "d3e9d2f01d3291e87ea65298317f86b8"
BOT_TOKEN = "8046672368:AAEN5l_oCsp4NwVnAsVKj2RanigmtIT2l6s"
OWNER_ID = 7383046042
# ==================================================

# Pyrogram client
bot = Client(
    "mybot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# /start command handler
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("Forward your post✅")

# Flask app for Render Web Service
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# Run bot in background thread
def run_bot():
    bot.run()

Thread(target=run_bot).start()

# Run Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
