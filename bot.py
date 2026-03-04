import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# المتغيرات اللي حنحطها بعدين في Railway
TOKEN = os.getenv("TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID"))
YOUR_ID = int(os.getenv("YOUR_ID"))

# الدالة اللي ترسل الأغاني لك تلقائي
async def forward_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ALLOWED_USER_ID:
        if update.message.audio:
            await context.bot.send_audio(
                chat_id=YOUR_ID,
                audio=update.message.audio.file_id,
                caption="🎵 نزلت لك أغنية جديدة ❤️"
            )

# إنشاء البوت وتشغيله
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.AUDIO, forward_song))

app.run_polling()
