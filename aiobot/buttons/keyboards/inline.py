from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Пример: админская инлайн-клавиатура для подтверждения/отклонения объявления

def admin_inline_keyboard(pk):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_{pk}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{pk}")
            ]
        ]
    ) 