import os
import time
from PIL import Image
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegraph import Telegraph
from EsproMusic import app


telegraph = Telegraph()

try:
    telegraph.create_account(short_name="EsproMusic")
except Exception:
    pass


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


def safe_upload(path: str) -> str:
    try:
        with open(path, "rb") as f:
            res = telegraph.upload_file(f)

        if isinstance(res, list) and len(res) > 0:
            item = res[0]

            if isinstance(item, dict):
                return item.get("src", "")

            return str(item)

        return ""

    except Exception:
        return ""


@app.on_message(filters.command("tgm"))
async def tgm_handler(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴍɪssɪɴɢ")

    media = message.reply_to_message
    status = await message.reply_text("⚡ sᴛᴀʀᴛɪɴɢ ᴜᴘʟᴏᴀᴅ...")

    files = []

    try:
        if media.photo or media.document:
            path = await media.download()

            if os.path.getsize(path) > 4 * 1024 * 1024:
                return await status.edit("❌ ғɪʟᴇ ᴛᴏᴏ ʙɪɢ (ᴍᴀx 4ᴍʙ)")

            files.append(path)

        elif media.video:
            return await status.edit("❌ ᴠɪᴅᴇᴏ ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ")

        elif media.media_group_id:
            msgs = await client.get_media_group(message.chat.id, media.id)

            for m in msgs:
                if m.photo or m.document:
                    path = await m.download()

                    if os.path.getsize(path) > 4 * 1024 * 1024:
                        continue

                    files.append(path)

        if not files:
            return await status.edit("❌ ɴᴏ ᴠᴀʟɪᴅ ғɪʟᴇs")

        html = ""

        for file_path in files:

            if file_path.endswith((".jpg", ".jpeg", ".png")):
                file_path = compress_image(file_path)

            src = safe_upload(file_path)

            if src:
                html += f'<img src="https://telegra.ph{src}"/><br>'

            if os.path.exists(file_path):
                os.remove(file_path)

        if not html:
            return await status.edit("❌ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ")

        title = auto_title(media.caption or "Espro Music")

        page = telegraph.create_page(
            title=title,
            html_content=html
        )

        link = "https://telegra.ph/" + page["path"]

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔗 ᴏᴘᴇɴ", url=link),
                    InlineKeyboardButton("📋 ᴄᴏᴘʏ", url=link),
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
        page = telegraph.create_page(
            title=title,
            html_content=f"<p>{text}</p>"
        )

        link = "https://telegra.ph/" + page["path"]

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
