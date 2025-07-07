import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# 🔐 Your Telegram Bot Token (hardcoded here)
TOKEN = "8139941411:AAGgOIb-DUP35-qQ44lgfh6USVDHwtY1y18"

# 🔎 Validate URL
def is_valid_url(url):
    return re.match(r'https?://', url)

# 🟢 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Team HR Downloader Bot!\n\n"
        "📥 Send me any **public video link** (YouTube, Instagram, TikTok, Twitter, etc), and I'll download it!\n\n"
        "🎵 Use /audio for audio only.\n\n"
        "❌ Private or login-required videos are not supported.\n\n"
        "👑 Owner - @its_lucifer_star"
    )

# 📥 Video Downloader
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid video link.")
        return

    await update.message.reply_text("📥 Downloading your video... Please wait.")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            await update.message.reply_video(f, caption=f"🎬 {info.get('title', 'Your Video')}\n\n👑 Powered by @its_lucifer_star")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}\n\n❗ This video may be private, restricted, or require login (not supported).")

# 🔊 Audio Downloader
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid video link.")
        return

    await update.message.reply_text("🎵 Downloading audio... Please wait.")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Make sure it's .mp3
            if not filename.endswith('.mp3'):
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        with open(filename, 'rb') as f:
            await update.message.reply_audio(f, caption=f"🎵 {info.get('title', 'Your Audio')}\n\n👑 Powered by @its_lucifer_star")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}\n\n❗ This video may be private, restricted, or require login (not supported).")

# 🚀 Launch the bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("audio", download_audio))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
