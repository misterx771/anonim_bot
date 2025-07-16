import asyncio
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 Токен бота и ID админа
BOT_TOKEN = "7990044460:AAFMYiXyWzeGDZoiEK1iIQi6cDA61hFcEPc"
ADMIN_ID = 2077750894

# 📦 Для хранения сообщений от пользователей
user_messages = {}

# ⚙️ Логирование
logging.basicConfig(level=logging.INFO)

# 📨 Обработка входящих сообщений от пользователей
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or "без_ника"
    chat_id = update.effective_chat.id
    text = update.message.text

    # Сохраняем последнее сообщение по username
    user_messages[username] = chat_id

    # Отправляем админу сообщение с кнопкой для ответа
    if chat_id != ADMIN_ID:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Сообщение от @{username}:\n{text}"
        )
        await context.bot.send_sticker(chat_id=ADMIN_ID, sticker="CAACAgIAAxkBAAEKc1NlriF_SXQd1oK8CmJPr6mVAVMxLQACuBwAAh4vSEma_e0IKPQ_EzQE")

# 🔁 Ответ админа пользователю через команду
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("Использование: /ответ @username сообщение")
        return

    username = context.args[0].lstrip("@")
    message_text = " ".join(context.args[1:])

    if username in user_messages:
        user_id = user_messages[username]
        await context.bot.send_message(chat_id=user_id, text=message_text)
        await update.message.reply_text("✅ Ответ отправлен.")
    else:
        await update.message.reply_text("❌ Пользователь не найден или ещё не писал.")

# 🚀 Основной запуск бота
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("ответ", reply_command))

    print("🤖 Бот запущен. Ожидаем сообщения...")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
