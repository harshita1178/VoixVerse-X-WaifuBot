from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, pm_users

# Try to import TelegramError safely
try:
    from telegram.error import TelegramError
except ImportError:
    TelegramError = Exception  # fallback

OWNER_ID = 8156600797
GROUP_ID = -1002439979524
CHANNEL_ID = -1002646820042

DENY_MSG = "🎐I've been summoned by Dogesh Bhai🍷 You can't control me!"
REPLY_MSG = "🍃Reply to a message to broadcast it."
DONE_MSG = "💫Broadcast sent to all successfully."

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
        else:
            await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=msg.chat_id,
                message_id=msg.message_id
            )
    except TelegramError:
        pass

# /broadcast command
async def broadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        return await update.message.reply_text(REPLY_MSG)

    msg = update.message.reply_to_message
    async for user in pm_users.find():
        await forward_with_buttons(context, user['_id'], msg)

    await update.message.reply_text(DONE_MSG)

# /gbroadcast command
async def gbroadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        return await update.message.reply_text(REPLY_MSG)

    msg = update.message.reply_to_message
    await forward_with_buttons(context, GROUP_ID, msg)
    await update.message.reply_text("✅ Sent to group.")

# /cbroadcast command
async def cbroadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        return await update.message.reply_text(REPLY_MSG)

    msg = update.message.reply_to_message
    await forward_with_buttons(context, CHANNEL_ID, msg)
    await update.message.reply_text("✅ Sent to channel.")

# Register handlers
application.add_handler(CommandHandler("broadcast", broadcast))
application.add_handler(CommandHandler("gbroadcast", gbroadcast))
application.add_handler(CommandHandler("cbroadcast", cbroadcast))
