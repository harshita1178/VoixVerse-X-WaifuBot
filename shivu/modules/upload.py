import urllib.request
from pymongo import ReturnDocument
from telegram import Update, MessageEntity
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, sudo_users, collection, db

WRONG_FORMAT_TEXT = """Wrong ❌ format...\n\nReply to an image with:\n/upload character-name anime-name rarity-number\n\nUse rarity number accordingly:\n1: ⚪ Common\n2: 🟣 Rare\n3: 🟢 Medium\n4: 🟡 Legendary\n5: 💮 Special Edition\n6: 🔮 Limited Edition\n7: 🎐 Celestial Beauty\n8: 🪽 Divine Edition\n9: 💦 Wet Elegance\n10: 🎴 Cosplay"""

rarity_map = {
    1: "⚪ Common",
    2: "🟣 Rare",
    3: "🟢 Medium",
    4: "🟡 Legendary",
    5: "💮 Special Edition",
    6: "🔮 Limited Edition",
    7: "🎐 Celestial Beauty",
    8: "🪽 Divine Edition",
    9: "💦 Wet Elegance",
    10: "🎴 Cosplay"
}

async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        return_document=ReturnDocument.AFTER
    )
    
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 1})
        return 1  # Start from 1 instead of 0
    
    return sequence_document['sequence_value']

async def upload(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask My Owner...')
        return

    message = update.message
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("Please reply to an image with correct format!\n\n" + WRONG_FORMAT_TEXT)
        return

    try:
        args = context.args if context.args else []
        if len(args) != 3:
            await message.reply_text(WRONG_FORMAT_TEXT)
            return
        
        character_name = args[0].replace('-', ' ').title()
        anime = args[1].replace('-', ' ').title()
        rarity = rarity_map.get(int(args[2]))
        if not rarity:
            await message.reply_text("Invalid rarity number. Check the rarity list.")
            return
        
        img_url = message.reply_to_message.photo[-1].file_id  # Fetch highest quality image
        id = str(await get_next_sequence_number('character_id')).zfill(2)
        character = {
            'img_url': img_url,
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': id
        }
        
        await collection.insert_one(character)
        await message.reply_text(f"✅ {character_name} from {anime} (Rarity: {rarity}) added successfully!")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

application.add_handler(CommandHandler("upload", upload))
