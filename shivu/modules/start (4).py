from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext
from shivu import application
import random
import asyncio # For delays

# GIF Lists (Updated with original 3 for GIF_PM)
GIF_PM = [
    "https://media0.giphy.com/media/BfevCgt1YxDTW/giphy.gif",  # Original 1
    "https://media4.giphy.com/media/6sv3Z8wXzyEzC/giphy.gif",  # Original 2
    "https://media4.giphy.com/media/5D8fDjKyQfuZW/giphy.gif",  # Original 3
    "https://media0.giphy.com/media/MugllcR6Gq8Y8/giphy.gif",
    "https://media2.giphy.com/media/sRKWXFDcXMC1W/giphy.gif",
    "https://media2.giphy.com/media/rYDwgBF6osqoE/giphy.gif",
    "https://media0.giphy.com/media/g9rtYY1BKdaQE/giphy.gif",
    "https://media0.giphy.com/media/KTCsHtu8pEZ32/giphy.gif",
    "https://media1.giphy.com/media/Me2aqz5T2AhbO/giphy.gif",
    "https://media1.giphy.com/media/QYPickEOksXNm/giphy.gif"
]

GIF_GC = [
    "https://media4.giphy.com/media/LUnjrcDnwdbi/giphy.gif",
    "https://media1.giphy.com/media/uemCr0wASMIsE/giphy.gif",
    "https://media2.giphy.com/media/RQjo6hWLt0PpS/giphy.gif",
    "https://media4.giphy.com/media/Hb8VDb6VygJQQ/giphy.gif",
    "https://media0.giphy.com/media/Q3IgmxMZI3r4k/giphy.gif",
    "https://media2.giphy.com/media/CWOkM9jcoVnlm/giphy.gif",
    "https://media0.giphy.com/media/AGaEzUZ5rPGrm/giphy.gif",
    "https://media3.giphy.com/media/HaOyeb1aQLlGU/giphy.gif",
    "https://media4.giphy.com/media/3ohc19U9adbyp0Kc9O/giphy.gif",
    "https://media1.giphy.com/media/xULW8JfaTiSY0jemc0/giphy.gif"
]

BUTTONS = [
    [InlineKeyboardButton("ADD ME", url="http://t.me/Daddy_Madara_WaifuBot?startgroup=new")],
    [InlineKeyboardButton("SUPPORT", url="https://t.me/Anime_Circle_Club"),
     InlineKeyboardButton("UPDATES", url="https://t.me/+vDcCB_w1fxw1YTll")],
    [InlineKeyboardButton("HELP", callback_data="help_msg")],
    [InlineKeyboardButton("SOURCE", url="https://github.com/MyNameIsShekhar/WAIFU-HUSBANDO-CATCHER")]
]

# List of emojis for the animation
EMOJIS_GC_ANIMATION = ['🍷', '☄️', '❄️', '👾', '💯', '🎊', '🌀', '🫧', '☔', '🪽']

# /start command
async def start(update: Update, context: CallbackContext):
    if update.effective_chat.type == "private":
        gif = random.choice(GIF_PM)
        caption = """
🍷 *The Shadow Rises.* ☄️
Reincarnated by Dogesh Bhai. My professional directive: Claim souls.

— Random anime character drops every 100 messages.
— Use /grasp to seize them.
— Track your dominance with /harem, /top.

This is not a game. It's a conquest.
[ + ] *Bind Me To Your Group.*
The hunt begins.
"""
        await update.message.reply_animation(
            animation=gif,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(BUTTONS),
            parse_mode='Markdown'
        )
    else: # This is the Group Chat (GC) logic
        gif = random.choice(GIF_GC)
        final_gc_caption = "👁️ *I observe.* For deeper truths, and to claim what is rightfully yours, approach me in a private message." 

        # Step 1: Send a text message to initiate the animation. No GIF yet.
        sent_message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=EMOJIS_GC_ANIMATION[0], # Start with the first emoji
        )

        # Step 2: Perform the emoji animation by editing the *text* of the message
        for i, emoji in enumerate(EMOJIS_GC_ANIMATION):
            if i > 0: # Skip the first emoji as it's already sent
                try:
                    await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=sent_message.message_id,
                        text=emoji,
                    )
                    await asyncio.sleep(0.3) # Adjust delay as needed
                except Exception as e:
                    print(f"Error during emoji animation: {e}")
                    break # Stop if editing fails

        # Step 3: Delete the animated emoji message
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=sent_message.message_id
            )
        except Exception as e:
            print(f"Error deleting temporary emoji message: {e}")

        # Step 4: Finally, send the GIF with the complete caption (text + GIF together)
        await context.bot.send_animation(
            chat_id=update.effective_chat.id,
            animation=gif,
            caption=final_gc_caption,
            reply_markup=InlineKeyboardMarkup(BUTTONS), # Added buttons here for GC
            parse_mode='Markdown' # Use Markdown for the final caption if needed
        )


# HELP Callback
async def help_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    text = (
        "Yo loser,\n\n"
        "I ain't your average Husbando bot, alright?\n"
        "I drop the Over Powered multiverse characters every 100 messages — and if you're slow, someone_else snatches your Husbando. Cry later.\n\n"
        "Wanna build a legacy? Use /grasp fast, flex with /harem, dominate the Husbando world.\n\n"
        "This ain't no kiddie game. This is your Harem. Your pride. Your obsession.\n\n"
        "So add me to your damn group and let the madness begin.\n"
        "You in, or still simping For These Korean 7 Gays?"
    )

    keyboard = [[InlineKeyboardButton("BACK", callback_data="back_start")]]
    await query.edit_message_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# BACK to START message
async def back_to_start(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    caption = """
🍷 *The Shadow Rises.* ☄️
Reincarnated by Dogesh Bhai. My professional directive: Claim souls.

— Random anime character drops every 100 messages.
— Use /grasp to seize them.
— Track your dominance with /harem, /top.

This is not a game. It's a conquest.
[ + ] *Bind Me To Your Group.*
The hunt begins.
"""
    await query.edit_message_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(BUTTONS),
        parse_mode='Markdown'
    )

# Register handlers
application.add_handler(CommandHandler("start", start, block=False))
application.add_handler(CallbackQueryHandler(help_callback, pattern="help_msg"))
application.add_handler(CallbackQueryHandler(back_to_start, pattern="back_start"))
