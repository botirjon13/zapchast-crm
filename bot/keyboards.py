from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_keyboard_by_role(role: str):
    """
    Role ga qarab tugmalar klaviaturasini qaytaradi.
    """
    if role == "admin":
        buttons = [
            [InlineKeyboardButton("Omborga tovar qo'shish", callback_data='add_product')],
            [InlineKeyboardButton("Hisobotlar", callback_data='reports')],
            [InlineKeyboardButton("Foydalanuvchilar", callback_data='users')],
        ]
    elif role == "seller":
        buttons = [
            [InlineKeyboardButton("Tovar sotish", callback_data='sell_product')],
            [InlineKeyboardButton("Mijozlar", callback_data='clients')],
        ]
    else:  # mijoz yoki boshqa rollar
        buttons = [
            [InlineKeyboardButton("Buyurtmalarim", callback_data='my_orders')],
        ]
    
    return InlineKeyboardMarkup(buttons)
