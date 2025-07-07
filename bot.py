import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Use your bot token directly for now
TOKEN = "8139941411:AAGgOIb-DUP35-qQ44lgfh6USVDHwtY1y18"

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Team HR Bot!\n\n"
        "📥 Send me any public video link (YouTube, Facebook, Instagram, etc.) and I will try to download it.\n"
        "🎧 Use /audio to get only audio.\n\n"
        "👑 Powered by @its_lucifer_star"
    )

# Validate URL
def is_valid_url(url):
    return re.match(r'^(?:http|ftp)s?://', url)

# Video handler
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid link.")
        return

    await update.message.reply_text("📥 Downloading video...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            await update.message.reply_video(f, caption=info.get('title', 'Downloaded video'))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# Audio handler
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid link.")
        return

    await update.message.reply_text("🎶 Downloading audio...")

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
            if filename.endswith('.webm') or filename.endswith('.m4a'):
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        with open(filename, 'rb') as f:
            await update.message.reply_audio(f, caption=info.get('title', 'Downloaded audio'))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# App Setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("audio", download_audio))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

# Run
app.run_polling()
