import time
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# Bot start hone ka time store karna
BOT_START_TIME = time.time()

# Function to calculate uptime
def get_uptime():
    seconds = int(time.time() - BOT_START_TIME)
    return str(datetime.timedelta(seconds=seconds))

async def start(update: Update, context: CallbackContext) -> None:
    start_time = time.time()  # Ping calculation ke liye

    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(chat_id=GROUP_ID, text=f"<a href='tg://user?id={user_id}'>{first_name}</a> STARTED THE BOT", parse_mode='HTML')
    else:
        if user_data['first_name'] != first_name or user_data['username'] != username:
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    # ✅ Private Chat Response (With Buttons & Image)
    if update.effective_chat.type == "private":
        ping_time = round((time.time() - start_time) * 1000, 3)  # Ping in ms

        caption = f""" 
🍃 ɢʀᴇᴇᴛɪɴɢs, ɪ'ᴍ ˹ᴡᴀɪғᴜ ɢꝛᴀʙʙᴇʀ ʙᴏᴛ˼ 🫧, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!  
━━━━━━━▧▣▧━━━━━━━  
⦾ ᴡʜᴀᴛ ɪ ᴅᴏ: ɪ sᴘᴀᴡɴ   
     ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ ғᴏʀ  
     ᴜsᴇʀs ᴛᴏ ɢʀᴀʙ.  
⦾ ᴛᴏ ᴜsᴇ ᴍᴇ: ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ  
     ɢʀᴏᴜᴘ ᴀɴᴅ ᴛᴀᴘ ᴛʜᴇ ʜᴇʟᴘ  
     ʙᴜᴛᴛᴏɴ ғᴏʀ ᴅᴇᴛᴀɪʟs.  
━━━━━━━▧▣▧━━━━━━━  

➜ ᴘɪɴɢ: {ping_time} ᴍs  
➜ ᴜᴘᴛɪᴍᴇ: {get_uptime()}  
"""

        keyboard = [
            [InlineKeyboardButton("✤ ᴀᴅᴅ ᴍᴇ ✤", url=f'http://t.me/Madara_X_Waifus_Bot?startgroup=new')],
            [InlineKeyboardButton("☊ 𝗌ᴜᴘᴘᴏʀᴛ ☊", url=f'https://t.me/{SUPPORT_CHAT}'),
             InlineKeyboardButton("✠ ᴜᴘᴅᴀᴛᴇ𝗦 ✠", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("✇ ʜᴇʟᴘ ✇", callback_data='help')],
            [InlineKeyboardButton("≎ ᴄʀᴇᴅɪᴛ ≎", url=f'https://t.me/{UPDATE_CHAT}')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(PHOTO_URL)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    # ✅ Group Chat Response (Simple Message)
    else:
        await update.message.reply_text(
            f"🍃 ɢʀᴇᴇᴛɪɴɢs, **{first_name}**! 🎀\n"
            "I'm ˹ᴡᴀɪғᴜ ɢꝛᴀʙʙᴇʀ ʙᴏᴛ˼ 🫧, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!\n"
            "Use `/waifu` to guess a character and `/help` for commands.",
            parse_mode="markdown"
        )
