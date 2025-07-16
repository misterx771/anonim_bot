import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import asyncio
import nest_asyncio

nest_asyncio.apply()

# 🔑 Токен бота
BOT_TOKEN = "7990044460:AAFMYiXyWzeGDZoiEK1iIQi6cDA61hFcEPc"

# 👤 Айди владельца (тебя)
OWNER_ID = 2077750894  # замени на свой Telegram ID

# Логирование
logging.basicConfig(level=logging.INFO)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Это анонимный бот. Напиши сюда сообщение!")

# Все текстовые сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if user.id == OWNER_ID:
        if context.user_data.get("reply_to"):
            target_id = context.user_data.pop("reply_to")
            await context.bot.send_message(
                chat_id=target_id,
                text=f"💬 Ответ от @x771:\n\n{text}"
            )
            await update.message.reply_text("✅ Ответ отправлен.")
        else:
            await update.message.reply_text("⚠️ Нет активного анонимного пользователя.")
    else:
        context.user_data["reply_to"] = user.id
        username = f"@{user.username}" if user.username else "❌ нет username"
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"📩 Новое анонимное сообщение:\n\n{text}\n\n👤 {username}"
        )
        await update.message.reply_text("✅ Ваше сообщение отправлено!")

# Запуск бота
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот работает...")
    await app.run_polling()

# Запуск асинхронного цикла
if __name__ == "__main__":
    asyncio.run(main())
