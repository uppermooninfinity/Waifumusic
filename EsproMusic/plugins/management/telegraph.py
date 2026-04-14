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


def upload_telegraph(path: str) -> str:
    try:
        with open(path, "rb") as f:
            r = requests.post(
                "https://telegra.ph/upload",
                files={"file": f},
                timeout=20
            )

        data = r.json()

        if isinstance(data, list) and "src" in data[0]:
            return "https://telegra.ph" + data[0]["src"]

        return ""

    except Exception:
        return ""


def smart_upload(path: str) -> str:
    link = upload_catbox(path)
    if link:
        return link

    return upload_telegraph(path)


@app.on_message(filters.command("tgm"))
async def tgm_handler(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇᴅɪᴀ")

    reply = message.reply_to_message

    if not (reply.photo or reply.document):
        return await message.reply_text("❌ ᴏɴʟʏ ɪᴍᴀɢᴇ / ғɪʟᴇ sᴜᴘᴘᴏʀᴛᴇᴅ")

    status = await message.reply_text("⚡ ᴜᴘʟᴏᴀᴅɪɴɢ...")

    try:
        path = await reply.download()

        if os.path.getsize(path) > 10 * 1024 * 1024:
            return await status.edit("❌ ғɪʟᴇ ᴛᴏᴏ ʙɪɢ")

        link = smart_upload(path)

        if not link:
            return await status.edit("❌ ᴀʟʟ ᴜᴘʟᴏᴀᴅ ᴍᴇᴛʜᴏᴅs ғᴀɪʟᴇᴅ")

        if os.path.exists(path):
            os.remove(path)

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
