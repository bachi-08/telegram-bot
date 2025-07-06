import os
import yt_dlp as youtube_dl
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Replace with your bot token
TOKEN = '7559815283:AAGqxL7BVX1JFWFhfh0NHYxlZemN4pqJutA'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube video link to download it!")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id

    if 'youtube.com' in text or 'youtu.be' in text:
        msg = await update.message.reply_text("⏳ Downloading...")

        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f'{chat_id}_video.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
            }

            # Run blocking yt-dlp code in separate thread
            await asyncio.to_thread(
                lambda: youtube_dl.YoutubeDL(ydl_opts).download([text])
            )

            # Check for downloaded video file
            for ext in ['mp4', 'mkv', 'webm']:
                filename = f"{chat_id}_video.{ext}"
                if os.path.exists(filename):
                    await context.bot.send_video(chat_id=chat_id, video=open(filename, 'rb'))
                    os.remove(filename)
                    break

            await msg.delete()

        except Exception as e:
            await update.message.reply_text(f"⚠️ Error: {str(e)}")

    else:
        await update.message.reply_text("❌ Please send a valid YouTube link.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
