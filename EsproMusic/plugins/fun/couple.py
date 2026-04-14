import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from EsproMusic import app


couple_cache = {}


quotes = [
    "💔 Ishq par zor nahi, Ghalib",
    "🌹 Hazaron khwahishein aisi",
    "💞 Love is when two souls become one",
    "✨ Some hearts are destined to meet",
    "💘 You are my today and all my tomorrows"
]


def make_pairs(users):
    random.shuffle(users)
    pairs = []

    for i in range(0, len(users) - 1, 2):
        pairs.append((users[i], users[i + 1]))

    if len(users) % 2 == 1:
        pairs.append((users[-1], None))

    return pairs


def format_user(user):
    if isinstance(user, str):
        return user
    return f"@{user}"


def build_text(pair, quote):
    a, b = pair

    a = format_user(a)
    b = "💔 ɴᴏ ᴘᴀʀᴛɴᴇʀ" if not b else format_user(b)

    return (
        "💞 ᴄᴏᴜᴘʟᴇ ɢᴇɴᴇʀᴀᴛᴏʀ 💞\n"
        "━━━━━━━━━━━━━━\n\n"
        f"👩‍❤️‍👨 {a}\n"
        f"💍 + 💍\n"
        f"{b}\n\n"
        "━━━━━━━━━━━━━━\n"
        f"{quote}\n"
        "━━━━━━━━━━━━━━"
    )


def buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💘 ɴᴇxᴛ ᴄᴏᴜᴘʟᴇ",
                    callback_data="next_couple"
                )
            ]
        ]
    )


@app.on_message(filters.command("couple") & filters.group)
async def couple_handler(client, message: Message):

    chat_id = message.chat.id

    members = []

    async for m in client.get_chat_members(chat_id):
        if m.user and not m.user.is_bot:
            members.append(m.user.username or m.user.first_name)

    if len(members) < 2:
        return await message.reply_text("❌ ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs")

    pairs = make_pairs(members)

    first_pair = random.choice(pairs)

    couple_cache[chat_id] = {
        "pairs": pairs,
        "current": first_pair
    }

    quote = random.choice(quotes)

    await message.reply_text(
        build_text(first_pair, quote),
        reply_markup=buttons()
    )


@app.on_callback_query(filters.regex("^next_couple$"))
async def next_couple(client, callback_query):

    chat_id = callback_query.message.chat.id

    if chat_id not in couple_cache:
        return await callback_query.answer(
            "❌ ʀᴜɴ /couple ғɪʀsᴛ",
            show_alert=True
        )

    data = couple_cache[chat_id]

    new_pair = random.choice(data["pairs"])
    quote = random.choice(quotes)

    data["current"] = new_pair

    try:
        await callback_query.message.edit_text(
            build_text(new_pair, quote),
            reply_markup=buttons()
        )

        await callback_query.answer("💞 ɴᴇxᴛ ᴄᴏᴜᴘʟᴇ ɢᴇɴᴇʀᴀᴛᴇᴅ")

    except Exception:
        await callback_query.answer("⚠️ ᴇʀʀᴏʀ, ʀᴇᴛʀʏ", show_alert=True)
