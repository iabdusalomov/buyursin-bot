from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def lang_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O‘zbekcha"), KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True
    )

def main_keyboard(lang):
    btn = {
        "ru": "➕ Подать объявление",
        "uz": "➕ E'lon joylashtirish",
        "en": "➕ Submit Ad"
    }
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn[lang])]],
        resize_keyboard=True
    )

def confirm_keyboard(lang):
    btns = {
        "ru": ["✅ Подтвердить", "✏️ Изменить", "❌ Отменить"],
        "uz": ["✅ Tasdiqlash", "✏️ O'zgartirish", "❌ Bekor qilish"],
        "en": ["✅ Confirm", "✏️ Edit", "❌ Cancel"]
    }
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b) for b in btns[lang]]],
        resize_keyboard=True
    )

def admin_inline_keyboard(ad_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"approve_{ad_id}"),
             InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{ad_id}")]
        ]
    ) 