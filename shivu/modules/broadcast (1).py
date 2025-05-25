from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, pm_users, top_global_groups_collection # top_global_groups_collection ko import kiya
import asyncio # For parallel sending

# Try to import TelegramError safely
try:
    from telegram.error import TelegramError
except ImportError:
    TelegramError = Exception  # fallback

OWNER_ID = 6675050163
GROUP_ID = -1002668191611
CHANNEL_ID = -1002109265407

DENY_MSG = "🎐I've been summoned by Dogesh Bhai🍷 You can't control me!"
REPLY_MSG = "🍃Reply to a message to broadcast it."
DONE_MSG = "💫Broadcast sent to all successfully."
SENT_TO_GROUPS_MSG = "✅ Broadcast sent to all groups."
FAILED_SENDS_COUNT_MSG = "\n⚠️ Failed to send to {} chats." # New message for failed count

# Helper function to forward messages with inline buttons
async def forward_with_buttons(context: CallbackContext, chat_id, msg):
    try:
        if msg.text:
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg.text,
                entities=msg.entities,
                reply_markup=msg.reply_markup
            )
        elif msg.photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=msg.photo[-1].file_id,
                caption=msg.caption or "",
                caption_entities=msg.caption_entities,
                reply_markup=msg.reply_markup
            )
        elif msg.video:
            await context.bot.send_video(
                chat_id=chat_id,
                video=msg.video.file_id,
                caption=msg.caption or "",
                caption_entities=msg.caption_entities,
                reply_markup=msg.reply_markup
            )
        else: # For other media types like audio, document, sticker, etc.
            await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )
        return True # Successfully sent
    except TelegramError as e:
        print(f"Failed to send to {chat_id}: {e}") # Debugging for failed sends
        return False # Failed to send
    except Exception as e:
        print(f"An unexpected error occurred sending to {chat_id}: {e}")
        return False


# /broadcast command (PMs)
async def broadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        return await update.message.reply_text(REPLY_MSG)

    msg = update.message.reply_to_message
    
    tasks = []
    async for user in pm_users.find(): # Iterating through cursor asynchronously
        tasks.append(forward_with_buttons(context, user['_id'], msg))
    
    results = await asyncio.gather(*tasks) # Send messages concurrently

    failed_sends = results.count(False)
    
    reply_text = DONE_MSG
    if failed_sends > 0:
        reply_text += FAILED_SENDS_COUNT_MSG.format(failed_sends)

    await update.message.reply_text(reply_text)

# /gbroadcast command (Single predefined group)
async def gbroadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        return await update.message.reply_text(REPLY_MSG)

    msg = update.message.reply_to_message
    
    if await forward_with_buttons(context, GROUP_ID, msg):
        await update.message.reply_text("✅ Sent to group.")
    else:
        await update.message.reply_text("❌ Failed to send to group.")


# /cbroadcast command (Single predefined channel)
async def cbroadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        return await update.message.reply_text(REPLY_MSG)

    msg = update.message.reply_to_message
    
    if await forward_with_buttons(context, CHANNEL_ID, msg):
        await update.message.reply_text("✅ Sent to channel.")
    else:
        await update.message.reply_text("❌ Failed to send to channel.")

# /spbroadcast command (Special broadcast to all groups from top_global_groups_collection)
async def spbroadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        return await update.message.reply_text(REPLY_MSG)

    msg = update.message.reply_to_message
    
    all_groups = await top_global_groups_collection.distinct("group_id")
    
    tasks = []
    for group_id in all_groups:
        tasks.append(forward_with_buttons(context, group_id, msg))
    
    results = await asyncio.gather(*tasks) # Send messages concurrently

    failed_sends = results.count(False)
    
    reply_text = SENT_TO_GROUPS_MSG
    if failed_sends > 0:
        reply_text += FAILED_SENDS_COUNT_MSG.format(failed_sends)

    await update.message.reply_text(reply_text)

# Register handlers
application.add_handler(CommandHandler("broadcast", broadcast))
application.add_handler(CommandHandler("gbroadcast", gbroadcast))
application.add_handler(CommandHandler("cbroadcast", cbroadcast))
application.add_handler(CommandHandler("spbroadcast", spbroadcast)) # Naya handler add kiya
