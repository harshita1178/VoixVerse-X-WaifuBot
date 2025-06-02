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

# Captions corresponding to each GIF in GIF_PM (order matters!)
GIF_PM_CAPTIONS = {
    "https://media0.giphy.com/media/BfevCgt1YxDTW/giphy.gif": """
🍷 *The Shadow Rises.* ☄️
Reincarnated by Dogesh Bhai. My professional directive: Claim souls.

— Random anime character drops every 100 messages.
— Use /grasp to seize them.
— Track your dominance with /harem, /top.

This is not a game. It's a conquest.
[ + ] *Bind Me To Your Group.*
The hunt begins.
""",
    "https://media4.giphy.com/media/6sv3Z8wXzyEzC/giphy.gif": """
🌟 *Welcome, Soul Seeker.* 🌟
I am here to guide your path to ultimate collection.

— Discover rare characters every 100 messages.
— Use /grasp to add them to your collection.
— Command your destiny with /harem and /top.

Join the quest.
""",
    "https://media4.giphy.com/media/5D8fDjKyQfuZW/giphy.gif": """
🌌 *A New Journey Begins.* 🌌
Unleash the power of legendary anime characters.

— Characters appear randomly in your group chats.
— Type /grasp swiftly to claim them.
— Showcase your dominance with /harem.

Your legend awaits.
""",
    "https://media0.giphy.com/media/MugllcR6Gq8Y8/giphy.gif": """
⚔️ *The Arena Awaits.* ⚔️
Collect, conquer, and prove your might.

— Rare characters are dropped regularly.
— Be quick to /grasp them.
— See your ranks with /harem and /top.

Are you ready for the challenge?
""",
    "https://media2.giphy.com/media/sRKWXFDcXMC1W/giphy.gif": """
🔮 *Secrets of the Multiverse.* 🔮
I bring forth beings of immense power.

— Characters manifest at random intervals.
— Use /grasp to add them to your side.
— View your powerful collection with /harem.

Embrace the mystery.
""",
    "https://media2.giphy.com/media/rYDwgBF6osqoE/giphy.gif": """
🚀 *Your Adventure Starts Now.* 🚀
Collect the mightiest heroes and villains.

— Characters appear in your groups without warning.
— A quick /grasp secures your prize.
— Dominate the leaderboards with /top.

The galaxy is yours to explore.
""",
    "https://media0.giphy.com/media/g9rtYY1BKdaQE/giphy.gif": """
✨ *The Stars Align.* ✨
Rare and powerful characters are within your reach.

— Look out for random character drops.
— Use /grasp to claim your desired soul.
— Track your progress with /harem and /top.

Your destiny unfolds.
""",
    "https://media0.giphy.com/media/KTCsHtu8pEZ32/giphy.gif": """
👑 *Ascend to Power.* 👑
Become the ultimate collector.

— Characters drop frequently in groups.
— Be the first to /grasp them.
— Build your empire with /harem.

Rule the collection.
""",
    "https://media1.giphy.com/media/Me2aqz5T2AhbO/giphy.gif": """
🌠 *Beyond the Horizon.* 🌠
New characters await your command.

— Engage in group chats to find them.
— Use /grasp to add them to your arsenal.
— See your elite team with /harem.

Explore the unknown.
""",
    "https://media1.giphy.com/media/QYPickEOksXNm/giphy.gif": """
📜 *The Prophecy Unfolds.* 📜
You are destined for greatness.

— Powerful characters will appear before you.
— Master the /grasp command.
— Chart your rise to the top with /top.

Fulfill your destiny.
"""
}

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

# Captions corresponding to each GIF in GIF_GC
GIF_GC_CAPTIONS = {
    "https://media4.giphy.com/media/LUnjrcDnwdbi/giphy.gif": "👁️ *I observe.* For deeper truths, and to claim what is rightfully yours, approach me in a private message.",
    "https://media1.giphy.com/media/uemCr0wASMIsE/giphy.gif": "✨ *A new presence is here.* For greater power, seek me in PM.",
    "https://media2.giphy.com/media/RQjo6hWLt0PpS/giphy.gif": "🌌 *Dimensions collide.* Find me in private for what awaits.",
    "https://media4.giphy.com/media/Hb8VDb6VygJQQ/giphy.gif": "👑 *The hunt begins.* Approach me in DM to join the conquest.",
    "https://media0.giphy.com/media/Q3IgmxMZI3r4k/giphy.gif": "🔮 *Whispers of power.* Connect with me privately to uncover more.",
    "https://media2.giphy.com/media/CWOkM9jcoVnlm/giphy.gif": "🌟 *New energies are stirring.* Message me directly to explore them.",
    "https://media0.giphy.com/media/AGaEzUZ5rPGrm/giphy.gif": "🔥 *The path is set.* DM me to begin your journey of collection.",
    "https://media3.giphy.com/media/HaOyeb1aQLlGU/giphy.gif": "🚀 *Beyond the ordinary.* Find me in private to unveil secrets.",
    "https://media4.giphy.com/media/3ohc19U9adbyp0Kc9O/giphy.gif": "📜 *An ancient call.* Speak with me in DM for destiny's embrace.",
    "https://media1.giphy.com/media/xULW8JfaTiSY0jemc0/giphy.gif": "⚔️ *Prepare for greatness.* Your true adventure starts in a private chat."
}

BUTTONS = [
    [InlineKeyboardButton("ADD ME", url="http://t.me/Daddy_Madara_WaifuBot?startgroup=new")],
    [InlineKeyboardButton("SUPPORT", url="https://t.me/Anime_Circle_Club"),
     InlineKeyboardButton("UPDATES", url="https://t.me/+vDcCB_w1fxw1YTll")],
    [InlineKeyboardButton("HELP", callback_data="help_msg")],
    [InlineKeyboardButton("SOURCE", url="https://github.com/MyNameIsShekhar/WAIFU-HUSBANDO-CATCHER")]
]

# List of emojis for the animation
EMOJIS_GC_ANIMATION = ['🎊', '⚡']

# /start command
async def start(update: Update, context: CallbackContext):
    if update.effective_chat.type == "private":
        gif = random.choice(GIF_PM)
        # Get the corresponding caption for the chosen GIF
        caption = GIF_PM_CAPTIONS.get(gif, """
🍷 *The Shadow Rises.* ☄️
Reincarnated by Dogesh Bhai. My professional directive: Claim souls.

— Random anime character drops every 100 messages.
— Use /grasp to seize them.
— Track your dominance with /harem, /top.

This is not a game. It's a conquest.
[ + ] *Bind Me To Your Group.*
The hunt begins.
""") # Default caption if GIF not found in dictionary

        await update.message.reply_animation(
            animation=gif,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(BUTTONS),
            parse_mode='Markdown'
        )
    else: # This is the Group Chat (GC) logic
        gif = random.choice(GIF_GC)
        # Get the corresponding caption for the chosen GC GIF
        final_gc_caption = GIF_GC_CAPTIONS.get(gif, "👁️ *I observe.* For deeper truths, and to claim what is rightfully yours, approach me in a private message.") 

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
                    await asyncio.sleep(0.5) # Delay increased from 0.3 to 0.5 seconds
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

    # New Help message for GC, keeping the GIF in place
    text = (
        "🌌 *The Grimoire of Souls.* 🌌\n\n"
        "This domain is not for the faint of heart.\n"
        "I am here to bind the strongest characters from across the multiverse to your command.\n\n"
        "*My Directives:*\n"
        "— Every 100 messages, a new soul manifests.\n"
        "— Employ /grasp to claim it before others do.\n"
        "— Monitor your growing dominion: /harem, /top.\n"
        "— Use /collection to see all available entities.\n\n"
        "Remember, every unclaimed soul is a lost opportunity.\n"
        "Your reign awaits. Now, proceed."
    )

    keyboard = [[InlineKeyboardButton("BACK", callback_data="back_start")]]
    
    # Use edit_message_caption to change text while keeping the GIF
    await query.edit_message_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# BACK to START message
async def back_to_start(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # When going back to start, you'll need to re-select a GIF and its caption
    # for the DM chat (since the original start message was random).
    # For simplicity, I'm setting it to the first GIF's caption for "BACK" button.
    # If you want it to be random again, you can re-implement random.choice here.
    gif_for_back = GIF_PM[0] # You can make this random if preferred
    caption_for_back = GIF_PM_CAPTIONS[gif_for_back]


    await query.edit_message_caption(
        caption=caption_for_back,
        reply_markup=InlineKeyboardMarkup(BUTTONS),
        parse_mode='Markdown'
    )

# Register handlers
application.add_handler(CommandHandler("start", start, block=False))
application.add_handler(CallbackQueryHandler(help_callback, pattern="help_msg"))
application.add_handler(CallbackQueryHandler(back_to_start, pattern="back_start"))
