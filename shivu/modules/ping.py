import time

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, sudo_users

# Owner ID yahan define kar rahe hain, assuming MADARA ka ID yahi hai
# Agar MADARA ka ID sudo_users mein nahi hai, toh use sudo_users mein add karna hoga.
# Ya fir, yahan direct Owner ID daal do.
OWNER_ID = 6675050163 # MADARA ka actual Telegram User ID yahan daalo

async def ping(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    # Check if the user is the owner
    if user_id == OWNER_ID:
        start_time = time.time()
        # Pehle "Yoo Madara What's up?" bhejo
        await update.message.reply_text("Yoo Madara What's up?")
        
        # Ab Pong! aur ping time bhejo
        message = await update.message.reply_text('Pong!☄️')
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)
        await message.edit_text(f'Pong! {elapsed_time}ms')
    
    # Check if the user is a sudo user (but not the owner, already handled)
    elif str(user_id) in sudo_users:
        start_time = time.time()
        message = await update.message.reply_text('Pong!☄️')
        end_time = time.time()
        elapsed_time = round((end_time - start_time) * 1000, 3)
        await message.edit_text(f'Pong! {elapsed_time}ms')
    
    # If neither owner nor sudo user
    else:
        await update.message.reply_text("Seriously Brohh I Am Not Working For You My Master Is Dogesh Bhai 🍷 So Shut Da Fukk off")
        return

application.add_handler(CommandHandler("ping", ping))
