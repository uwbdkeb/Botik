
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_phone_button():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📞 Отправить номер", request_contact=True)]],
        resize_keyboard=True
    )

def get_driver_menu():
    return ReplyKeyboardMarkup(
        [["🚛 Начать смену"], ["📦 Список доставки"], ["🔚 Завершить смену"]],
        resize_keyboard=True
    )

def get_admin_menu():
    return ReplyKeyboardMarkup(
        [
            ["🛠️ Админка"],
            ["👥 Водители", "🚗 Машины"],
            ["📊 Отчёт смен", "💬 Чат водителей"]
        ],
        resize_keyboard=True
    )

def get_car_keyboard(cars):
    keyboard = []
    for car in cars:
        keyboard.append([f"🚗 {car.brand} {car.model} ({car.number})"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_admin_inline_keyboard():
    keyboard = [
        [InlineKeyboardButton("👥 Управление водителями", callback_data="manage_drivers")],
        [InlineKeyboardButton("🚗 Управление машинами", callback_data="manage_cars")],
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")]
    ]
    return InlineKeyboardMarkup(keyboard)
