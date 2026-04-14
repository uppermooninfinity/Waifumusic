import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from EsproMusic import app


couple_cache = {}


def get_couples(users):
    random.shuffle(users)
    pairs = []

    for i in range(0, len(users) - 1, 2):
        pairs.append((users[i], users[i + 1]))

    if len(users) % 2 == 1:
        pairs.append((users[-1], "💔 ɴᴏ ᴘᴀʀᴛɴᴇʀ"))

    return pairs


def make_text(couple):
    a, b = couple

    return (
        "💞 ᴄᴏᴜᴘʟᴇ ɢᴇɴᴇʀᴀᴛᴏʀ 💞\n\n"
        f"👩‍❤️‍👨 {a}  +  {b}\n\n"
        "✨ ʟᴏᴠᴇ ɪs ɪɴ ᴛʜᴇ ᴀɪʀ ✨"
    )


def buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💘 ᴡᴀɴɴᴀ sᴇᴇ ɴᴇxᴛ ᴏɴᴇ", callback_data="next_couple")
            ]
        ]
    )


@app.on_message(filters.command("couple") & filters.group)
async def couple_handler(client, message: Message):

    chat_id = message.chat.id

    members = []

    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot:
            members.append(member.user.first_name)

    if len(members) < 2:
        return await message.reply_text("❌ ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs")

    couples = get_couples(members)

    couple_cache[chat_id] = couples

    first = couples[0]

    await message.reply_text(
        make_text(first),
        reply_markup=buttons()
    )


@app.on_callback_query(filters.regex("next_couple"))
async def next_couple(client, callback_query):

    chat_id = callback_query.message.chat.id

    if chat_id not in couple_cache:
        return await callback_query.answer("❌ ɴᴏ ᴅᴀᴛᴀ, ʀᴜɴ /couple", show_alert=True)

    couples = couple_cache[chat_id]

    new_pair = random.choice(couples)

    await callback_query.message.edit_text(
        make_text(new_pair),
        reply_markup=buttons()
    )

    await callback_query.answer("💞 ɴᴇxᴛ ᴄᴏᴜᴘʟᴇ ɢᴇɴᴇʀᴀᴛᴇᴅ")
