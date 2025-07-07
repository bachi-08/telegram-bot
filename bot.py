import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# ✅ Bot Token (hardcoded)
TOKEN = "8139941411:AAGgOIb-DUP35-qQ44lgfh6USVDHwtY1y18"

# 📌 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome To Team HR Bot!\n\n"
        "📥 Send me any video link — YouTube, Instagram, Facebook, Twitter, etc — and I'll download it for you!\n\n"
        "🎵 Use /audio for audio only.\n\n"
        "👑 Owner - @its_lucifer_star"
    )

# 📌 URL validation
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
        r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return re.match(regex, url)

# 📥 Video Download
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not is_valid_url(url):
        await update.message.reply_text("⚠️ Please send a valid video link.")
        return

    await update.message.reply_text("📥 Downloading your video, please wait...")
    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best',
            'cookiefile': 'cookies.txt'  # ✅ Uses Instagram login cookies
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        caption = f"🎬 <b>Title:</b> {info.get('title')}\n"
        caption += f"📺 <b>Uploader:</b> {info.get('uploader')}\n"
        tags = info.get('tags')
        caption += f"🏷️ <b>Tags:</b> {', '.join(tags[:10])}" if tags else "🏷️ <b>Tags:</b> Not available"
        caption += "\n\n👑 Powered by @its_lucifer_star"

        with open(filename, 'rb') as f:
            await update.message.reply_video(f, caption=caption, parse_mode="HTML")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# 🎵 Audio Download
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
            'cookiefile': 'cookies.txt',  # ✅ Uses Instagram login cookies
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if filename.endswith(('.webm', '.m4a')):
                filename = filename.rsplit('.', 1)[0] + '.mp3'

        caption = f"🎵 <b>Title:</b> {info.get('title')}\n"
        caption += f"📺 <b>Uploader:</b> {info.get('uploader')}\n"
        tags = info.get('tags')
        caption += f"🏷️ <b>Tags:</b> {', '.join(tags[:10])}" if tags else "🏷️ <b>Tags:</b> Not available"
        caption += "\n\n👑 Powered by @its_lucifer_star"

        with open(filename, 'rb') as f:
            await update.message.reply_audio(f, caption=caption, parse_mode="HTML")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# 🧠 Bot Setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("audio", download_audio))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

# 🚀 Start the bot
app.run_polling()
