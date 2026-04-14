import os
from pyrogram import filters
from pyrogram.types import Message
from telegraph import Telegraph
from EsproMusic import app

telegraph = Telegraph()
telegraph.create_account(short_name="EsproMusic")


# 🔥 /tgm → MEDIA TO TELEGRAPH
@app.on_message(filters.command("tgm"))
async def tgm_handler(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ / ᴠɪᴅᴇᴏ")

    reply = message.reply_to_message

    if not (reply.photo or reply.video or reply.document):
        return await message.reply_text("❌ sᴜᴘᴘᴏʀᴛs ᴘʜᴏᴛᴏ / ᴠɪᴅᴇᴏ / ғɪʟᴇ")

    msg = await message.reply_text("⚡ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ...")

    file_path = None

    try:
        file_path = await reply.download()

        response = telegraph.upload_file(file_path)
        link = f"https://telegra.ph{response[0]}"

        await msg.edit(
            f"🖼️ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ\n\n🔗 {link}"
        )

    except Exception as e:
        await msg.edit(f"❌ ᴇʀʀᴏʀ: `{e}`")

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


# 🔥 /tgt → TEXT TO TELEGRAPH PAGE
@app.on_message(filters.command("tgt"))
async def tgt_handler(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ")

    reply = message.reply_to_message

    text = reply.text or reply.caption

    if not text:
        return await message.reply_text("❌ ɴᴏ ᴛᴇxᴛ ғᴏᴜɴᴅ")

    msg = await message.reply_text("⚡ ᴄʀᴇᴀᴛɪɴɢ ᴘᴀɢᴇ...")

    try:
        page = telegraph.create_page(
            title="Espro Music",
            html_content=f"<p>{text}</p>"
        )

        link = f"https://telegra.ph/{page['path']}"

        await msg.edit(
            f"📝 ᴛᴇʟᴇɢʀᴀᴘʜ ᴘᴀɢᴇ\n\n🔗 {link}"
        )

    except Exception as e:
        await msg.edit(f"❌ ᴇʀʀᴏʀ: `{e}`")
