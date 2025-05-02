from pyrogram import Client, filters
import random
import string
from shivu import user_collection, application, collection 
from shivu import shivuu as app
from shivu import shivuu as bot

# Dictionary to store generated codes and their amounts, and user claims
generated_codes = {}

# Function to generate a random string of length 10
def generate_random_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.on_message(filters.command(["gen"]))
async def gen(client, message):
    sudo_user_id = 7044622285  # Change to your actual sudo ID
    if message.from_user.id != sudo_user_id:
        await message.reply_text("❌ Only authorized users can use this command.")
        return
    
    try:
        amount = int(message.command[1])  # Get the amount
        quantity = int(message.command[2])  # Get the quantity
    except (IndexError, ValueError):
        await message.reply_text("⚠ Invalid format. Usage: `/gen <amount> <quantity>`")
        return
    
    code = generate_random_code()
    
    # Store the generated code
    generated_codes[code] = {'amount': amount, 'quantity': quantity, 'claimed_by': []}
    
    await message.reply_text(
        f"✅ Generated Code: `{code}`\n💰 Amount: `{amount:,}` Zexis\n🎟 Quantity: `{quantity}`"
    )

@app.on_message(filters.command(["redeem"]))
async def redeem(client, message):
    code = " ".join(message.command[1:])  
    user_id = message.from_user.id
    
    if code in generated_codes:
        code_info = generated_codes[code]
        
        if user_id in code_info['claimed_by']:
            await message.reply_text("❌ You have already claimed this code.")
            return
        
        if len(code_info['claimed_by']) >= code_info['quantity']:
            await message.reply_text("❌ This code has been fully claimed.")
            return
        
        await user_collection.update_one({'id': user_id}, {'$inc': {'zexis': code_info['amount']}})
        
        code_info['claimed_by'].append(user_id)
        
        await message.reply_text(f"🎉 Redeemed successfully! `{code_info['amount']:,}` Zexis added to your balance.")
    else:
        await message.reply_text("❌ Invalid code.")

# Sudo user IDs
sudo_user_ids = ["6087651372"]
generated_waifus = {}

@bot.on_message(filters.command(["sgen"]))
async def waifugen(client, message):
    if str(message.from_user.id) not in sudo_user_ids:
        await message.reply_text("❌ You are not authorized to generate waifus.")
        return
    
    try:
        character_id = message.command[1]  
        quantity = int(message.command[2])  
    except (IndexError, ValueError):
        await message.reply_text("⚠ Invalid format. Usage: `/sgen <character_id> <quantity>`")
        return

    waifu = await collection.find_one({'id': character_id})
    if not waifu:
        await message.reply_text("❌ Invalid character ID. Waifu not found.")
        return

    code = generate_random_code()
    
    generated_waifus[code] = {'waifu': waifu, 'quantity': quantity}
    
    await message.reply_text(
        f"✅ Generated Code: `{code}`\n👩 Name: {waifu['name']}\n⭐ Rarity: {waifu['rarity']}\n🎟 Quantity: `{quantity}`"
    )

@bot.on_message(filters.command(["sredeem"]))
async def claimwaifu(client, message):
    code = " ".join(message.command[1:])  
    user_id = message.from_user.id
    user_mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"

    if code in generated_waifus:
        details = generated_waifus[code]
        
        if details['quantity'] > 0:
            waifu = details['waifu']
            
            await user_collection.update_one({'id': user_id}, {'$push': {'characters': waifu}})
            
            details['quantity'] -= 1
            
            if details['quantity'] == 0:
                del generated_waifus[code]
            
            await message.reply_photo(
                photo=waifu['img_url'],
                caption=(
                    f"🎊 Congratulations {user_mention}!\n"
                    f"👩 Name: {waifu['name']}\n"
                    f"⭐ Rarity: {waifu['rarity']}\n"
                    f"📺 Anime: {waifu['anime']}\n"
                )
            )
        else:
            await message.reply_text("❌ This code has already been fully claimed.")
    else:
        await message.reply_text("❌ Invalid code.")
