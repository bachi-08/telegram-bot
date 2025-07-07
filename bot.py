import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

# ✅ Your bot token
TOKEN = "8139941411:AAGgOIb-DUP35-qQ44lgfh6USVDHwtY1y18"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a public video link from YouTube, Instagram, Facebook, etc.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("⚠️ Please send a valid video link.")
        return

    await update.message.reply_text("📥 Downloading, please wait...")

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get("url")
            title = info.get("title")

        await update.message.reply_text(f"✅ Title: {title}\n🔗 Download: {video_url}")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
