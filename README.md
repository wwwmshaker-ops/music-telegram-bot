from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import yt_dlp
import os

# المتغيرات من Railway
TOKEN = os.environ.get("TOKEN")
YOUR_ID = int(os.environ.get("YOUR_ID"))
ALLOWED_USER_ID = int(os.environ.get("ALLOWED_USER_ID"))

async def start(update: Update, context):
    await update.message.reply_text("أهلا! أرسل اسم الأغنية وسأحملها لك 🎵")

async def download_song(update: Update, context):
    user_id = update.message.from_user.id
    if user_id != ALLOWED_USER_ID:
        await update.message.reply_text("❌ أنت غير مسموح لك باستخدام هذا البوت.")
        return

    query = update.message.text
    await update.message.reply_text(f"🔎 جاري البحث عن: {query}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': 'song.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # البحث على YouTube وتحميل أول نتيجة
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        
        # إرسال الأغنية لك
        await context.bot.send_audio(chat_id=YOUR_ID, audio=open(filename, 'rb'))
        await update.message.reply_text(f"✅ الأغنية جاهزة: {info['title']}")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {e}")
    finally:
        # حذف الملف بعد الإرسال لتوفير المساحة
        if os.path.exists("song.mp3"):
            os.remove("song.mp3")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_song))
    app.run_polling()
