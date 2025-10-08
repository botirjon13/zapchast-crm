import os
import sys
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz (importlar ishlashi uchun)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importlar
from database.db import init_db, get_user_role, add_user
from bot.keyboards import get_keyboard_by_role

# Admin va sotuvchilar ro'yxati (telegram user ID bo'yicha)
ADMINS = [1262207928]          # O'zgartiring: bu yerga admin ID kiriting
SELLERS = [8450201406]         # O'zgartiring: bu yerga sotuvchi ID kiriting


# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "NoUsername"

    # Foydalanuvchini rolini aniqlaymiz
    if user_id in ADMINS:
        role = "admin"
    elif user_id in SELLERS:
        role = "seller"
    else:
        role = "client"

    # Foydalanuvchini bazaga qo‘shamiz
    await add_user(user_id, username, role)

    # Rolga qarab klaviatura
    keyboard = get_keyboard_by_role(role)
    await update.message.reply_text(f"Xush kelibsiz, {role}!", reply_markup=keyboard)


# Tugmalarni bosish
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "check_stock":
        await query.edit_message_text("📦 Ombordagi mahsulotlar ro‘yxati...")
    elif data == "sales_report":
        await query.edit_message_text("📊 Sotuvlar hisoboti: kunlik, oylik, yillik.")
    elif data == "add_product":
        await query.edit_message_text("➕ Yangi tovar qo‘shish.")
    elif data == "my_orders":
        await query.edit_message_text("🛒 Sizning buyurtmalaringiz.")
    else:
        await query.edit_message_text("⚙️ Funksiya ishlab chiqilmoqda.")


# Main funksiyasi
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    TOKEN = os.getenv("BOT_TOKEN")  # Railway yoki .env dan oladi

    if not TOKEN:
        print("❌ BOT_TOKEN aniqlanmagan. .env faylga qo‘shing yoki Railway'da sozlang.")
        exit(1)

    # Dastur ilovasi
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Bazani ishga tushiramiz
    asyncio.run(init_db())

    # Botni ishga tushiramiz
    print("✅ Bot ishga tushdi...")
    app.run_polling()
