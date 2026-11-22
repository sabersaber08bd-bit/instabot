import os
import asyncio
import shutil
import uuid
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
MAX_SIZE = 49 * 1024 * 1024

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("صيفط ليا رابط ديال الفيديو 🎥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.startswith("http"):
        await update.message.reply_text("صيفط ليا رابط صحيح ❌")
        return

    await update.message.reply_text("كنتيليشارجي... ⏳")
    unique = str(uuid.uuid4())[:8]
    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': f'video_{unique}.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.getsize(filename) > MAX_SIZE:
            await update.message.reply_text("الفيديو كبير بزاف > 49MB ❌")
            os.remove(filename)
            return

        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f, caption="هاهو الفيديو ديالك ✅")

        shutil.copy(filename, "/sdcard/Download/" + filename)
        await update.message.reply_text("تحفظ ليك فـ Download ✅")
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"وقع مشكل: {e}")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
