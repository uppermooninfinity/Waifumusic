from typing import Union

from pyrogram import filters, types
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from EsproMusic import app
from EsproMusic.utils import help_pannel
from EsproMusic.utils.database import get_lang
from EsproMusic.utils.decorators.language import LanguageStart, languageCB
from EsproMusic.utils.inline.help import help_back_markup
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers


# ================= PRIVATE =================
@app.on_message(filters.command(["help", "utils"]) & filters.private & ~BANNED_USERS)
async def helper_private(client, message: Message):

    language = await get_lang(message.chat.id)
    _ = get_string(language)

    keyboard = help_pannel(_)

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["help_1"].format(SUPPORT_CHAT),
        reply_markup=keyboard,
    )


# ================= GROUP =================
@app.on_message(filters.command(["help", "utils"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_group(client, message: Message, _):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="➜ ᴏᴘᴇɴ ɪɴ ᴅᴍ",
                    url=f"https://t.me/{app.username}?start=help",
                )
            ],
            [
                InlineKeyboardButton(
                    text="➜ ᴏᴘᴇɴ ʜᴇʀᴇ",
                    callback_data="open_help_here",
                )
            ],
        ]
    )

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["help_2"],
        reply_markup=keyboard,
    )


# ================= OPEN HERE (FIXED) =================
@app.on_callback_query(filters.regex("^open_help_here$") & ~BANNED_USERS)
@languageCB
async def open_help_here(client, query, _):

    try:
        await query.answer()
    except:
        pass

    keyboard = help_pannel(_, True)
    msg = query.message

    if msg.photo:
        await msg.edit_caption(
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )
    else:
        await msg.edit_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


# ================= BACK =================
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
@languageCB
async def back_help(client, query, _):

    try:
        await query.answer()
    except:
        pass

    keyboard = help_pannel(_, True)
    msg = query.message

    if msg.photo:
        await msg.edit_caption(
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )
    else:
        await msg.edit_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


# ================= HELP CALLBACK =================
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):

    try:
        await CallbackQuery.answer()
    except:
        pass

    callback_data = CallbackQuery.data.strip()

    if len(callback_data.split(None, 1)) < 2:
        return

    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    try:
        if cb == "hb1":
            txt = helpers.HELP_1
        elif cb == "hb2":
            txt = helpers.HELP_2
        elif cb == "hb3":
            txt = helpers.HELP_3
        elif cb == "hb4":
            txt = helpers.HELP_4
        elif cb == "hb5":
            txt = helpers.HELP_5
        elif cb == "hb6":
            txt = helpers.HELP_6
        elif cb == "hb7":
            txt = helpers.HELP_7
        elif cb == "hb8":
            txt = helpers.HELP_8
        elif cb == "hb9":
            txt = helpers.HELP_9
        elif cb == "hb10":
            txt = helpers.HELP_10
        elif cb == "hb11":
            txt = helpers.HELP_11
        elif cb == "hb12":
            txt = helpers.HELP_12
        elif cb == "hb13":
            txt = helpers.HELP_13
        elif cb == "hb14":
            txt = helpers.HELP_14
        elif cb == "hb15":
            txt = helpers.HELP_15
        elif cb == "hb16":
            txt = helpers.HELP_16
        else:
            return

        if CallbackQuery.message.photo:
            await CallbackQuery.edit_message_caption(
                caption=txt,
                reply_markup=keyboard
            )
        else:
            await CallbackQuery.edit_message_text(
                txt,
                reply_markup=keyboard
            )

    except:
        pass
