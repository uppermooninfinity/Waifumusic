import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from EsproMusic import app


couple_cache = {}


ghalib_quotes = [
    "💔 'Ishq par zor nahi, hai ye woh aatish Ghalib, jo lagaye na lage aur bujhaaye na bane.'",
    "🌹 'Hazaron khwahishein aisi ke har khwahish pe dam nikle.'",
    "💞 'Dil hi toh hai na sang-o-khisht, dard se bhar na aaye kyun.'",
    "✨ 'Mohabbat mein nahi hai farq jeene aur marne ka.'",
    "💔 'Ishq ne Ghalib nikamma kar diya, warna hum bhi aadmi the kaam ke.'"
]

love_quotes = [
    "💖 Love is not found, it is built in silence.",
    "🌙 Two souls, one universe, infinite emotions.",
    "💞 When hearts align, distance disappears.",
    "✨ You are my today and all of my tomorrows.",
    "💘 Love is when silence becomes conversation."
]


def get_couples(users):
    random.shuffle(users)
    pairs = []

    for i in range(0, len(users) - 1, 2):
        pairs.append((users[i], users[i + 1]))

    if len(users) % 2 == 1:
        pairs.append((users[-1], "💔 ɴᴏ ᴘᴀʀᴛɴᴇʀ"))

    return pairs


def make_text(couple, quote):
    a, b = couple

    return (
        "💞 ᴄᴏᴜᴘʟᴇ ɢᴇɴᴇʀᴀᴛᴏʀ 💞\n"
        "━━━━━━━━━━━━━━\n\n"
        f"👩‍❤️‍👨 {a}\n"
        f"💍  +  💍\n"
        f"{b}\n\n"
        "━━━━━━━━━━━━━━\n"
        f"{quote}\n"
        "━━━━━━━━━━━━━━\n"
        "💫 ʟᴏᴠᴇ ɪs ᴄʀᴇᴀᴛᴇᴅ ʜᴇʀᴇ 💫"
    )


def buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💘 ᴡᴀɴɴᴀ sᴇᴇ ɴᴇxᴛ ᴄᴏᴜᴘʟᴇ",
                    callback_data="next_couple"
                )
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
        return await message.reply_text("❌ ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴍᴇᴍʙᴇʀs")

    couples = get_couples(members)

    couple_cache[chat_id] = {
        "couples": couples,
        "last": None
    }

    pair = random.choice(couples)
    quote = random.choice(ghalib_quotes + love_quotes)

    couple_cache[chat_id]["last"] = pair

    await message.reply_text(
        make_text(pair, quote),
        reply_markup=buttons()
    )


@app.on_callback_query(filters.regex("next_couple"))
async def next_couple(client, callback_query):

    chat_id = callback_query.message.chat.id

    if chat_id not in couple_cache:
        return await callback_query.answer(
            "❌ ʀᴜɴ /couple ғɪʀsᴛ",
            show_alert=True
        )

    data = couple_cache[chat_id]
    couples = data["couples"]

    new_pair = random.choice(couples)
    quote = random.choice(ghalib_quotes + love_quotes)

    data["last"] = new_pair

    await callback_query.message.edit_text(
        make_text(new_pair, quote),
        reply_markup=buttons()
    )

    await callback_query.answer("💞 ɴᴇxᴛ ʟᴏᴠᴇ sᴛᴏʀʏ ɢᴇɴᴇʀᴀᴛᴇᴅ")
