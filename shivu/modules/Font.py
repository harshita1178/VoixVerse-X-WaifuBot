import asyncio
import random
import os # Ye os module env variables ke liye, ab jarurat nahi, but rakh sakte ho
from pyrogram import Client, filters
from pyrogram.enums import ChatType # Import ChatType enum
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- !!! CRITICAL SECURITY WARNING !!! ---
# DEAR USER: Hardcoding your API_ID, API_HASH, and BOT_TOKEN directly into your
# code and pushing it to a public GitHub repository is EXTREMELY INSECURE.
# Anyone can see these credentials and misuse your Telegram account and bot.
# It is HIGHLY RECOMMENDED to use environment variables (e.g., via a .env file)
# or a secure configuration management system for these sensitive details.
# Proceed at your own risk.
# --- !!! CRITICAL SECURITY WARNING !!! ---

# --- Bot Configuration (YOUR CREDENTIALS ADDED DIRECTLY) ---
# ** DO NOT SHARE THIS FILE PUBLICLY ON GITHUB IF THESE ARE YOUR REAL CREDENTIALS **
API_ID = 22099263  # Your Telegram API ID
API_HASH = "12efef2ba448d268459dc136427d1ba0"  # Your Telegram API Hash
BOT_TOKEN = "7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY"  # Your BotFather Bot Token

# Initialize the Pyrogram Client
app = Client(
    "my_waifu_bot_session",  # Session name for Pyrogram
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Font Feature Logic ---
# Font Conversion Helper Function
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

# Font Styles Dictionary
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
            safe_text_to_format = text_to_format[:50] # Limit for callback_data
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
    print(f"DEBUG: Callback data received: {callback_query.data}")

    try:
        data_parts = callback_query.data.split("_", 2)
        
        if len(data_parts) < 3:
            print(f"ERROR: Insufficient data parts in callback_query.data: {callback_query.data}")
            await callback_query.answer("Callback data incomplete. Please try again.", show_alert=True)
            return

        font_name = data_parts[1]
        original_text = data_parts[2]

        print(f"DEBUG: Extracted font_name: {font_name}")
        print(f"DEBUG: Extracted original_text: {original_text}")

        if font_name in font_styles:
            formatted_text = font_styles[font_name](original_text)
            
            print(f"DEBUG: Formatted text: {formatted_text}")

            await callback_query.answer(f"Text ko {font_name} mein badal diya!", show_alert=False)
            
            await callback_query.edit_message_text(
                f"Original text: `{original_text}`\n"
                f"Formatted text ({font_name}): `{formatted_text}`",
                parse_mode="Markdown"
            )
        else:
            print(f"DEBUG: Font name '{font_name}' not found in font_styles dictionary.")
            await callback_query.answer("Invalid font style selected.", show_alert=True)
    except Exception as e:
        print(f"ERROR: General error in font_callback_handler for data {callback_query.data}: {e}")
        await callback_query.answer("Kuch error ho gaya. Phir se try karo.", show_alert=True)


# --- Auto Chat Feature Logic ---

# ONLY this group ID will have auto chat enabled.
# Add your specific group ID here, example: -100123456789
ENABLED_CHATS = [-1002668191611] # <--- Tumhara group ID yahan add kar diya gaya hai

# Random phrases for "ladkiyon ki tarah" baat karna
GIRLY_PHRASES = [
    "Hii everyone! 😊 Kya chal raha hai?",
    "Aww, so sweet! 🥰",
    "Hehe, that's cute! 😉",
    "Kya kar rahe ho sab log? Koi exciting news? ✨",
    "Maza aa raha hai group mein! 🌸",
    "Oopsie! 🙈 Sorry agar kuch galat keh diya.",
    "Waise, sabne dinner kar liya? 😋",
    "Mujhe toh yeh topic bahut pasand aaya! 😍",
    "Tum sab bahut achhe ho! 💕",
    "Just chilling with my phone... 🛋️",
    "Kiske paas koi naya meme hai? 😂",
    "Good vibes only! 💖",
    "Aap logon se baat karke din ban gaya! ✨",
    "Koi bore ho raha hai kya? Main hoon yahan! 😉",
    "Sending virtual hugs! 🤗",
    "Soch rahi thi... 🤔 Kya karun aaj?",
    "Sab theek ho na? ❤️",
    "Meri taraf se ek smile! 😄",
    "Chalo, thodi masti karte hain! 🥳",
    "Kahaani sunani hai kisi ko? 📖"
]

# Keyword-based replies
KEYWORD_REPLIES = {
    "hello": ["Hiii! 🤗", "Hey there! 😊", "Hellooo! Kaise ho? 👋"],
    "hi": ["Hiii! 🤗", "Hey there! 😊", "Hellooo! Kaise ho? 👋"],
    "kaise ho": ["Main theek hoon! Aap kaise ho? 😊", "Mast chal raha hai, aap batao? ✨", "Sab badhiya! Thanks for asking! 💕"],
    "kya kar rahe ho": ["Bas, thoda rest kar rahi thi. Aap? 🛋️", "Soch rahi thi, kya special hai aaj? 🤔", "Kuch khaas nahi, group mein chat kar rahi hoon. 😉"],
    "bot": ["Haanji, main yahi hoon! 😊", "Mujhe bulaaya? 😉", "Kya keh rahe ho mere baare mein? 👀"],
    "love": ["Aww, so sweet! 🥰", "Love is in the air! ❤️", "Pyaar bhari baatein! 💕"],
    "good night": ["Good night! Sweet dreams! 😴✨", "Shubh Ratri! 🌙", "Take care! Sleep well! 😊"],
    "gn": ["Good night! Sweet dreams! 😴✨", "Shubh Ratri! 🌙", "Take care! Sleep well! 😊"],
    "good morning": ["Good morning! Have a lovely day! ☀️", "Subah ho gayi maam! ☕", "Hey, good morning! 😊"],
    "gm": ["Good morning! Have a lovely day! ☀️", "Subah ho gayi maam! ☕", "Hey, good morning! 😊"],
}

# --- Auto Chat Logic ---
last_message_time = {} # To keep track of last message sent in each chat
AUTO_CHAT_INTERVAL_MIN = 30 # Minimum interval before sending another random message (seconds)
AUTO_CHAT_INTERVAL_MAX = 120 # Maximum interval (seconds)

@app.on_message(filters.group) # Corrected filter: filters.group handles both normal groups and supergroups
async def auto_chat_handler(client, message):
    chat_id = message.chat.id

    # Check if auto chat is enabled for this ONLY specified group
    if chat_id not in ENABLED_CHATS:
        return # Do nothing if chat is not in the enabled list

    current_time = asyncio.get_event_loop().time()

    # Avoid immediate replies to every message (anti-spam)
    if message.from_user and message.from_user.is_self: # Don't reply to self messages
        return
    if message.text and len(message.text) < 3: # Ignore very short messages to avoid spam
        return

    # Randomly decide to send a message
    if random.random() < 0.2: # 20% chance to reply to any message
        pass # Proceed to reply logic
    else:
        return # Don't reply this time


    # --- Keyword-based Reply ---
    if message.text:
        msg_text = message.text.lower()
        for keyword, replies in KEYWORD_REPLIES.items():
            if keyword in msg_text:
                await asyncio.sleep(random.uniform(1, 3)) # Short random delay before replying
                await message.reply_text(random.choice(replies))
                last_message_time[chat_id] = current_time # Update last message time
                return # Reply to keyword and stop

    # --- Random General Message ---
    # Check if enough time has passed since the last random message
    if chat_id not in last_message_time or \
       (current_time - last_message_time[chat_id]) > random.uniform(AUTO_CHAT_INTERVAL_MIN, AUTO_CHAT_INTERVAL_MAX):
        
        await asyncio.sleep(random.uniform(2, 5)) # Random delay before sending general message
        await client.send_message(chat_id, random.choice(GIRLY_PHRASES))
        last_message_time[chat_id] = current_time # Update last message time


# --- Start the Bot ---
print("Bot is starting...")
# This line starts the bot and keeps it running to listen for updates.
app.run()
print("Bot started!")
