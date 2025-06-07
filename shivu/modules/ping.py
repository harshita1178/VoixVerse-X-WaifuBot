import time
import random

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, sudo_users # Assuming shivu and sudo_users are correctly imported from your project

# Owner ID yahan define kar rahe hain
OWNER_ID = 6675050163 # MADARA ka actual Telegram User ID yahan daalo

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

    # Check if the user is the owner
    if user_id == OWNER_ID:
        start_time = time.time()
        # Pehle "Yoo Madara What's up?" bhejo
        await update.message.reply_text("Yoo Madara What's up?")
        
        # Ab Pong! aur ping time bhejo, aur shayari
        message = await update.message.reply_text('Pong!☄️')
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)
        await message.edit_text(f'Pong! {elapsed_time}ms\n\n**Shayari for you:**\n{random_shayari}')
    
    # Check if the user is a sudo user (but not the owner, already handled)
    elif str(user_id) in sudo_users:
        start_time = time.time()
        message = await update.message.reply_text('Pong!☄️')
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)
        await message.edit_text(f'Pong! {elapsed_time}ms\n\n**Shayari for you:**\n{random_shayari}')
    
    # If neither owner nor sudo user
    else:
        await update.message.reply_text("Seriously Brohh I Am Not Working For You My Master Is Dogesh Bhai 🍷 So Shut Da Fukk off")
        return

application.add_handler(CommandHandler("ping", ping))
