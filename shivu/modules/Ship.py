import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# --- IMPORTANT: THIS MODULE WILL ALWAYS START ITS OWN CLIENT INSTANCE ---
# Since you do not want to modify main.py or __init__.py, and 'app' is not
# globally exposed by shivu, this module must run as a completely separate
# Pyrogram bot instance.
#
# !!! WARNING: This is NOT the ideal way to integrate modules in a framework.
# It leads to multiple bot instances running, consuming more resources,
# and potentially causing conflicts or unexpected behavior.
# Use this approach ONLY if you absolutely cannot modify main.py or __init__.py.
# ---

# --- YOUR BOT CREDENTIALS (HARDCODED HERE FOR THIS STANDALONE MODULE) ---
# Replace these with your actual API_ID, API_HASH, and BOT_TOKEN.
# THIS IS INSECURE IF PUBLICLY SHARED.
API_ID = 22099263 # Tumhari API ID
API_HASH = "12efef2ba448d268459dc136427d1ba0" # Tumhari API Hash
BOT_TOKEN = "7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY" # Tumhari Bot Token

# Initialize a NEW Pyrogram Client instance specifically for this module.
# The session name 'ship_command_bot' will create a separate .session file.
app = Client(
    "ship_command_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("INFO: Initializing a separate Pyrogram Client for 'ship_command.py'.")
print("WARNING: This module is running as a standalone bot instance due to 'app' import issues.")

# --- Love Compatibility Percentages ---
LOVE_PERCENTAGES = [
    "0-10%", "11-20%", "21-30%", "31-40%", "41-50%",
    "51-60%", "61-70%", "71-80%", "81-90%", "91-100%"
]

# --- Ship Name Combiner (Simple example) ---
def generate_ship_name(name1: str, name2: str) -> str:
    name1 = name1.replace(" ", "")
    name2 = name2.replace(" ", "")
    
    if len(name1) >= 3 and len(name2) >= 3:
        if random.random() < 0.5: # 50% chance for Name1_Name2
            return name1[:len(name1)//2] + name2[len(name2)//2:]
        else: # 50% chance for Name2_Name1
            return name2[:len(name2)//2] + name1[len(name1)//2:]
    else:
        # Fallback for very short names
        return f"{name1}{name2}"

@app.on_message(filters.command("ship"))
async def ship_command(client: Client, message: Message):
    if len(message.command) > 2:
        # Case: /ship Name1 Name2
        name1 = message.command[1]
        name2 = message.command[2]
        
        love_percentage = random.choice(LOVE_PERCENTAGES)
        ship_name = generate_ship_name(name1, name2)
        
        await message.reply_text(
            f"💖 Shipping **{name1}** and **{name2}**...\n"
            f"Love Compatibility: **{love_percentage}**\n"
            f"Your Ship Name: **{ship_name.capitalize()}**! ✨"
        )
    elif message.reply_to_message:
        # Case: /ship (reply to someone)
        user1 = message.from_user
        user2 = message.reply_to_message.from_user

        if user1.id == user2.id:
            await message.reply_text("Self-love is great, but you can't ship yourself with yourself! 😉")
            return
            
        name1 = user1.first_name
        name2 = user2.first_name

        love_percentage = random.choice(LOVE_PERCENTAGES)
        ship_name = generate_ship_name(name1, name2)
        
        await message.reply_text(
            f"💖 Shipping **{name1}** and **{name2}**...\n"
            f"Love Compatibility: **{love_percentage}**\n"
            f"Your Ship Name: **{ship_name.capitalize()}**! ✨",
            reply_to_message_id=message.reply_to_message.id
        )
    else:
        # Case: /ship (no reply, no arguments)
        await message.reply_text(
            "🚢 Reply to someone's message to ship, or use `/ship Name1 Name2`!"
        )

# Note: app.run() is NOT included here.
# This module will be loaded by shivu's main script,
# which is responsible for running the Pyrogram client.
# However, if shivu does not 'run' the 'app' instance created here,
# this module's commands will not function.
