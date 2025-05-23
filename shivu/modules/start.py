import time
import datetime
import random

from motor.motor_asyncio import AsyncIOMotorClient
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, ApplicationBuilder

# MongoDB Setup
MONGO_URL = "mongodb+srv://your_mongo_url"
client = AsyncIOMotorClient(MONGO_URL)
db = client["your_database_name"]
collection = db["users"]

# Constants
GROUP_ID = -1001234567890  # Apna Telegram group ID daalo
SUPPORT_CHAT = "YourSupportChat"
UPDATE_CHAT = "YourUpdateChat"

DM_PHOTO_URLS = [
    "https://files.catbox.moe/va3999.jpg",
    "https://files.catbox.moe/0n5o2x.jpg",
    "https://files.catbox.moe/sv4364.jpg"
]

GC_PHOTO_URLS = [
    "https://files.catbox.moe/6ymnck.jpg",
    "https://files.catbox.moe/nqe4j8.jpg",
    "https://files.catbox.moe/sohjvo.jpg"
]

# Bot start hone ka time store karna
BOT_START_TIME = time.time()

def get_uptime():
    seconds = int(time.time() - BOT_START_TIME)
    return str(datetime.timedelta(seconds=seconds))

async def start(update: Update, context: CallbackContext) -> None:
    start_time = time.time()
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})
    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=f"<a href='tg://user?id={user_id}'>{first_name}</a> STARTED THE BOT",
            parse_mode='HTML'
        )
    else:
        if user_data['first_name'] != first_name or user_data['username'] != username:
            await collection.update_one(
                {"_id": user_id},
                {"$set": {"first_name": first_name, "username": username}}
            )

    if update.effective_chat.type == "private":
        ping_time = round((time.time() - start_time) * 1000, 3)
        caption = f"""
🍃 ɢʀᴇᴇᴛɪɴɢs, ɪ'ᴍ ˹ᴡᴀɪғᴜ ɢꝛᴀʙʙᴇʀ ʙᴏᴛ˼ 🫧, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!
━━━━━━━▧▣▧━━━━━━━
⦾ ᴡʜᴀᴛ ɪ ᴅᴏ: ɪ sᴘᴀᴡɴ ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ ғᴏʀ ᴜsᴇʀs ᴛᴏ ɢʀᴀʙ.
⦾ ᴛᴏ ᴜsᴇ ᴍᴇ: ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴛᴀᴘ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ᴅᴇᴛᴀɪʟs.
━━━━━━━▧▣▧━━━━━━━

➜ ᴘɪɴɢ: {ping_time} ᴍs
➜ ᴜᴘᴛɪᴍᴇ: {get_uptime()}
"""
        keyboard = [
            [InlineKeyboardButton("✤ ᴀᴅᴅ ᴍᴇ ✤", url='http://t.me/Madara_X_Waifus_Bot?startgroup=new')],
            [InlineKeyboardButton("☊ 𝗌ᴜᴘᴘᴏʀᴛ ☊", url=f'https://t.me/{SUPPORT_CHAT}'),
             InlineKeyboardButton("✠ ᴜᴘᴅᴀᴛᴇ𝗦 ✠", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("✇ ʜᴇʟᴘ ✇", callback_data='help')],
            [InlineKeyboardButton("≎ ᴄʀᴇᴅɪᴛ ≎", url=f'https://t.me/{UPDATE_CHAT}')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(DM_PHOTO_URLS)

        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo_url,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode='markdown'
            )
        except Exception as e:
            print(f"Error: {e}")

    else:
        photo_url = random.choice(GC_PHOTO_URLS)
        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo_url,
                caption=f"🍃 ɢʀᴇᴇᴛɪɴɢs, **{first_name}**! 🎀\n"
                        "I'm ˹ᴡᴀɪғᴜ ɢꝛᴀʙʙᴇʀ ʙᴏᴛ˼ 🫧, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!\n"
                        "Use `/waifu` to guess a character and `/help` for commands.",
                parse_mode="markdown"
            )
        except Exception as e:
            print(f"Error: {e}")

# Bot Setup
TOKEN = "your_telegram_bot_token"
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    application.run_polling()
