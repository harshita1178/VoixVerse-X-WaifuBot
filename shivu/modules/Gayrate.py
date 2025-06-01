import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# --- IMPORTANT: ATTEMPT TO IMPORT 'app' FROM SHIVU'S MAIN CLIENT ---
# Agar yeh import fail hota hai, toh yeh module apne hardcoded credentials se
# ek alag Pyrogram Client instance banayega.
try:
    from shivu import app
    print("INFO: Pyrogram 'app' client imported successfully from shivu for owner_gayrate.")
    # Agar 'app' mil gaya, toh fallback credentials ki zaroorat nahi.
    API_ID_FOR_FALLBACK = None
    API_HASH_FOR_FALLBACK = None
    BOT_TOKEN_FOR_FALLBACK = None
except ImportError:
    print("ERROR: Could not import 'app' from shivu for owner_gayrate. Using fallback client.")
    print("This means 'app' is not globally exposed by shivu or shivu's __init__.py isn't set up for import.")
    print("As a fallback, this module will attempt to create its own client instance.")
    # --- FALLBACK CREDENTIALS (ONLY IF 'app' IMPORT FAILS) ---
    # !!! WARNING: If this fallback client is used, it will run as a separate bot instance
    # and might conflict or not integrate with other shivu modules.
    # Replace these with your actual credentials if this fallback is used.
    API_ID_FOR_FALLBACK = 22099263
    API_HASH_FOR_FALLBACK = "12efef2ba448d268459dc136427d1ba0"
    BOT_TOKEN_FOR_FALLBACK = "7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY" # Apni bot token yahan daalna!
    app = Client("fallback_owner_gayrate_bot", api_id=API_ID_FOR_FALLBACK, api_hash=API_HASH_FOR_FALLBACK, bot_token=BOT_TOKEN_FOR_FALLBACK)


# --- OWNER ID ---
OWNER_ID = 6675050163 # Tumhari owner ID yahan set ho chuki hai

# --- GAY RATES ---
GAY_RATES = [38, 53, 69, 106]

# --- Timer Numbers ---
TIMER_NUMBERS = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]

@app.on_message(filters.command("gayrate"))
async def owner_only_gayrate(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id == OWNER_ID: # Yahan check ho raha hai ki command chalane wala owner hai ya nahi
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
            
            # Khudh ko tag karne par alag message
            if target_user.id == user_id:
                await message.reply_text("🤔 Bhai, khud ka gay rate check nahi kar sakte! Kisi aur ko tag karo! 😉")
                return

            gay_rate = random.choice(GAY_RATES)
            
            if gay_rate == 106:
                # Gay rate dikhao
                await message.reply_text(f"🏳️‍🌈 **{target_user.first_name}**'s Gay Rate: **{gay_rate}%**")
                
                # Timer numbers send karo
                for number in TIMER_NUMBERS:
                    await client.send_message(
                        chat_id=message.chat.id,
                        text=number,
                        reply_to_message_id=message.reply_to_message.id # Jisko tag kiya uske message ko reply karega
                    )
                    await asyncio.sleep(1) # 1 second wait karo
                
                # Congratulations message
                await message.reply_text(f"Wow congratulations **{target_user.first_name}** you are a perfect gay!")
            else:
                # Normal gay rate message
                await message.reply_text(f"🏳️‍🌈 **{target_user.first_name}**'s Gay Rate: **{gay_rate}%**")
        else:
            # Agar owner ne kisi ko tag nahi kiya
            await message.reply_text("🤔 Tag someone to check their gay rate, Master Dogesh Bhai!")
    else:
        # Agar owner ke alawa kisi aur ne command chalaya
        await message.reply_text("My master is Dogesh Bhai don't try to control me bitch")

# Note: app.run() is NOT included here.
# This module will be loaded by shivu's main script,
# which is responsible for running the Pyrogram client.
