import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import nest_asyncio

BOT_TOKEN = "7990044460:AAFMYiXyWzeGDZoiEK1iIQi6cDA61hFcEPc"
OWNER_ID = 2077750894  # Замени на свой Telegram ID

# Активация nest_asyncio
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Это анонимный бот.\n\nОтправь сюда сообщение — и оно будет доставлено!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if user.id == OWNER_ID:
        if context.user_data.get("reply_to"):
            original_user_id = context.user_data.pop("reply_to")
            try:
                await context.bot.send_message(chat_id=original_user_id, text=f"✉️ Сообщение от @x771:\n{text}")
                await update.message.reply_text("✅ Ответ отправлен.")
            except Exception as e:
                await update.message.reply_text("❌ Ошибка при отправке.")
        else:
            await update.message.reply_text("❗️Нет пользователя для ответа.")
    else:
        msg = (
            f"📨 Новое анонимное сообщение:\n\n"
            f"{text}\n\n"
            f"👤 @{user.username if user.username else 'Без username'}"
        )
        await context.bot.send_message(chat_id=OWNER_ID, text=msg)
        context.user_data["reply_to"] = user.id
        await update.message.reply_text("✅ Сообщение отправлено!")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен. Ожидаем сообщения...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
