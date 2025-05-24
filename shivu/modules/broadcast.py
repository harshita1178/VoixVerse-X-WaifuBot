from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.constants import ChatType

# Sirf woh collections import karo jo tumhe chahiye (groups aur users)
from shivu import application, top_global_groups_collection, user_collection 

async def broadcast(update: Update, context: CallbackContext) -> None:
    OWNER_ID = 6675050163
    
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    message_to_broadcast = update.message.reply_to_message

    if message_to_broadcast is None:
        await update.message.reply_text("Please reply to a message to broadcast.")
        return

    # Sirf groups aur users ki IDs fetch karo
    all_groups = await top_global_groups_collection.distinct("group_id")
    all_users = await user_collection.distinct("id")

    # Groups aur users ki unique IDs ko combine karo
    all_recipients = list(set(all_groups + all_users))

    failed_sends = 0
    successful_sends = 0

    for chat_id in all_recipients:
        try:
            # Message ko har recipient ko forward karo
            await context.bot.forward_message(chat_id=chat_id,
                                              from_chat_id=message_to_broadcast.chat_id,
                                              message_id=message_to_broadcast.message_id)
            successful_sends += 1
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
            failed_sends += 1

    await update.message.reply_text(
        f"I'VE COMPLETED MY MISSION ☄️\n"
        f"Successfully sent to {successful_sends} chats/users.\n"
        f"Failed to send to {failed_sends} chats/users."
    )

# Command handler add karo
application.add_handler(CommandHandler("broadcast", broadcast, block=False))
