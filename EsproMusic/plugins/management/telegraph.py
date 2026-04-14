import os
import requests
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from EsproMusic import app
from pyrogram.enums import ButtonStyle

def upload_catbox(path: str) -> str:
    try:
        with open(path, "rb") as f:
            r = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": f},
                timeout=30
            )

        if r.status_code == 200:
            return r.text.strip()

        return ""

    except Exception:
        return ""


@app.on_message(filters.command("tgm"))
async def tgm_handler(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇᴅɪᴀ")

    media = message.reply_to_message

    if not (media.photo or media.document or media.video):
        return await message.reply_text("❌ ᴏɴʟʏ ᴍᴇᴅɪᴀ sᴜᴘᴘᴏʀᴛᴇᴅ")

    status = await message.reply_text("⚡ ᴜᴘʟᴏᴀᴅɪɴɢ...")

    try:
        path = await media.download()

        if os.path.getsize(path) > 10 * 1024 * 1024:
            return await status.edit("❌ ғɪʟᴇ ᴛᴏᴏ ʙɪɢ (10MB max)")

        link = upload_catbox(path)

        if os.path.exists(path):
            os.remove(path)

        if not link:
            return await status.edit("❌ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ")

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔗 ᴏᴘᴇɴ", url=link, style=ButtonStyle.SUCCESS),
                    InlineKeyboardButton("📋 ᴄᴏᴘʏ", url=link, style=ButtonStyle.DANGER),
                ]
            ]
        )

        await status.edit(
            "🖼️ ᴜᴘʟᴏᴀᴅ sᴜᴄᴄᴇss\n\n"
            f"🔗 {link}",
            reply_markup=buttons
        )

    except Exception as e:
        await status.edit(f"❌ ᴇʀʀᴏʀ\n➤ {e}")


@app.on_message(filters.command("tgt"))
async def tgt_handler(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ")

    text = message.reply_to_message.text or message.reply_to_message.caption

    if not text:
        return await message.reply_text("❌ ɴᴏ ᴛᴇxᴛ ғᴏᴜɴᴅ")

    link = "https://telegra.ph/removed-system"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📋 ᴄᴏᴘʏ ᴛᴇxᴛ", callback_data="copy_text", style=ButtonStyle.DANGER),
            ]
        ]
    )

    await message.reply_text(
        "📝 ᴛᴇxᴛ ʀᴇᴀᴅʏ\n\n"
        f"{text}\n\n"
        "⚡ ɴᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ᴜsᴇᴅ (sᴛᴀʙʟᴇ ᴍᴏᴅᴇ)",
        reply_markup=buttons
    )
