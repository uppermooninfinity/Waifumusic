import os
import time
import requests
from PIL import Image
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from EsproMusic import app
from pyrogram.enums import ButtonStyle

def clean_text(text: str) -> str:
    return text.replace("<", "").replace(">", "").replace("&", "and")


def auto_title(text: str) -> str:
    if not text:
        return "Espro Music"
    return text[:30].strip().title()


def compress_image(path: str):
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        new_path = path + "_compressed.jpg"
        img.save(new_path, "JPEG", quality=60)
        return new_path
    except:
        return path


def telegraph_upload(path: str) -> str:
    try:
        with open(path, "rb") as f:
            r = requests.post(
                "https://telegra.ph/upload",
                files={"file": f},
                timeout=20
            )

        data = r.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0].get("src", "")

        return ""

    except Exception:
        return ""


@app.on_message(filters.command("tgm"))
async def tgm_handler(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇᴅɪᴀ")

    media = message.reply_to_message
    status = await message.reply_text("⚡ ᴘʀᴏᴄᴇssɪɴɢ...")

    files = []

    try:
        if media.photo or media.document:
            path = await media.download()

            if os.path.getsize(path) > 4 * 1024 * 1024:
                return await status.edit("❌ ғɪʟᴇ ᴛᴏᴏ ʙɪɢ (4ᴍʙ max)")

            files.append(path)

        elif media.video:
            return await status.edit("❌ ᴠɪᴅᴇᴏ ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")

        elif media.media_group_id:
            msgs = await client.get_media_group(message.chat.id, media.id)

            for m in msgs:
                if m.photo or m.document:
                    path = await m.download()

                    if os.path.getsize(path) <= 4 * 1024 * 1024:
                        files.append(path)

        if not files:
            return await status.edit("❌ ɴᴏ ᴠᴀʟɪᴅ ғɪʟᴇs")

        html = ""

        for file_path in files:

            if file_path.endswith((".jpg", ".jpeg", ".png")):
                file_path = compress_image(file_path)

            src = telegraph_upload(file_path)

            if src:
                html += f'<img src="https://telegra.ph{src}"/><br>'

            if os.path.exists(file_path):
                os.remove(file_path)

        if not html:
            return await status.edit("❌ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ")

        title = auto_title(media.caption or "Espro Music")

        page_data = {
            "title": title,
            "author_name": "Espro Music",
            "content": [[
                {
                    "tag": "p",
                    "children": [html]
                }
            ]]
        }

        r = requests.post(
            "https://telegra.ph/createPage",
            data=page_data
        )

        result = r.json()

        if not result.get("ok"):
            return await status.edit("❌ ᴘᴀɢᴇ ᴄʀᴇᴀᴛᴇᴅ ғᴀɪʟᴇᴅ")

        link = "https://telegra.ph/" + result["result"]["path"]

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔗 ᴏᴘᴇɴ", url=link, style=ButtonStyle.SUCCESS),
                    InlineKeyboardButton("📋 ᴄᴏᴘʏ", url=link, style=ButtonStyle.DANGER),
                ]
            ]
        )

        await status.edit(
            "🖼️ ᴛᴇʟᴇɢʀᴀᴘʜ ʀᴇᴀᴅʏ\n\n"
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

    text = clean_text(text)
    title = auto_title(text)

    status = await message.reply_text("⚡ ᴄʀᴇᴀᴛɪɴɢ ᴘᴀɢᴇ...")

    try:
        data = {
            "title": title,
            "author_name": "Espro Music",
            "content": [[
                {
                    "tag": "p",
                    "children": [text]
                }
            ]]
        }

        r = requests.post(
            "https://telegra.ph/createPage",
            data=data
        )

        result = r.json()

        if not result.get("ok"):
            return await status.edit("❌ ᴘᴀɢᴇ ғᴀɪʟᴇᴅ")

        link = "https://telegra.ph/" + result["result"]["path"]

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔗 ᴏᴘᴇɴ", url=link),
                    InlineKeyboardButton("📋 ᴄᴏᴘʏ", url=link),
                ]
            ]
        )

        await status.edit(
            "📝 ᴘᴀɢᴇ ʀᴇᴀᴅʏ\n\n"
            f"🔗 {link}",
            reply_markup=buttons
        )

    except Exception as e:
        await status.edit(f"❌ ᴇʀʀᴏʀ\n➤ {e}")
