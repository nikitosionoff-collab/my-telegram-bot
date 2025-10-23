from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import asyncio

# ✅ Укажи свои коды и файл
VALID_CODES = ["GIFT2025", "MEDITA25"]
VOICE_FILE_PATH = "meditation.ogg.mp3"  # Название файла с медитацией
DELAY_SECONDS = 10  # Задержка: 3600 секунд = 1 час

# Храним статус пользователя
user_states = {}

# При /start — приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = "awaiting_code"
    await update.message.reply_text(
        "Привет 👋\nЧтобы получить медитацию, введи, пожалуйста, свой код:"
    )

# При вводе текста
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_states.get(user_id) != "awaiting_code":
        return

    if text in VALID_CODES:
        user_states[user_id] = "code_valid"

        # Отправляем аудио
        with open(VOICE_FILE_PATH, "rb") as audio:
            await update.message.reply_audio(audio=InputFile(audio))
        await update.message.reply_text("Вот твоя медитация 🎧")

        # Через время отправим предложение урока
        asyncio.create_task(send_lesson_offer(context, user_id))
    else:
        await update.message.reply_text("Код неверный ❌ Попробуй ещё раз:")

# Через время предлагаем пробный урок
async def send_lesson_offer(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    await asyncio.sleep(DELAY_SECONDS)
    await context.bot.send_message(
        chat_id=user_id,
        text="Надеюсь, тебе понравилась медитация 🙏\n\nГотов(-а) на бесплатный пробный урок? Напиши в ответ — и договоримся 😊"
    )

# Запускаем бота
if __name__ == "__main__":
    app = ApplicationBuilder().token("8474008550:AAHQxRMwFj9Y6NecDTXMUg0vaEBM-2h2J00").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
