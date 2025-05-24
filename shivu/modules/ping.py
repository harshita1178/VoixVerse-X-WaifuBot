import time

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, sudo_users

async def ping(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        update.message.reply_text("Seriously Brohh I Am Not Working For You My Master Is Dogesh Bhai 🍷 So Shut Da Fukk off")
        return
    start_time = time.time()
    message = await update.message.reply_text('Pong!☄️')
    end_time = time.time()
    elapsed_time = round((end_time - start_time) * 1000, 3)
    await message.edit_text(f'Pong! {elapsed_time}ms')

application.add_handler(CommandHandler("ping", ping))
