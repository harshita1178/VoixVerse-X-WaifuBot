
import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from shivu import application, SUPPORT_CHAT, UPDATE_CHAT, db, GROUP_ID

collection = db['total_pm_users']

PHOTO_URL = [
    "https://graph.org/file/f41fb95c96b068e55cdd2-1e00669b0b8458dc5f.jpg",
    "https://graph.org/file/3b8e66af1a005897f1ada-e290ec29df788f01cf.jpg"
]

async def start(update: Update, context: CallbackContext) -> None:
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

    if update.effective_chat.type == "private":
        caption = f"""
  ╔═══════════════════════════════╗
✾ Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ 🍃, MADARA X WAIFU ʙᴏᴛ🫧 
  ╚═══════════════════════════════╝
╔═══════════════════════════════╗
║ ➻  I ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ғɪɴᴅ ʏᴏᴜʀ Waifu Hᴜsʙᴀɴᴅᴏ 
║      ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ. 
║ ➻  Yᴏᴜ ᴄᴀɴ sᴇᴀʟ ᴛʜɪs ʙʏ ᴜsɪɴɢ /waifu ᴄᴏᴍᴍᴀɴᴅ 
║      ᴀɴᴅ ᴀdd ʏᴏᴜʀ ʜᴀʀᴇᴍ. 
╚═══════════════════════════════╝
  "Tᴀᴘ 'Hᴇʟᴘ' ғᴏʀ ᴀ ʟɪsᴛ ᴏғ ᴀʟʟ ᴄᴏᴍᴍᴀɴds."
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

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
    ***Help Section :***
    
***/waifu - to guess character (only works in group)***
***/fav - add your fav***
***/trade - to trade character***
***/gift - give any character from***
***/harem - to see your harem***
***/top - to see top users***
***/changetime - change character appear time***
    """ 
        help_keyboard = [[InlineKeyboardButton("⤂ʙᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)

        await context.bot.edit_message_caption(chat_id=query.message.chat_id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':
        # "Back" button click hone par start message wapas bhej do
