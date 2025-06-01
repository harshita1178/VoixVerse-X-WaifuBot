import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- IMPORTANT: TRYING TO IMPORT 'app' FROM SHIVU'S MAIN CLIENT ---
# This is the crucial part. We are assuming 'app' (your Pyrogram Client instance)
# is available for import from the 'shivu' package.
# If your shivu setup is different, this line might cause an error.
try:
    from shivu import app
    print("INFO: Pyrogram 'app' client imported successfully from shivu.")
except ImportError:
    print("ERROR: Could not import 'app' from shivu. The bot might not function correctly.")
    print("This usually means 'app' is not globally exposed by shivu, or shivu's __init__.py is not setting it up for import.")
    print("As a fallback, using hardcoded credentials for a separate client instance.")
    # Fallback Client (Only used if 'from shivu import app' fails)
    # WARNING: If this fallback client is used, it will run as a separate bot instance
    # and might conflict or not integrate with other shivu modules.
    API_ID = 22099263
    API_HASH = "12efef2ba448d268459dc136427d1ba0"
    BOT_TOKEN = "7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY"
    app = Client("fallback_combined_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# --- Font Feature Logic ---
def convert_to_unicode_font(text, start_upper, start_lower):
    converted_text = ""
    for char in text:
        if 'A' <= char <= 'Z':
            if start_upper and (start_upper + (ord(char) - ord('A'))) <= 0x1F77F:
                converted_text += chr(start_upper + (ord(char) - ord('A')))
            else:
                converted_text += char
        elif 'a' <= char <= 'z':
            if start_lower and (start_lower + (ord(char) - ord('a'))) <= 0x1F77F:
                converted_text += chr(start_lower + (ord(char) - ord('a')))
            else:
                converted_text += char
        else:
            converted_text += char
    return converted_text

font_styles = {
    "Typewriter": lambda text: convert_to_unicode_font(text, 0x1D68C, 0x1D696),
    "Outline": lambda text: convert_to_unicode_font(text, 0x1D538, 0x1D552),
    "Serif": lambda text: convert_to_unicode_font(text, 0x1D68C, 0x1D696),
    "SMALL CAPS": lambda text: "".join(
        chr(0xFF21 + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else c
        for c in text.upper()
    ),
    "script": lambda text: convert_to_unicode_font(text, 0x1D49C, 0x1D4B6),
    "tiny": lambda text: "".join(
        chr(0x1D586 + (ord(c) - ord('a'))) if 'a' <= c <= 'z' else
        chr(0x1D56C + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else c
        for c in text
    ),
    "COMIC": lambda text: "".join(f"C{c}C" for c in text),
    "Sans": lambda text: convert_to_unicode_font(text, 0x1D5BA, 0x1D5D4),
    "CIRCLES": lambda text: "".join(
        chr(0x24B6 + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else
        chr(0x24D0 + (ord(c) - ord('a'))) if 'a' <= c <= 'z' else
        c for c in text
    ),
    "Gothic": lambda text: convert_to_unicode_font(text, 0x1D504, 0x1D51E),
    "S P E C I A L": lambda text: " ".join(list(text.upper())),
    "S Q U A R E S": lambda text: "".join(f"[{c}]" for c in text),
    "R E V E R S E": lambda text: text[::-1],
    "Andalucia": lambda text: "~" + text + "~",
    "𝕸𝖆𝖉𝖆𝖗𝖆": lambda text: convert_to_unicode_font(text, 0x1D56C, 0x1D586),
    "𝕃𝕀ℕ𝔼𝕐𝕋ℍ𝕀ℕ𝔾": lambda text: "Liney" + text + "Thing",
    "SxTopt": lambda text: "Sx" + text + "Topt",
    "FMxOazMein": lambda text: "FMxOaz" + text + "Mein",
    "Clouds": lambda text: "☁️" + text + "☁️",
    "Happy": lambda text: "😊" + text + "😊",
    "Sad": lambda text: "😔" + text + "😔"
}

# /font Command Handler
@app.on_message(filters.command("font"))
async def font_command_handler(client, message):
    if len(message.command) > 1:
        text_to_format = " ".join(message.command[1:])
        buttons = []
        row = []
        for i, (font_name, _) in enumerate(font_styles.items()):
            safe_text_to_format = text_to_format[:50]
            callback_data = f"font_{font_name}_{safe_text_to_format}"
            
            row.append(InlineKeyboardButton(font_name, callback_data=callback_data))
            
            if (i + 1) % 3 == 0:
                buttons.append(row)
                row = []
        
        if row:
            buttons.append(row)

        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            "Apne text ke liye font style chuno:",
            reply_markup=reply_markup
        )
    else:
        await message.reply_text("Kripya format karne ke liye text dein. Example: `/font YourText`")

# Callback Query Handler for Font Selection
@app.on_callback_query(filters.regex(r"^font_"))
async def font_callback_handler(client, callback_query):
    print(f"DEBUG: Font callback data received: {callback_query.data}")

    try:
        data_parts = callback_query.data.split("_", 2)
        
        if len(data_parts) < 3:
            print(f"ERROR: Insufficient data parts in font callback. Data: {callback_query.data}")
            await callback_query.answer("Callback data incomplete. Please try again.", show_alert=True)
            return

        font_name = data_parts[1]
        original_text = data_parts[2]

        if font_name in font_styles:
            formatted_text = font_styles[font_name](original_text)
            
            print(f"DEBUG: Formatted font text: {formatted_text}")

            await callback_query.answer(f"Text ko {font_name} mein badal diya!", show_alert=False)
            
            await callback_query.edit_message_text(
                f"Original text: `{original_text}`\n"
                f"Formatted text ({font_name}): `{formatted_text}`",
                parse_mode="Markdown"
            )
        else:
            print(f"DEBUG: Font name '{font_name}' not found.")
            await callback_query.answer("Invalid font style selected.", show_alert=True)
    except Exception as e:
        print(f"ERROR: General error in font_callback_handler: {e}")
        await callback_query.answer("Kuch error ho gaya. Phir se try karo.", show_alert=True)


# --- Auto Chat & Conversation Feature Logic ---

# ONLY this group ID will have auto chat enabled.
ENABLED_CHATS = [-1002668191611] # Your specific group ID

# Conversation starters and general replies
CONVERSATION_STARTERS = [
    "Hii {user_mention}! Kya kar rahe ho? 😊",
    "Hey {user_mention}! Kaise ho? Kuch exciting chal raha hai? ✨",
    "Hello {user_mention}! Aaj ka din kaisa raha? 🌸",
    "Waise {user_mention}, kya chal raha hai? Koi news? 😉",
    "Hi {user_mention}! Koi baat chit shuru kare? 😄",
    "Kya kar rahe ho {user_mention}? Timepass kaise ho raha hai? 🤔",
    "Heyyy {user_mention}! Group mein thoda active ho jao! 😉",
    "Aapki raaye kya hai {user_mention} is topic par? 👀"
]

RANDOM_CONVERSATION_REPLIES = [
    "Aww, so sweet! 🥰 Aapki baat bilkul sahi hai, {user_mention}!",
    "Hehe, {user_mention} toh bahut funny ho! 😂",
    "Bilkul sahi kaha {user_mention}! Meri bhi yahi soch hai. 👍",
    "Hmm, {user_mention} ki baat mein dum hai! 🤔",
    "Oh really, {user_mention}? Aur kya hua? 👀",
    "Interesting {user_mention}! Is baare mein aur batao. ✨",
    "Mujhe {user_mention} ki baat pasand aayi! 😍",
    "Haanji {user_mention}, main bhi yahi soch rahi thi! 😊",
    "Awesome {user_mention}! Koi aur idea? 💡",
    "Aapne toh dil jeet liya {user_mention}! 💕",
    "Lagta hai {user_mention} aaj full form mein hain! 🥳",
    "Sahi hai {user_mention}, sahi pakda! 😉",
    "Toh {user_mention}, next kya? 🤔",
    "Yeh toh kamaal hai {user_mention}! 😄",
    "Absolutely {user_mention}! No doubt. 💯"
]

# A set to keep track of user IDs for whom we have sent a greeting recently
RECENTLY_GREETED_USERS = {} # {chat_id: {user_id: timestamp}}
GREETING_COOLDOWN = 3600 # 1 hour cooldown for greeting a specific user in a specific chat

@app.on_message(filters.group & ~filters.me & filters.text) # Only in groups, not bot's own messages, and only text messages
async def continuous_auto_chat_handler(client, message):
    chat_id = message.chat.id

    if message.text and message.text.startswith('/'): # Ignore commands
        return

    if chat_id not in ENABLED_CHATS: # Check if auto chat is enabled for this specific group
        return

    user_id = message.from_user.id
    user_first_name = message.from_user.first_name if message.from_user else "someone"
    # Create a user mention (Pyrogram's way for tagging)
    user_mention = f"[{user_first_name}](tg://user?id={user_id})" 

    current_time = asyncio.get_event_loop().time()

    should_send_greeting = False
    if chat_id not in RECENTLY_GREETED_USERS:
        RECENTLY_GREETED_USERS[chat_id] = {}
        should_send_greeting = True
    
    if user_id not in RECENTLY_GREETED_USERS[chat_id] or \
       (current_time - RECENTLY_GREETED_USERS[chat_id].get(user_id, 0)) > GREETING_COOLDOWN:
        should_send_greeting = True
        
    
    # Random delay before replying
    await asyncio.sleep(random.uniform(2, 5))

    if should_send_greeting and random.random() < 0.3: # 30% chance for a greeting if cooldown met
        reply_text = random.choice(CONVERSATION_STARTERS).format(user_mention=user_mention)
        await client.send_message(chat_id, reply_text, reply_to_message_id=message.id, parse_mode="Markdown")
        RECENTLY_GREETED_USERS[chat_id][user_id] = current_time
    else:
        # Otherwise, send a random conversation reply
        reply_text = random.choice(RANDOM_CONVERSATION_REPLIES).format(user_mention=user_mention)
        await client.send_message(chat_id, reply_text, reply_to_message_id=message.id, parse_mode="Markdown")

# The `app.run()` call is usually in your main __init__.py or __main__.py.
# If you are placing this code in a module, you should NOT include app.run() here.
# shivu's main script will handle starting the bot.
# This code defines the handlers, which will automatically register with the 'app'
# instance once this module is imported by shivu.
