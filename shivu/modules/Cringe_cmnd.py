import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message # Message type ko import karna mat bhoolna

# --- IMPORTANT: ATTEMPT TO IMPORT 'app' FROM SHIVU'S MAIN CLIENT ---
# This is the crucial part. We are assuming 'app' (your Pyrogram Client instance)
# is available for import from the 'shivu' package.
# If your shivu setup is different, this line might cause an error.
try:
    from shivu import app
    print("INFO: Pyrogram 'app' client imported successfully from shivu for new_fun_commands.")
except ImportError:
    print("ERROR: Could not import 'app' from shivu for new_fun_commands. Handlers might not register.")
    print("This means 'app' is not globally exposed by shivu or shivu's __init__.py isn't set up for it.")
    print("If you see this error, you might need to adjust shivu's core setup or the import line.")
    # Fallback (unlikely to work perfectly with shivu's module system if 'app' is not found)
    # This fallback is mainly for standalone testing.
    # If the bot doesn't work, this 'app' is the reason.
    # Note: Replace with your actual credentials if testing standalone
    API_ID = 22099263
    API_HASH = "12efef2ba448d268459dc136427d1ba0"
    BOT_TOKEN = "7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY"
    app = Client("fallback_new_fun_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# --- GIF URLs (UPDATED WITH YOUR PROVIDED LINKS) ---
KISS_GIFS = [
    "https://media1.giphy.com/media/MQVpBqASxSlFu/giphy.gif?cid=6c09b952asqslwq69hignwee1xz7aqgwmu38u53dmsgr5nhl&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media0.giphy.com/media/QGc8RgRvMonFm/giphy.gif?cid=6c09b952csgbe8udzya4qf0e0qplsiag1hr33thaikvqxew9&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/VXsUx3zjzwMhi/giphy.gif?cid=6c09b952k89rj0w7nakwh88gdlucj0n2in893hnlv7ts7uxx&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media3.giphy.com/media/zkppEMFvRX5FC/giphy.gif?cid=6c09b9523psuxv89ic9c6ozwt3eza6pvrkinpmg16z5i9rwu&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"
]

SLAP_GIFS = [
    "https://media4.giphy.com/media/90cAvw5mBQHa1QNFG9/giphy.gif?cid=6c09b952sfdnlse5k5rdd3h4swh61o10d3istcq8zforbsut&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media2.giphy.com/media/8TpEwyNgVypZm/giphy.gif?cid=6c09b952num1z7mgop8hyw981o7p2dhms9eip7kt8wec97l8&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media3.giphy.com/media/6BZaFXBVPBtok/giphy.gif?cid=6c09b952v27ecyebx24enw2272db08gz2mlli6hqnclr52np&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/l0Iy0vtShgNwyIRG0/giphy.gif?cid=6c09b952bkkv5sexjrwu7y1x86e0nphkzb0ef3fcneoh9ijj&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"
]

# --- Commands ---

@app.on_message(filters.command("kiss"))
async def kiss_command(client: Client, message: Message):
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        kisser = message.from_user

        if target_user.id == kisser.id:
            await message.reply_text("🤔 You can't kiss yourself, silly! Try kissing someone else! 😉")
            return

        gif_url = random.choice(KISS_GIFS)
        await client.send_animation(
            chat_id=message.chat.id,
            animation=gif_url,
            caption=f"💋 **{kisser.first_name}** gave a lovely kiss to **{target_user.first_name}**!",
            reply_to_message_id=message.reply_to_message.id
        )
    else:
        await message.reply_text(
            "WHAT THE HELL BROH YOU DONT HAVE ANY GIRLFRIEND ? PLEASE DONT TRY TO USE HIS COMMAND CUZZ IT'S NOT FOR YOU BITCH"
        )

@app.on_message(filters.command("slap"))
async def slap_command(client: Client, message: Message):
    if message.reply_to_message:
        slapper = message.from_user
        target_user = message.reply_to_message.from_user

        if target_user.id == slapper.id:
            await message.reply_text("✋ You can't slap yourself! Unless you're into that... 😉")
            return
            
        gif_url = random.choice(SLAP_GIFS)
        await client.send_animation(
            chat_id=message.chat.id,
            animation=gif_url,
            caption=f"💥 **{slapper.first_name}** just slapped **{target_user.first_name}**! Ouch! 🤣",
            reply_to_message_id=message.reply_to_message.id
        )
    else:
        await message.reply_text(
            "WHAT I DON'T BELEIVE IT, KIDDING IT'S JUST AS I EXPECTED"
        )

@app.on_message(filters.command("cringe"))
async def cringe_command(client: Client, message: Message):
    await message.reply_text(
        "AJ KAMAYENGA TO KAL BETH KAR KHAYENGA APNI MEHNAT PER BHAROSA RAKH PYAR TO DOBARA BHI HO JAYEGA AHHH MERI JAN"
    )

# Note: app.run() is NOT included here.
# This module will be loaded by shivu's main script,
# which is responsible for running the Pyrogram client.
