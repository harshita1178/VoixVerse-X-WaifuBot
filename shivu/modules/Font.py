import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- !!! CRITICAL SECURITY WARNING !!! ---
# DEAR USER: Hardcoding your API_ID, API_HASH, and BOT_TOKEN directly into your
# code and pushing it to a public GitHub repository is EXTREMELY INSECURE.
# Anyone can see these credentials and misuse your Telegram account and bot.
# It is HIGHLY RECOMMENDED to use environment variables (e.g., via a .env file)
# or a secure configuration management system for these sensitive details.
# Proceed at your own risk.
# --- !!! CRITICAL SECURITY WARNING !!! ---

# --- Bot Configuration (YOUR CREDENTIALS ADDED DIRECTLY) ---
# ** DO NOT SHARE THIS FILE PUBLICLY ON GITHUB IF THESE ARE YOUR REAL CREDENTIALS **
API_ID = 22099263  # Your Telegram API ID - Added by user request
API_HASH = "12efef2ba448d268459dc136427d1ba0"  # Your Telegram API Hash - Added by user request
BOT_TOKEN = "7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY"  # Your BotFather Bot Token - Added by user request

# Initialize the Pyrogram Client
app = Client(
    "my_font_bot_session",  # Session name for Pyrogram, can be anything
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Font Conversion Helper Function ---
# This function converts standard English alphabets to various Unicode mathematical
# alphanumeric symbols, mimicking different font styles.
# You might need to research specific Unicode ranges for more advanced or
# "real" font styles not directly representable by standard Unicode blocks.
def convert_to_unicode_font(text, start_upper, start_lower):
    converted_text = ""
    for char in text:
        # Check if character is an English alphabet (A-Z or a-z)
        if 'A' <= char <= 'Z':
            # Check if the target Unicode range is valid for uppercase
            # Using 0x1F77F as a general upper bound for Plane 1 unicode chars
            if start_upper and (start_upper + (ord(char) - ord('A'))) <= 0x1F77F:
                converted_text += chr(start_upper + (ord(char) - ord('A')))
            else:
                converted_text += char  # Fallback if no specific unicode for uppercase
        elif 'a' <= char <= 'z':
            # Check if the target Unicode range is valid for lowercase
            if start_lower and (start_lower + (ord(char) - ord('a'))) <= 0x1F77F:
                converted_text += chr(start_lower + (ord(char) - ord('a')))
            else:
                converted_text += char  # Fallback if no specific unicode for lowercase
        else:
            converted_text += char  # Keep non-alphabetic characters as they are
    return converted_text

# --- Font Styles Dictionary ---
# This dictionary maps font names to lambda functions that convert text to that style.
# The Unicode ranges used here are common for mathematical alphanumeric symbols.
# Some "fonts" are placeholders or simple transformations.
font_styles = {
    "Typewriter": lambda text: convert_to_unicode_font(text, 0x1D68C, 0x1D696), # Monospace
    "Outline": lambda text: convert_to_unicode_font(text, 0x1D538, 0x1D552), # Double-Struck
    "Serif": lambda text: convert_to_unicode_font(text, 0x1D68C, 0x1D696), # Often similar to Monospace, adjust if true Serif unicode needed
    "SMALL CAPS": lambda text: "".join(
        chr(0xFF21 + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else c # Fullwidth for small caps effect
        for c in text.upper()
    ),
    "script": lambda text: convert_to_unicode_font(text, 0x1D49C, 0x1D4B6), # Mathematical Script
    "tiny": lambda text: "".join(
        chr(0x1D586 + (ord(c) - ord('a'))) if 'a' <= c <= 'z' else # Tiny lowercase
        chr(0x1D56C + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else c # Bold Fraktur for uppercase as a substitute
        for c in text
    ),
    "COMIC": lambda text: "".join(f"C{c}C" for c in text), # Example: Simple prefix/suffix
    "Sans": lambda text: convert_to_unicode_font(text, 0x1D5BA, 0x1D5D4), # Sans-serif
    "CIRCLES": lambda text: "".join(
        chr(0x24B6 + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else
        chr(0x24D0 + (ord(c) - ord('a'))) if 'a' <= c <= 'z' else
        c for c in text
    ), # Enclosed Alphanumerics
    "Gothic": lambda text: convert_to_unicode_font(text, 0x1D504, 0x1D51E), # Fraktur
    "S P E C I A L": lambda text: " ".join(list(text.upper())), # Spaced out
    "S Q U A R E S": lambda text: "".join(f"[{c}]" for c in text), # Enclosed in brackets
    "R E V E R S E": lambda text: text[::-1], # Reversed text
    "Andalucia": lambda text: "~" + text + "~", # Placeholder (Requires specific font library/image generation for true effect)
    "𝕸𝖆𝖉𝖆𝖗𝖆": lambda text: convert_to_unicode_font(text, 0x1D56C, 0x1D586), # Bold Fraktur (similar to screenshot)
    "𝕃𝕀ℕ𝔼𝕐𝕋ℍ𝕀ℕ𝔾": lambda text: "Liney" + text + "Thing", # Placeholder
    "SxTopt": lambda text: "Sx" + text + "Topt", # Placeholder
    "FMxOazMein": lambda text: "FMxOaz" + text + "Mein", # Placeholder
    "Clouds": lambda text: "☁️" + text + "☁️", # Emojis as decoration
    "Happy": lambda text: "😊" + text + "😊", # Emojis as decoration
    "Sad": lambda text: "😔" + text + "😔" # Emojis as decoration
}

# --- /font Command Handler ---
@app.on_message(filters.command("font"))
async def font_command_handler(client, message):
    if len(message.command) > 1:
        text_to_format = " ".join(message.command[1:])
        buttons = []
        row = []
        # Create inline keyboard buttons for each font style
        for i, (font_name, _) in enumerate(font_styles.items()):
            # Telegram callback_data has a 64-byte limit. Truncate text if too long.
            # For very long texts, consider storing the text in a temporary database
            # and sending only an ID in callback_data.
            safe_text_to_format = text_to_format[:50] # Limit to approx 50 characters
            callback_data = f"font_{font_name}_{safe_text_to_format}"
            
            row.append(InlineKeyboardButton(font_name, callback_data=callback_data))
            
            # Arrange buttons in rows of 3, as seen in the screenshot
            if (i + 1) % 3 == 0:
                buttons.append(row)
                row = []
        
        # Add any remaining buttons in the last row
        if row:
            buttons.append(row)

        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            "Apne text ke liye font style chuno:",
            reply_markup=reply_markup
        )
    else:
        await message.reply_text("Kripya format karne ke liye text dein. Example: `/font YourText`")

# --- Callback Query Handler for Font Selection ---
@app.on_callback_query(filters.regex(r"^font_"))
async def font_callback_handler(client, callback_query):
    # callback_query.data will be in the format: "font_<font_name>_<original_text>"
    print(f"DEBUG: Callback data received: {callback_query.data}") # DEBUG LINE

    try:
        data_parts = callback_query.data.split("_", 2) # Splits into ['font', 'FontName', 'YourText']
        
        # Basic check to prevent IndexError if data_parts is too short
        if len(data_parts) < 3:
            print(f"ERROR: Insufficient data parts in callback_query.data: {callback_query.data}")
            await callback_query.answer("Callback data incomplete. Please try again.", show_alert=True)
            return

        font_name = data_parts[1]
        original_text = data_parts[2]

        print(f"DEBUG: Extracted font_name: {font_name}")    # DEBUG LINE
        print(f"DEBUG: Extracted original_text: {original_text}") # DEBUG LINE

        if font_name in font_styles:
            formatted_text = font_styles[font_name](original_text)
            
            print(f"DEBUG: Formatted text: {formatted_text}") # DEBUG LINE

            # Show a brief notification to the user (appears at the top of the screen)
            await callback_query.answer(f"Text ko {font_name} mein badal diya!", show_alert=False)
            
            # Edit the original message to display the formatted text
            await callback_query.edit_message_text(
                f"Original text: `{original_text}`\n"
                f"Formatted text ({font_name}): `{formatted_text}`",
                parse_mode="Markdown" # Use Markdown to render backticks as monospace/code
            )
        else:
            print(f"DEBUG: Font name '{font_name}' not found in font_styles dictionary.") # DEBUG LINE
            await callback_query.answer("Invalid font style selected.", show_alert=True)
    except Exception as e:
        print(f"ERROR: General error in font_callback_handler for data {callback_query.data}: {e}")
        await callback_query.answer("Kuch error ho gaya. Phir se try karo.", show_alert=True)

# --- Start the Bot ---
print("Bot is starting...")
# This line starts the bot and keeps it running to listen for updates.
app.run()
print("Bot started!")
