from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from EsproMusic import app
from EsproMusic.utils.database import get_lang
from EsproMusic.utils.decorators.language import LanguageStart, languageCB
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers


# 🔥 INLINE PANEL DIRECT (NO IMPORT)
def build_help_panel(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(_["H_B_1"], callback_data="help_callback hb1"),
                InlineKeyboardButton(_["H_B_2"], callback_data="help_callback hb2"),
                InlineKeyboardButton(_["H_B_3"], callback_data="help_callback hb3"),
            ],
            [
                InlineKeyboardButton(_["H_B_4"], callback_data="help_callback hb4"),
                InlineKeyboardButton(_["H_B_5"], callback_data="help_callback hb5"),
                InlineKeyboardButton(_["H_B_6"], callback_data="help_callback hb6"),
            ],
            [
                InlineKeyboardButton(_["H_B_7"], callback_data="help_callback hb7"),
                InlineKeyboardButton(_["H_B_8"], callback_data="help_callback hb8"),
                InlineKeyboardButton(_["H_B_9"], callback_data="help_callback hb9"),
            ],
            [
                InlineKeyboardButton(_["H_B_10"], callback_data="help_callback hb10"),
                InlineKeyboardButton(_["H_B_11"], callback_data="help_callback hb11"),
                InlineKeyboardButton(_["H_B_12"], callback_data="help_callback hb12"),
            ],
            [
                InlineKeyboardButton(_["H_B_13"], callback_data="help_callback hb13"),
                InlineKeyboardButton(_["H_B_14"], callback_data="help_callback hb14"),
                InlineKeyboardButton(_["H_B_15"], callback_data="help_callback hb15"),
            ],
            [
                InlineKeyboardButton(_["H_B_16"], callback_data="help_callback hb16"),
            ],
            [
                InlineKeyboardButton(_["CLOSE_BUTTON"], callback_data="close"),
            ],
        ]
    )


def back_panel(_):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(_["BACK_BUTTON"], callback_data="back_help")]]
    )


# ================= PRIVATE =================
@app.on_message(filters.command(["help", "utils"]) & filters.private & ~BANNED_USERS)
async def help_private(client, message: Message):

    language = await get_lang(message.chat.id)
    _ = get_string(language)

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["help_1"].format(SUPPORT_CHAT),
        reply_markup=build_help_panel(_),
    )


# ================= GROUP =================
@app.on_message(filters.command(["help", "utils"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_group(client, message: Message, _):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➜ ᴏᴘᴇɴ ɪɴ ᴅᴍ",
                    url=f"https://t.me/{app.username}?start=help",
                )
            ],
            [
                InlineKeyboardButton(
                    "➜ ᴏᴘᴇɴ ʜᴇʀᴇ",
                    callback_data="open_here",
                )
            ],
        ]
    )

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["help_2"],
        reply_markup=keyboard,
    )


# ================= OPEN HERE (INLINE SAME FILE) =================
@app.on_callback_query(filters.regex("^open_here$"))
@languageCB
async def open_here(client, query, _):

    await query.answer()

    msg = query.message

    if msg.photo:
        await msg.edit_caption(
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=build_help_panel(_),
        )
    else:
        await msg.edit_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=build_help_panel(_),
        )


# ================= BACK =================
@app.on_callback_query(filters.regex("^back_help$"))
@languageCB
async def back_help(client, query, _):

    await query.answer()

    msg = query.message

    if msg.photo:
        await msg.edit_caption(
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=build_help_panel(_),
        )
    else:
        await msg.edit_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=build_help_panel(_),
        )


# ================= HELP CALLBACK =================
@app.on_callback_query(filters.regex("help_callback"))
@languageCB
async def helper_cb(client, query, _):

    await query.answer()

    cb = query.data.split()[1]
    keyboard = back_panel(_)

    data = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
        "hb16": helpers.HELP_16,
    }

    text = data.get(cb)
    if not text:
        return

    if query.message.photo:
        await query.message.edit_caption(text, reply_markup=keyboard)
    else:
        await query.message.edit_text(text, reply_markup=keyboard)
