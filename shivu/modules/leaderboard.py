import os
import random
import html
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from pymongo import MongoClient
import asyncio # asyncio for run_polling

# --- Bot Configuration ---
# Yeh tumhara bot token hai, BotFather se mila hoga
BOT_TOKEN = "7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY"

# Yeh photos ki list hai jo bot messages ke saath bhejega
PHOTO_URL = [
    "https://files.catbox.moe/peias3.jpg"
]

# Yeh tumhari Telegram User ID hai (bot owner)
OWNER_ID = 6675050163

# Yeh un users ki IDs hain jinhe special (sudo) access milega
SUDO_USERS = ["6675050163", "1831848202"]

# --- Database Configuration ---
# Yeh tumhara MongoDB connection string hai
MONGO_URI = "mongodb+srv://BesicWaifubot:TGDARK11798@cluster0.rg9k8ag.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Tumhare URI se assume kiya gaya database ka naam 'Cluster0' hai
DB_NAME = "Cluster0" 

# MongoDB client aur database connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Database collections - yahan data store hoga
user_collection = db["users"]
top_global_groups_collection = db["top_global_groups"]
group_user_totals_collection = db["group_user_totals"]

# --- Application Object ---
# Python-Telegram-Bot ka main application object
application = Application.builder().token(BOT_TOKEN).build()


# --- Command Functions ---

async def global_leaderboard(update: Update, context: CallbackContext) -> None:
    cursor = top_global_groups_collection.aggregate([
        {"$project": {"group_name": 1, "count": 1}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>ᴛᴏᴘ 𝟷𝟶 ɢʀᴏᴜᴘs ᴡʜᴏ ɢʀᴀʙʙᴇᴅ ᴍᴏsᴛ ᴄʜᴀʀᴀᴄᴛᴇʀs</b>\n\n"

    for i, group in enumerate(leaderboard_data, start=1):
        group_name = html.escape(group.get('group_name', 'Unknown'))

        # Truncate group name if too long
        if len(group_name) > 10:
            group_name = group_name[:15] + '...'
        count = group['count']
        leaderboard_message += f'{i}. <b>{group_name}</b> ➾ <b>{count}</b>\n'

    photo_url = random.choice(PHOTO_URL)
    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')

async def ctop(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    cursor = group_user_totals_collection.aggregate([
        {"$match": {"group_id": chat_id}},
        {"$project": {"username": 1, "first_name": 1, "character_count": "$count"}},
        {"$sort": {"character_count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>ᴛᴏᴘ 𝟷𝟶 ᴜsᴇʀs ᴡʜᴏ ɢʀᴀʙʙᴇᴅ ᴄʜᴀʀᴀᴄᴛᴇʀs ᴍᴏsᴛ ᴛɪᴍᴇ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ....</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        # Truncate first name if too long
        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = user['character_count']
        # Ensure username is not 'Unknown' for link
        if username != 'Unknown':
             leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➾ <b>{character_count}</b>\n'
        else:
             leaderboard_message += f'{i}. <b>{first_name}</b> ➾ <b>{character_count}</b>\n'


    photo_url = random.choice(PHOTO_URL)
    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')


async def leaderboard(update: Update, context: CallbackContext) -> None:
    cursor = user_collection.aggregate([
        {
            "$project": {
                "username": 1,
                "first_name": 1,
                "character_count": {
                    "$cond": {
                        "if": {"$isArray": "$characters"},
                        "then": {"$size": "$characters"},
                        "else": 0
                    }
                }
            }
        },
        {"$sort": {"character_count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>ᴛᴏᴘ 𝟷𝟶 ᴜsᴇʀs ᴡɪᴛʜ ᴍᴏsᴛ ᴄʜᴀʀᴀᴄᴛᴇʀs</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        # Truncate first name if too long
        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = user['character_count']
        # Ensure username is not 'Unknown' for link
        if username != 'Unknown':
            leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➾ <b>{character_count}</b>\n'
        else:
            leaderboard_message += f'{i}. <b>{first_name}</b> ➾ <b>{character_count}</b>\n'

    photo_url = random.choice(PHOTO_URL)
    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')

async def stats(update: Update, context: CallbackContext) -> None:
    # Authorization check using OWNER_ID
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    user_count = await user_collection.count_documents({})
    group_count = await group_user_totals_collection.distinct('group_id')

    await update.message.reply_text(f'Total Users: {user_count}\nTotal groups: {len(group_count)}')

async def send_users_document(update: Update, context: CallbackContext) -> None:
    # Authorization check using SUDO_USERS list
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text('Only For Sudo users...')
        return
    
    cursor = user_collection.find({})
    users = []
    async for document in cursor:
        users.append(document)
    
    user_list = ""
    for user in users:
        user_list += f"{user.get('first_name', 'Unknown')} (ID: {user.get('id', 'N/A')})\n" # Added user ID for better info
    
    with open('users.txt', 'w', encoding='utf-8') as f: # Added encoding
        f.write(user_list)
    
    with open('users.txt', 'rb') as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    os.remove('users.txt')

async def send_groups_document(update: Update, context: CallbackContext) -> None:
    # Authorization check using SUDO_USERS list
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text('Only For Sudo users...')
        return
    
    cursor = top_global_groups_collection.find({})
    groups = []
    async for document in cursor:
        groups.append(document)
    
    group_list = ""
    for group in groups:
        group_list += f"{group.get('group_name', 'Unknown')} (ID: {group.get('group_id', 'N/A')})\n" # Added group ID for better info
    
    with open('groups.txt', 'w', encoding='utf-8') as f: # Added encoding
        f.write(group_list)
    
    with open('groups.txt', 'rb') as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    os.remove('groups.txt')


# --- Command Handlers ---
application.add_handler(CommandHandler('ctop', ctop, block=False))
application.add_handler(CommandHandler('stats', stats, block=False))
application.add_handler(CommandHandler('Topgroups', global_leaderboard, block=False))
application.add_handler(CommandHandler('list', send_users_document, block=False))
application.add_handler(CommandHandler('groups', send_groups_document, block=False))
application.add_handler(CommandHandler('top', leaderboard, block=False))


# --- Main Function to Run the Bot ---
async def main():
    print("Bot started polling...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
