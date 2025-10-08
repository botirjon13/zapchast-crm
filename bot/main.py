import sys
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Loyihaning ildiz papkasini python path ga qo‘shamiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import init_db, get_user_role, add_user
from bot.keyboards import get_keyboard_by_role

# keyingi kodlar...

# Telegram token va rol uchun IDlar
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

ADMINS = {1262207928, 298157746}  # Admin Telegram IDlarni yozing
SELLERS = {8450201406}  # Sotuvchi Telegram IDlarni yozing

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Bazada foydalanuvchini qo'shish yoki tekshirish
    role = get_user_role(user_id)
    if role is None:
        # Rolni aniqlash
        if user_id in ADMINS:
            role = "admin"
        elif user_id in SELLERS:
            role = "sotuvchi"
        else:
            role = "mijoz"
        add_user(user_id, user.full_name, role)

    keyboard = get_keyboard_by_role(role)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Salom, {role.capitalize()}! Menyuni tanlang:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    role = get_user_role(user_id) or "mijoz"

    # Oddiy misol: bot tugma bosilganda javob beradi
    if data == "warehouse":
        if role != "admin":
            await query.edit_message_text("Bu bo‘lim faqat adminlar uchun.")
            return
        await query.edit_message_text("Ombor bo‘limi hozircha ishlanmoqda.")

    elif data == "sell":
        if role not in {"admin", "sotuvchi"}:
            await query.edit_message_text("Bu bo‘lim faqat admin va sotuvchilar uchun.")
            return
        await query.edit_message_text("Sotuv bo‘limi hozircha ishlanmoqda.")

    elif data == "reports":
        if role != "admin":
            await query.edit_message_text("Bu bo‘lim faqat adminlar uchun.")
            return
        await query.edit_message_text("Hisobotlar bo‘limi hozircha ishlanmoqda.")

    elif data == "customers":
        if role not in {"admin", "sotuvchi"}:
            await query.edit_message_text("Bu bo‘lim faqat admin va sotuvchilar uchun.")
            return
        await query.edit_message_text("Mijozlar bo‘limi hozircha ishlanmoqda.")

    elif data == "settings":
        if role != "admin":
            await query.edit_message_text("Bu bo‘lim faqat adminlar uchun.")
            return
        await query.edit_message_text("Sozlamalar bo‘limi hozircha ishlanmoqda.")

    elif data == "my_orders":
        if role != "mijoz":
            await query.edit_message_text("Bu bo‘lim faqat mijozlar uchun.")
            return
        await query.edit_message_text("Sizning buyurtmalaringiz hozircha yo‘q.")

    elif data == "payments":
        if role != "mijoz":
            await query.edit_message_text("Bu bo‘lim faqat mijozlar uchun.")
            return
        await query.edit_message_text("To‘lovlar bo‘limi hozircha ishlanmoqda.")

    elif data == "support":
        await query.edit_message_text("Yordam bo‘limi hozircha ishlanmoqda.")

    else:
        await query.edit_message_text("Noma’lum buyruq.")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot ishga tushdi...")
    application.run_polling()

if __name__ == "__main__":
    # Bazani ishga tushiramiz
    init_db()
    main()
