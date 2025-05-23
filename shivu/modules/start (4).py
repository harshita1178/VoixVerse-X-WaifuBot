from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext
from shivu import application
import random

# GIF Lists
GIF_PM = [
    "https://media0.giphy.com/media/BfevCgt1YxDTW/giphy.gif",
    "https://media4.giphy.com/media/6sv3Z8wXzyEzC/giphy.gif",
    "https://media4.giphy.com/media/5D8fDjKyQfuZW/giphy.gif"
]

GIF_GC = [
    "https://media2.giphy.com/media/HXN6ZE2FbnH44/giphy.gif",
    "https://media1.giphy.com/media/bJ0TSiVhirmlG/giphy.gif",
    "https://media0.giphy.com/media/8SEnoMhrEeBDa/giphy.gif"
]

BUTTONS = [
    [InlineKeyboardButton("ADD ME", url="http://t.me/Daddy_Madara_WaifuBot?startgroup=new")],
    [InlineKeyboardButton("SUPPORT", url="https://t.me/Anime_Circle_Club"),
     InlineKeyboardButton("UPDATES", url="https://t.me/+vDcCB_w1fxw1YTll")],
    [InlineKeyboardButton("HELP", callback_data="help_msg")],
    [InlineKeyboardButton("SOURCE", url="https://github.com/MyNameIsShekhar/WAIFU-HUSBANDO-CATCHER")]
]

# /start command
async def start(update: Update, context: CallbackContext):
    if update.effective_chat.type == "private":
        gif = random.choice(GIF_PM)
        caption = """
✨ *Summoning Jutsu Activated!* ✨  
I’m not just a bot...  
*I’m the gatekeeper to your legendary Harem.*

*Here’s what I do:*  
— After every *100 messages* in your group  
— I drop a *random anime character*  
— First to use */guess* wins them  
— Build your collection with */harem*, */top*, and more

*This isn’t just a game —*  
*This is your rise to becoming the Harem King/Queen.*

So what now?  
Just one click...  
*Unleash the madness. Rule the waifu world.*

[ + ] *Add Me To Your Group*  
Let the hunt begin!
"""
        await update.message.reply_animation(animation=gif, caption=caption, reply_markup=InlineKeyboardMarkup(BUTTONS), parse_mode='Markdown')
    else:
        await update.message.reply_text("🎴Alive!?... Connect to me in PM for more information.")

# HELP Callback
async def help_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    text = (
        "Yo loser,\n\n"
        "I ain't your average Husbando bot, alright?\n"
        "I drop the Over Powered multiverse characters every 100 messages — and if you're slow, someone else snatches your Husbando. Cry later.\n\n"
        "Wanna build a legacy? Use /guess fast, flex with /harem, dominate the Husbando world.\n\n"
        "This ain't no kiddie game. This is your Harem. Your pride. Your obsession.\n\n"
        "So add me to your damn group and let the madness begin.\n"
        "You in, or still simping For These Korean 7 Gays?"
    )

    keyboard = [[InlineKeyboardButton("BACK", callback_data="back_start")]]
    await query.edit_message_caption(caption=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# BACK to START message
async def back_to_start(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    caption = """
✨ *Summoning Jutsu Activated!* ✨  
I’m not just a bot...  
*I’m the gatekeeper to your legendary Harem.*

*Here’s what I do:*  
— After every *100 messages* in your group  
— I drop a *random anime character*  
— First to use */guess* wins them  
— Build your collection with */harem*, */top*, and more

*This isn’t just a game —*  
*This is your rise to becoming the Harem King/Queen.*

So what now?  
Just one click...  
*Unleash the madness. Rule the waifu world.*

[ + ] *Add Me To Your Group*  
Let the hunt begin!
"""
    await query.edit_message_caption(caption=caption, reply_markup=InlineKeyboardMarkup(BUTTONS), parse_mode='Markdown')

# Register
application.add_handler(CommandHandler("start", start, block=False))
application.add_handler(CallbackQueryHandler(help_callback, pattern="help_msg"))
application.add_handler(CallbackQueryHandler(back_to_start, pattern="back_start"))
