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
# The session name 'lemc_command_bot' will create a separate .session file.
app = Client(
    "lemc_command_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("INFO: Initializing a separate Pyrogram Client for 'lemc_command.py'.")
print("WARNING: This module is running as a standalone bot instance due to 'app' import issues.")


# --- OWNER ID ---
OWNER_ID = 6675050163 # Tumhari owner ID yahan set ho chuki hai

@app.on_message(filters.command("lemc"))
async def lemc_command(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id == OWNER_ID: # Check karo ki command chalane wala owner hai ya nahi
        if message.reply_to_message:
            # Owner ne reply kiya hai
            target_user = message.reply_to_message.from_user
            
            # Agar owner khud ko tag kare
            if target_user.id == user_id:
                await message.reply_text("😂 Apne aap ko kyun lemc kar rahe ho, Master Dogesh Bhai? Kisi aur ko tag karo!")
                return

            await message.reply_text(
                f"Beta Jitna Tu Hoshiyar Hena Usse Jyada Bada Mera Hathiyar Hain\n"
                f"Writing By - Dogesh Bhai 🪽",
                reply_to_message_id=message.reply_to_message.id # Tag kiye gaye message ko reply karega
            )
        else:
            # Owner ne reply nahi kiya
            await message.reply_text("🤔 Master Dogesh Bhai, kisko lemc karna hai? Reply to someone's message!")
    else:
        # Non-owner ne command chalaya
        await message.reply_text("My master is Dogesh Bhai don't try to control me bitch")

# Note: app.run() is NOT included here.
# This module will be loaded by shivu's main script,
# which is responsible for running the Pyrogram client.
# However, if shivu does not 'run' the 'app' instance created here,
# this module's commands will not function.
