import asyncio
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


START_STICKER = "CAACAgUAAxkBAAEB..."


async def intro_flow(message: Message):
    opening = await message.reply("✨ ʜᴇʟᴘ & ᴜᴛɪʟɪᴛɪᴇs ʟᴏᴀᴅɪɴɢ...")
    await asyncio.sleep(2)
    try:
        await opening.delete()
    except:
        pass

    try:
        st = await message.reply_sticker(START_STICKER)
        await asyncio.sleep(2)
        await st.delete()
    except:
        pass


@app.on_message(filters.command(["help", "utils"]) & filters.private & ~BANNED_USERS)
async def help_private(client, message: Message):

    await intro_flow(message)

    language = await get_lang(message.chat.id)
    _ = get_string(language)

    keyboard = help_pannel(_)

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["help_1"].format(SUPPORT_CHAT),
        reply_markup=keyboard,
    )


@app.on_message(filters.command(["help", "utils"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_group(client, message: Message, _):

    await intro_flow(message)

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


# 🔥 FIXED OPEN HERE
@app.on_callback_query(filters.regex("^open_help_here$") & ~BANNED_USERS)
@languageCB
async def open_here(client, q, _):

    try:
        await q.answer()
    except:
        pass

    keyboard = help_pannel(_, True)

    try:
        # if message is photo → edit caption
        await q.message.edit_caption(
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )
    except:
        # fallback if it's text
        await q.message.edit_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
@languageCB
async def back_help(client, q, _):

    try:
        await q.answer()
    except:
        pass

    keyboard = help_pannel(_, True)

    try:
        await q.message.edit_caption(
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )
    except:
        await q.message.edit_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


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

        try:
            await CallbackQuery.edit_message_caption(
                caption=txt,
                reply_markup=keyboard
            )
        except:
            await CallbackQuery.edit_message_text(
                txt,
                reply_markup=keyboard
            )

    except:
        pass
