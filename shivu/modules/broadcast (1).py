from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, pm_users

# Try to import TelegramError safely
try:
    from telegram.error import TelegramError
except ImportError:
    TelegramError = Exception # fallback

OWNER_ID = 6675050163
GROUP_ID = -1002668191611
CHANNEL_ID = -1002109265407

# GIF URLs for success and failure
BROADCAST_SUCCESS_GIF = "https://media2.giphy.com/media/JXibbAa7ysN9K/giphy.gif?cid=6c09b95281857tp7w7enieht8s28j2kvgrvwd0kxudhc8tpd&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"
BROADCAST_FAILURE_GIF = "https://media1.giphy.com/media/ZdX2YnrtjpmYo/giphy.gif?cid=6c09b952yazow7c49fodh2x6quwilmn3bfy8lmle87cg41wx&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"

GBROADCAST_SUCCESS_GIF = "https://media2.giphy.com/media/cxPtMDHG8Ljry/giphy.gif?cid=6c09b95236qhdx1x0ktttnl2w2783sn3ugwvwmtos2tmqyp7&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"
GBROADCAST_FAILURE_GIF = "https://media1.giphy.com/media/NOycFdfd1y7Cg/giphy.gif?cid=6c09b952kzq6nvijqi3psn62nq2bkvkin7yekky7qhg0pl09&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"

CBROADCAST_SUCCESS_GIF = "https://media0.giphy.com/media/MdLFOyVZtoUPm/giphy.gif?cid=6c09b9523lypwjlvk1qf1gztpv3kv637ydszu91y2554hvl8&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"
CBROADCAST_FAILURE_GIF = "https://media1.giphy.com/media/BcSfi7jRHsLV6/giphy.gif?cid=6c09b952ej3ys3kwqy8c5eohwqy1kgwmcm09dyucyrengoa3&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"


DENY_MSG = "🎐I've been summoned by Dogesh Bhai🍷 You can't control me! Sun Of BITCH "
REPLY_MSG = "🍃Reply to a message to broadcast it."
DONE_MSG = "🍫Broadcast sent to all successfully." # This will be replaced by GIF messages


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
        return True # Indicate success
    except TelegramError:
        return False # Indicate failure


# /broadcast command
async def broadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        await update.message.reply_animation(
            animation=BROADCAST_FAILURE_GIF,
            caption=REPLY_MSG
        )
        return

    msg = update.message.reply_to_message
    success_count = 0
    total_users = 0
    async for user in pm_users.find():
        total_users += 1
        if await forward_with_buttons(context, user['_id'], msg):
            success_count += 1
    
    if success_count > 0: # If at least one broadcast was successful
        await update.message.reply_animation(
            animation=BROADCAST_SUCCESS_GIF,
            caption=f"🍫Broadcast sent to {success_count}/{total_users} users successfully."
        )
    else: # If no broadcast was successful (e.g., all failed due to user blocks)
        await update.message.reply_animation(
            animation=BROADCAST_FAILURE_GIF,
            caption="😔 Failed to broadcast to any user. They might have blocked the bot."
        )


# /gbroadcast command
async def gbroadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        await update.message.reply_animation(
            animation=GBROADCAST_FAILURE_GIF,
            caption=REPLY_MSG
        )
        return

    msg = update.message.reply_to_message
    if await forward_with_buttons(context, GROUP_ID, msg):
        await update.message.reply_animation(
            animation=GBROADCAST_SUCCESS_GIF,
            caption="🪽Broadcast sent to the group successfully."
        )
    else:
        await update.message.reply_animation(
            animation=GBROADCAST_FAILURE_GIF,
            caption="💔 Failed to broadcast to the group. Check if the bot is admin or if the group ID is correct."
        )


# /cbroadcast command
async def cbroadcast(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text(DENY_MSG)

    if not update.message.reply_to_message:
        await update.message.reply_animation(
            animation=CBROADCAST_FAILURE_GIF,
            caption=REPLY_MSG
        )
        return

    msg = update.message.reply_to_message
    if await forward_with_buttons(context, CHANNEL_ID, msg):
        await update.message.reply_animation(
            animation=CBROADCAST_SUCCESS_GIF,
            caption="☔Broadcast sent to the channel successfully."
        )
    else:
        await update.message.reply_animation(
            animation=CBROADCAST_FAILURE_GIF,
            caption="❌ Failed to broadcast to the channel. Check if the bot is admin or if the channel ID is correct."
        )

# Register handlers
application.add_handler(CommandHandler("broadcast", broadcast))
application.add_handler(CommandHandler("gbroadcast", gbroadcast))
application.add_handler(CommandHandler("cbroadcast", cbroadcast))
