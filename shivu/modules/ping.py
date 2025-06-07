import time
import random

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, sudo_users # Make sure shivu and sudo_users are correctly imported from your main project

# Owner ID yahan define kar rahe hain
OWNER_ID = 6675050163 # MADARA ka actual Telegram User ID yahan daalo

# Image URL
PING_IMAGE_URL = "https://files.catbox.moe/th21me.jpg"

# List of shayaris
SHAYARIS = [
    "Me - Hey Miss Would You Like To Dance With Me?\nGirl - I don't dance with a kid\nMe - Sorry I Didn't know you are pregent",
    "Me - Can I get a picture of you?\nShe - Why?\nMe - So I can show santa what I want for Christmas",
    "Me - I'm really glad I bought life insurance\nShe - Why?!\nMe - Cuz whenever I see you, my heart stopped",
    "Koi accha lage toh Usse pyaar mat karna, Uske liye neende Kharab mat karna, Do din toh woh aayenge khushi se milne, Teesre din kahenge intezaar mat karna",
    "Jaante hue bhi anjaan banti ho, Is tarah mujhe pareshan karti ho, Puchti ho mujhe kya pasand hai, Jawab khud ho phir bhi sawal Karti ho..!!",
    "Khud ka haal dekhne ki bhi fursat nahi hai mujhe,\nAur vo hai ki gairon se ishq karne ka ilzaam lagaya karte hain",
    "Mohabbat Hai Isliye Dil Darta Hai Tumhein Khone Se\nAgar Matlab Hota Toh Kya Farq Padhta Tere Hone Na Hone Se",
    "Tumhe jo mila hai Wo kisi ne khoya hoga,\nJiske sath har pal muskarte ho Koi uske liye roya hoga,\nHar koi yaha jarur hara hai Apni Sachi Mohhbatt se,\nAjj jiske sath app yadde bana rhe ho koi uski yadde leke soya hoga",
    "Nafrat nahi hai tujhse par ab mohabbat bhi nhi rahi\nBichadne ka dukh to bahut hai par ab milne ki chahat nhi rahi..!",
    "Ajnabi se the aap humare liye, hume dosti karna acha laga,\nTairna toh aata tha par aapki aankhon mein dubna acha laga."
]

async def ping(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    # Select a random shayari
    random_shayari = random.choice(SHAYARIS)

    # Prepare the caption
    caption_text = f"**Shayari for you:**\n{random_shayari}\n\n"

    # Check if the user is the owner or a sudo user
    if user_id == OWNER_ID or str(user_id) in sudo_users:
        start_time = time.time()
        
        # Send the photo with the initial caption
        # We don't send a separate "Yoo Madara" message here, it's combined with the photo caption.
        message = await update.message.reply_photo(
            photo=PING_IMAGE_URL,
            caption=caption_text + "Calculating ping..." # Initial message while calculating
        )
        
        # Calculate elapsed time
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)
        
        # Edit the caption of the SAME photo message to add the ping time
        await message.edit_caption(
            caption=caption_text + f'Pong! {elapsed_time}ms'
        )
    
    # If neither owner nor sudo user, send the restricted message
    else:
        await update.message.reply_text("Seriously Brohh I Am Not Working For You My Master Is Dogesh Bhai 🍷 So Shut Da Fukk off")
        return

# Add the command handler to your application
application.add_handler(CommandHandler("ping", ping))
