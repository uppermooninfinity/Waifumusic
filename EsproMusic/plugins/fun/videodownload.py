import os
import re
import yt_dlp
from pyrogram import filters
from pyrogram.types import Message
from EsproMusic import app


def is_valid_url(text: str):
    return re.search(r"(youtube\.com|youtu\.be|instagram\.com)", text)


def download_video(url: str):
    try:
        path = "downloads"
        os.makedirs(path, exist_ok=True)

        ydl_opts = {
            "outtmpl": f"{path}/%(title).50s.%(ext)s",
            "format": "mp4/best",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        return file_path

    except Exception as e:
        print("DOWNLOAD ERROR:", e)
        return None


@app.on_message(filters.command("download"))
async def downloader(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜᴛᴜʙᴇ / ɪɴsᴛᴀ ʟɪɴᴋ")

    url = message.reply_to_message.text

    if not url or not is_valid_url(url):
        return await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ")

    status = await message.reply_text("⚡ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")

    try:
        file_path = download_video(url)

        if not file_path or not os.path.exists(file_path):
            return await status.edit("❌ ᴅᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ")

        await status.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ...")

        await message.reply_video(
            video=file_path,
            caption="✅ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴠɪᴅᴇᴏ"
        )

        os.remove(file_path)

        await status.delete()

    except Exception as e:
        await status.edit(f"❌ ᴇʀʀᴏʀ\n➤ {e}")
