import sys
import os

# Loyihaning ildiz papkasini python path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

from database.db import init_db, get_user_role, add_user
from bot.keyboards import get_keyboard_by_role

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Tokenni environment variables orqali bering

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.username or "Foydalanuvchi"

    # Bazadan rolni olamiz yoki yangi foydalanuvchi sifatida qo'shamiz
    role = await get_user_role(user_id)
    if role is None:
        # Oldindan ma'lum qilingan admin va seller IDlari
        ADMIN_IDS = [1262207928]   # O'zgartiring o'zingizga mos
        SELLER_IDS = [8450201406]  # O'zgartiring o'zingizga mos

        if user_id in ADMIN_IDS:
            role = "admin"
        elif user_id in SELLER_IDS:
            role = "seller"
        else:
            role = "customer"

        await add_user(user_id, user_name, role)

    keyboard = get_keyboard_by_role(role)
    await update.message.reply_text(f"Salom, {user_name}! Sizning rol: {role}", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Tugma bosilganda kerakli amallarni shu yerda bajarish mumkin
    await query.edit_message_text(text=f"Siz {data} tugmasini bosdingiz.")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(init_db())  # ✅ TO‘G‘RI USUL
    main()
