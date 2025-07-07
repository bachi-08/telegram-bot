import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8139941411:AAGgOIb-DUP35-qQ44lgfh6USVDHwtY1y18"  # Your bot token here

def is_valid_url(url):
    regex = re.compile(r'^(?:http|ftp)s?://[^\s]+$')
    return re.match(regex, url)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me any video link (YouTube, Instagram, Facebook, Twitter, etc.)\n"
        "I'll try to download it for you!\n"
        "Use /audio to download audio only."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid URL.")
        return

    await update.message.reply_text("📥 Downloading your video...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'retries': 3,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                await update.message.reply_text("⚠️ Could not download this video.")
                return
            filename = ydl.prepare_filename(info)

        caption = f"🎬 <b>Title:</b> {info.get('title', 'N/A')}\n"
        caption += f"📺 <b>Uploader:</b> {info.get('uploader', 'N/A')}\n"
        caption += "\n👑 Powered by @its_lucifer_star"

        with open(filename, 'rb') as f:
            await update.message.reply_video(f, caption=caption, parse_mode="HTML")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid URL.")
        return

    await update.message.reply_text("🎶 Downloading audio...")

    ydl_opts = {
        'outtmpl': 'audio.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'retries': 3,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                await update.message.reply_text("⚠️ Could not download this audio.")
                return
            filename = ydl.prepare_filename(info)
            if filename.endswith(('.webm', '.m4a')):
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        caption = f"🎵 <b>Title:</b> {info.get('title', 'N/A')}\n"
        caption += f"📺 <b>Uploader:</b> {info.get('uploader', 'N/A')}\n"
        caption += "\n👑 Powered by @its_lucifer_star"

        with open(filename, 'rb') as f:
            await update.message.reply_audio(f, caption=caption, parse_mode="HTML")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("audio", download_audio))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
