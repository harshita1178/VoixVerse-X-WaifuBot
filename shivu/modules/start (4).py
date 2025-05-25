from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext
from shivu import application
import random

# GIF Lists
GIF_PM = [
    "https://media0.giphy.com/media/MugllcR6Gq8Y8/giphy.gif?cid=6c09b952hnnz2h6zxjjlqtazycplp2b7zy9u7elexn8ebu2a&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media2.giphy.com/media/sRKWXFDcXMC1W/giphy.gif?cid=6c09b952bxbkr207gwstxo2m7sla8sbswx1xtbg6o3syr2jl&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media2.giphy.com/media/rYDwgBF6osqoE/giphy.gif?cid=6c09b952xzf7yoeu8djcad5sx6g7f5rkkv13uejq110eh929&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media0.giphy.com/media/g9rtYY1BKdaQE/giphy.gif?cid=6c09b952od1gfvhno4lvfomijurmv0cql15z4jyk19oge11l&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media0.giphy.com/media/KTCsHtu8pEZ32/giphy.gif?cid=6c09b952qdwbbvgudgwnqhi4cv4ce5le4gnnvcdt6mbv50pq&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/Me2aqz5T2AhbO/giphy.gif?cid=6c09b952s5mia9aa06ur9jy0qcl444hqpqptf0gkc5hfmg4t&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/QYPickEOksXNm/giphy.gif?cid=6c09b952zod6e1kwvcayr1wjdyljq74qrl1egfx2go5liflg&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"
]

GIF_GC = [
    "https://media4.giphy.com/media/LUnjrcDnwdbi/giphy.gif?cid=6c09b952708v30w4q92kz6vn5bv654fxdeh5rrm743gpgmnp&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/uemCr0wASMIsE/giphy.gif?cid=6c09b952q4a21nisetece1golfk230e3ia94o5j1f8jjtd6p&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media2.giphy.com/media/RQjo6hWLt0PpS/giphy.gif?cid=6c09b952dfbmovsvipqzrxuxd3h5gtxw8fo9zv4vjrilg4kv&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/Hb8VDb6VygJQQ/giphy.gif?cid=6c09b952vde7sxx24bq3vnpuw6o4jt28bjc5pqfur3j8p225&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media0.giphy.com/media/Q3IgmxMZI3r4k/giphy.gif?cid=6c09b952sde09wxukbdk3t1a7veqzsxolquhwif41rgwh1wy&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media2.giphy.com/media/CWOkM9jcoVnlm/giphy.gif?cid=6c09b9525u5210ywpqjggwu4tpnsujw6892jxbw1ty6ipx3j&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media0.giphy.com/media/AGaEzUZ5rPGrm/giphy.gif?cid=6c09b999eky8wn6yupknspt9uozs2b3ezfw00d3mht8lgfe6&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media3.giphy.com/media/HaOyeb1aQLlGU/giphy.gif?cid=6c09b952hgh2pb3l7h3lfdkdsl7yzg4csvpaxgzitu4wxspu&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/3ohc19U9adbyp0Kc9O/giphy.gif?cid=6c09b952tcucsqcri72v1s7olhdesn60ydp9ivm5mwgomvr3&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/xULW8JfaTiSY0jemc0/giphy.gif?cid=6c09b952x21w8em7pg1noq5ju62s7ictjkne8cp4g8sdgyj7&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g"
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
    else:
        gif = random.choice(GIF_GC)
        caption = "🎴Alive!?... Connect to me in PM for more information."
        await context.bot.send_animation(
            chat_id=update.effective_chat.id,
            animation=gif,
            caption=caption
        )

# HELP Callback
async def help_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    text = (
        "Yo loser,\n\n"
        "I ain't your average Husbando bot, alright?\n"
        "I drop the Over Powered multiverse characters every 100 messages — and if you're slow, someone else snatches your Husbando. Cry later.\n\n"
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
