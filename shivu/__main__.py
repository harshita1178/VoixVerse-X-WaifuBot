import importlib
import time
import random
import re
import asyncio
from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

from shivu import (collection, top_global_groups_collection, group_user_totals_collection, 
                   user_collection, user_totals_collection, shivuu, application, 
                   SUPPORT_CHAT, UPDATE_CHAT, db, LOGGER)
from shivu.modules import ALL_MODULES

locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}
last_user = {}
warned_users = {}
spawn_times = {}  # Store character spawn times

# Load all modules
for module_name in ALL_MODULES:
    importlib.import_module(f"shivu.modules.{module_name}")

def escape_markdown(text):
    escape_chars = r'*_`~>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

async def message_counter(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id

    if chat_id not in locks:
        locks[chat_id] = asyncio.Lock()
    lock = locks[chat_id]

    async with lock:
        chat_frequency = await user_totals_collection.find_one({'chat_id': chat_id})
        message_frequency = chat_frequency.get('message_frequency', 100) if chat_frequency else 100

        if chat_id in last_user and last_user[chat_id]['user_id'] == user_id:
            last_user[chat_id]['count'] += 1
            if last_user[chat_id]['count'] >= 10:
                if user_id in warned_users and time.time() - warned_users[user_id] < 600:
                    return
                else:
                    await update.message.reply_text(
    f"🌀 OYE SALE {update.effective_user.first_name}, CHUP KAR GANDU!👺\n"
    "⏳ BHARWA SPAMMER CHAMMAR JAAT KE KIDE TU CHUP KAR 10 MINUTE🪽  ."
                    )
                    warned_users[user_id] = time.time()
                    return
        else:
            last_user[chat_id] = {'user_id': user_id, 'count': 1}

        message_counts[chat_id] = message_counts.get(chat_id, 0) + 1

        if message_counts[chat_id] % message_frequency == 0:
            await send_image(update, context)
            message_counts[chat_id] = 0

async def send_image(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    all_characters = list(await collection.find({}).to_list(length=None))

    if chat_id not in sent_characters:
        sent_characters[chat_id] = []

    if len(sent_characters[chat_id]) == len(all_characters):
        sent_characters[chat_id] = []

    character = random.choice([c for c in all_characters if c['id'] not in sent_characters[chat_id]])

    sent_characters[chat_id].append(character['id'])
    last_characters[chat_id] = character
    spawn_times[chat_id] = time.time()  # Store spawn time

    if chat_id in first_correct_guesses:
        del first_correct_guesses[chat_id]

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=character['img_url'],
        caption=f"""🌬️ 𝗔 𝗺𝘆𝘀𝘁𝗲𝗿𝗶𝗼𝘂𝘀 {character['rarity']} ᴡᴀɪꜰᴜ ʜᴀꜱ ᴇᴍᴇʀɢᴇᴅ! ✨

⏳ 𝘽𝙚 𝙦𝙪𝙞𝙘𝙠 — 𝘀𝗵𝗲 𝗺𝗮𝘆 𝘃𝗮𝗻𝗶𝘀𝗵 𝘀𝗼𝗼𝗻...

➡️ 𝙐𝙨𝙚 /grasp <ɴᴀᴍᴇ> ᴛᴏ ᴄʟᴀɪᴍ ʜᴇʀ ɪɴᴛᴏ ʏᴏᴜʀ ʜᴀʀᴇᴍ.""",
        parse_mode='Markdown'
    )

async def grasp(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id not in last_characters:
        return

    if chat_id in first_correct_guesses:
        await update.message.reply_text(
    "❌ 𝗢𝗼𝗽𝘀! 𝗬𝗼𝘂𝗿 𝗴𝘂𝗲𝘀𝘀 𝗱𝗶𝗱𝗻'𝘁 𝗺𝗮𝘁𝗰𝗵.\n"
    "🔎 𝗧𝗿𝘆 𝗴𝘂𝗲𝘀𝘀𝗶𝗻𝗴 𝗮𝗴𝗮𝗶𝗻!"
        )
        return

    guess = ' '.join(context.args).lower() if context.args else ''

    if "()" in guess or "&" in guess.lower():
        await update.message.reply_text(
    "❌ 𝗢𝗼𝗽𝘀! 𝗬𝗼𝘂𝗿 𝗴𝘂𝗲𝘀𝘀 𝗱𝗶𝗱𝗻'𝘁 𝗺𝗮𝘁𝗰𝗵.\n"
    "🔎 𝗧𝗿𝘆 𝗴𝘂𝗲𝘀𝘀𝗶𝗻𝗴 𝗮𝗴𝗮𝗶𝗻!"
        )
        return

    name_parts = last_characters[chat_id]['name'].lower().split()

    if sorted(name_parts) == sorted(guess.split()) or any(part == guess for part in name_parts):
        first_correct_guesses[chat_id] = user_id
        time_taken = round(time.time() - spawn_times.get(chat_id, time.time()), 2)  # Calculate time taken

        user = await user_collection.find_one({'id': user_id})
        if user:
            update_fields = {}
            if hasattr(update.effective_user, 'username') and update.effective_user.username != user.get('username'):
                update_fields['username'] = update.effective_user.username
            if update.effective_user.first_name != user.get('first_name'):
                update_fields['first_name'] = update.effective_user.first_name
            if update_fields:
                await user_collection.update_one({'id': user_id}, {'$set': update_fields})
            await user_collection.update_one({'id': user_id}, {'$push': {'characters': last_characters[chat_id]}})
        else:
            await user_collection.insert_one({
                'id': user_id,
                'username': update.effective_user.username,
                'first_name': update.effective_user.first_name,
                'characters': [last_characters[chat_id]],
            })

        keyboard = [[InlineKeyboardButton("See Harem", switch_inline_query_current_chat=f"collection.{user_id}")]]
        
        # FIXED LINE: Now uses 'anime' instead of 'source'
        source_name = last_characters[chat_id].get('anime', 'Unknown Archives')

        await update.message.reply_text(
    f"✅ ||• ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ɢʟᴏᴡꜱ ʙʀɪɢʜᴛᴇʀ!\n\n"
    f"💖 <b>𝗪𝗔𝗜𝗙𝗨:</b> {escape(last_characters[chat_id]['name'])}\n"
    f"👑 <b>𝗥𝗔𝗥𝗜𝗧𝗬:</b> {escape(last_characters[chat_id]['rarity'])}\n"
    f"📖 <b>𝗦𝗢𝗨𝗥𝗖𝗘:</b> {escape(source_name)} <i>(1/1)</i>\n"
    f"⏳ <b>𝗦𝗨𝗠𝗠𝗢𝗡𝗘𝗗 𝗜𝗡:</b> {time_taken}s\n\n"
    f"✨ 𝐂𝐡𝐞𝐫𝐢𝐬𝐡 𝐡𝐞𝐫 — 𝐛𝐨𝐧𝐝𝐬 𝐛𝐨𝐫𝐧 𝐭𝐡𝐫𝐨𝐮𝐠𝐡 𝐟𝐚𝐭𝐞 𝐚𝐫𝐞 𝐞𝐭𝐞𝐫𝐧𝐚𝐥! ✨",
    parse_mode='HTML',
    reply_markup=InlineKeyboardMarkup(keyboard)
      )
    
    else:
        await update.message.reply_text("❌ The name you entered doesn't match any character. Try again!")

async def fav(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("💡 Please provide a character ID to mark as favorite.")
        return

    character_id = context.args[0]

    user = await user_collection.find_one({'id': user_id})
    if not user:
        await update.message.reply_text("🚫 You haven't claimed any characters yet.")
        return

    character = next((c for c in user['characters'] if c['id'] == character_id), None)
    if not character:
        await update.message.reply_text("❌ This character isn't in your collection!")
        return

    user['favorites'] = [character_id]

    await user_collection.update_one({'id': user_id}, {'$set': {'favorites': user['favorites']}})

    await update.message.reply_text(
    f"⭐ 𝗪𝗔𝗜𝗙𝗨 <b>{escape(character['name'])}</b> 𝗶𝘀 𝗻𝗼𝘄 𝘆𝗼𝘂𝗿 𝗳𝗮𝘃𝗼𝗿𝗶𝘁𝗲!"
    )

def main() -> None:
    application.add_handler(CommandHandler("grasp", grasp, block=False))
    application.add_handler(CommandHandler("fav", fav, block=False))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_counter, block=False))
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    shivuu.start()
    LOGGER.info("Bot started")
    main()
