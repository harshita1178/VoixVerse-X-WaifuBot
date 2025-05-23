from pyrogram import Client, filters
from pyrogram.types import Message

OWNER_ID = 6675050163

@Client.on_message(filters.command("all") & filters.group)
async def tag_all_one_by_one(c: Client, m: Message):
    if m.from_user.id != OWNER_ID:
        await m.reply_text("SHUT UP YOU STUPID BAKA 😠 THIS COMMAND IS NOT FOR YOU")
        return

    text = m.text.split(None, 1)
    if len(text) == 1:
        return await m.reply("Please provide a message after /all")

    base_msg = text[1]

    async for member in c.get_chat_members(m.chat.id):
        user = member.user
        if user.is_bot:
            continue
        try:
            await m.reply(f"{base_msg} {user.mention}")
        except Exception:
            continue
            
