import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType

# IMPORTANT: Assuming 'app' (your Pyrogram Client instance) is accessible here.
# Ensure that 'app' is the correct Pyrogram Client instance from your main shivu setup.
# If this import fails, you might need to adjust how 'app' is made available to modules.
try:
    from shivu import app
except ImportError:
    # This fallback is for testing if 'app' isn't available from 'shivu' directly.
    # In a real shivu setup, 'app' must be the one initialized in shivu's core.
    print("WARNING: 'app' (Pyrogram Client) not found from shivu. Using fallback client for testing.")
    # You MUST replace these with your actual credentials if testing standalone,
    # but for shivu's module system, 'app' should be imported.
    API_ID = 22099263
    API_HASH = "12efef2ba448d268459dc136427d1ba0"
    BOT_TOKEN = "7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY"
    app = Client("fallback_auto_chat_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# --- Configuration for Auto Chat ---
# ONLY this group ID will have auto chat enabled.
ENABLED_CHATS = [-1002668191611] # <--- Tumhara diya gaya group ID yahan add kar diya gaya hai

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

# Filters for groups and supergroups only
@app.on_message(filters.group | filters.supergroup)
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

# --- Optional: Command to Toggle Auto Chat (Requires app in main shivu or database) ---
# Is code ko directly run karne ke liye iski zarurat nahi, but agar tum enable/disable karna chahoge
# toh tumhe app instance se interaction aur database/persistent storage ki zaroorat padegi.
# Upar ki logic simple hardcoded list (ENABLED_CHATS) use karti hai.
