import asyncio
from pyrogram import filters, Client, types as t
from shivu import shivuu as bot
from shivu import user_collection, collection
import random
import time

# Cooldown & Streaks
cooldowns = {}
roll_streaks = {}
streak_rewards = {5: "🌟 RARE REWARD", 10: "💎 LEGENDARY BONUS"}

# Advanced Congratulatory Messages
def get_congratulatory_message(mention, character):
    partners = f" 💑 Best Couple: {character['partner']}" if character.get("partner") else ""
    return (
        f"🎉 Congratulations, {mention}! You've just married **{character['name']}** "
        f"from **{character['anime']}**! 💍{partners}"
    )

# Failure Message Variations
def get_rejection_message(mention):
    return random.choice(
        [
            f"💔 Oh no, {mention}, your proposal got rejected. Try again later!",
            f"👻 {mention}, no luck this time. Your soulmate slipped away into the shadows!"
        ]
    )

# Streak Bonus Message Generator
def get_streak_bonus_message(mention, streak):
    reward = streak_rewards.get(streak, "🔥 Keep it up!")
    return f"🔥 {mention}, you've hit a streak of {streak} rolls! {reward}"

# Cooldown Timer with Dynamic Emojis
def get_cooldown_message(cooldown_time):
    emoji_sequence = ["⏳", "⌛", "🕒"]
    return f"{random.choice(emoji_sequence)} Please wait {cooldown_time} seconds before rolling again."

# Advanced Marry Command with Special Features
@bot.on_message(filters.command(["marry"]))
async def marry_command(_, message: t.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    mention = message.from_user.mention

    # Cooldown Check
    if user_id in cooldowns and time.time() - cooldowns[user_id] < 60:
        cooldown_time = int(60 - (time.time() - cooldowns[user_id]))
        return await message.reply_text(get_cooldown_message(cooldown_time), quote=True)

    cooldowns[user_id] = time.time()

    # Roll Dice Animation
    await message.reply_text("🎲 Rolling the dice for your proposal... 🎲")
    dice_msg = await bot.send_dice(chat_id)
    dice_value = dice_msg.dice.value

    # Success (1, 2, or 3) - 45% Chance
    if dice_value in [1, 2, 6]:
        characters = await get_unique_characters(user_id)
        if characters:
            for character in characters:
                await user_collection.update_one(
                    {"id": user_id}, {"$push": {"characters": character}}
                )
                roll_streaks[mention] = roll_streaks.get(mention, 0) + 1

                img_url = character["img_url"]
                caption = get_congratulatory_message(mention, character)
                await message.reply_photo(photo=img_url, caption=caption)

                if roll_streaks[mention] > 1:
                    await message.reply_text(
                        get_streak_bonus_message(mention, roll_streaks[mention])
                    )
        else:
            await message.reply_text(
                "🌪️ No unique characters left! Try marrying someone else."
            )
    else:
        # Rejection Handling
        roll_streaks[mention] = 0
        await message.reply_text(get_rejection_message(mention))

# Fetch Unique Characters Based on User
async def get_unique_characters(receiver_id, target_rarities=["⚪️ Common", "🟣 Rare", "🟢 Medium", "🟡 Legendary"]):
    try:
        pipeline = [
            {"$match": {"rarity": {"$in": target_rarities}, "id": {"$nin": await get_user_ids(receiver_id)}}},
            {"$sample": {"size": 1}},
        ]
        cursor = collection.aggregate(pipeline)
        return await cursor.to_list(length=1)
    except Exception as e:
        print(f"Error in fetching characters: {e}")
        return []

# Utility Function for Retrieving Existing User IDs
async def get_user_ids(receiver_id):
    user_data = await user_collection.find_one({"id": receiver_id})
    return [char["id"] for char in user_data.get("characters", [])] if user_data else []
