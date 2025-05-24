from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.constants import ChatType

from shivu import application, top_global_groups_collection, user_collection, channel_collection # Assuming you have a channel_collection now

async def broadcast(update: Update, context: CallbackContext) -> None:
    OWNER_ID = 6675050163
    
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    message_to_broadcast = update.message.reply_to_message

    if message_to_broadcast is None:
        await update.message.reply_text("Please reply to a message to broadcast.")
        return

    # Fetch all chats, users, and channels
    all_groups = await top_global_groups_collection.distinct("group_id")
    all_users = await user_collection.distinct("id")
    all_channels = await channel_collection.distinct("channel_id") # Assuming 'channel_id' is the field

    # Combine all unique chat IDs (groups, users, channels)
    all_recipients = list(set(all_groups + all_users + all_channels))

    failed_sends = 0

    for chat_id in all_recipients:
        try:
            # Forward the message to each recipient
            await context.bot.forward_message(chat_id=chat_id,
                                              from_chat_id=message_to_broadcast.chat_id,
                                              message_id=message_to_broadcast.message_id)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
            failed_sends += 1

    await update.message.reply_text(f"I'VE COMPLETED MY MISSION ☄️\nFailed to send to {failed_sends} chats/users/channels.")

# Add the command handler
application.add_handler(CommandHandler("broadcast", broadcast, block=False))
