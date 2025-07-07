from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os
import re

# 📌 Your Bot Token
TOKEN = '8139941411:AAGgOIb-DUP35-qQ44lgfh6USVDHwtY1y18'  # << Replace this with your actual bot token


# 📌 /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome To Team HR Bot!\n\n"
        "📥 Send me any video link — YouTube, Instagram, Facebook, Twitter, etc — and I'll download it for you!\n\n"
        "🎵 Use /audio for audio only.\n\n"
        "👑 Owner - @its_lucifer_star"
    )


# 📌 Validate URL
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
        r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return re.match(regex, url)


# 📌 Video download handler
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid video link.")
        return

    await update.message.reply_text("📥 Downloading your video, please wait...")
    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        caption_text = f"🎬 <b>Title:</b> {info.get('title')}\n"
        caption_text += f"📺 <b>Uploader:</b> {info.get('uploader')}\n"
        tags = info.get('tags')
        if tags:
            caption_text += f"🏷️ <b>Tags:</b> {', '.join(tags[:10])}"
        else:
            caption_text += "🏷️ <b>Tags:</b> Not available"

        caption_text += "\n\n👑 Powered by @its_lucifer_star"

        with open(filename, 'rb') as f:
            await update.message.reply_video(f, caption=caption_text, parse_mode="HTML")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


# 📌 Audio download handler
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid video link.")
        return

    await update.message.reply_text("🎶 Downloading audio only, please wait...")
    try:
        ydl_opts = {
            'outtmpl': 'audio.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Ensure proper audio filename extension
            if filename.endswith('.webm') or filename.endswith('.m4a'):
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        caption_text = f"🎵 <b>Title:</b> {info.get('title')}\n"
        caption_text += f"📺 <b>Uploader:</b> {info.get('uploader')}\n"
        tags = info.get('tags')
        if tags:
            caption_text += f"🏷️ <b>Tags:</b> {', '.join(tags[:10])}"
        else:
            caption_text += "🏷️ <b>Tags:</b> Not available"

        caption_text += "\n\n👑 Powered by @its_lucifer_star"

        with open(filename, 'rb') as f:
            await update.message.reply_audio(f, caption=caption_text, parse_mode="HTML")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


# 📌 Bot application setup
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("audio", download_audio))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

# Run the bot
app.run_polling()
