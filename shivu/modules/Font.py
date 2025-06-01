import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Bot Configuration ---
API_ID = os.getenv("22099263")  # Get from my.telegram.org
API_HASH = os.getenv("12efef2ba448d268459dc136427d1ba0")  # Get from my.telegram.org
BOT_TOKEN = os.getenv("7537641512:AAGAejMiQIVyTwWTY2X_p0JF7InPFCOfYPY")  # Get from @BotFather

if not all([API_ID, API_HASH, BOT_TOKEN]):
    print("Error: API_ID, API_HASH, or BOT_TOKEN environment variables are not set.")
    print("Please set them in a .env file or directly in your environment.")
    exit()

app = Client(
    "my_font_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Font Conversion Helper Function ---
# Yeh function Unicode mathematical alphanumeric symbols ko use karta hai.
# Har font ke liye sahi Unicode range search karna hoga.
def convert_to_unicode_font(text, start_upper, start_lower):
    converted_text = ""
    for char in text:
        # Check if character is an English alphabet (A-Z or a-z)
        if 'A' <= char <= 'Z':
            # Check if the target Unicode range is valid for uppercase
            if start_upper and (start_upper + (ord(char) - ord('A'))) <= 0x1F77F: # Max Unicode Plane 1 (Supplementary Multilingual Plane)
                converted_text += chr(start_upper + (ord(char) - ord('A')))
            else:
                converted_text += char # Fallback if no specific unicode for uppercase
        elif 'a' <= char <= 'z':
            # Check if the target Unicode range is valid for lowercase
            if start_lower and (start_lower + (ord(char) - ord('a'))) <= 0x1F77F:
                converted_text += chr(start_lower + (ord(char) - ord('a')))
            else:
                converted_text += char # Fallback if no specific unicode for lowercase
        else:
            converted_text += char # Keep non-alphabetic characters as they are
    return converted_text

# --- Font Styles Dictionary ---
# Yahan saare font styles aur unke conversion functions hain.
# Maine realistic examples diye hain, par kuch fonts ke liye tujhe accurate Unicode
# ranges dhoondhne honge ya custom logic likhna hoga.
font_styles = {
    "Typewriter": lambda text: convert_to_unicode_font(text, 0x1D68C, 0x1D696), # Monospace
    "Outline": lambda text: convert_to_unicode_font(text, 0x1D538, 0x1D552), # Double-Struck
    "Serif": lambda text: convert_to_unicode_font(text, 0x1D68C, 0x1D696), # Default unicode (often same as Typewriter, adjust if needed)
    "SMALL CAPS": lambda text: "".join(
        chr(0xFF21 + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else c # Fullwidth for small caps feel
        for c in text.upper()
    ),
    "script": lambda text: convert_to_unicode_font(text, 0x1D49C, 0x1D4B6), # Mathematical Script
    "tiny": lambda text: "".join(
        chr(0x1D586 + (ord(c) - ord('a'))) if 'a' <= c <= 'z' else # Tiny lowercase (adjust range for uppercase if needed)
        chr(0x1D56C + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else c
        for c in text
    ),
    "COMIC": lambda text: "".join(f"C{c}C" for c in text), # Example, just to show customization
    "Sans": lambda text: convert_to_unicode_font(text, 0x1D5BA, 0x1D5D4), # Sans-serif
    "CIRCLES": lambda text: "".join(
        chr(0x24B6 + (ord(c) - ord('A'))) if 'A' <= c <= 'Z' else
        chr(0x24D0 + (ord(c) - ord('a'))) if 'a' <= c <= 'z' else
        c for c in text
    ), # Enclosed Alphanumerics
    "Gothic": lambda text: convert_to_unicode_font(text, 0x1D504, 0x1D51E), # Fraktur
    "S P E C I A L": lambda text: " ".join(list(text.upper())),
    "S Q U A R E S": lambda text: "".join(f"[{c}]" for c in text),
    "R E V E R S E": lambda text: text[::-1], # Reverse for example
    "Andalucia": lambda text: "~" + text + "~", # Placeholder, requires a custom font logic or image gen
    "𝕸𝖆𝖉𝖆𝖗𝖆": lambda text: convert_to_unicode_font(text, 0x1D56C, 0x1D586), # Bold Fraktur (similar to the screenshot's Madara)
    "𝕃𝕀ℕ𝔼𝕐𝕋ℍ𝕀ℕ𝔾": lambda text: "Liney" + text + "Thing", # Placeholder
    "SxTopt": lambda text: "Sx" + text + "Topt", # Placeholder
    "FMxOazMein": lambda text: "FMxOaz" + text + "Mein", # Placeholder
    "Clouds": lambda text: "☁️" + text + "☁️",
    "Happy": lambda text: "😊" + text + "😊",
    "Sad": lambda text: "😔" + text + "😔"
}

# --- /font Command Handler ---
@app.on_message(filters.command("font"))
async def font_command_handler(client, message):
    if len(message.command) > 1:
        text_to_format = " ".join(message.command[1:])
        buttons = []
        row = []
        for i, (font_name, _) in enumerate(font_styles.items()):
            # Callback data format: "font_<font_name>_<original_text>"
            # We limit original_text length in callback_data to avoid issues (Telegram limit is 64 bytes)
            # For longer texts, consider storing text in a temporary dict/db and use an ID in callback_data.
            # For simplicity, here we'll truncate.
            safe_text_to_format = text_to_format[:50] # Limit to ~50 chars for callback_data
            callback_data = f"font_{font_name}_{safe_text_to_format}"
            row.append(InlineKeyboardButton(font_name, callback_data=callback_data))
            
            # Create a new row after every 3 buttons (as in screenshot)
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
    # callback_query.data will be something like "font_FontName_YourText"
    try:
        # Split into 'font', 'font_name', 'text'
        data_parts = callback_query.data.split("_", 2)
        font_name = data_parts[1]
        original_text = data_parts[2]

        if font_name in font_styles:
            formatted_text = font_styles[font_name](original_text)
            
            # Show a brief notification to the user
            await callback_query.answer(f"Text ko {font_name} mein badal diya!", show_alert=False)
            
            # Edit the original message to show the formatted text
            await callback_query.edit_message_text(
                f"Original text: `{original_text}`\n"
                f"Formatted text ({font_name}): `{formatted_text}`",
                parse_mode="Markdown" # Use Markdown for code blocks/monospace text
            )
        else:
            await callback_query.answer("Invalid font style select kiya gaya.", show_alert=True)
    except Exception as e:
        print(f"Error in font_callback_handler: {e}")
        await callback_query.answer("Kuch error ho gaya. Phir se try karo.", show_alert=True)

# --- Start the Bot ---
print("Bot is starting...")
app.run()
print("Bot started!")
