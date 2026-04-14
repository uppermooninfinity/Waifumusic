import os
import time
import asyncio
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


async def progress(current, total, msg, start):
    percent = int(current * 100 / total)
    elapsed = time.time() - start
    speed = current / elapsed if elapsed > 0 else 0

    bar = "█" * (percent // 10) + "░" * (10 - percent // 10)

    try:
        await msg.edit(
            f"📤 ᴜᴘʟᴏᴀᴅɪɴɢ...\n"
            f"[{bar}] {percent}%\n"
            f"⚡ {speed/1024:.2f} KB/s"
        )
    except:
        pass


def compress_image(path: str):
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        new_path = path + "_compressed.jpg"
        img.save(new_path, "JPEG", quality=60)
        return new_path
    except:
        return path


@app.on_message(filters.command("tgm"))
async def tgm_handler(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇᴅɪᴀ")

    media = message.reply_to_message
    status = await message.reply_text("⚡ sᴛᴀʀᴛɪɴɢ ᴜᴘʟᴏᴀᴅ...")

    files = []

    try:
        # multiple media support
        if media.photo or media.video or media.document:
            files.append(await media.download())

        elif media.media_group_id:
            msgs = await client.get_media_group(message.chat.id, media.id)
            for m in msgs:
                if m.photo or m.video or m.document:
                    files.append(await m.download())

        html_content = ""
        start = time.time()

        for file_path in files:
            if file_path.endswith((".jpg", ".jpeg", ".png")):
                file_path = compress_image(file_path)

            await progress(len(files), len(files), status, start)

            upload = telegraph.upload_file(file_path)

            if isinstance(upload, list) and upload:
                path = upload[0]
                if isinstance(path, dict):
                    path = path.get("src", "")

                html_content += f'<img src="https://telegra.ph{path}"/><br>'

            if os.path.exists(file_path):
                os.remove(file_path)

        if not html_content:
            return await status.edit("❌ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ")

        title = auto_title(media.caption or "Espro Music")

        page = telegraph.create_page(
            title=title,
            html_content=html_content
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
            "📝 ᴘᴀɢᴇ ᴄʀᴇᴀᴛᴇᴅ\n\n"
            f"🔗 {link}",
            reply_markup=buttons
        )

    except Exception as e:
        await status.edit(f"❌ ᴇʀʀᴏʀ\n➤ {e}")
