# main.py

import logging
import asyncio
import nest_asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes,
    filters
)

nest_asyncio.apply()

# ADMIN ID
ADMIN_ID = 2077750894
# TOKEN
BOT_TOKEN = "7990044460:AAFMYiXyWzeGDZoiEK1iIQi6cDA61hFcEPc"

# Foydalanuvchilar xabarlari uchun vaqtincha saqlovchi
user_messages = {}

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["✉️ Yuborish"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("✋ Anonim xabar yo‘llash uchun tugmani bosing.", reply_markup=reply_markup)

# Foydalanuvchidan anonim xabar qabul qilish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if text == "✉️ Yuborish":
        await update.message.reply_text("Xabaringizni yozing. U anonim tarzda yuboriladi.")
        return

    # Saqlab qo‘yamiz, shunda admin javob bera oladi
    user_messages[user.id] = user.username or f"id:{user.id}"

    # Adminga yuboramiz
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 Yangi anonim xabar:\n\n{text}\n\n👤 Yuboruvchi: @{user.username or 'no_username'} (id: {user.id})"
    )

    await update.message.reply_text("✅ Xabaringiz anonim tarzda yuborildi.")

# Admindan foydalanuvchiga javob
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Foydalanuvchi ID va xabarni yozing:\nMasalan: /reply 123456789 Salom!")
        return

    user_id = int(context.args[0])
    reply_text = " ".join(context.args[1:])

    try:
        await context.bot.send_message(chat_id=user_id, text=f"💬 Admindan javob:\n\n{reply_text}")
        await update.message.reply_text("✅ Javob yuborildi.")
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")

# Botni ishga tushurish
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot ishga tushdi...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
